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
K = 522  # inaudible
N = 525  # incompris

CNTRL = 2


class KeyHandler(unohelper.Base, XKeyHandler):
    def __init__(self, mission):
        self.mission = mission

    def disposing(self, ev):
        pass

    def keyPressed(self, ev):

        if ev.Modifiers == CNTRL:

            if ev.KeyCode == B:
                self.mission.wrap_last_word_into_brackets()

            elif ev.KeyCode == Q:
                self.mission.apply_question_style()

            elif ev.KeyCode == R:
                self.mission.apply_answer_style()

            elif ev.KeyCode == K:
                tc = get_timecode(milliseconds=False)
                self.mission.insert_text(f"[{tc} inaudible]")

            elif ev.KeyCode == N:
                tc = get_timecode(milliseconds=False)
                self.mission.insert_text(f"[{tc} incompris]")
            else:
                return False

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
            return False

        return True

    def keyReleased(self, ev):
        return False
