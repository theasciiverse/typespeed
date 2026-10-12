# Typespeed (Asciiverse packaging)

Typespeed 0.6.5, the terminal typing game, with Debian's patches and a few
of ours, packaged for the Asciiverse catalog and as system packages. Not
our code: keep changes small and list every one in PATCHES.md.

- No upstream repository exists; history starts from the release tarball
  (tag `0.6.5`), then Debian's patches (tag `debian/0.6.5-12`), then ours.
  `origin` is github.com/theasciiverse/typespeed.
- Release: tag `v0.6.5-av.<n>` and push it.
- Local static build: `docker run --rm -v "$PWD":/src -w /src alpine:3.22
  sh asciiverse/build.sh` leaves `src/typespeed`.
- Curses keypad mode: arrow keys arrive as application cursor codes
  (ESC O B), which matters when scripting input.
- Preview: `python3 asciiverse/record-preview.py` (needs pyte).
