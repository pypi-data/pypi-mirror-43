import fnmatch
import logging

import AppKit
from ApplicationServices import (
    AXIsProcessTrusted,
    AXUIElementCreateApplication,
    AXUIElementCreateSystemWide,
    CFEqual,
    NSWorkspace,
)
from atomacos import converter
from atomacos._macos import (
    PAXUIElementCopyActionNames,
    PAXUIElementCopyAttributeNames,
    PAXUIElementCopyAttributeValue,
    PAXUIElementCopyElementAtPosition,
    PAXUIElementGetPid,
    PAXUIElementIsAttributeSettable,
    PAXUIElementPerformAction,
    PAXUIElementSetAttributeValue,
    PAXUIElementSetMessagingTimeout,
)
from atomacos.errors import (
    AXError,
    AXErrorAPIDisabled,
    AXErrorCannotComplete,
    AXErrorIllegalArgument,
    AXErrorNotImplemented,
    AXErrorNoValue,
    AXErrorUnsupported,
)
from PyObjCTools import AppHelper

logger = logging.getLogger(__name__)


class AXUIElement(object):
    def __init__(self, ref=None):
        self.ref = ref
        self.converter = converter.Converter(self.__class__)

    def __repr__(self):
        """Build a descriptive string for UIElements."""
        c = repr(self.__class__).partition("<class '")[-1].rpartition("'>")[0]

        _attributes = self.ax_attributes
        for element_describer in ("AXTitle", "AXValue", "AXRoleDescription"):
            if element_describer in _attributes:
                title = self.__getattr__(element_describer)
                if title:
                    break
        else:
            title = ""

        if "AXRole" in _attributes:
            role = self.AXRole
        else:
            role = "<No role!>"

        if len(title) > 20:
            title = title[:20] + "...'"

        return "<%s %s %s>" % (c, role, title)

    def __getattr__(self, item):
        if item in self.ax_attributes:
            return self._get_ax_attribute(item)
        elif item in self.ax_actions:

            def perform_ax_action():
                self._perform_ax_actions(item)

            return perform_ax_action
        else:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (type(self), item)
            )

    def __setattr__(self, key, value):
        if key.startswith("AX"):
            try:
                if key in self.ax_attributes:
                    self._set_ax_attribute(key, value)
            except AXErrorIllegalArgument:
                pass
        else:
            super(AXUIElement, self).__setattr__(key, value)

    def __dir__(self):
        return (
            self.ax_attributes
            + self.ax_actions
            + list(self.__dict__.keys())
            + dir(super(AXUIElement, self))  # not working in python 2
        )

    def _get_ax_attribute(self, item):
        """Get the value of the the specified attribute"""
        if item in self.ax_attributes:
            try:
                attr_value = PAXUIElementCopyAttributeValue(self.ref, item)
                return self.converter.convert_value(attr_value)
            except AXErrorNoValue:
                return None

        raise AttributeError("'%s' object has no attribute '%s'" % (type(self), item))

    def _set_ax_attribute(self, name, value):
        """
        Set the specified attribute to the specified value
        """
        settable = PAXUIElementIsAttributeSettable(self.ref, name)

        if not settable:
            raise AXErrorUnsupported("Attribute is not settable")

        PAXUIElementSetAttributeValue(self.ref, name, value)

    def _activate(self):
        """Activate the application (bringing menus and windows forward)."""
        ra = AppKit.NSRunningApplication
        app = ra.runningApplicationWithProcessIdentifier_(self.pid)
        # NSApplicationActivateAllWindows | NSApplicationActivateIgnoringOtherApps
        # == 3 - PyObjC in 10.6 does not expose these constants though so I have
        # to use the int instead of the symbolic names
        app.activateWithOptions_(3)

    @property
    def ax_attributes(self):
        """
        Get a list of attributes available on the AXUIElement
        """
        try:
            names = PAXUIElementCopyAttributeNames(self.ref)
            return list(names)
        except AXError:
            return []

    @property
    def ax_actions(self):
        """
        Get a list of actions available on the AXUIElement
        """
        try:
            names = PAXUIElementCopyActionNames(self.ref)
            return list(names)
        except AXError:
            return []

    def _perform_ax_actions(self, name):
        PAXUIElementPerformAction(self.ref, name)

    @property
    def bundle_id(self):
        """Return the bundle ID of the application."""
        ra = AppKit.NSRunningApplication
        app = ra.runningApplicationWithProcessIdentifier_(self.pid)
        return app.bundleIdentifier()

    @property
    def pid(self):
        pid = PAXUIElementGetPid(self.ref)
        return pid

    @classmethod
    def from_pid(cls, pid):
        """
        Get an AXUIElement reference to the application by specified PID.
        """
        app_ref = AXUIElementCreateApplication(pid)

        if app_ref is None:
            raise AXErrorUnsupported("Error getting app ref")

        return cls(ref=app_ref)

    @classmethod
    def systemwide(cls):
        """Get an AXUIElement reference for the system accessibility object."""
        app_ref = AXUIElementCreateSystemWide()

        if app_ref is None:
            raise AXErrorUnsupported("Error getting a11y object")

        return cls(ref=app_ref)

    @classmethod
    def from_bundle_id(cls, bundle_id):
        """
        Get the top level element for the application with the specified
        bundle ID, such as com.vmware.fusion.
        """
        ra = AppKit.NSRunningApplication
        # return value (apps) is always an array. if there is a match it will
        # have an item, otherwise it won't.
        apps = ra.runningApplicationsWithBundleIdentifier_(bundle_id)
        if len(apps) == 0:
            raise ValueError(
                ("Specified bundle ID not found in " "running apps: %s" % bundle_id)
            )
        pid = apps[0].processIdentifier()
        return cls.from_pid(pid)

    @classmethod
    def from_localized_name(cls, name):
        """Get the top level element for the application with the specified
        localized name, such as VMware Fusion.

        Wildcards are also allowed.
        """
        # Refresh the runningApplications list
        apps = get_running_apps()
        for app in apps:
            if fnmatch.fnmatch(app.localizedName(), name):
                pid = app.processIdentifier()
                return cls.from_pid(pid)
        raise ValueError("Specified application not found in running apps.")

    @classmethod
    def frontmost(cls):
        """Get the current frontmost application.

        Raise a ValueError exception if no GUI applications are found.
        """
        # Refresh the runningApplications list
        apps = get_running_apps()
        for app in apps:
            pid = app.processIdentifier()
            ref = cls.from_pid(pid)
            try:
                if ref.AXFrontmost:
                    return ref
            except (
                AttributeError,
                AXErrorUnsupported,
                AXErrorCannotComplete,
                AXErrorAPIDisabled,
                AXErrorNotImplemented,
            ):
                # Some applications do not have an explicit GUI
                # and so will not have an AXFrontmost attribute
                # Trying to read attributes from Google Chrome Helper returns
                # ErrorAPIDisabled for some reason - opened radar bug 12837995
                pass
        raise ValueError("No GUI application found.")

    @classmethod
    def with_window(cls):
        """Get a random app that has windows.

        Raise a ValueError exception if no GUI applications are found.
        """
        # Refresh the runningApplications list
        apps = get_running_apps()
        for app in apps:
            pid = app.processIdentifier()
            ref = cls.from_pid(pid)
            if hasattr(ref, "windows") and len(ref.windows()) > 0:
                return ref
        raise ValueError("No GUI application found.")

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if self.ref is None and other.ref is None:
            return True

        if self.ref is None or other.ref is None:
            return False

        return CFEqual(self.ref, other.ref)

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_element_at_position(self, x, y):
        if self.ref is None:
            raise AXErrorUnsupported(
                "Operation not supported on null element references"
            )

        try:
            element = PAXUIElementCopyElementAtPosition(self.ref, x, y)
        except AXErrorIllegalArgument:
            raise ValueError("Arguments must be two floats.")

        return self.__class__(element)

    @staticmethod
    def launch_app_by_bundle_id(bundle_id):
        """Launch the application with the specified bundle ID"""
        # NSWorkspaceLaunchAllowingClassicStartup does nothing on any
        # modern system that doesn't have the classic environment installed.
        # Encountered a bug when passing 0 for no options on 10.6 PyObjC.
        ws = AppKit.NSWorkspace.sharedWorkspace()
        # Sorry about the length of the following line
        r = ws.launchAppWithBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifier_(  # noqa: B950
            bundle_id,
            AppKit.NSWorkspaceLaunchAllowingClassicStartup,
            AppKit.NSAppleEventDescriptor.nullDescriptor(),
            None,
        )
        # On 10.6, this returns a tuple - first element bool result, second is
        # a number. Let's use the bool result.
        if not r[0]:
            raise RuntimeError("Error launching specified application. %s" % str(r))

    @staticmethod
    def launch_app_by_bundle_path(bundle_path, arguments=None):
        """Launch app with a given bundle path.

        Return True if succeed.
        """
        if arguments is None:
            arguments = []

        bundleUrl = AppKit.NSURL.fileURLWithPath_(bundle_path)
        workspace = AppKit.NSWorkspace.sharedWorkspace()
        configuration = {AppKit.NSWorkspaceLaunchConfigurationArguments: arguments}

        return workspace.launchApplicationAtURL_options_configuration_error_(
            bundleUrl,
            AppKit.NSWorkspaceLaunchAllowingClassicStartup,
            configuration,
            None,
        )

    @staticmethod
    def terminate_app_by_bundle_id(bundle_id):
        """Terminate app with a given bundle ID.
        Requires 10.6.

        Return True if succeed.
        """
        ra = AppKit.NSRunningApplication
        appList = ra.runningApplicationsWithBundleIdentifier_(bundle_id)
        if appList:
            app = appList[0]
            return app and app.terminate()
        return False

    def set_timeout(self, timeout):
        if self.ref is None:
            raise AXErrorUnsupported(
                "Operation not supported on null element references"
            )

        try:
            PAXUIElementSetMessagingTimeout(self.ref, timeout)
        except AXErrorIllegalArgument:
            raise ValueError("Accessibility timeout values must be non-negative")


def get_frontmost_pid():
    """Return the PID of the application in the foreground."""
    frontmost_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    pid = frontmost_app.processIdentifier()
    return pid


def axenabled():
    """Return the status of accessibility on the system."""
    return AXIsProcessTrusted()


def get_running_apps():
    """Get a list of the running applications."""
    AppHelper.callLater(1, AppHelper.stopEventLoop)
    AppHelper.runConsoleEventLoop()
    # Get a list of running applications
    ws = AppKit.NSWorkspace.sharedWorkspace()
    apps = ws.runningApplications()
    return apps
