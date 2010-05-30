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
Setup default configuration options
use logic.globalDict which is stored between loading blend files
'''
from bge import events
from bge import logic

def main():
	try:	conf = logic.globalDict['CONFIG']
	except:	conf = logic.globalDict['CONFIG'] = {}

	def confdef(opt, value):
		if opt not in conf:
			conf[opt] = value
	
	confdef('PLAYER_COUNT', 1)
	confdef('GRAPHICS_DETAIL', 2) # 2 == high	
	confdef('GRAPHICS_GLSL', 1) # toggle
	
	# Keys
	
	# P1
	confdef('KEY_UP_P1', events.UPARROWKEY)
	confdef('KEY_DOWN_P1', events.DOWNARROWKEY)
	confdef('KEY_LEFT_P1', events.LEFTARROWKEY)
	confdef('KEY_RIGHT_P1', events.RIGHTARROWKEY) 
	
	# P2
	confdef('KEY_UP_P2', events.WKEY) 
	confdef('KEY_DOWN_P2', events.SKEY)
	confdef('KEY_LEFT_P2', events.AKEY)
	confdef('KEY_RIGHT_P2', events.DKEY) 
	
	# P1
	confdef('KEY_JUMP_P1', events.MKEY) 
	confdef('KEY_THROW_P1', events.SPACEKEY) 
	confdef('KEY_ACTION_P1', events.NKEY) 
	
	# P2
	confdef('KEY_JUMP_P2', events.GKEY)
	confdef('KEY_THROW_P2', events.JKEY)
	confdef('KEY_ACTION_P2', events.HKEY)
	
	# 
	from bge import render
	render.showMouse(True)
