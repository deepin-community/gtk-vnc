#!/bin/sh

set -e
set -v

rm -rf build

meson build

ninja -C build dist

rpmbuild --nodeps \
   --define "_sourcedir `pwd`/build/meson-dist/" \
   -ba --clean build/gtk-vnc.spec

rpmbuild --nodeps \
   --define "_sourcedir `pwd`/build/meson-dist/" \
   -ba --clean build/mingw-gtk-vnc.spec
