import unohelper
import os, pyuno
from com.sun.star.awt import XActionListener


from utils import get_package_location

DLG_LOCATION = "dialogs"


class ActionListener(unohelper.Base, XActionListener):

    def disposing(self, ev):
        pass

    def actionPerformed(self, ev):
        cmd = str(ev.ActionCommand)
        if cmd == "send":
            dlg = ev.Source.getContext()
            dlg.endDialog(1)


class DialogBase:
    def __init__(self, ctx, dlg_name):
        """

        :param ctx:
        :param data:
        :param dlg_name: name of the box without extension (.xdl)
        """
        self.component_context = ctx.getComponentContext()
        self.smgr = self.component_context.getServiceManager()
        path = self.get_dlg_path(dlg_name)

        instance= self.smgr.createInstanceWithContext(
            "com.sun.star.awt.DialogProvider",
            self.component_context
        )
        try:
            path = pyuno.fileUrlToSystemPath(path)
        except:
            pass
        path = pyuno.systemPathToFileUrl(path)
        self.dlg = instance.createDialog(path)

    def execute(self):
        return self.dlg.execute()

    def get_dlg_path(self, name):
        path = get_package_location(self.component_context)
        return os.path.join(path, DLG_LOCATION, f"{name}.xdl")


class BalDlg(DialogBase):
    def __init__(self, ctx):
        super().__init__(ctx, 'bal')
        self.add_listener()

    def add_listener(self):
        listener = ActionListener()
        btn = self.dlg.getControl("valid")
        btn.ActionCommand = "send"
        btn.addActionListener(listener)

    def get_data(self) -> dict:
        """Order of triggering might be important."""
        return {
            # timecodes
            'remove_ms': self.dlg.getControl('remove_ms').State,
            'fix_timecodes': self.dlg.getControl('fix_timecodes').State,
            'style_tc': self.dlg.getControl('style_tc').State,
            'rm_double_space': self.dlg.getControl('rm_double_space').State,
            'rm_empty_lines': self.dlg.getControl('rm_empty_lines').State,
            'force_styling': self.dlg.getControl('force_styling').State,
            'force_breaklines': self.dlg.getControl('force_breaklines').State,
        }
