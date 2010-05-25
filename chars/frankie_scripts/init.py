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
This script runs when frankie is initialized,
it backs up properties for respawning, sets his unique ID and
assignes custom keyconfig and a screen (when 2 player splitscreen), 
when there is only 1 player, the second player removes himself.

This also uses the configuration to set the GLSL detail options
'''


# --------------------- Copied from start_menu.blend, init_options
# Do this so we can import frankie into a blend file and have options there
# will never overwrite existing ones.
# When startng the game from the menu this is not needed.

# Setup default configuration options
import GameKeys
import GameLogic
import GameTypes

def main(cont):
	
	def main_defaults():
		try:	conf = GameLogic.globalDict['CONFIG']
		except:	conf = GameLogic.globalDict['CONFIG'] = {}

		def confdef(opt, value):
			if opt not in conf:
				conf[opt] = value

		confdef('PLAYER_COUNT', 2)
		confdef('GRAPHICS_DETAIL', 1) # 2 == high
		
		
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
		
	main_defaults()
	# ---------------------

	# Use for debugging when you dont want a camera
	WITHOUT_CAMERA = False



	globalDict = GameLogic.globalDict

	try:	conf = GameLogic.globalDict['CONFIG']
	except:	conf = None

	print('\n\nCONF!!!')
	for item in conf.items():
		print(item)

	try:	ID = globalDict['PLAYER_ID'] = globalDict['PLAYER_ID'] + 1
	except:	ID = globalDict['PLAYER_ID'] = 0

	# Backup player properties
	try:	globalDict['PROP_BACKUP']
	except:	globalDict['PROP_BACKUP'] = {}

	try:	PROPS = globalDict['PROP_BACKUP'][ID]
	except:	PROPS = globalDict['PROP_BACKUP'][ID] = {}

	# Setup screens for multi player
	own_camera= cont.owner # The Camera

	own_player = cont.sensors['init_generic'].owner
	# For respawning.

	own_player['id'] = ID

	print('frank_init: ID:', ID)

	def setPlayers():
		import Rasterizer
		
		# menu leaves mouse on
		if ID==0: Rasterizer.showMouse(False)
		
		playcount = conf['PLAYER_COUNT']
		
		if playcount != 1 and playcount != 2:
			cont.activate('set_camera')
			return True
		if ID != 0 and ID != 1:
			print("Unsupported number of players, running anyway")
			cont.activate('set_camera')
			return True
		
		# Single player game. no tricks
		if playcount == 1:
			if ID == 0:
				pass
			else:
				return False
		
		elif playcount == 2:

			# Split screen
			own_camera.useViewport = True
			
			w = Rasterizer.getWindowWidth()
			h = Rasterizer.getWindowHeight()
			if ID == 0:
				# Vert
				#own_camera.setViewport(0, h/2, w, h) 
				# Hoz
				own_camera.setViewport(0, 0, int(w/2), h)
			if ID == 1:
				# Vert
				#own_camera.setViewport(0, 0, w, h/2) 
				# Hoz
				own_camera.setViewport(int(w/2), 0, w, h) 
		
		if not WITHOUT_CAMERA:
			cont.activate('set_camera')
		
		return True

	def setHUD():
		try:	hud_dict = GameLogic.globalDict['HUD']
		except:	hud_dict = GameLogic.globalDict['HUD'] = {}
		
		hud_dict['life_p%d' % (ID+1)] = own_player['life'] # will be life_p1 or life_p2
		hud_dict['bonecount_p%d' % (ID+1)] = 0 # will be life_p1 or life_p2
		
		# store animals we have hit
		hud_dict['hitlist_p%d' % (ID+1)] = []
		
		if WITHOUT_CAMERA:
			return
		
		# Only add the hud once.
		if ID == 0:# and conf['PLAYER_COUNT'] == 1:
			cont.activate('set_hud')
		
		

	def setKeys():
		import GameKeys
		
		# First see if we have a valid joystick
		sensors = cont.sensors
		# print(len(sensors), 'sensors')
		joySensors = [s for s in sensors if type(s) == GameTypes.SCA_JoystickSensor]
		keySensors = [s for s in sensors if type(s) == GameTypes.SCA_KeyboardSensor]
		
		own_joy = joySensors[0].owner
		own_kb = keySensors[0].owner
		
		# If we have a valid joystick, then remove keyboard, else remove joystick object.
		for sens in joySensors:
			sens.index = ID # player index can match joystick index
		
		# Use the last joystick sensor
		if sens.connected:
			# remove the keyboard object and dont bother setting up keyconfig
			print('Player', ID, 'using joystick')
			own_kb.endObject()
			return
		else:
			# No joystick connected at ID, setup keys
			print('Player', ID, 'using keyboard')
			own_joy.endObject()
		
		
		
		# Done With joystick, Fallback to keys!
		
		if not conf:
			print("config not loaded")
			return
		
		# First player, leave keys as is
		KEY_MAPPING = None
		
		# Odd but ID 1 is most common key mapping
		# this is because for a single player ID zero is removed
		
		if ID==0:
			# For second player only now
			KEY_MAPPING = {\
			GameKeys.UPARROWKEY : conf['KEY_UP_P1'],\
			GameKeys.LEFTARROWKEY : conf['KEY_LEFT_P1'],\
			GameKeys.DOWNARROWKEY : conf['KEY_DOWN_P1'],\
			GameKeys.RIGHTARROWKEY : conf['KEY_RIGHT_P1'],\
			GameKeys.NKEY : conf['KEY_ACTION_P1'],\
			GameKeys.MKEY : conf['KEY_JUMP_P1'],\
			GameKeys.SPACEKEY : conf['KEY_THROW_P1'],\
			}
		elif ID==1:
			KEY_MAPPING = {\
			GameKeys.UPARROWKEY : conf['KEY_UP_P2'],\
			GameKeys.LEFTARROWKEY : conf['KEY_LEFT_P2'],\
			GameKeys.DOWNARROWKEY : conf['KEY_DOWN_P2'],\
			GameKeys.RIGHTARROWKEY : conf['KEY_RIGHT_P2'],\
			GameKeys.NKEY : conf['KEY_ACTION_P2'],\
			GameKeys.MKEY : conf['KEY_JUMP_P2'],\
			GameKeys.SPACEKEY : conf['KEY_THROW_P2'],\
			}
		
		if KEY_MAPPING:	
			for sens in cont.sensors:
				if type(sens) == GameTypes.SCA_KeyboardSensor:
					sens.key = KEY_MAPPING[sens.key]
		else:
			print('Cannot map keys for player ID', ID)
				
	def backupPosition():
		# For respawning. run BEFORE backupProps
		own_player['orig_pos'] = '%.3f %.3f %.3f' % tuple(own_player.worldPosition)

	def backupProps():
		# These are restored when respawning
		for propName in own_player.getPropertyNames():
			PROPS[propName] = own_player[propName]

	def restoreProps():
		for prop, value in PROPS.items():
			own_player[prop] = value

	def setPortal():
		# This may run when entering a new scene, we may be entering from a portal
		# 2nd players are placed higher, make sure portal enteries have enough room above
		
		sce = GameLogic.getCurrentScene()
		
		try:	scene_name = globalDict['PORTAL_SCENENAME']
		except:	scene_name = ''
		
		if scene_name and scene_name != sce.name:
			# we have come from another blend file that needs to switch to a scene.
			# first switch the scene, this script will run again and 
			
			set_scene_actu = cont.actuators['portal_scene']
			set_scene_actu.scene = scene_name
			cont.activate(set_scene_actu)
			return
		
		try:	target_name = globalDict['PORTAL_OBNAME']
		except: return
		
		try:
			target_ob = sce.objects[target_name] # alredy has 'OB' prefix
		except:
			print('Oops: portal switch error,', target_name, 'object is not in the scene')
			return
		
		pos = target_ob.worldPosition
		pos[2] += 1.0 * ID # move other players higher so they dont overlap
		
		own_player.localPosition = pos
		own_player.localOrientation = target_ob.worldOrientation
		
		# Keep GameLogic.PORTAL_OBNAME incase there are more players
		
		
		# Annoying, the 'Loading Text', needs to be turned off if we're only 
		for sce in GameLogic.getSceneList():
			if sce.name == 'hud':
				ob = sce.objects.get('OBloading')
				if ob:
					ob.visible = False
					
					

	def setGfxQuality():
		import Rasterizer
		# return
		# Only to this once
		if ID != 0:
			return
		
		
		
		conf = GameLogic.globalDict['CONFIG']
		
		if conf['GRAPHICS_DETAIL'] == 0:
			print("\tconfig: setting deytail low")
			Rasterizer.setGLSLMaterialSetting("lights", 1)
			Rasterizer.setGLSLMaterialSetting("shaders", 0)
			Rasterizer.setGLSLMaterialSetting("shadows", 0)
			Rasterizer.setGLSLMaterialSetting("ramps", 0)
			Rasterizer.setGLSLMaterialSetting("nodes", 0)
			Rasterizer.setGLSLMaterialSetting("extra_textures", 1)
		elif conf['GRAPHICS_DETAIL'] == 1:
			print("\tconfig: setting deytail med")
			Rasterizer.setGLSLMaterialSetting("lights", 1)
			Rasterizer.setGLSLMaterialSetting("shaders", 0)
			Rasterizer.setGLSLMaterialSetting("shadows", 0)
			Rasterizer.setGLSLMaterialSetting("ramps", 1)
			Rasterizer.setGLSLMaterialSetting("nodes", 0)
			Rasterizer.setGLSLMaterialSetting("extra_textures", 1)
		else: # high quality
			print("\tconfig: setting deytail high")
			Rasterizer.setGLSLMaterialSetting("lights", 1)
			Rasterizer.setGLSLMaterialSetting("shaders", 1)
			Rasterizer.setGLSLMaterialSetting("shadows", 1)
			Rasterizer.setGLSLMaterialSetting("ramps", 1)
			Rasterizer.setGLSLMaterialSetting("nodes", 1)
			Rasterizer.setGLSLMaterialSetting("extra_textures", 1)
		
	
	def setup_player():
		
		# If the player cant be initialized, dont do anything else
		
		if not setPlayers():
			own_player.endObject()		
			print("REMOVING PLAYER", ID)
			return
		else:
			print("ADDING PLAYER", ID)
		
		setHUD()
		if PROPS != {}:
			restoreProps()
		
		setKeys()
		setPortal() # If we have a portal
		backupPosition() # MUST run before backing up props
		backupProps() # backup changes to GameLogic dict
		
		setGfxQuality()
	
	setup_player()

