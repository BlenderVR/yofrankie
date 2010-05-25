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
use GameLogic.globalDict which is stored between loading blend files
'''
import GameKeys
import GameLogic

def main():
	try:	conf = GameLogic.globalDict['CONFIG']
	except:	conf = GameLogic.globalDict['CONFIG'] = {}

	def confdef(opt, value):
		if opt not in conf:
			conf[opt] = value
	
	confdef('PLAYER_COUNT', 1)
	confdef('GRAPHICS_DETAIL', 2) # 2 == high	
	confdef('GRAPHICS_GLSL', 1) # toggle
	
	# Keys
	
	# P1
	confdef('KEY_UP_P1', GameKeys.UPARROWKEY)
	confdef('KEY_DOWN_P1', GameKeys.DOWNARROWKEY)
	confdef('KEY_LEFT_P1', GameKeys.LEFTARROWKEY)
	confdef('KEY_RIGHT_P1', GameKeys.RIGHTARROWKEY) 
	
	# P2
	confdef('KEY_UP_P2', GameKeys.WKEY) 
	confdef('KEY_DOWN_P2', GameKeys.SKEY)
	confdef('KEY_LEFT_P2', GameKeys.AKEY)
	confdef('KEY_RIGHT_P2', GameKeys.DKEY) 
	
	# P1
	confdef('KEY_JUMP_P1', GameKeys.MKEY) 
	confdef('KEY_THROW_P1', GameKeys.SPACEKEY) 
	confdef('KEY_ACTION_P1', GameKeys.NKEY) 
	
	# P2
	confdef('KEY_JUMP_P2', GameKeys.GKEY)
	confdef('KEY_THROW_P2', GameKeys.JKEY)
	confdef('KEY_ACTION_P2', GameKeys.HKEY)
	
	# 
	import Rasterizer
	Rasterizer.showMouse(True)
