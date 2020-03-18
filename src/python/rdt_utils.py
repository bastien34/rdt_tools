import logging
import uno
import unohelper
from com.sun.star.task import XJobExecutor
from com.sun.star.awt import FontWeight

# debug
from IPython.core.debugger import Pdb
ipdb = Pdb()
from debug import mri


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('doc_cleaner')


class Mission:

    def __init__(self):
        self.ctx = XSCRIPTCONTEXT.getComponentContext()
        self.smgr = self.ctx.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx )
        self.doc = self.desktop.getCurrentComponent()
        self._remove_blank_space_at_the_end_of_lines()
        logger.debug('Mission instanciated!')

    def _remove_blank_space_at_the_end_of_lines(self):
        rd = self.doc.createReplaceDescriptor()
        rd.SearchRegularExpression = True
        rd.SearchString = '\s*$'
        rd.ReplaceString = ""
        self.doc.replaceAll(rd)

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

    def upperise_question(self):
        vtext = self.doc.Text
        text_enum = vtext.createEnumeration()

        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                # element.CharWeight is not reliable. We check first & last letter
                # to determine if **element** is a question
                if element.getStart().CharWeight == FontWeight.BOLD \
                        or element.getEnd().CharWeight == FontWeight.BOLD:
                    element.ParaStyleName = "Inter Q"
                    element.String = element.String.upper()

    def remove_blank_line(self):
        rd = self.doc.createReplaceDescriptor()
        rd.SearchRegularExpression = True
        rd.SearchString = '^\s*$'
        rd.ReplaceString = ""
        self.doc.replaceAll(rd)


def timecode_cleaner(*args):
    doc = Mission()
    doc.clean_timecode()


def order_question(*args):
    doc = Mission()
    doc.upperise_question()


def upperise_question(*args):
    doc = Mission()
    doc.upperise_question()


def remove_blank_line(*args):
    doc = Mission()
    doc.remove_blank_line()


g_exportedScripts = (
    timecode_cleaner,
    order_question,
    upperise_question,
    remove_blank_line,
)
