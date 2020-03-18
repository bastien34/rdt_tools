import logging
import uno
import unohelper
from com.sun.star.task import XJobExecutor
from com.sun.star.awt import FontWeight

# debug
# from IPython.core.debugger import Pdb
# ipdb = Pdb()
# from debug import mri


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('doc_cleaner')

QUESTION_CSS = "Inter Q"


class Mission:

    def __init__(self):
        self.ctx = XSCRIPTCONTEXT.getComponentContext()
        self.smgr = self.ctx.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx )
        self.doc = self.desktop.getCurrentComponent()
        self.text = self.doc.Text
        self._remove_blank_space_at_the_end_of_lines()
        self._apply_question_style()
        logger.debug('Mission instanciated!')

    def _remove_blank_space_at_the_end_of_lines(self):
        logger.debug('  - clean: remove blank space at end of lines')
        rd = self.doc.createReplaceDescriptor()
        rd.SearchRegularExpression = True
        rd.SearchString = '\s*$'
        rd.ReplaceString = ""
        self.doc.replaceAll(rd)

    def _apply_question_style(self):
        logger.debug('  - clean: apply style Inter Q')

        # check if document has INTERQ style
        styles = self.doc.getStyleFamilies().getByName("ParagraphStyles")
        if not styles.hasByName(QUESTION_CSS):
            return

        text_enum = self.text.createEnumeration()
        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                # element.CharWeight is not reliable. We check first & last letter
                # to determine if **element** is a question
                if element.getStart().CharWeight == FontWeight.BOLD \
                        or element.getEnd().CharWeight == FontWeight.BOLD:
                    element.ParaStyleName = "Inter Q"

    def clean_timecode(self):
        logger.debug('Clean timecode')

        # Create Regex descriptor
        rd = self.doc.createReplaceDescriptor()
        rd.SearchRegularExpression = True

        # Replace . or blank char with ':'
        rd.SearchString = '(\d{1,2})\s?[:|.](\d{2})\s?[:|.](\d{2})'
        rd.ReplaceString = "$1:$2:$3"
        self.doc.replaceAll(rd)

        # Replace () or [] with blank char
        rd.SearchString = '[\(|\[](\d{1,2})\s?[:|.](\d{2})\s?[:|.](\d{2})[\)|\]]'
        rd.ReplaceString = "$1:$2:$3"
        self.doc.replaceAll(rd)

        # Be sure hours is made of 2 chars
        rd.SearchString = '\<(\d{1}):(\d{2}):(\d{2})'
        rd.ReplaceString = "0$1:$2:$3"
        self.doc.replaceAll(rd)

        # Place the brackets
        rd.SearchString = '(\d{2}):(\d{2}):(\d{2})'
        rd.ReplaceString = "[$1:$2:$3]"
        self.doc.replaceAll(rd)

    def question_upper(self):
        logger.debug('Upperise question')
        text_enum = self.text.createEnumeration()

        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                if element.ParaStyleName == QUESTION_CSS:
                    element.String = element.String.upper()

    def question_lower(self):
        logger.debug('question lower')
        text_enum = self.text.createEnumeration()

        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                if element.ParaStyleName == QUESTION_CSS and element.String:
                    q = f"{element.String[0:1].upper()}{element.String[1:].lower()}"
                    element.String = q

    def remove_blank_line(self):
        logger.debug('Remove blank lines')
        rd = self.doc.createReplaceDescriptor()
        rd.SearchRegularExpression = True
        rd.SearchString = '^$'
        rd.ReplaceString = ""
        self.doc.replaceAll(rd)

    def order_question(self):
        logger.debug("order question")
        text_enum = self.text.createEnumeration()

        i = 0
        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                if element.ParaStyleName == QUESTION_CSS:
                    element.String = f"{i} - {element.String}"
                    i += 1


def timecode_cleaner(*args):
    logger.debug("call to timecode cleaner")
    doc = Mission()
    doc.clean_timecode()


def order_question(*args):
    logger.debug("call to order_question")
    doc = Mission()
    doc.order_question()


def question_upper(*args):
    logger.debug("call to upperise question")
    doc = Mission()
    doc.question_upper()


def question_lower(*args):
    logger.debug("call to lower question")
    doc = Mission()
    doc.question_lower()


def remove_blank_line(*args):
    logger.debug("call to remove_blank_lines")
    doc = Mission()
    doc.remove_blank_line()


g_exportedScripts = (
    timecode_cleaner,
    order_question,
    question_upper,
    question_lower,
    remove_blank_line,
)
