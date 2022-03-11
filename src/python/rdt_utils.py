# import logging


# debug
# from debug import mri
from prefix_dialogs import PrefixDialog
from models import Mission
from handlers.bal_handler import BalDlg
from utils import msgbox


context = XSCRIPTCONTEXT


def clean_text(*args):
    doc = context.getDocument()
    if not doc.getDocumentProperties().Title:
        msgbox("Ce fichier ne semble pas être une mission.",
               title='Fichier non valide', boxtype='error')
        return
    dlg = BalDlg(context)
    if dlg.execute():
        methods = dlg.get_data()
        mission = Mission(context.getComponentContext())
        for method in methods.keys():
            if hasattr(mission, method) and methods.get(method):
                getattr(mission, method)()


def prefix_questions_and_answers(*args):
    pd = PrefixDialog(ctx=context.getComponentContext())
    dlg = pd.create()
    if dlg.execute():
        p_question = dlg.getControl('p_question').Text
        p_answer = dlg.getControl('p_answer').Text
        count = dlg.getControl('count').State
        dlg.dispose()
        doc = Mission(context.getComponentContext())
        doc.prefix_questions_and_answers(p_question, p_answer, count)


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


g_exportedScripts = (
    clean_text,
    order_question,
    question_upper,
    question_lower,
    remove_blank_line,
    prefix_questions_and_answers,
    remove_milliseconds_from_tc,
    wrap_last_word_into_brackets,
)
