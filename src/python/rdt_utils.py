# import logging


# debug
from debug import mri
from prefix_dialogs import PrefixDialog, FolderOpenDialog
from models import Mission
from audio_controls import open_vlc
from key_handler import KeyHandler
from handlers.bal_handler import BalDlg
from utils import msgbox


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
        msgbox("Ce fichier n'est pas identifié comme une mission ",
               title='Fichier non valide', boxtype='error')
        return
    dlg = BalDlg(context)
    if dlg.execute():
        methods = dlg.get_data()
        mission = Mission(context)
        for method in methods.keys():
            if hasattr(mission, method) and methods.get(method):
                getattr(mission, method)()


def order_question(*args):
    doc = Mission(context.getComponentContext())
    doc.order_question()


def question_upper(*args):
    doc = Mission(context.getComponentContext())
    doc.question_upper()


def question_lower(*args):
    doc = Mission(context.getComponentContext())
    doc.question_lower()


def remove_blank_line(*args):
    doc = Mission(context)
    doc.remove_blank_line()


def remove_milliseconds_from_tc(*args):
    doc = Mission(context)
    doc.remove_milliseconds_from_tc()


def wrap_last_word_into_brackets(*args):
    doc = Mission(context)
    doc.wrap_last_word_into_brackets()


def get_things_up(*args):
    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    comp = desktop.getCurrentComponent()
    if comp not in KeyHandler.components:
        cc = comp.getCurrentController()
        cc.addKeyHandler(KeyHandler(context, comp))


def get_things_down(*args):
    Mission(context.getComponentContext()).remove_key_handler(context)


def vlc_launcher(*args):
    get_things_up()
    cmpctx = context.getComponentContext()
    url = FolderOpenDialog(cmpctx).execute()
    open_vlc(url)


g_exportedScripts = (
    clean_text,
    # order_question,
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
