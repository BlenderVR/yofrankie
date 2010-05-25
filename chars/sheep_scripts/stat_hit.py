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

# This file has almost an exact copy in frank.blend - frank_projectile_hit
def main(cont):
	PROJECTILE_SPEED = 5.0
	own = cont.owner
	#sens = cont.sensors['projectile_touch']
	for sens in cont.sensors:		
		hit_ob = sens.hitObject
		if hit_ob:
			if 'projectile' in hit_ob:
				s = hit_ob.getLinearVelocity()
				s = s[0]*s[0] + s[1]*s[1] + s[2]*s[2]
				# print('hit_speed', s)
				# Is this going to hit us???
				if s > PROJECTILE_SPEED:
					if 'kill' in hit_ob:
						own['hit'] = max(hit_ob['kill'], own['hit'])
						GameLogic.bonecount+=hit_ob['kill'] #add the amount of health lost to the 'total broken bones' counter
					else:
						own['hit'] = max(1, own['hit'])
			elif 'kill' in hit_ob:
				own['hit'] = max(hit_ob['kill'], own['hit'])
