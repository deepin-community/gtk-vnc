#!/bin/sh

SOURCE_ROOT=$1
BUILD_ROOT=$2

$SOURCE_ROOT/build-aux/gitlog-to-changelog > $MESON_DIST_ROOT/ChangeLog

# Only gtk-vnc.spec is put into the tarball,
# otherwise rpmbuild -ta $tarball.tar.gz would fail
cp $BUILD_ROOT/gtk-vnc.spec $MESON_DIST_ROOT/

out="`git log --pretty=format:'%aN <%aE>' | sort -u`"
perl -p -e "s/#authorslist#// and print '$out'" < $SOURCE_ROOT/AUTHORS.in > $MESON_DIST_ROOT/AUTHORS
