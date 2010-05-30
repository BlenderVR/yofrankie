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
whenever the "hit" property changes
deal with adjustring the life, changing to dead state and updating the HUD

we dont need to know why the hit propert changes, this can be done by touching a kill property or
some other character attacking us could do this.
'''
from bge import logic

def main(cont):
	
	own = cont.owner
	
	# See frank_stat_hit, this sets the hit property that triggers this script
	hit = own['hit']
	
	if hit == 0 or own['revive_time'] < 1.0:
		return
	
	own['hit'] = 0
	
	own['life']= max(0, own['life'] - hit)
	own['revive_time']= 0.0
		
	# Update the HUD
	hud_dict = logic.globalDict['HUD']
	if own['id'] == 0:	hud_dict['life_p1'] = own['life']
	else:			hud_dict['life_p2'] = own['life']
	cont.activate('send_healthchange') # send message to hud telling it to update health

	# are we dead?
	if own['life'] == 0:
		cont.activate('dead_state')
		return
	
	# Play Hit Anim
	if own['carrying']:
		cont.deactivate('hit')
		cont.activate('hit_carry')
	else:
		cont.deactivate('hit_carry')
		cont.activate('hit')
	
	# Always flash color
	cont.activate('hit_flashred')
