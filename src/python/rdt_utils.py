import logging


# debug
# from debug import mri

from dialogs import PrefixDialog
from models import Mission
from audio_controls import open_vlc

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('doc_cleaner')


ctx = XSCRIPTCONTEXT.getComponentContext()


def prefix_questions_and_answers(*args):
    PD = PrefixDialog(ctx=ctx)
    dlg = PD.create()
    if dlg.execute():
        p_question = dlg.getControl('p_question').Text
        p_answer = dlg.getControl('p_answer').Text
        dlg.dispose()
        doc = Mission(ctx)
        doc.prefix_questions_and_answers(p_question, p_answer)


def clean_text(*args):
    doc = Mission(ctx)
    doc.clean_text()


def order_question(*args):
    doc = Mission(ctx)
    doc.order_question()


def question_upper(*args):
    doc = Mission(ctx)
    doc.question_upper()


def question_lower(*args):
    doc = Mission(ctx)
    doc.question_lower()


def remove_blank_line(*args):
    doc = Mission(ctx)
    doc.remove_blank_line()


def remove_milliseconds_from_tc(*args):
    doc = Mission(ctx)
    doc.remove_milliseconds_from_tc()


def wrap_last_word_into_brackets(*args):
    doc = Mission(ctx)
    doc.wrap_last_word_into_brackets()


def get_things_up(*args):
    Mission(ctx).attach_key_handler()


def vlc_launcher(*args):
    open_vlc()


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
    vlc_launcher,
)
