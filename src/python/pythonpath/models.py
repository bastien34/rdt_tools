import re

from com.sun.star.awt import FontWeight
from com.sun.star.beans import PropertyValue
from com.sun.star.awt.FontSlant import ITALIC
# from debug import mri
from reg_strings import CLEAN_REPLACING_STR, TIMECODE_FIX
from utils import convert_tc_to_seconds


QUESTION_STYLE = "Inter Q"
ANSWER_STYLE = "Inter R"


class Mission:
    def __init__(self, ctx):
        self.ctx = ctx
        self.smgr = self.ctx.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx)
        self.doc = self.desktop.getCurrentComponent()
        self.text = self.doc.Text

    def remove_ms(self):
        self.remove_milliseconds_from_tc()

    def fix_timecodes(self):
        for str_to_replace in TIMECODE_FIX:
            self._replace_string(*str_to_replace)

    def style_tc(self):
        self.apply_style_to_orphan_timecode()

    def rm_empty_lines(self):
        self.remove_blank_line()

    def rm_double_space(self):
        self._remove_blank_space_at_the_end_of_lines()
        self.remove_double_space()

    def force_styling(self):
        self.style_document()

    def force_breaklines(self):
        self._replace_string('\n', '\n')

    def _replace_string(self, search_str, new_str):
        """Function to search & replace regex."""
        rd = self.doc.createReplaceDescriptor()
        rd.SearchRegularExpression = True
        rd.SearchString = search_str
        rd.ReplaceString = new_str
        self.doc.replaceAll(rd)

    def parse_text(self, func):
        """todo: Might be used as decorator."""
        text_enum = self.text.createEnumeration()
        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                func(element)

    def get_selection(self):
        controller = self.doc.getCurrentController()
        return controller.getSelection().getByIndex(0).String

    def _remove_blank_space_at_the_end_of_lines(self):
        self._replace_string('\s*$', '')

    def style_document(self):
        # check if document has INTERQ style
        styles = self.doc.getStyleFamilies().getByName("ParagraphStyles")
        if not styles.hasByName(QUESTION_STYLE):
            return
        self.parse_text(self._apply_document_style)

    def prefix_questions_and_answers(self, p_question, p_answer):
        text_enum = self.text.createEnumeration()
        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                if self.is_bold_element(element):
                    self._prefix_str(p_question, element)
                else:
                    self._prefix_str(p_answer, element)

    def _apply_document_style(self, element):
        is_title = 'title' in element.ParaStyleName.lower()
        if self.is_time_code(element) or is_title:
            return
        if self.is_bold_element(element):
            element.ParaStyleName = QUESTION_STYLE
        else:
            element.ParaStyleName = ANSWER_STYLE

    def is_bold_element(self, element):
        start_str = element.getStart()
        end_str = element.getEnd()
        return start_str.CharWeight == end_str.CharWeight == FontWeight.BOLD

    def is_time_code(self, el):
        string = el.String
        pattern = "^\[\d\d:\d\d:\d\d(.\d+)?\]$"
        return re.search(pattern, string)

    def _apply_style(self, style):
        # todo: this run all over the text & apply style for each line
        controller = self.doc.getCurrentController()
        controller.ViewCursor.ParaStyleName = style

    def apply_question_style_(self):
        """Access direct from libo config."""
        self._apply_style(QUESTION_STYLE)

    def apply_answer_style(self):
        """Access direct from libo config."""
        self._apply_style(ANSWER_STYLE)

    def remove_first_line(self):
        """
        Let here as example but not used any more.
        """
        text_enum = self.text.createEnumeration()
        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                element.dispose()
                break

    def _prefix_str(self, prefix, element):
        string = element.String
        pattern = "^\[\d\d:\d\d:\d\d(.\d+)?\]$"
        match = re.search(pattern, string)
        if string and not match:
            element.String = prefix + " : " + string

    def remove_double_space(self):
        for str_to_replace in CLEAN_REPLACING_STR:
            self._replace_string(*str_to_replace)

    def remove_milliseconds_from_tc(self):
        self._replace_string('(\d{2}:\d{2}:\d{2})(?:[\.|\,](\d+))', "$1$3")

    def wrap_last_word_into_brackets(self):
        controller = self.doc.getCurrentController()
        selected = self.get_selection()
        if selected:
            ns = self._wrap_word_into_brackets(selected)
            controller.getSelection().getByIndex(0).String = ns
        else:
            viewCursor = controller.getViewCursor()
            try:
                textCursor = self.text.createTextCursorByRange(viewCursor)
                textCursor.gotoPreviousWord(False)
                textCursor.gotoNextWord(True)
                expr = self._wrap_word_into_brackets(textCursor.String)
                textCursor.String = expr + " "
                viewCursor.goRight(0, False)
            except:
                pass

    def _wrap_word_into_brackets(self, expression: str) -> str:
        expression = expression.strip()
        return "[" + expression + "]"

    def question_upper(self):
        text_enum = self.text.createEnumeration()

        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                if element.ParaStyleName == QUESTION_STYLE:
                    element.String = element.String.upper()

    def question_lower(self):
        text_enum = self.text.createEnumeration()

        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                if element.ParaStyleName == QUESTION_STYLE and element.String:
                    q = f"{element.String[0:1].upper()}{element.String[1:].lower()}"
                    element.String = q

    def remove_blank_line(self):
        self._replace_string('^$', '')

    def apply_style_to_orphan_timecode(self):
        bold = PropertyValue('CharWeight', 0, FontWeight.BOLD, 0)
        color = PropertyValue('CharColor', 0, 6710932, 0)
        rd = self.doc.createReplaceDescriptor()
        rd.SearchRegularExpression = True
        rd.SearchString = '^\s?(\[\d{2}:\d{2}:\d{2}(.\d+)?\])\s?$'
        rd.setReplaceAttributes((bold, color))
        rd.ReplaceString = "$1"
        self.doc.replaceAll(rd)

    def order_question(self):
        """Place a incremental number before each question"""
        text_enum = self.text.createEnumeration()

        i = 0
        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                if element.ParaStyleName == QUESTION_STYLE:
                    element.String = f"{i} - {element.String}"
                    i += 1

    def get_selected_timecode(self) -> int:
        selected = self.get_selection()
        pattern = "\d\d:\d\d:\d\d"
        match = re.search(pattern, selected)
        if match:
            return convert_tc_to_seconds(match.group())

    def insert_timecode(self, timecode: str):
        self.insert_text('[' + timecode + ']')


    def insert_text(self, expression):
        controller = self.doc.getCurrentController()
        controller.getSelection().getByIndex(0).String = expression + ' '
