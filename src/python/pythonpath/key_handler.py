import unohelper
from com.sun.star.awt import XKeyHandler
from audio_controls import Player


REWIND = 768  # F1
PLAYPAUSE = 769
FORWARD = 770
PUSH_TIMECODE = 771
DECREASE_RATE = 772
RESET_RATE = 773
INCREASE_RATE = 774

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
        self.player = self._init_player()

    def _init_player(self):
        try:
            self.player = Player()
        except:
            return None

    def disposing(self, ev):
        pass

    def keyPressed(self, ev):
        if not self.player:
            if not self._init_player():
                return False

        if ev.Modifiers == CNTRL:

            if ev.KeyCode == B:
                self.mission.wrap_last_word_into_brackets()

            elif ev.KeyCode == Q:
                self.mission.apply_question_style()

            elif ev.KeyCode == R:
                self.mission.apply_answer_style()

            elif ev.KeyCode == K:
                tc = self.player.get_timecode(milliseconds=False)
                self.mission.insert_text(f"[{tc} inaudible]")

            elif ev.KeyCode == N:
                tc = self.player.get_timecode(milliseconds=False)
                self.mission.insert_text(f"[{tc} incompris]")
            else:
                return False

        # Audio controls

        elif ev.KeyCode == PLAYPAUSE:
            self.player.play_pause(self.mission.get_selected_timecode())

        elif ev.KeyCode == REWIND:
            self.player.rewind()

        elif ev.KeyCode == FORWARD:
            self.player.forward()

        elif ev.KeyCode == PUSH_TIMECODE:
            self.mission.insert_timecode(self.player.get_timecode())

        elif ev.KeyCode == DECREASE_RATE:
            self.player.decrease_rate()

        elif ev.KeyCode == RESET_RATE:
            self.player.reset_rate()

        elif ev.KeyCode == INCREASE_RATE:
            self.player.increase_rate()

        else:
            return False

        return True

    def keyReleased(self, ev):
        return False
