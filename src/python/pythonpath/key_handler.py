import socket
import json
import logging

import unohelper
from com.sun.star.awt import XKeyHandler

from models import Mission
from utils import timestamps_in_milliseconds, milliseconds_to_timecode, msgbox

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('RDT_TOOLS')


# in case of wx use
import wx_player as pl

# to use with vlc
import vlc_player as ac


KB_REWIND = 768  # F1
KB_PLAYPAUSE = 769
KB_FORWARD = 770
KB_TIMESTAMP = 771
KB_SPEED_DOWN = 772
KB_SPEED_RESET = 773
KB_SPEED_UP = 774


NVIVO = 779  # F12
QUESTION = 778
STANDARD = 777

B = 513
Q = 528
R = 529
K = 522  # inaudible
N = 525  # incompris
Y = 536  # incompris


CNTRL = 2


def send_data(code, **kwargs):
    json_data = json.dumps({'code': code, **kwargs})
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((pl.HOST, pl.PORT))
        s.send(json_data.encode('utf-8'))
        return s.recv(1024)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @property
    def is_running(cls):
        return bool(cls._instances)


class KeyHandler(unohelper.Base, XKeyHandler, metaclass=Singleton):

    components = set()

    def __init__(self, ctx, component, player):
        self.ctx = ctx
        KeyHandler.components.add(component)
        self.player = player

    def disposing(self, ev):
        pass

    def keyPressed(self, ev):
        logger.debug(f"Key code pressed: {ev.KeyCode}")
        try:
            if ev.Modifiers == CNTRL:

                if ev.KeyCode == B:
                    self.mission.wrap_last_word_into_brackets()

                elif ev.KeyCode == Q:
                    self.mission.apply_question_style()

                elif ev.KeyCode == R:
                    self.mission.apply_answer_style()

                elif ev.KeyCode == K:
                    ts = milliseconds_to_timecode(int(send_data(pl.TIMESTAMP)))
                    self.mission.insert_text(f"[inaudible {ts}]")

                elif ev.KeyCode == Y:
                    self.mission.remove_line()

                elif ev.KeyCode == N:
                    ts = milliseconds_to_timecode(int(send_data(pl.TIMESTAMP)))
                    self.mission.insert_text(f"[incompris {ts}]")
                else:
                    return False

            # Audio controls

            elif ev.KeyCode == KB_PLAYPAUSE:
                ts = self.mission.get_selected_timecode()
                if ts:
                    # send_data(pl.READ_FROM_TIMESTAMP,
                    #           timestamp=timestamps_in_milliseconds(ts))
                    ts = timestamps_in_milliseconds(ts)
                    self.player.play_pause(timecode=ts)
                else:
                    # send_data(pl.PLAY_PAUSE)
                    self.player.play_pause()

            elif ev.KeyCode == KB_REWIND:
                # send_data(pl.REWIND)
                self.player.rewind(ac.REWIND_DELAY)

            elif ev.KeyCode == KB_FORWARD:
                # send_data(pl.FORWARD)
                self.player.forward(ac.FORWARD_DELAY)

            elif ev.KeyCode == KB_TIMESTAMP:
                # ts = int(send_data(pl.TIMESTAMP))
                # self.mission.insert_timecode(milliseconds_to_timecode(ts))
                ts = self.player.get_timecode()
                self.mission.insert_timecode(ts)

            elif ev.KeyCode == KB_SPEED_DOWN:
                # send_data(pl.SPEED_DOWN)
                self.player.decrease_rate()

            elif ev.KeyCode == KB_SPEED_RESET:
                # send_data(pl.SPEED_RESET)
                self.player.reset_rate()

            elif ev.KeyCode == KB_SPEED_UP:
                # send_data(pl.SPEED_UP)
                self.player.increase_rate()
            else:
                return False

        except Exception as e:
            msgbox("VLC is closed ! We start it again. ")
            self.player.renew()
        return True

    @property
    def mission(self):
        return Mission(self.ctx)

    def keyReleased(self, ev):
        return False
