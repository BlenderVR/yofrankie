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


import GameLogic
import Mathutils
from Mathutils import Vector, RotationMatrix

def main(cont):
	
	if not cont.sensors['trigger_warp_script'].positive:
		return 
	
	own = cont.owner
	own_pos = Vector(own.worldPosition)
	
	sce = GameLogic.getCurrentScene()
	#for ob in sce.objects:
	#	print(ob.name)
	
	actu_add_object = cont.actuators['add_dyn_portal']
	
	# Incase we are called from the main menu
	blendFiles = GameLogic.getBlendFileList('//')
	blendFiles += GameLogic.getBlendFileList('//levels')
	blendFiles += GameLogic.getBlendFileList('//../levels')
	blendFiles += GameLogic.getBlendFileList('//../../../levels')
	
	# Remove doubles
	# blendFiles	= list(set(blendFiles)) # breaks py2.3
	blendFiles = dict([(b, None) for b in blendFiles]).keys()
	blendFiles = list(blendFiles) # py3 has its own dict_keys type
	
	blendFiles.sort()
	
	
	if own['mini_level']:
		# Mini level selector
		for b in blendFiles[:]:
			if not('minilevel_' in b or 'level_selector.blend' in b):
				blendFiles.remove(b)
	else:
		# normal level selector
		for b in blendFiles[:]:
			# get rid or start_menu, this blend, and any blends not containing minilevel_
			if 'minilevel_' in b or \
				'ending.blend' in b or \
				'library.blend' in b or \
				'level_selector.blend' in b or \
				'_backup.blend' in b:
				
				blendFiles.remove(b)

	print(blendFiles)
	
	totFiles = len(blendFiles)
	
	if not totFiles:
		print("No Levels Found!")
		return
	
	# Some vars for positioning the portals
	start = Vector(7,0,0) # rotate this point around to place the portals to new levels
	
	
	totFiles = float(totFiles)
	# print('PLACING')
	for i,f in enumerate(blendFiles):
		ang = 360 * (i/totFiles)
		# print(i,f,ang)
		mat = RotationMatrix(ang, 3, 'z')
		pos_xy = list((start * mat) + own_pos)  # rotate and center around the gamelogic object
		
		ray_down = pos_xy[:]
		ray_down[2] -= 1.0
		
		print(pos_xy)
		pos_xy[2] = 500 # cast down from on high
		#pos_xy[2] = 16 # cast down from on high
		ob_hit, hit_first, nor_first = own.rayCast(ray_down, pos_xy, 1000) # 'ground')
		if ob_hit:
			pos_xy[2] = hit_first[2]
		else:
			# Rary a ray would ,iss the ground but could happen.
			pos_xy[2] = own_pos[2] 
		
		#own.setPosition(pos_xy)
		
		actu_add_object.instantAddObject()
		new_portal = actu_add_object.objectLastCreated
		
		#new_portal.setPosition(hit_first)
		new_portal.worldPosition = pos_xy
		new_portal.worldOrientation = mat.transpose()
		if nor_first:
			new_portal.alignAxisToVect(nor_first, 2)
		
		new_portal['portal_blend'] = '//' + f
		
		# BUG THIS SHOULD WORK!!!!
		'''
		new_portal_text = new_portal.children
		new_portal_text.Text = f.replace('_', ' ').split('.')[0]
		'''
		
	
	# Since we use instantAddObject(), there is no need to activate the actuator
	# GameLogic.addActiveActuator(actu_add_object, 1)
	
	own.endObject() # may as well distroy, wont use anymore
