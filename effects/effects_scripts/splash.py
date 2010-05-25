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


# this script is applied to one empty,
# using multiple collision sensors on water surfaces to detect the splash
# the empty will be moved to the collision location and instantly add the object
# this needs to be done because groups cant be moved once added by addObject actuators.

# Warning, this module must be reloaded between scenes of the objects will become invalid
import GameLogic

SPLASH_LS = [None, None, None, None]

def splash_init():
	sce = GameLogic.getCurrentScene()
	SPLASH_LS[0] = sce
	try:		SPLASH_LS[1] = sce.objectsInactive['OBfx_splash']
	except:	SPLASH_LS[1] = None
	
	try:		SPLASH_LS[2] = sce.objectsInactive['OBfx_splash_small']
	except:	SPLASH_LS[2] = None
	
	try:		SPLASH_LS[3] = sce.objectsInactive['OBfx_lava_splash']
	except:	SPLASH_LS[3] = None

def main(cont):
	own= cont.owner
	
	sce = SPLASH_LS[0]
	# Incase we switch scenes
	if sce.invalid:
		splash_init()
		sce = SPLASH_LS[0]
	
	is_lava = ('lava' in own)
	
	
	for sens in cont.sensors: # one or more water surface meshes	
		if sens.positive:
			for ob in sens.hitObjectList:
				
				if is_lava:
					ob_add = SPLASH_LS[3]
				else:
					if 'pickup' in ob:
						ob_add = SPLASH_LS[1]
					else:
						ob_add = SPLASH_LS[2]
				if ob_add:
					sce.addObject(ob_add, ob, 300)
				else:
					print("splash add error, object is not available in this level")
				

# Initialize for the first time
splash_init()
