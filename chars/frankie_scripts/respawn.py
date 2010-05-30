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


'''
This script restores frankie to his original location
restores properties and updates the hud.
'''
from bge import logic

def main(cont):
	own = cont.owner
	
	# If somthing is carrying us. tell it to not bother anymore.
	parent = own.parent
	if parent:
		if 'carrying' in parent:
			parent['carrying'] = 0
		else:
			print('\twarning, parented to a non "carrying" object. should never happen')
		
		own.removeParent()
	
	own.restoreDynamics() # only needed for reviving from lava
	
	own.localPosition = [float(num) for num in own['orig_pos'].split()]
	own.setLinearVelocity((0.0, 0.0, 0.0), True)
	
	props = logic.globalDict['PROP_BACKUP'][own['id']]
	
	# We backed these up, see frank_init
	for prop, value in props.items():
		own[prop] = value
	
	# Update the HUD
	hud_dict = logic.globalDict['HUD']
	if own['id'] == 0:	hud_dict['life_p1'] = own['life']
	else:				hud_dict['life_p2'] = own['life']
	
