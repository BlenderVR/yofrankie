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


# Better only keep a subset of our props

'''
when touching a "portal" property object, use its properties to move to its target.
possible targets are object, scene or blendfile (or a mix)
When loading scenes or blendfiles, "frank_init" scripts check for the portal settings and finish off the positioning.
'''

import GameLogic

def backupProps(own):
	# We could reset others but these are likely to cause problems
	PROPS = GameLogic.globalDict['PROP_BACKUP'][own['id']]
	# We backed these up, see frank_init
	# Only backup "life" and inventory -> "item_*"
	PROPS['life'] = own['life']
	for propName in own.getPropertyNames():
		if propName.startswith('item_'):
			PROPS[propName] = own[propName]


def main(cont):
	
	own = cont.owner
	globalDict = GameLogic.globalDict
	
	portal_ob = cont.sensors['portal_touch'].hitObject
	
	if not portal_ob:
		return
	
	sce = GameLogic.getCurrentScene()
	target_name = portal_ob['portal']
	
	# incase the portal was set before
	# we dont want to use an invalid value
	try:	del globalDict['PORTAL_OBNAME']
	except:	pass
	
	try:	del globalDict['PORTAL_SCENENAME']
	except:	pass
		
	blend_name = portal_ob.get('portal_blend', '') # No way to check if this really matches up to a blend
	scene_name = portal_ob.get('portal_scene', '') # No way to check if this really matches up to a scene
	
	
	# A bit dodgy, for the first logic tick show the loading text only
	# portal collision must be on pulse so its gets a second tick and runs the portal code below.
	if blend_name or scene_name:
		for sce in GameLogic.getSceneList():
			if sce.name == 'hud':
				loading_ob = sce.objects['OBloading']
				if not loading_ob.visible:
					loading_ob.visible = True
					return
	# done with loading text!
	
	
	if blend_name:
		# todo, allow blend AND scene switching. at the moment can only do blend switching.
		set_blend_actu = cont.actuators['portal_blend']
		set_blend_actu.fileName = blend_name
		
		try:	del globalDict['PLAYER_ID'] # regenerate ID's on restart
		except:	pass
		
		if target_name:
			globalDict['PORTAL_OBNAME'] = 'OB' + target_name
		
		if scene_name:
			globalDict['PORTAL_SCENENAME'] = scene_name
				
		# Backup props
		backupProps(own)
		
		cont.activate(set_blend_actu)
		
	elif scene_name:
		# portal_ob
		set_scene_actu = cont.actuators['portal_scene']
		set_scene_actu.scene = scene_name
		
		try:	del globalDict['PLAYER_ID'] # regenerate ID's on restart
		except:	pass
		
		if target_name:
			globalDict['PORTAL_OBNAME'] = 'OB' + target_name
		
		# Backup props
		backupProps(own)
		
		cont.activate(set_scene_actu)
	else:
		# Simple, only move to the portal.
		try:
			target_ob = sce.objects['OB'+target_name]
		except:
			print('Oops: portal switch error,', target_name, 'object is not in the scene')
			return
		
		# We may be gliding, make sure there is no timeoffset
		own_rig = cont.sensors['rig_linkonly'].owner # The rig owns this! - cheating way ti get the rig/
		own_rig.timeOffset = own_rig.defTimeOffset
		
		own.localPosition = target_ob.worldPosition
		own.localOrientation = target_ob.worldOrientation
		own.setLinearVelocity((0.0, 0.0, 0.0))
		
		# set the state incase we are climbing or somthing
		set_state_actu = cont.actuators['fall_state_switch']
		
		cont.activate(set_state_actu)
