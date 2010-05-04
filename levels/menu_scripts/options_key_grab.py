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
Used for configuring keys.
This script runs all actuators when a key is pressed.

The object name of the key sensor patches up with the key config name
This way the key pressed is written to the configuration.
'''
import GameKeys
import GameLogic

def main(cont):
	# This is set in init_options
	conf = GameLogic.globalDict['CONFIG']
	
	own = cont.owner
	
	# print("Grabbing Key", own.getName())
	
	# We only have 1 key sensor
	# its name is used to reference the python setting
	sensor = cont.sensors[0] 
	
	own_display = sensor.owner # the sensor is on the object displaying the text
	
	key_id = None
	
	for k_id, press_stat in sensor.events:
		# print('key id', k_id, press_stat)
		if not press_stat == 3: #1 is down 3, is for key up... ok???
			key_id = k_id
			break
		
	if key_id == None:
		print('NoKey Presed')
		return
	
	
	# Lets be tricky here
	# the object name is prefixed by the Python dictionary key for configuring it.
	# remember to remove OB
	conf_dict_key = own_display.name[2:].split('.')[0]
	
	conf[conf_dict_key] = key_id
	
	# Display the name
	own_display['Text'] = GameKeys.EventToString(key_id).replace('ARROW', '').replace('KEY', '').lower()
	
	# Go to next state
	for actu in cont.actuators:
		cont.activate(actu)
