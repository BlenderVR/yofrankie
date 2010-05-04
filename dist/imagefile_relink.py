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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# This script must run inside blender
import Blender
import bpy


def replace_ext(path, ext):
	return '.'.join( path.split('.')[:-1] ) + '.' + ext

change = False

for i in bpy.data.images:
	if i.lib==None:
		filename = i.filename
		filename_abs = Blender.sys.expandpath(filename)
		
		if not Blender.sys.exists(filename_abs):
			filename_jpg = replace_ext(filename_abs, 'jpg')
			if Blender.sys.exists(filename_jpg):
				print "\tfixed path", filename_jpg
				i.filename = replace_ext(filename, 'jpg')
				change = True

filename = Blender.Get('filename')

if change:
	# Workaround for G.curscreen being null
	# in 2.49 this crashes in BG mode
	# Blender.Window.SetScreen(Blender.Window.GetScreens()[0])
	print "Saving", filename
	Blender.Save(filename, True) # True==Overwrite
else:
	print "No Changes", filename
# Incase were not running in background mode
# Blender.Quit()
