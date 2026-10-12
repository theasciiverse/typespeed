#!/usr/bin/env python3
"""Records asciiverse/typespeed.cast, typespeed's catalog preview, at 100x30
(hub/RECORDING.md): the menu, the "Unix commands" word list, then about
30 s of play by a simple typist that reads the screen (pyte) and types the
word nearest the right edge, at roughly 90 words per minute. Quits through
the menu at the end. Needs pyte (pip install pyte). Usage, from the repo
root after asciiverse/build.sh:
    python3 asciiverse/record-preview.py"""
import os, pty, re, struct, fcntl, select, shutil, tempfile, termios, time
import pyte

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
home = tempfile.mkdtemp()
env = dict(os.environ, HOME=home, TERM="xterm-256color", COLORTERM="truecolor", LANG="C.UTF-8",
           TYPESPEED_WORDDIR=f"{root}/words", TYPESPEED_RULEDIR=f"{root}/rules")
screen = pyte.Screen(100, 30)
stream = pyte.ByteStream(screen)
DOWN = b"\x1bOB"          # typespeed's curses keypad mode: application cursor keys

pid, fd = pty.fork()
if pid == 0:
    os.execvpe("asciinema", ["asciinema", "rec", "--overwrite", "-q", "-i", "2",
        "--capture-env", "TERM,COLORTERM,LANG", "-c", f"{root}/src/typespeed",
        f"{root}/asciiverse/typespeed.cast"], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))

def pump(t):
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.02)
        if r:
            try: stream.feed(os.read(fd, 65536))
            except OSError: return

def key(k, wait):
    os.write(fd, k); pump(wait)

pump(3.0)
key(b"1", 1.5)                                  # Test Your Speed
for _ in range(13): key(DOWN, 0.18)             # down to "Unix commands"
key(b"\r", 2.5)

end = time.time() + float(os.environ.get('PLAY_SECONDS', 25))
while time.time() < end:
    # words fly above the divider, which curses draws in the line-drawing
    # charset; pyte shows those characters as plain 'q'
    rows = []
    for l in screen.display:
        if re.match(r"\s*q{20,}", l): break
        rows.append(l)
    words = [(m.end(), m.group()) for l in rows for m in re.finditer(r"\S+", l)]
    if not words:
        pump(0.2); continue
    word = max(words)[1]                        # the one closest to escaping
    for c in word: key(c.encode(), 0.11)
    key(b"\r", 0.35)

pump(1.5)
key(b"\x1b", 2.5)                               # end the game: result screen
# then keep answering until typespeed has quit: any key leaves the result
# screen, a high score asks for a name, 7 quits from the menu
for _ in range(40):
    if os.waitpid(pid, os.WNOHANG)[0]: break
    shown = "\n".join(screen.display)
    if "Choose:" in shown:
        key(b"7", 1.0)
    elif "Enter your name" in shown:        # a high score: it needs a name
        for c in b"Asciiverse": key(bytes([c]), 0.12)
        key(b"\r", 1.5)
    else:
        key(b"\r", 1.0)
shutil.rmtree(home, ignore_errors=True)
