import re

from com.sun.star.awt import FontWeight
from reg_strings import CLEAN_REPLACING_STR, TIMECODE_FIX


TIMECODE_STYLE = 'Timecode'

QUESTION_STYLE = "Question"
VERBATIM_STYLE = "Verbatim"


class Mission:
    def __init__(self, ctx):
        self.ctx = ctx
        self.smgr = self.ctx.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx)
        self.doc = self.desktop.getCurrentComponent()
        self.text = self.doc.Text
        self.question_style = QUESTION_STYLE
        self.verbatim_style = VERBATIM_STYLE

    def remove_ms(self):
        self.remove_milliseconds_from_tc()

    def fix_timecodes(self):
        for str_to_replace in TIMECODE_FIX:
            self._replace_string(*str_to_replace)
        self.parse_text(self._add_brackets_to_timecode)

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
        # check if document has correct styles
        # todo: after summer 22 remove inter Q check
        styles = self.doc.getStyleFamilies().getByName("ParagraphStyles")
        if not styles.hasByName(VERBATIM_STYLE):
            self.question_style = 'Inter Q'
            self.verbatim_style = 'Inter R'
        if not styles.hasByName('Inter Q'):
            return
        print(self.question_style, self.verbatim_style)
        self.parse_text(self._apply_document_style)

    def prefix_questions_and_answers(self, p_question, p_answer, must_count=False):
        text_enum = self.text.createEnumeration()
        i = 0

        def get_prefix_to_place(element):
            if self.is_bold_element(element):
                return p_question
            return p_answer

        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                string = self.get_prefixable_string(element)
                if string:
                    i += 1
                    count = str(i) if must_count else ''
                    prefix = get_prefix_to_place(element)
                    element.String = prefix + count + " : " + string

    def _apply_style(self, style):
        # todo: this run all over the text & apply style for each line
        controller = self.doc.getCurrentController()
        controller.ViewCursor.ParaStyleName = style

    def get_prefixable_string(self, element):
        """
        Style name containing 'title' are excluded (document title & subtile).
        """
        string = element.String
        pattern = "^\[\d\d:\d\d:\d\d(.\d+)?\]$"
        match = re.search(pattern, string)
        if not match and 'title' not in element.ParaStyleName.lower():
            return string

    def _apply_document_style(self, element):
        self.create_timecode_style()

        is_title = 'title' in element.ParaStyleName.lower()
        is_line = 'line' == element.ParaStyleName

        if is_title or is_line:
            return

        if self.is_bold_element(element):
            element.ParaStyleName = self.question_style
        else:
            element.ParaStyleName = self.verbatim_style

        if self.is_time_code(element):
            element.ParaStyleName = TIMECODE_STYLE

    def is_bold_element(self, element):
        start_str = element.getStart()
        end_str = element.getEnd()
        return start_str.CharWeight == end_str.CharWeight == FontWeight.BOLD

    def is_time_code(self, el):
        string = el.String
        pattern = "^\[\d\d:\d\d:\d\d(.\d+)?\]$"
        return re.search(pattern, string)

    def apply_question_style(self):
        """Access direct from libo config."""
        self._apply_style(self.question_style)

    def apply_answer_style(self):
        """Access direct from libo config."""
        self._apply_style(self.verbatim_style)

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

    def _add_brackets_to_timecode(self, element):
        # replace parenthesis with brackets
        self.sub = re.sub(r'[\[|(]?\b(\d{2}:\d{2}:\d{2}(?:\.\d+)?)\b[]|)]?',
                          r'[\1]', element.String)
        element.String = self.sub
        # avoid [bla bla [HH:MM:SS] (remove the double opening bracket)
        element.String = re.sub(r'(\[[^\]]*)\[', r'\1', element.String)
        element.String = re.sub(r'\]([^\[]*\])', r'\1', element.String)

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
                if element.ParaStyleName == self.question_style:
                    element.String = element.String.upper()

    def question_lower(self):
        text_enum = self.text.createEnumeration()

        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                if element.ParaStyleName == self.question_style and element.String:
                    q = f"{element.String[0:1].upper()}{element.String[1:].lower()}"
                    element.String = q

    def remove_blank_line(self):
        self._replace_string('^$', '')

    def remove_line(self):
        vCursor = self.doc.getCurrentController().getViewCursor()
        vCursor.gotoStartOfLine(False)
        vCursor.gotoEndOfLine(True)
        vCursor.goRight(1, True)
        vCursor.setString('')

    def apply_style_to_orphan_timecode(self):
        pass

    def create_timecode_style(self):
        """
        If styles are not found, create them. Used only for timecode
        style, for now.
        :return:
        """
        new_style = self.doc.createInstance('com.sun.star.style.ParagraphStyle')
        par_styles = self.doc.getStyleFamilies()['ParagraphStyles']
        if not par_styles.hasByName(TIMECODE_STYLE):
            par_styles.insertByName(TIMECODE_STYLE, new_style)
            new_style.ParentStyle = self.question_style
            new_style.CharColor = 6710932
            new_style.CharWeight = FontWeight.BOLD

        # bold = PropertyValue('CharWeight', 0, FontWeight.BOLD, 0)
        # color = PropertyValue('CharColor', 0, 6710932, 0)
        # rd = self.doc.createReplaceDescriptor()
        # rd.SearchRegularExpression = True
        # rd.SearchString = '^\s?(\[\d{2}:\d{2}:\d{2}(.\d+)?\])\s?$'
        # rd.setReplaceAttributes((bold, color))
        # rd.ReplaceString = "$1"
        # mri(rd)
        # self.doc.replaceAll(rd)

    def order_question(self):
        """
        Place an incremental number before each alinea.

            B1: je pose une question et je veux une réponse.
            A2: première réponse
            A3: deuxième

        """
        text_enum = self.text.createEnumeration()

        i = 1
        while text_enum.hasMoreElements():
            element = text_enum.nextElement()
            if element.supportsService("com.sun.star.text.Paragraph"):
                if not self.is_orphan_timecode(element.String):
                    i = self._prefix(element, i)

    def _prefix(self, element, i):
        if element.ParaStyleName == self.question_style:
            element.String = f"B{i} : {element.String}"
            i += 1
        elif element.ParaStyleName == self.verbatim_style:
            element.String = f"A{i} : {element.String}"
            i += 1
        return i

    def get_selected_timecode(self):
        selected = self.get_selection()
        match = self.is_timecode(selected)
        if match:
            return match

    def is_timecode(self, selected: str):
        pattern = "\d\d:\d\d:\d\d"
        match = re.search(pattern, selected)
        if match:
            return match.group()

    def is_orphan_timecode(self, selected: str):
        pattern = "^\d\d:\d\d:\d\d$"
        match = re.search(pattern, selected)
        if match:
            return match.group()

    def insert_timecode(self, timecode: str):
        self.insert_text(timecode)

    def insert_text(self, expression):
        controller = self.doc.getCurrentController()
        controller.getSelection().getByIndex(0).String = expression + ' '
