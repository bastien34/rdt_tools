#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Bastien Roques
Date: 21-03-2022
"""

__version__ = '22.03.21'

from wxasync import WxAsyncApp, StartCoroutine
import asyncio
import json
import datetime

import wx
import vlc
from os.path import basename, expanduser, isfile, join as joined
import sys


EVT_RESULT_ID = wx.NewIdRef(count=1)

# Socket
HOST = '127.0.0.1'
PORT = 8888

# Vlc commands
PLAY_PAUSE = '10'
REWIND = '20'
FORWARD = '30'
SPEED_UP = '40'
SPEED_DOWN = '50'
SPEED_RESET = '55'
TIMESTAMP = '60'
READ_FROM_TIMESTAMP = '70'

FORWARD_DELAY = 3000
REWIND_DELAY = 3000

TITLE = 'RDT Player'


class Player(wx.Frame):
    """The main window has to deal with events.
    """
    def __init__(self, title='', video=''):
        wx.Frame.__init__(self, None, -1, title=TITLE, pos=wx.DefaultPosition,
                          size=(550, 600))

        self.video = video

        # Menu Bar
        #   File Menu
        self.frame_menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.file_menu.Append(1, "&Open...", "Open from file...")
        self.file_menu.AppendSeparator()
        self.file_menu.Append(2, "&Close", "Quit")
        self.Bind(wx.EVT_MENU, self.OnOpen, id=1)
        self.Bind(wx.EVT_MENU, self.OnExit, id=2)
        self.frame_menubar.Append(self.file_menu, "File")
        self.SetMenuBar(self.frame_menubar)

        # Panels
        # The first panel holds the video and it's all black
        self.videopanel = wx.Panel(self, -1)
        self.videopanel.SetBackgroundColour(wx.BLACK)

        # The second panel holds controls
        ctrlpanel = wx.Panel(self, -1)
        self.clock = wx.StaticText(ctrlpanel)
        self.clock.SetLabel('HH:MM:SS')
        self.timeslider = wx.Slider(ctrlpanel, -1, 0, 0, 1000)
        self.timeslider.SetRange(0, 1000)
        self.pause = wx.Button(ctrlpanel, label="Pause")
        self.pause.Disable()
        self.play = wx.Button(ctrlpanel, label="Play")
        self.stop = wx.Button(ctrlpanel, label="Stop")
        self.stop.Disable()
        self.mute = wx.Button(ctrlpanel, label="Mute")
        self.volslider = wx.Slider(ctrlpanel, -1, 0, 0, 100, size=(100, -1))
        self.rateLabel = wx.StaticText(ctrlpanel, -1, '1.0', (50, -1))
        # Bind controls to events
        self.Bind(wx.EVT_BUTTON, self.OnPlay,   self.play)
        self.Bind(wx.EVT_BUTTON, self.OnPause,  self.pause)
        self.Bind(wx.EVT_BUTTON, self.OnStop,   self.stop)
        self.Bind(wx.EVT_BUTTON, self.OnMute,   self.mute)
        self.Bind(wx.EVT_SLIDER, self.OnVolume, self.volslider)
        self.Bind(wx.EVT_SCROLL, self.OnTimer, self.timeslider)

        # Give a pretty layout to the controls
        ctrlbox = wx.BoxSizer(wx.VERTICAL)
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        # box1 contains the timeslider

        box1.Add(self.clock, 1, flag=wx.EXPAND, border=10)
        box1.Add(self.timeslider, 2)
        # box2 contains some buttons and the volume controls
        box2.Add(self.play, flag=wx.RIGHT, border=5)
        box2.Add(self.pause)
        box2.Add(self.stop)
        box2.Add((-1, -1), 1)
        box2.Add(self.mute)
        box2.Add(self.volslider, flag=wx.TOP | wx.LEFT, border=5)
        box2.Add(self.rateLabel, flag=wx.TOP | wx.LEFT, border=5)
        # Merge box1 and box2 to the ctrlsizer
        ctrlbox.Add(box1, flag=wx.EXPAND | wx.BOTTOM, border=10)
        ctrlbox.Add(box2, 1, wx.EXPAND)
        ctrlpanel.SetSizer(ctrlbox)

        # Put everything togheter
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.videopanel, 1, flag=wx.EXPAND)
        sizer.Add(ctrlpanel, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)

        # # log panel
        # logPan = wx.Panel(self)
        # logbox = wx.BoxSizer(wx.HORIZONTAL)
        # logbox.Add((10, 100))
        # # logbox.AddStretchSpacer(1)
        # self.logctrl = wx.TextCtrl(logPan, style=wx.TE_MULTILINE)
        # logPan.SetSizer(logbox)
        # logbox.Add(self.logctrl, flag=wx.EXPAND | wx.BOTTOM, border=10)

        self.SetSizer(sizer)
        self.SetMinSize((350, 300))
        # logPan.SetSizer(logbox)

        # finally create the timer, which updates the timeslider
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

        # EVT_RESULT(self, self.socket_handler)
        StartCoroutine(self.run_server, self)

    # def log(self, text):
    #     self.logctrl.AppendText(text + "\r\n")

    async def handle_connection(self, reader, writer):
        data = await reader.read(100)
        message = json.loads(data.decode())
        addr = writer.get_extra_info('peername')
        # self.log(f"Received {message!r} from {addr!r}")
        # self.log(f"Send: {message!r}")
        resp = self.socket_handler(message)
        writer.write(f"{resp}".encode())
        await writer.drain()
        # self.log("Close the connection")
        writer.close()

    async def run_server(self):
        server = await asyncio.start_server(self.handle_connection, HOST, PORT)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        # self.log(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()

    def socket_handler(self, message, timestamp=None):
        order = message['code']
        if order == PLAY_PAUSE:
            self.OnPause()
        if order == REWIND:
            self.OnRewind()
        if order == FORWARD:
            self.OnForward()
        elif order == TIMESTAMP:
            return self.OnTimeStamp()
        elif order == READ_FROM_TIMESTAMP:
            self.OnSetTimeStamp(message['timestamp'])
        elif order == SPEED_UP:
            self.OnRate(method=1)
        elif order == SPEED_DOWN:
            self.OnRate(method=-1)
        elif order == SPEED_RESET:
            self.OnRate()
        return

    def OnExit(self, evt):
        """Closes the window.
        """
        self.Close()

    def OnOpen(self, evt):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        # if a file is already running, then stop it.
        self.OnStop(None)

        video = self.video
        if video:
            self.video = ''
        else:  # Create a file dialog opened in the current home directory,
            # to show all kind of files, having as title "Choose a ...".
            dlg = wx.FileDialog(self, "Choose a video file", expanduser('~'),
                                      "", "*.*", wx.FD_OPEN)  # XXX wx.OPEN
            if dlg.ShowModal() == wx.ID_OK:
                video = joined(dlg.GetDirectory(), dlg.GetFilename())
            # finally destroy the dialog
            dlg.Destroy()

        if isfile(video):  # Creation
            self.Media = self.Instance.media_new(str(video))
            self.player.set_media(self.Media)
            # print(str(video))
            # Report the title of the file chosen
            title = self.player.get_title()
            # if an error was encountred while retrieving the title,
            # otherwise use filename
            self.SetTitle("%s - %s" % (title if title != -1 else 'wxVLC', basename(video)))
            self.SetTitle(f"RDT - {basename(video)}")
            # set the window id where to render VLC's video output
            handle = self.videopanel.GetHandle()
            if sys.platform.startswith('linux'):  # for Linux using the X Server
                self.player.set_xwindow(handle)
            elif sys.platform == "win32":  # for Windows
                self.player.set_hwnd(handle)
            elif sys.platform == "darwin":  # for MacOS
                self.player.set_nsobject(handle)
            self.OnPlay(None)

            # set the volume slider to the current volume
            # self.volslider.SetValue(self.player.audio_get_volume() / 2)

    def OnPlay(self, evt=None):
        """Toggle the status to Play/Pause.

        If no file is loaded, open the dialog window.
        """

        # check if there is a file to play, otherwise open a
        # wx.FileDialog to select a file
        if not self.player.get_media():
            self.OnOpen(None)
            # Try to launch the media, if this fails display an error message
        elif self.player.play():  # == -1:
            self.errorDialog("Unable to play.")
        else:
            # adjust window to video aspect ratio
            # w, h = self.player.video_get_size()
            # if h > 0 and w > 0:  # often (0, 0)
            #     self.videopanel....
            self.timer.Start(1000)  # XXX millisecs
            self.play.Disable()
            self.pause.Enable()
            self.stop.Enable()

    def OnPause(self, evt=None):
        """Pause the player.
        """
        if self.player.is_playing():
            self.play.Enable()
            self.pause.Disable()
        elif self.player.can_pause():
            self.play.Disable()
            self.pause.Enable()
        else:
            self.OnPlay()
        self.player.pause()

    def OnStop(self, evt):
        """Stop the player.
        """
        self.player.stop()
        # reset the time slider
        self.timeslider.SetValue(0)
        self.timer.Stop()
        self.play.Enable()
        self.pause.Disable()
        self.stop.Disable()

    def OnTimer(self, evt):
        """Update the time slider according to the current movie time.
        """
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        if evt.EventType == wx.EVT_TIMER.typeId:
            length = self.player.get_length()
            self.timeslider.SetRange(-1, length)
            time = self.player.get_time()
            self.timeslider.SetValue(time)
        else:
            time = self.timeslider.GetValue()
            self.timeslider.SetValue(time)
            self.player.set_time(time)
        self.set_timer(time)

    def set_timer(self, position):
        """Update Timer Slider control."""
        str_pos = str(datetime.timedelta(milliseconds=position)).split('.')[0]
        self.clock.SetLabel(str_pos)

    def OnMute(self, evt):
        """Mute/Unmute according to the audio button.
        """
        muted = self.player.audio_get_mute()
        self.player.audio_set_mute(not muted)
        self.mute.SetLabel("Mute" if muted else "Unmute")
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        # self.volslider.SetValue(self.player.audio_get_volume() / 2)

    def OnVolume(self, evt):
        """Set the volume according to the volume sider.
        """
        volume = self.volslider.GetValue() * 2
        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def OnRate(self, evt=None, method=0):
        """Set the volume according to the volume sider.
        """
        rate = self.player.get_rate()
        if method > 0:
            new_rate = rate + 0.1
        elif method < 0:
            new_rate = rate - 0.1
        else:
            new_rate = 1
        print("new rate: ", new_rate)
        self.player.set_rate(new_rate)
        self.rateLabel.SetLabel(str(round(new_rate, 1)))

    def OnRewind(self, evt=None):
        self.player.set_time(self.player.get_time() - REWIND_DELAY)

    def OnForward(self, evt=None):
        self.player.set_time(self.player.get_time() + FORWARD_DELAY)

    def OnTimeStamp(self, evt=None):
        return self.player.get_time()

    def OnSetTimeStamp(self, position):
        self.player.set_time(position)

    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        edialog = wx.MessageDialog(self, errormessage, 'Error', wx.OK|
                                                                wx.ICON_ERROR)
        edialog.ShowModal()


async def main(video=''):
    print(sys.argv)
    app = WxAsyncApp()
    frame = Player(video=video)
    frame.Show()
    app.SetTopWindow(frame)
    await app.MainLoop()


if __name__ == "__main__":
    _video = ''

    while len(sys.argv) > 1:
        arg = sys.argv.pop(1)
        if arg.lower() in ('-v', '--version'):
            try:
                print(vlc.libvlc_get_version())
            except AttributeError:
                pass
            sys.exit(0)

        elif arg.startswith('-'):
            print('usage: %s  [-v | --version]  [<video_file_name>]' % (sys.argv[0],))
            sys.exit(1)

        elif arg:
            _video = expanduser(arg)
            if not isfile(_video):
                print(f'{sys.argv[0]} error: no such file: {arg}')
                sys.exit(1)

    asyncio.run(main(_video))
