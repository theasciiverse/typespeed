#!/bin/sh
# Lays out the av archive in stage/: the start script at the top, the
# binary in lib/, and the word lists and rules beside them.
set -eu
rm -rf stage && mkdir -p stage/lib stage/words stage/rules
cp src/typespeed stage/lib/typespeed
cp asciiverse/typespeed stage/typespeed
cp words/words.* stage/words/
cp rules/rule.* stage/rules/
cp COPYING README stage/
