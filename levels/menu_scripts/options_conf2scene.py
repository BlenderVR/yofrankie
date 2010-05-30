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
Take options from the dict and set the scene up from these.
'''

from bge import events
from bge import logic

ITEM_PREFIX = 'item_'

def main():
	# print('Setting scene properties from python configuration dictionary')
	# print('using dictionary - logic.globalDict["CONFIG"]')
	
	conf = logic.globalDict['CONFIG']
	sce = logic.getCurrentScene()
	
	
	# ***************************
	# First gather item_ prefixed
	# objects to use for config
	
	obs_radio = []
	obs_toggle = []
	obs_key = []
	
	for ob in sce.objects:
		name = ob.name
		
		# Keys are not menu items, they are a special case
		if name.startswith('KEY_'):
			obs_key.append(ob)
			continue
		
		elif not name.startswith(ITEM_PREFIX):
			continue
		
		
		if 'conf_key' not in ob:
			# This is normal, some items are just triggered.
			# and are not for configuring
			continue
		
		conf_key = ob['conf_key']
		
		if conf_key not in conf:
			print('\tMenu error - item:', ob.name, 'uses conf_key:', conf_key, 'not found in logic.globalDict["CONFIG"], ignoring')
			continue
		
		if 'radio' in ob:
			obs_radio.append(ob)
		elif 'toggle' in ob:
			obs_toggle.append(ob)
		else:
			print('\tMenu error - item:', ob.name, 'uses conf_key:', conf_key, 'is not a toggle or a radio button, ignoring')
			
	
	# ***************************
	# Radio - for graphics detail
	radio_items = []
	for ob in obs_radio:
		conf_key = ob['conf_key']
		if conf_key not in radio_items:
			radio_items.append(conf_key)
	# for py 2.4+ can use sets
	# radio_items = set([ob.conf_key for ob in obs_radio])
	
	for conf_key in radio_items:
		conf_value = conf[conf_key]

		for ob in obs_radio:
			if ob['conf_key'] == conf_key:
				if ob['radio'] == conf_value:
					ob['enabled'] = 1
				else:
					ob['enabled'] = 0
			
		
	# ***************************
	# Toggle - for switches
	## print('\tToggles')
	for ob in obs_toggle:
		## print('\tSetting toggle state for', ob.getName(), 'conf_key:', ob.conf_key, 'state:', conf[ob.conf_key])
		ob['toggle'] = conf[ob['conf_key']]
	
	
	# ***************************
	# Key Setings
	key_mapping = dict([(ob.name.split('.')[0], ob) for ob in obs_key ]) # object names to key names

	def confKeyObSet(opt):
		try:	ob=	key_mapping[opt]
		except: ob = None
		if ob:		ob['Text'] = events.EventToString(conf[opt]).replace('ARROW', '').replace('KEY', '').lower()
		else:		print('no object found for', opt)
	
	keys = [
		'KEY_UP_P1',\
		'KEY_DOWN_P1',\
		'KEY_LEFT_P1',\
		'KEY_RIGHT_P1',\


		'KEY_UP_P2',\
		'KEY_DOWN_P2',\
		'KEY_LEFT_P2',\
		'KEY_RIGHT_P2',\


		'KEY_JUMP_P1',\
		'KEY_THROW_P1',\
		'KEY_ACTION_P1',\


		'KEY_JUMP_P2',\
		'KEY_THROW_P2',\
		'KEY_ACTION_P2',\
	]
	
	for key in keys:
		confKeyObSet(key)
