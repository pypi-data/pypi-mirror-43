"""Automated Testing on macOS"""
# flake8: noqa: F401
__version__ = "0.3.0.dev84"

from atomacos import a11y
from atomacos import errors
from atomacos.AXClasses import NativeUIElement
from atomacos.Clipboard import Clipboard
from atomacos.Prefs import Prefs

Error = errors.AXError
ErrorAPIDisabled = errors.AXErrorAPIDisabled
ErrorInvalidUIElement = errors.AXErrorInvalidUIElement
ErrorCannotComplete = errors.AXErrorCannotComplete
ErrorUnsupported = errors.AXErrorUnsupported
ErrorNotImplemented = errors.AXErrorNotImplemented

getAppRefByLocalizedName = NativeUIElement.getAppRefByLocalizedName
terminateAppByBundleId = NativeUIElement.terminateAppByBundleId
launchAppByBundlePath = NativeUIElement.launchAppByBundlePath
setSystemWideTimeout = NativeUIElement.setSystemWideTimeout
getAppRefByBundleId = NativeUIElement.getAppRefByBundleId
launchAppByBundleId = NativeUIElement.launchAppByBundleId
getFrontmostApp = NativeUIElement.getFrontmostApp
getAppRefByPid = NativeUIElement.getAppRefByPid
