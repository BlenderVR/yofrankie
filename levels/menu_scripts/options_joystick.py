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
Detect if we have any joysticks and
remove the keyconfig objects if we have them plugged in
'''
from bge import logic

def main(cont):
	own = cont.owner
	
	# Only run once
	if not cont.sensors['joy_opts_init'].positive:
		return
	
	# Note, after entering key config, this 
	joy_p1_connected = cont.sensors['joy_detect_p1'].connected
	joy_p2_connected = cont.sensors['joy_detect_p2'].connected
	
	if joy_p1_connected:
		cont.activate('end_keys_p1')
		cont.activate('set_joy_message_p1')
		
	if joy_p2_connected:
		cont.activate('end_keys_p2')
		cont.activate('set_joy_message_p2')
	
	cont.activate('remove_joy_detect')
