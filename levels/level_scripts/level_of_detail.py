# -*- coding: utf-8 -*-
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


# remove objects based on detail setting.
from bge import logic
def main(cont):
	own = cont.owner
	sce = logic.getCurrentScene()
	
	conf = logic.globalDict.get('CONFIG', {})
	detail = conf.get('GRAPHICS_DETAIL', 2)
	
	# detail is a pref, can be 0,1,2: 2 is high detail, dont do anything

	for ob in sce.objects:
		lod_level= ob.get('lod_level')
		if lod_level != None:
			end = False
			
			if detail==0:
				end = (lod_level < 2)
			elif detail==1:
				end = (lod_level < 1)
			
			if end:		ob.endObject()
			else:		del ob['lod_level']
		
	own.endObject()
