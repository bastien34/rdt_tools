# import logging


# debug
from debug import mri
from prefix_dialogs import PrefixDialog, FolderOpenDialog
from models import Mission
# from audio_controls import open_vlc
# from key_handler import KeyHandler
from handlers.bal_handler import BalDlg



context = XSCRIPTCONTEXT


def prefix_questions_and_answers(*args):
    pd = PrefixDialog(ctx=context)
    dlg = pd.create()
    if dlg.execute():
        p_question = dlg.getControl('p_question').Text
        p_answer = dlg.getControl('p_answer').Text
        dlg.dispose()
        doc = Mission(context)
        doc.prefix_questions_and_answers(p_question, p_answer)


def clean_text(*args):
    doc = context.getDocument()
    if not doc.getDocumentProperties().Title:
        return
    dlg = BalDlg(context)
    if dlg.execute():
        methods = dlg.get_data()
        mission = Mission(context)
        for method in methods.keys():
            if hasattr(mission, method) and methods.get(method):
                getattr(mission, method)()


def order_question(*args):
    pass
    # doc = Mission(context)
    # doc.order_question()


def question_upper(*args):
    pass
    # doc = Mission(context)
    # doc.question_upper()


def question_lower(*args):
    pass
    # doc = Mission(context)
    # doc.question_lower()


def remove_blank_line(*args):
    pass
    # doc = Mission(context)
    # doc.remove_blank_line()


def remove_milliseconds_from_tc(*args):
    pass
    # doc = Mission(context)
    # doc.remove_milliseconds_from_tc()


def wrap_last_word_into_brackets(*args):
    pass

    # doc = Mission(context)
    # doc.wrap_last_word_into_brackets()


def get_things_up(*args):
    pass
    # smgr = context.ServiceManager
    # desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop",
    #                                          context)
    # comp = desktop.getCurrentComponent()
    # if comp not in KeyHandler.components:
    #     cc = comp.getCurrentController()
    #     cc.addKeyHandler(KeyHandler(context, comp))


def get_things_down(*args):
    pass
    # Mission(context).remove_key_handler(context)


def vlc_launcher(*args):
    pass
    # get_things_up()
    # url = FolderOpenDialog(context).execute()
    # open_vlc(url)


g_exportedScripts = (
    clean_text,
    order_question,
    question_upper,
    question_lower,
    remove_blank_line,
    prefix_questions_and_answers,
    remove_milliseconds_from_tc,
    wrap_last_word_into_brackets,
    get_things_up,
    get_things_down,
    vlc_launcher,
)
