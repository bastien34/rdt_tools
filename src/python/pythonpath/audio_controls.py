import subprocess
import dbus
import decimal
from utils import seconds_to_timecode


BUS_NAME = 'org.mpris.MediaPlayer2'
VLC_BUS = BUS_NAME + '.vlc'
PLAYER_BUS = BUS_NAME + '.Player'
OBJECT_PATH = '/org/mpris/MediaPlayer2'

REWIND_VALUE = 3000000
FORWARD_VALUE = 3000000



class Player:
    def __init__(self):
        proxy = dbus.SessionBus().get_object(VLC_BUS, OBJECT_PATH)
        self.interface = dbus.Interface(proxy, dbus_interface=PLAYER_BUS)
        self.property = dbus.Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')

    def play_pause(self, timecode=None):
        if timecode:
            self.interface.Seek(timecode)
            self.interface.Play()
        else:
            self.interface.PlayPause()

    def forward(self, value=FORWARD_VALUE):
        self.interface.Seek(self.position + value)

    def rewind(self, value=REWIND_VALUE):
        self.interface.Seek(self.position - value)

    @property
    def rate(self):
        return self.property.Get(PLAYER_BUS, 'Rate')

    @rate.setter
    def rate(self, rate: decimal.Decimal):
        if 0.5  < rate < 2:
            self.property.Set(PLAYER_BUS, 'Rate', rate)

    def increase_rate(self):
        self.rate = self.rate + 0.1

    def decrease_rate(self):
        self.rate = self.rate - 0.1

    def reset_rate(self):
        self.rate = 1.0

    @property
    def position(self):
        """Return position in seconds"""
        pos = self.property.Get(PLAYER_BUS, 'Position').as_integer_ratio()[0]
        return pos / 1000000

    @position.setter
    def position(self, position: decimal.Decimal):
        self.property.Set(PLAYER_BUS, 'Position', position)

    def get_timecode(self, milliseconds=True):
        total_seconds = int(self.position)
        ms = int((self.position - total_seconds) * 1000)
        hours, seconds = total_seconds // 3600, total_seconds % 3600
        minutes, seconds = seconds // 60, seconds % 60
        tc = f"{hours:02}:{minutes:02}:{seconds:02}"
        if milliseconds:
            return f"{tc}.{ms}"
        return tc



# def get_timecode(milliseconds=True):
#     cmd = ["playerctl", "position"]
#     process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
#     position = process.communicate()[0].decode('utf-8')
#     m, ss = divmod(float(position), 60)
#     h, m = divmod(m, 60)
#     seconds = int(ss)
#     ms = int((ss - seconds) * 1000)
#     if milliseconds:
#         return f"[{int(h):02}:{int(m):02}:{seconds:02}.{ms}] "
#     else:
#         return f"{int(h):02}:{int(m):02}:{seconds:02}"