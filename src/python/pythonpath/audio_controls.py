import subprocess


def forward():
    cmd = ["playerctl", "position", '2+']
    subprocess.run(cmd)


def rewind():
    cmd = ["playerctl", "position", '2-']
    subprocess.run(cmd)


def play_pause(position):
    if position:
        subprocess.run(["playerctl", "position", str(position)])
        subprocess.run(["playerctl", "play"])
    else:
        subprocess.run(["playerctl", "play-pause"])


def get_timecode(milliseconds=True):
    cmd = ["playerctl", "position"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    position = process.communicate()[0].decode('utf-8')
    m, ss = divmod(float(position), 60)
    h, m = divmod(m, 60)
    seconds = int(ss)
    ms = int((ss - seconds) * 1000)
    if milliseconds:
        return f"[{int(h):02}:{int(m):02}:{seconds:02}.{ms}] "
    else:
        return f"{int(h):02}:{int(m):02}:{seconds:02}"