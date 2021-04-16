import logging


# debug
# from debug import mri
import uno
from dialogs import PrefixDialog, FolderOpenDialog
from models import Mission
from audio_controls import open_vlc
from utils import path_to_url
from key_handler import KeyHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('doc_cleaner')

TRUC = None

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
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    comp = desktop.getCurrentComponent()
    if not comp in KeyHandler.components:
        cc = comp.getCurrentController()
        cc.addKeyHandler(KeyHandler(ctx, comp))


def get_things_down(*args):
    Mission(ctx).remove_key_handler(ctx)


def vlc_launcher(*args):
    get_things_up()
    url = FolderOpenDialog(ctx).execute()
    open_vlc(url)


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
