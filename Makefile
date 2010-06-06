# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ##### END GPL LICENSE BLOCK #####

NAME = yofrankie
VERSION = 1.1b

BLENDER = blender
PYTHON = python
SVN = svn
PACKAGE_DIR = ./package
PREFIX ?= /usr/local

dist_dirs = \
	audio \
	chars \
	dist \
	effects \
	franci_test \
	hud \
	levels \
	menus \
	props \
	textures \
	$(NULL)

dist_files = \
	CC-BY3.0 \
	COPYING \
	GPL-2 \
	Makefile \
	README.TXT \
	yo_frankie_stub.blend \
	$(NULL)

all:
	# Copy files into a package dir
	rm -rf $(PACKAGE_DIR)
	
	# copy with svn export or normal copy if this is not a checkout
	if test -d .svn; \
	then $(SVN) export . $(PACKAGE_DIR); \
	else mkdir ./package; cp -pR audio chars effects hud levels menus props textures $(PACKAGE_DIR)/; \
	fi
	# end shell command
	
	# Convert images, correct blendfile paths
	# TODO - this is broken with 2.48a, because blend files saved have no G.curscreen
	$(PYTHON) dist/imagefile_compress.py $(BLENDER) $(PACKAGE_DIR)
	
	# Compress all blendfiles
	$(PYTHON) dist/blendfile_gzip.py $(PACKAGE_DIR)

clean:
	rm -rf $(PACKAGE_DIR)

install:
	install -d $(DESTDIR)$(PREFIX)/share/yofrankie-bge
	cp -rT $(PACKAGE_DIR) $(DESTDIR)$(PREFIX)/share/yofrankie-bge
	install -D -m 755 dist/yofrankie-bge $(DESTDIR)$(PREFIX)/games/yofrankie-bge
	install -D -m 755 dist/yofrankie-bge.6 $(DESTDIR)$(PREFIX)/share/man/man6/yofrankie-bge.6
	install -D -m 644 dist/yofrankie-bge.desktop $(DESTDIR)$(PREFIX)/share/applications/yofrankie-bge.desktop
	install -D -m 644 dist/yofrankie.png $(DESTDIR)$(PREFIX)/share/icons/hicolor/128x128/apps/yofrankie-bge.png
	install -d $(DESTDIR)$(PREFIX)/share/icons/hicolor/48x48/apps
	convert dist/yofrankie.png -resize 48 $(DESTDIR)$(PREFIX)/share/icons/hicolor/48x48/apps/yofrankie-bge.png
	# Move font into font directory
	install -d $(DESTDIR)$(PREFIX)/share/fonts/truetype
	mv $(DESTDIR)$(PREFIX)/share/yofrankie-bge/menus/yo_frankie.ttf $(DESTDIR)$(PREFIX)/share/fonts/truetype
	ln -s ../../fonts/truetype/yo_frankie.ttf $(DESTDIR)$(PREFIX)/share/yofrankie-bge/menus/yo_frankie.ttf

gz:
	tar -c --exclude-vcs --transform="s@^@$(NAME)-$(VERSION)/@" $(dist_dirs) $(dist_files) | gzip -cn9 > $(NAME)-$(VERSION).tar.gz

bzip2:
	tar -c --exclude-vcs --transform="s@^@$(NAME)-$(VERSION)/@" $(dist_dirs) $(dist_files) | bzip2 -cz9 > $(NAME)-$(VERSION).tar.bz2

lzma:
	tar -c --exclude-vcs --transform="s@^@$(NAME)-$(VERSION)/@" $(dist_dirs) $(dist_files) | lzma -cz9 > $(NAME)-$(VERSION).tar.lzma

xz:
	tar -c --exclude-vcs --transform="s@^@$(NAME)-$(VERSION)/@" $(dist_dirs) $(dist_files) | xz -cz9 > $(NAME)-$(VERSION).tar.xz

dist: bzip2

.PHONY: all clean install dist gz bzip2 lzma xz
