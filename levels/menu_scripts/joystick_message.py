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
Detect if we have any joysticks and set a message
for the main menu
'''
from bge import logic

def main(cont):
	own = cont.owner
	
	# Only run once
	if not cont.sensors['joy_text_init'].positive:
		return
	
	joy_p1_connected = cont.sensors['joy_detect_p1'].connected
	joy_p2_connected = cont.sensors['joy_detect_p2'].connected
	
	if joy_p1_connected and joy_p2_connected:
		own['Text'] = 'Two joysticks found'
	elif joy_p1_connected:
		own['Text'] = 'one joystick found'
	else:
		own['Text'] = 'no joysticks found'
