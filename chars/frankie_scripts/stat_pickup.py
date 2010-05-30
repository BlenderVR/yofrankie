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


# Detect collision with pickup and act on this

from bge import logic

def main(cont):
	
	own = cont.owner

	# Cant pickup when hurt
	# print(own.hit, own.revive_time)
	if own['hit'] or own['revive_time'] < 1.0 or own['carrying'] or own['carried']:
		print("Cant collect items when hit, reviving, carrying or carried")
		return 
	
	sens_pickup = cont.sensors['pickup_touch']
	
	pickup_objects = sens_pickup.hitObjectList
	
	if not pickup_objects or len(pickup_objects) == 0: 
		return
	
	DONE_PICKUP = False
	LIFE_PICKUP = False
	
	# Loop over all colliding pickup onjects
	for pickup in pickup_objects:
		# We can either pickup an item or get life!
		
		if 'life' in pickup: # LIFE PICKUP
			# Play Flash Anim!
			life_max = own['life_max']
			life = own['life'] + pickup['life']
			if life < life_max:
				# Life, we have enough
				own['life'] = life
			else:
				own['life'] = own['life_max']
				
			logic.frankhealth = own['life']
			cont.activate('pickup_flash_life')
			cont.activate('send_healthchange')
			DONE_PICKUP = LIFE_PICKUP = True
			
			
		elif 'boost' in pickup: # BOOST PICKUP
			# now youll run faster etc
			# The value for boost is ignored
			own['boosted'] = -10.0 # As long is its under 0, boost will apply
			DONE_PICKUP = True
			
		else: # ITEM PICKUP
			item_attr = pickup['pickup']
			
			if not item_attr.startswith('item_'):
				print('Incorrect name', own, item_attr)
			else:
				own[item_attr] = own.get(item_attr, 0) + 1
				
				# Should be smarter here, for now just set the thor item to this one.
				own['throw_item'] = item_attr
				DONE_PICKUP = True
				
				
		# May pickup multiple objects at once.
		pickup.endObject() # delayed removes this object from the scene

	# Play pickup animation only if walking and on the ground.
	if DONE_PICKUP:
		# WARNING - test with state attribute assumes running 
		# is on state 3, Id prefer not to use these kinds of tests
		# since running could be moved from state 3 but for now its ok.
		if own['grounded'] != 0 and not (cont.state & (1<<2)):
			cont.activate('pickup_anim')
		if LIFE_PICKUP:
			cont.activate('sfx_life_pickup')
			hud_dict = logic.globalDict['HUD']
			if own['id'] == 0:	hud_dict['life_p1'] = own['life']
			else:				hud_dict['life_p2'] = own['life']
			cont.activate('send_healthchange')
		else:
			cont.activate('sfx_item_pickup')
