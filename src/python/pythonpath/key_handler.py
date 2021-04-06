import unohelper
from com.sun.star.awt import XKeyHandler
from audio_controls import forward, rewind, get_position, play_pause


retour = 768  # F1
avance = 770
playPause = 769
position = 771
lireTC = 772
nVivo = 779  # F12
question = 778
standard = 777
correctTimecodeKey = 778
B = 513

CNTRL = 2


class KeyHandler(unohelper.Base, XKeyHandler):
    def __init__(self, mission):
        self.mission = mission

    def disposing(self, ev):
        pass

    def keyPressed(self, ev):
        print(ev.KeyCode)

        if ev.Modifiers == CNTRL and ev.KeyCode == B:
            self.mission.wrap_last_word_into_brackets()
            print('into brackets')

        if ev.KeyCode == playPause:
            print('play - pause')
            playPause(self.mission.get_selected_timecode())
            return True

        return False

    def keyReleased(self, ev):
        return False

