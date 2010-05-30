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
This script is used to change between active menu items
as well as exectuting each menu item.

This script runs on an empty object and recieves input
from keys, mouse and joystick.
'''

from bge import logic

ITEM_PREFIX = 'item_'

def menu_items(sce):
	'''
	Return all names starting with item_ - in a sorted list
	'''
	ls = [ob for ob in sce.objects if ob.name.startswith(ITEM_PREFIX)]
	ls.sort(key=lambda a: a.name)
	return ls

def menu_mouse_item_index(cont, own, items):
	'''
	Return the item under the mouse
	'''
	# Handle mouse
	mouse_ob = cont.sensors['mouse_over'].hitObject
	if not mouse_ob:
		# Happens so often, dont bother printing
		# print('\tmouseover: nomouse ob')
		return -1
	
	mouse_obname = mouse_ob.name
	
	# is this a valid item?
	if not mouse_obname.startswith(ITEM_PREFIX):
		print('\tmouseover: mouse ob name is wrong', mouse_obname)
		return -1
	
	# Check this object is in the list
	for i, ob in enumerate(items):
		if ob.name == mouse_obname:
			return i
	
	# could not find
	print('\tmouseover: mouse ob no matches', mouse_obname)
	return -1
				
	

def menu_activate(cont, own, item_ob, items):
	'''
	use same syntax as portals for scenes and/or blendfiles
	see frank.blend -> frank_portal text for similar script
	'''
	
	globalDict = logic.globalDict
	portal_ob = item_ob # just so we can use copied script 
	
		
	# incase the portal was set before
	# we dont want to use an invalid value
	try:	del globalDict['PORTAL_OBNAME']
	except:	pass
	
	try:	del globalDict['PORTAL_SCENENAME']
	except:	pass
	
	blend_name = scene_name = target_name = ''

	if 'portal' in portal_ob: # check for a spesific object
		target_name = portal_ob['portal']
	
	if 'portal_blend' in portal_ob:	
		blend_name = portal_ob['portal_blend'] # No way to check if this really matches up to a scene
	
	if 'portal_scene' in portal_ob:
		scene_name = portal_ob['portal_scene'] # No way to check if this really matches up to a scene
	
	
	if blend_name:
		# todo, allow blend AND scene switching. at the moment can only do blend switching.
		set_blend_actu = cont.actuators['portal_blend']
		set_blend_actu.fileName =  blend_name 
		
		try:	del globalDict['PLAYER_ID'] # regenerate ID's on restart
		except:	pass
		
		if target_name:
			globalDict['PORTAL_OBNAME'] = target_name
		
		if scene_name:
			globalDict['PORTAL_SCENENAME'] = scene_name
		
		cont.activate(set_blend_actu)
		
		'''
		SPECIAL CASE - Set GLSL 
		'''
		from bge import render
		if logic.globalDict['CONFIG']['GRAPHICS_GLSL']:
			render.setMaterialMode(2) # use GLSL textures
		else:
			render.setMaterialMode(0) # texface
		
		
	elif scene_name:
		# portal_ob
		set_scene_actu = cont.actuators['portal_scene']
		set_scene_actu.scene =  scene_name 
		
		try:	del globalDict['PLAYER_ID'] # regenerate ID's on restart
		except:	pass
		
		if target_name:
			globalDict['PORTAL_OBNAME'] = target_name
		
		cont.activate(set_scene_actu)
	else:
		# Not a portal
				
		conf = logic.globalDict['CONFIG']
		
		if 'trigger' in item_ob:
			# This should have its own logic thats activated on trigger.
			# print("trigger", item_ob.name)
			item_ob['trigger'] = True
			
			# Configuration spesific
		elif 'toggle' in item_ob:
			item_ob['toggle'] = not item_ob['toggle']
			
			if 'conf_key' in item_ob:
				conf[item_ob['conf_key']] = item_ob['toggle']
			
		elif 'radio' in item_ob:
			conf_key = item_ob['conf_key']
			
			for ob in items:
				if ob.get('conf_key') == conf_key:
					print(ob.name)
					ob['enabled'] = 0
			
			item_ob['enabled'] = 1
			conf[item_ob['conf_key']] = item_ob['radio'] # The index of this radio
		
		# print(conf)


def main(cont):
	'''
	Take user input and change the active menu or select an item.
	'''
	own = cont.owner
	sce = logic.getCurrentScene()
	
	items = menu_items(sce)
	
	if not items:
		print('error: no object starting with "item_" exiting, is this scene a menu?')
		return
	
	# Set all inactive
	act = -1
	for i, item in enumerate(items):
		if item['active']:
			act = i
			break
	
	if act == -1:
		act = 0
	else:
		for item in items: # make sure only 1 is active
			item['active'] = False
	
	items[act]['active'] = True
	
	
	KEY_ENTER = False
	
	# There are a number of sensors that start with "enter_"
	# use any of these to enter the menu
	for sens in cont.sensors:
		if sens.name.startswith('enter_') and sens.positive:
			KEY_ENTER = True
			break
	
	# The mouse can also enter, but check that its is over a valid item first
	if KEY_ENTER == False:
		if cont.sensors['mouse_click'].positive:
			# Its probably safe to assume this index is alredy set
			# from mouse motion, but assign it anyway just incase.
			act_click = menu_mouse_item_index(cont, own, items)
			
			if act_click != -1:
				act = act_click
				KEY_ENTER = True
	
	
	if KEY_ENTER:
		menu_activate(cont, own, items[act], items)
		return
	
	
	# Get keyup down from keyboard or joystick.
	KEY_UP = cont.sensors['key_up'].positive
	KEY_DOWN = cont.sensors['key_down'].positive
	if not KEY_UP:		KEY_UP =	cont.sensors['joy_up_p1'].positive
	if not KEY_DOWN:	KEY_DOWN =	cont.sensors['joy_down_p1'].positive
	if not KEY_UP:		KEY_UP =	cont.sensors['joy_up_p2'].positive
	if not KEY_DOWN:	KEY_DOWN =	cont.sensors['joy_down_p2'].positive
	
	PLAY_SOUND = False
	
	if KEY_UP or KEY_DOWN:
		# Cycle up and down the menu items when key or joystics are pressed.
		if len(items) > 1:
			items[act]['active'] = False
			
			if KEY_DOWN:
				if act+1 == len(items):	act =  0
				else:					act += 1
			elif KEY_UP:
				if act == 0:			act =  len(items)-1
				else:					act -= 1
			
			items[act]['active'] = True
			PLAY_SOUND = True
			
	else:
		# If were moving the mouse, find the item under the mouse and set it active
		if cont.sensors['mouse_movement'].positive:
			idx = menu_mouse_item_index(cont, own, items)
			if idx != -1 and idx != act:
				items[act]['active'] = False
				items[idx]['active'] = True
				PLAY_SOUND = True
	
	if PLAY_SOUND:
		# Enter the play sound state which has an actuator that plays.
		# This is done rather then directly accessinng a play sound actuator
		# because the sound actuator needs a negative event if it is to play
		# sound over and over again, and the state gives it this negative event.
		cont.activate('play_sound')
