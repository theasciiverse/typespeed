# Changes from upstream

This is the Asciiverse packaging of Typespeed 0.6.5 (GPL-2.0-or-later) by
Jani Ollikainen and Jaakko Manelius, with later work by Tobias Stoeckmann;
the last upstream release (typespeed.sourceforge.net). History here starts
from the release tarball as Debian distributes it
(typespeed_0.6.5.orig.tar.gz, sha256
5c860385ceed8a60f13217cc0192c4c2b4705c3e80f9866f7d72ff306eb72961), tagged
`0.6.5`.

## Debian's patches

From typespeed 0.6.5-12 (typespeed_0.6.5-12.debian.tar.xz, sha256
031623fad0f73c64fed1b2074c2ffbe4ad163ccf999a940b5889c8b03ee43a8d), one
commit each: a typo in the Italian translation (Dafydd Harries), the GCC 10
build fix (Sudip Mukherjee), and propagating CC from configure to make
(credited to Helmut Grohne in Debian's changelog; the patch file names no
author). Tagged `debian/0.6.5-12`.

## Ours

- **Scores without setgid games.** Typespeed opens a system-wide high
  score file (/var/games/typespeed.score) at start and exits if it cannot,
  which needs a setgid install. Now, when that file cannot be opened, it
  keeps scores in ~/.typespeed/score, the file it already uses when a
  player has a ~/.typespeed/config, creating it if needed.
- **Relocatable data folders.** TYPESPEED_WORDDIR and TYPESPEED_RULEDIR
  override the compiled-in folders (read after /etc/typespeedrc), so av's
  install finds its word lists and rules.
- **musl.** typespeed.h includes <time.h> for clock_t, and typespeed.c
  declares xsnprintf like the other files do.
- **How to play it, at the top of README.** A short note on installing and
  starting it with av, or from a release archive; the original text follows
  unchanged.

## Packaging (new files)

- `asciiverse/build.sh`: static Linux build in Alpine, macOS builds per
  architecture; translations off (--disable-nls).
- `asciiverse/typespeed`, `asciiverse/stage.sh`: av's start script and the
  archive layout (binary in lib/, words/ and rules/ beside it).
- `asciiverse/nfpm.yaml`: .deb, .rpm, .apk and Arch packages; no setgid.
- `asciiverse/record-preview.py`: records the catalog preview with a
  typist that reads the screen through pyte.
- `.github/workflows/release.yml`: builds all of it on a tag.

## Not built

- Windows. Network play is in the game but untested here.
