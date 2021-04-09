import dbus
import decimal
import subprocess

from dbus import DBusException

BUS_NAME = 'org.mpris.MediaPlayer2'
VLC_BUS = BUS_NAME + '.vlc'
PLAYER_BUS = BUS_NAME + '.Player'
OBJECT_PATH = '/org/mpris/MediaPlayer2'

REWIND_VALUE = 1000000  # time is in microseconds
FORWARD_VALUE = 3000000


class Player:
    def __init__(self):
        proxy = dbus.SessionBus().get_object(VLC_BUS, OBJECT_PATH)
        self.interface = dbus.Interface(proxy, dbus_interface=PLAYER_BUS)
        self.track_interface = dbus.Interface(proxy, dbus_interface=BUS_NAME + '.TrackList')
        self.property = dbus.Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')

    def add_track(self, file_path):
        self.track_interface.AddTrack(file_path, '/', True)

    def play_pause(self, timecode=None):
        if timecode:
            timecode = timecode * 1000000
            self.interface.SetPosition(self.trackid, timecode)
            self.interface.Play()
        else:
            self.interface.PlayPause()

    def forward(self, value=FORWARD_VALUE):
        self.interface.Seek(value)

    def rewind(self, value=REWIND_VALUE):
        self.interface.Seek(- value)

    @property
    def rate(self):
        return self.property.Get(PLAYER_BUS, 'Rate')

    @rate.setter
    def rate(self, rate: decimal.Decimal):
        if 0.5 < rate < 2:
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

    def get_timecode(self, milliseconds=True):
        total_seconds = int(self.position)
        ms = int((self.position - total_seconds) * 1000)
        hours, seconds = total_seconds // 3600, total_seconds % 3600
        minutes, seconds = seconds // 60, seconds % 60
        tc = f"{hours:02}:{minutes:02}:{seconds:02}"
        if milliseconds:
            return f"{tc}.{ms}"
        return tc

    @property
    def metadata(self):
        return self.property.Get(PLAYER_BUS, 'Metadata')

    @property
    def trackid(self):
        return str(self.metadata['mpris:trackid'])


def open_vlc(file_path=None):
    try:
        proxy = dbus.SessionBus().get_object(VLC_BUS, OBJECT_PATH)
    except DBusException:
        subprocess.Popen(['vlc'])
    p = Player()
    p.add_track(file_path)


