import unohelper
from com.sun.star.awt import XActionListener
from utils import get_package_location

from debug import mri


PREFIX_DIALOG_LOCATION = "/dialogs/prefixDialog.xdl"


class ActionListener(unohelper.Base, XActionListener):

    def disposing(self, ev):
        pass

    def actionPerformed(self, ev):
        cmd = str(ev.ActionCommand)
        if cmd == "send":
            dlg = ev.Source.getContext()
            data = {
                'p_question': str(dlg.getControl("p_question").Text),
                'p_answer': str(dlg.getControl("p_answer").Text),
            }
            dlg.endExecute()


class PrefixDialog(object):

    def __init__(self, ctx):
        self.ctx = ctx
        self.smgr = self.ctx.getServiceManager()

    def create(self):
        instance = self.smgr.createInstanceWithContext(
            "com.sun.star.awt.DialogProvider", self.ctx)
        path = get_package_location(self.ctx)
        dlg = instance.createDialog(path + PREFIX_DIALOG_LOCATION)
        self._add_listener(dlg)
        return dlg

    def _add_listener(self, dlg):
        listener = ActionListener()
        btn = dlg.getControl("validButton")
        btn.ActionCommand = "send"
        btn.addActionListener(listener)


class FolderOpenDialog(object):
    """ To pick up a folder. """

    def __init__(self, ctx):
        self.ctx = ctx
        self.smgr = self.ctx.getServiceManager()

        try:
            self.folder_picker_srv = "com.sun.star.ui.dialogs.FilePicker"
        except:
            traceback.print_exc()

    def create(self):
        return self.smgr.createInstanceWithContext(
            self.folder_picker_srv, self.ctx)

    def execute(self):
        fp = self.create()
        result = None
        if fp.execute():
            return fp.Files[0]
