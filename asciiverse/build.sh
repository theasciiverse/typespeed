#!/bin/sh
# Builds typespeed. Linux: run inside alpine:3.22 for a fully static binary
# (ncurses linked in); macOS: run on the runner with CC_ARCH set to x86_64
# or arm64, linking the system's ncurses.
#   docker run --rm -v "$PWD":/src -w /src alpine:3.22 sh asciiverse/build.sh
# Leaves src/typespeed. Translations are off (--disable-nls): the game's
# texts stay in English, and no gettext has to be linked in.
# Data folders are compiled in as /usr/share/typespeed/{words,rules} for
# the system packages; av's start script points TYPESPEED_WORDDIR and
# TYPESPEED_RULEDIR at the folders next to it instead.
set -eu
if [ -f /etc/alpine-release ]; then
  apk add --no-cache build-base ncurses-dev ncurses-static >/dev/null
  ldflags="-static"
else
  ldflags=""
fi
cc="cc${CC_ARCH:+ -arch $CC_ARCH}"
./configure --prefix=/usr --datadir=/usr/share --localstatedir=/var --disable-nls CC="$cc" LDFLAGS="$ldflags" >/dev/null
make clean >/dev/null 2>&1 || true
make >/dev/null
strip src/typespeed
