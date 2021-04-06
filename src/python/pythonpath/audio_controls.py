import subprocess


def forward():
    cmd = ["playerctl", "position", '2+']
    subprocess.run(cmd)


def rewind():
    cmd = ["playerctl", "position", '2-']
    subprocess.run(cmd)


def play_pause(position):
    if position:
        cmd = ["playerctl", "position", position]
    else:
        cmd = ["playerctl", "play-pause"]
    subprocess.run(cmd)


def get_timecode():
    cmd = ["playerctl", "position"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    position = process.communicate()[0].decode('utf-8')
    m, ss = divmod(float(position), 60)
    h, m = divmod(m, 60)
    s = int(ss)
    ms = int((ss - s) * 1000)
    return f"[{int(h):02}:{int(m):02}:{s:02}.{ms}]"