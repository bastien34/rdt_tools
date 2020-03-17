import logging
import uno
import unohelper
from com.sun.star.task import XJobExecutor

# debug
from IPython.core.debugger import Pdb
ipdb = Pdb()
from utils import mri


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('tcm')


ctx = XSCRIPTCONTEXT


class TimeCodeCleaner(unohelper.Base, XJobExecutor):

    def __init__(self, ctx):
        self.ctx = ctx

    def trigger(self, args):
        logger.debug("Logger says Launcher's been called.")
        desktop = self.ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx )
        doc = desktop.getCurrentComponent()

        try:
            search = doc.createSearchDescriptor()
            search.SearchRegularExpression = True
            search.SearchString = "orking"

            found = doc.findFirst( search )
            while found:
                found.String = found.String.replace( "o", u"\xa0" )
                logger.debug('something has been done.')
                found = doc.findNext( found.End, search)
        except:
            logger.debug('Something has not been done!!!')


def get_current_doc():
    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx )
    logger.debug('Getting current doc!')
    return desktop.getCurrentComponent()


def timecode_cleaner_(*args):
    logger.debug('Launching timecode cleaner')
    doc = get_current_doc()

    # Create Regex descriptor
    rd = doc.createReplaceDescriptor()
    rd.SearchRegularExpression = True

    # Replace . or blank char with ':'
    rd.SearchString = '(\d{1,2})\s?[:|.](\d{2})\s?[:|.](\d{2})'
    rd.ReplaceString = "$1:$2:$3"
    doc.replaceAll(rd)

    # Replace () or [] with blank char
    rd.SearchString = '[\(|\[](\d{1,2})\s?[:|.](\d{2})\s?[:|.](\d{2})[\)|\]]'
    rd.ReplaceString = "$1:$2:$3"
    doc.replaceAll(rd)

    # Be sure hours is made of 2 chars
    rd.SearchString = '\<(\d{1}):(\d{2}):(\d{2})'
    rd.ReplaceString = "0$1:$2:$3"
    doc.replaceAll(rd)

    # Place the brackets
    rd.SearchString = '(\d{2}):(\d{2}):(\d{2})'
    rd.ReplaceString = "[$1:$2:$3]"
    doc.replaceAll(rd)


# def order_question(*args):
def timecode_cleaner(*args):
    from com.sun.star.beans import PropertyValue
    from com.sun.star.awt import FontWeight

    doc = get_current_doc()

    # Remove blank char at the end of lines
    rd = doc.createReplaceDescriptor()
    rd.SearchRegularExpression = True
    rd.SearchString = '\s$'
    rd.ReplaceString = ""
    doc.replaceAll(rd)

    vtext = doc.Text
    text_enum = vtext.createEnumeration()

    styles = doc.StyleFamilies.getByName("ParagraphStyles")
    interQ = styles.getByName("Inter Q")

    while text_enum.hasMoreElements():
        element = text_enum.nextElement()
        if element.supportsService("com.sun.star.text.Paragraph"):
            if element.CharWeight in (FontWeight.BOLD,):
                logger.debug("bold detected")
                element.String = element.String.upper()

            else:
                logger.debug(element.ParaStyleName)
                if element.String.startswith("Ça ne"):
                    mri(element)
                    element.ParaStyleName = "Inter Q"

    # todo: a solution is to select first word, see if it's bold and
    # todo: apply interq style there, then upperise()

    # Create Regex descriptor
    # rd = doc.createReplaceDescriptor()
    # rd.SearchStyles = True
    # rd.SearchAll = True
    # search_attr = PropertyValue()
    # search_attr.Name = "CharWeight"
    # search_attr.Value = FontWeight.BOLD
    #
    # mri(rd)
    # repl_attr = PropertyValue()
    # repl_attr.Name = "CharWeight"
    # repl_attr.Value = FontWeight.NORMAL
    #
    # rd.SetSearchAttributes((search_attr,))
    # rd.SetReplaceAttributes((repl_attr,))
    #
    # doc.replaceAll(rd)


g_exportedScripts = timecode_cleaner,
