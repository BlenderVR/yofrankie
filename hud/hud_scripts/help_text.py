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
sets the key text for the help screen
'''

import GameKeys
import GameLogic

def main(cont):
	own = cont.owner
	
	try:	conf = GameLogic.globalDict['CONFIG']
	except:	conf = GameLogic.globalDict['CONFIG'] = {}
	
	children = [(ob.name, ob) for ob in own.children]
	children.sort()
	
	obs_p1 = [ pair[1] for pair in children if '_p1' in pair[0] ]
	obs_p2 = [ pair[1] for pair in children if '_p2' in pair[0] ]
	
	
	if not conf:
		for ob in obs_p1:		ob['Text'] = 'debug'
		for ob in obs_p2:		ob['Text'] = 'debug'
		return
	
	# Override key text
	joy_p1 = cont.sensors['joy_test_p1'].connected
	joy_p2 = cont.sensors['joy_test_p2'].connected
	
	# Always do player 1
	keys_p1 = []
	keys_p2 = []
	
	
	if not joy_p1:
		for item in conf.items():
			if item[0].startswith('KEY_') and item[0].endswith('_P1'):
				keys_p1.append( item )
	
		keys_p1.sort()
		
	if not joy_p2:
		for item in conf.items():
			if item[0].startswith('KEY_') and item[0].endswith('_P2'):
				keys_p2.append( item )
			
		keys_p2.sort()
	
	
	text_p1 = ['player 1 keys']
	text_p2 = ['player 2 keys']
	
	for keys, text, obs, joy_connected in [(keys_p1, text_p1, obs_p1, joy_p1), (keys_p2, text_p2, obs_p2, joy_p2)]:
		if joy_connected:
			text.append( 'using joystick' )
		else:
			for key, value in keys:
				# KEY_UP_P1 -> up
				name = key.split('_')[1].lower()
				val = GameKeys.EventToString(value).replace('KEY', '').lower()
				text.append('%s - %s' % (name, val))
		
		for i, line in enumerate(text):
			obs[i]['Text'] = line

