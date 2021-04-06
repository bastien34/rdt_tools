import unohelper
from com.sun.star.awt import XKeyHandler
from audio_controls import forward, rewind, get_timecode, play_pause


REWIND = 768  # F1
FORWARD = 770
PLAYPAUSE = 769
PUSH_TIMECODE = 771

NVIVO = 779  # F12
QUESTION = 778
STANDARD = 777

B = 513
Q = 528
R = 529

CNTRL = 2


class KeyHandler(unohelper.Base, XKeyHandler):
    def __init__(self, mission):
        self.mission = mission

    def disposing(self, ev):
        pass

    def keyPressed(self, ev):
        key_pressed = True

        # Editing

        if ev.Modifiers == CNTRL and ev.KeyCode == B:
            self.mission.wrap_last_word_into_brackets()

        elif ev.Modifiers == CNTRL and ev.KeyCode == Q:
            self.mission.apply_question_style()

        elif ev.Modifiers == CNTRL and ev.KeyCode == R:
            self.mission.apply_answer_style()

        # Audio controls

        elif ev.KeyCode == PLAYPAUSE:
            play_pause(self.mission.get_selected_timecode())

        elif ev.KeyCode == REWIND:
            rewind()

        elif ev.KeyCode == FORWARD:
            forward()

        elif ev.KeyCode == PUSH_TIMECODE:
            self.mission.insert_timecode(get_timecode())

        else:
            key_pressed = False

        return key_pressed

    def keyReleased(self, ev):
        return False

