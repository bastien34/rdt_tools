import unohelper
from com.sun.star.awt import XActionListener
from utils import get_package_location

from debug import mri


PREFIX_DIALOG_LOCATION = "/dialogs/prefixDialog.xdl"


class ActionListener(unohelper.Base, XActionListener):
    # def __init__(self, data):
    #     self.data = data

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

    def __init__(self, context_component):
        self.component = context_component
        self.service_manager = self.component.getServiceManager()
        instance = self.service_manager.createInstanceWithContext(
            "com.sun.star.awt.DialogProvider",
            self.component
        )
        path = get_package_location(self.component)
        self.dlg = instance.createDialog(path + PREFIX_DIALOG_LOCATION)
        self._add_listener()

    def _add_listener(self):
        listener = ActionListener()
        btn = self.dlg.getControl("validButton")
        btn.ActionCommand = "send"
        btn.addActionListener(listener)
