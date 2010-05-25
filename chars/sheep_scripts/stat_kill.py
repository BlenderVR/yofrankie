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

def update_hud(cont, own):
	
	projectile_id = own['projectile_id']
	if projectile_id == -1: # we died on our own.
		return
	
	# Get the hitlist for this player
	try:	hitlist = GameLogic.globalDict['HUD']['hitlist_p%d' % (projectile_id+1)]
	except:	return # Not initialized yet.... ignore for a couble of redraws
	
	id = own['id']
	new_item = (id, own['type'], own['life'], own['lifemax'])
	
	DO_INSERT = True
	for i,item in enumerate(hitlist):
		if item[0] == id: # update existing stat?
			hitlist[i] = new_item
			DO_INSERT = False
			break
	
	# ok its not in the list, add it
	if DO_INSERT:
		hitlist.append(new_item)


# --- 
# See frank_stat_hit, this sets the hit property that triggers this script.
def main(cont):
	own = cont.owner
	
	# print(own.hit, 'own.hit')
	
	if own['hit']==0 or own['revive_time'] < 1.0:
		own['hit'] = 0
		return
	
	# Dont do this, breaks lava death
	'''
	if own['grounded'] == 0:
		# trigger so will re-run
		print('\tchar: not on ground, not reacting to hit yet')
		return
	'''
	
	sens_kill = cont.sensors['hit_detect']
	
	if not sens_kill.positive: # Why would this be false??
		return
	
	own['life'] = life = max(own['life'] - own['hit'], 0)
	
	own['hit'] = 0
	own['revive_time'] = 0.0
	
	
	# Update the hitlist
	update_hud(cont, own)
	
	# play sound if we have one. make sure name is sfx_*
	for actu_sound in cont.actuators:
		if actu_sound.name.startswith('sfx_'):
			cont.activate(actu_sound)
	
	
	if life == 0:
		cont.activate('dead_state')
		return
	
	"""
	actu_hit = actu_kicked = None
	for actu in cont.actuators:
		name = actu.name
		if name.startswith('hit'):
			actu_hit = actu
			break
		elif name.startswith('kicked'):
			actu_kicked = actu
			break
	
	# Play Hit Anim
	print('\nSHEEP WAS HIT!!!!!\n')
	print('own["attack_type"]', own['attack_type'])
	if own['attack_type']=='kick':
		own['attack_type'] = ''
		if actu_kicked:
			actu_hit = actu_kicked
	
	cont.activate(actu_hit)
	"""
	# State switch time - stop us from switching 
	
	# Dont set a new state for a while, play recover anim
	# own['state_switch_time'] = -4.0
	cont.activate('hit_state')
	
