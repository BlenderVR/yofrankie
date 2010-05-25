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
	own=cont.owner
	sens_msg = cont.sensors['hit_list_msg']
	
	# Get all messages and update the ID's we need to.
	messages_player_ids = list(sens_msg.bodies) # BUG in 2.49a, not in 2.49 :| "string" in CListValue
	
	# checking for a zero length list is not helpful
	# if we get one, just update both chars
	
	hud_dict = GameLogic.globalDict['HUD']
	
	actus = [(s.name, s) for s in cont.actuators]
	actus.sort()
	
	
	# In this case we just want to update the lists
	## print('\thud: messages for predator ids are:', messages_player_ids)
	
	if messages_player_ids == None or '-1' in messages_player_ids or len(messages_player_ids) == 0:
		if GameLogic.globalDict['CONFIG']['PLAYER_COUNT'] == 1:
			messages_player_ids = ['0']
		else:
			messages_player_ids = ['0', '1']
		
		UPDATE_ONLY = True
	else:
		UPDATE_ONLY = False
	
	for player_id in messages_player_ids:
		# player_id is the projectile_id
		# which is frankies or momo's id - 0 or 1
		
		# No player hit it, but it could still be in the hit list
		# would be nice to update all objects in the hitlist in this case
		
		
		player_num = str(int(player_id)+1)
		
		hitlist = hud_dict['hitlist_p' + player_num]
		
		if UPDATE_ONLY==False:
			# add to the players bonecount, cheat here a bit, dont actually use the actuator, just get its owner
			bonecount = hud_dict['bonecount_p' + player_num] + 1
			hud_dict['bonecount_p' + player_num] = bonecount 
			cont.actuators['set_bonecount_p' + player_num].owner['Text'] = '%.4d' % bonecount 
			# Done with bonetext
	
		## print('\thud: hitlist - ', hitlist)
		
		
		prefix = 'replace_hitlist_p' + player_num
		
		# 5 replace mesh actuators in order.
		actus_icons = [s[1] for s in actus if s[0].startswith(prefix)]
		
		# print('actu_icons', actus_icons, prefix, actus)
		
		
		# remove all hitlist items that are invisible now
		
		for actu in actus_icons:
			actu_own = actu.owner
			icon_id = actu_own['id']
			if actu_own.visible == False and icon_id != -1:
				actu_text = actu_own.children[0]
				
				# Invalid again
				actu_own['id'] = -1
				actu_text['Text'] = ''
				
				
				if hitlist:
					del_list = []
					i = 0
					for id, char_type, life, lifemax in hitlist:
						if icon_id == id:
							del_list.append(i) # should only really exist once, but just incase
						i += 1
					
					while del_list:
						hitlist.pop(del_list.pop())
					
			
		while len(hitlist) > 6:
			hitlist.pop()
		
		
		actus_id = [ actu.owner['id'] for actu in actus_icons ]
		
		i = 0
		
		for id, char_type, life, lifemax in hitlist:
			actu = actus_icons[i]
			if actus_id[i]==id:
				UPDATE_FULL = False
			else:
				UPDATE_FULL = True
			
			if life==0:		icon_mesh_name = 'icon_%s_dead' % char_type
			else:			icon_mesh_name = 'icon_%s' % char_type
			icon_text = '%d/%d' % (life, lifemax)
			
			# Get the text object and assign it somthing.
			actu_own = actu.owner
			actu_text = actu_own.children[0]
			
			## print('\thud: setting icon!', i, id, icon_mesh_name, life, lifemax)
			
			current_mesh = actu.mesh
			if current_mesh: current_mesh = current_mesh.name[2:]
			
			# print("\thud debug", icon_mesh_name, current_mesh, icon_text, actu_text.Text, UPDATE_FULL)
			
			
			if UPDATE_FULL == False and icon_mesh_name == current_mesh and icon_text == actu_text['Text']:
				# print("NOTHING TO DO")
				pass
			else:
				if icon_text != actu_text['Text']:
					actu_text['Text'] = icon_text
				
				if icon_mesh_name != current_mesh:
					actu.mesh = icon_mesh_name
					actu.instantReplaceMesh()
				
				
				actu_own.setVisible(True, True) # recursive, also sets text invisible
				actu_own['id'] = id
				
				# A bit sneaky but its quicker to set the state from here. it will turn its self off after.
				actu_own.state = 1<<15 # state 16
				
				# cont.activate('inactive_state_p%s_%d' % (player_num, i))
				# cont.activate('active_state_p%s_%d' % (player_num, i))
				
				
			i+=1
		
		# Clear any remaining
		## print('actus_icons', len(actus_icons), actus_icons)
		for i in range(i, 6):
			
			actu = actus_icons[i]
				
			# Get the text object and assign it somthing.
			actu_own = actu.owner
			actu_text = actu_own.children[0]
			
			actu_own.setVisible(False, True) # recursive, also sets text invisible
			cont.activate('inactive_state_p%s_%d' % (player_num, i))
		
## print("\n\nUPDATING HUD")
