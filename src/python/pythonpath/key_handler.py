import unohelper
from com.sun.star.awt import XKeyHandler
from audio_controls import Player
from models import Mission
# from debug import mri

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


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print('call not in instance')
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        print('already created')
        return cls._instances[cls]

    @property
    def is_running(cls):
        return bool(cls._instances)


class KeyHandler(unohelper.Base, XKeyHandler, metaclass=Singleton):

    components = set()

    def __init__(self, ctx, component):
        self.ctx = ctx
        KeyHandler.components.add(component)

    def disposing(self, ev):
        pass

    def keyPressed(self, ev):

       # print(ev.KeyCode)

        try:
            player = Player()
        except:
            return False

        if ev.Modifiers == CNTRL:

            if ev.KeyCode == B:
                self.mission.wrap_last_word_into_brackets()

            elif ev.KeyCode == Q:
                self.mission.apply_question_style()

            elif ev.KeyCode == R:
                self.mission.apply_answer_style()

            elif ev.KeyCode == K:
                tc = player.get_timecode(milliseconds=False)
                self.mission.insert_text(f"[{tc} inaudible]")

            elif ev.KeyCode == N:
                tc = player.get_timecode(milliseconds=False)
                self.mission.insert_text(f"[{tc} incompris]")
            else:
                return False

        # Audio controls

        elif ev.KeyCode == PLAYPAUSE:
            # player.play_pause()
            player.play_pause(self.mission.get_selected_timecode())

        elif ev.KeyCode == REWIND:
            player.rewind()

        elif ev.KeyCode == FORWARD:
            player.forward()

        elif ev.KeyCode == PUSH_TIMECODE:
            self.mission.insert_timecode(player.get_timecode())

        elif ev.KeyCode == DECREASE_RATE:
            player.decrease_rate()

        elif ev.KeyCode == RESET_RATE:
            player.reset_rate()

        elif ev.KeyCode == INCREASE_RATE:
            player.increase_rate()

        else:
            return False

        return True

    @property
    def mission(self):
        return Mission(self.ctx)

    def keyReleased(self, ev):
        return False
