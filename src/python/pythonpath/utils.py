import os
import pyuno
import uno
from datetime import timedelta


from com.sun.star.awt.MessageBoxType import (
    MESSAGEBOX,
    INFOBOX,
    ERRORBOX,
    WARNINGBOX,
    QUERYBOX
)
from com.sun.star.awt.MessageBoxButtons import (
    BUTTONS_OK,
    BUTTONS_OK_CANCEL,
    BUTTONS_YES_NO,
    BUTTONS_YES_NO_CANCEL,
    BUTTONS_RETRY_CANCEL,
    BUTTONS_ABORT_IGNORE_RETRY,
)
from com.sun.star.awt.MessageBoxButtons import (
    DEFAULT_BUTTON_OK,
    DEFAULT_BUTTON_CANCEL,
    DEFAULT_BUTTON_RETRY,
    DEFAULT_BUTTON_YES,
    DEFAULT_BUTTON_NO,
    DEFAULT_BUTTON_IGNORE,
)
from com.sun.star.awt.MessageBoxResults import (
    YES as MBR_YES,
    NO as MBR_NO,
    CANCEL as MBR_CANCEL,
)

IMPLEMENTATION_NAME = "com.rdt.comp.Utils"


def path_to_url(path):
    if not path.startswith('file://'):
        return pyuno.systemPathToFileUrl(os.path.realpath(path))


def get_package_path(file_to_find):
    """
    Returns the path for template or image, using the constant
     TEMPLATE_NAME or LOGO_URL, which does not start with a "/".
    """
    working_dir = os.path.join(os.path.dirname(__file__), file_to_find)
    path = os.path.normpath(working_dir)
    if path.startswith('file:'):
        path = path.split(':')[1]
    assert os.path.isfile(path)
    return path_to_url(path)


def get_package_location(ctx):
    srv = ctx.getByName(
        "/singletons/com.sun.star.deployment.PackageInformationProvider")
    return srv.getPackageLocation(IMPLEMENTATION_NAME)


def milliseconds_to_timecode(ms: int) -> str:
    h, m, s = str(timedelta(milliseconds=ms)).split(':')
    return f"[{h:02s}:{m:02s}:{s[:4]:04}]"


def timestamps_in_milliseconds(tc: str) -> int:
    h, m, s = tc.split(':')
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000

def createUnoService(service, ctx=None, args=None):
    if not ctx:
        ctx = uno.getComponentContext()
    smgr = ctx.getServiceManager()
    if ctx and args:
        return smgr.createInstanceWithArgumentsAndContext(service, args, ctx)
    elif args:
        return smgr.createInstanceWithArguments(service, args)
    elif ctx:
        return smgr.createInstanceWithContext(service, ctx)
    else:
        return smgr.createInstance(service)


def msgbox(message, title="Message", boxtype='message', buttons='ok', frame=None):
    """
    BUTTON YES_NO_CANCEL
        return 2 for Yes
        return 3 for No
        return 0 for Cancel

    BUTTON OK_CANCEL:
        OK -> 1 ; CANCEL -> 0
    """
    types = {'message': MESSAGEBOX, 'info': INFOBOX, 'error': ERRORBOX,
             'warning': WARNINGBOX, 'query': QUERYBOX}
    _btns = {'yes_no_cancel': BUTTONS_YES_NO_CANCEL, 'ok': BUTTONS_OK,
             'ok_cancel': BUTTONS_OK_CANCEL}
    tk = createUnoService("com.sun.star.awt.Toolkit")
    if not frame:
        desktop = createUnoService("com.sun.star.frame.Desktop")
        frame = desktop.ActiveFrame
        if frame.ActiveFrame:
            # top window is a subdocument
            frame = frame.ActiveFrame
    win = frame.ComponentWindow
    box = tk.createMessageBox(win, types[boxtype], _btns[buttons], title, message)
    return box.execute()

