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
its a pitty we need this script at all, but knowing if we are on the ground or not isnt that simple
basically use ray and collision sensors to detect of we are on the ground, keeping the "grounded" property up to date
there may be a better way to do this, like use second collision object at frankies feet- but for now this is OK.
'''
import GameLogic

def main(cont):
	own = cont.owner
	
	# Cant land while being carried
	if own['carried']:
		return
	
	#FALL_LIMIT = -0.5 # How much we need to be falling before the ray cast is used
	
	sens_touchGround = cont.sensors['ground_test']
	# sens_ledgeCollide = cont.sensors['ledge_collide']
	
	
	# Note, cont.sensors['ground_ray'] sensor isnt strictly needed however adding this avoids jitter when running over bumps.
	if sens_touchGround.positive or (cont.sensors['ground_ray'].positive and own['jump_time'] > 0.5):
		if own['grounded'] == 0: # was flying
			# print(own.getLinearVelocity()[2], 'own.getLinearVelocity()[2]')
			# print(own.jump_time, 'own.jump_time')
			
			# Change the state
			cont.activate('idle_state')
			own['grounded'] = 1
			
			# print(" SETTING ON GROUND ")
	else: # off the ground
		if own['grounded'] == 1: # just left the ground
			# Change the state
			cont.activate('fall_state')
			own['grounded'] = 0
			# print(" SETTING ON AIR ")
