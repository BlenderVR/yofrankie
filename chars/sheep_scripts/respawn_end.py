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


import GameLogic

def main(cont):
	own = cont.owner
	
	# be careful here, whatever is our parent should probably be told we're detaching.
	# they are not right now.
	own.removeParent()
	
	own.restoreDynamics() # only needed for reviving from lava
	
	if 'carried' in own:
		own['carried'] = 0
	
	own['grounded'] = 0
	own['attack_type'] = ''
	own['life'] = own['lifemax']
	
	if 'projectile_id' in own:
		own['projectile_id'] = -1
	
	own['target_time'] = 0.0
	own['revive_time'] = 0.0
	
	own.setLinearVelocity((0.0, 0.0, 0.0), 1)
	own.localPosition = (own['x_orig'], own['y_orig'], own['z_orig'])
	# print("respawn")
