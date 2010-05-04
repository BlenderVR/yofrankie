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
	
	if own['type'] == 'shp':
		return
	
	sens_attack = cont.sensors['predator_collide']
	
	predator_ob = sens_attack.hitObject
	
	if not predator_ob:
		return
	
	if not ('hit' in predator_ob and predator_ob.has_key('life')):
		print('\tattack: predator missing "hit" or "life" property')
		return
	
	if predator_ob['life'] <= 0:
		# print('\tattack: predator alredy dead')
		return
	
	# face the predator, this is always activated
	# so we only need to spesify what to track to.
	actu_track = cont.actuators['track_predator']
	actu_track.object = predator_ob
	
	# Dont track, until we enter the state, only set the track ob
	# since the state does the tracking
	
	# Change to attacking state
	cont.activate('predator_attack_state')
