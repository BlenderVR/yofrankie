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


from bge import logic

HIT_MAXDIST = 0.8

def main(cont):
	own = cont.owner
	
	actu_track = cont.actuators['track_predator']
	predator_ob = actu_track.object # 0 is so we get the object, not the name
	
	if not predator_ob:
		# print("the predator must have been removed")
		return
		
	# Who are we attacking?
	
	# print(predator_ob, type(predator_ob))
	'''
	# See what state of the animation 
	sens_attack_time = cont.sensors['action_frame_hit']
	
	# 
	if not sens_attack_time.positive:
		print('Cant hit yet!')
		return
	'''
	
	# Frankie may have escaped! see if we can still get him
	predator_dist = own.getDistanceTo(predator_ob)
	if predator_dist < HIT_MAXDIST:
		# print("Hitting frabnkie", predator_ob.name, predator_dist)
		predator_ob['hit'] = 1
	#else:
	#	print('frankie got away at!', predator_dist)
	
	actu_track.object = None # stop tracking the predator
