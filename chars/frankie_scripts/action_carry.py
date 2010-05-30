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
Run when a carry object hits us and attach it to our hand if all is right (and the moons are aligned)
'''
from bge import logic
from mathutils import Matrix

# We use this a lot, just to be neat
def dontCatch(cont):
	cont.deactivate('catch')


def do_catch(cont, own, ob_carry, ob_catch_bonechild):
	
	own_pos = own.worldPosition
		
	'''
	If we are ok to catch an object, this function runs on all catchable objects
	and catches the first catchable one since its possible we collide with multiple.
	'''
	
	if ob_carry.get('grounded', 0) != 0:
		print('\tcant catch: carry object not airbourne')
		return False
	
	if ob_carry['carried'] == 1:
		print('\tcant catch: alredy being carried by another')
		return False
	
	ob_carry_pos = ob_carry.worldPosition
	
	if ob_carry_pos[2] < own_pos[2]+0.1:
		print('\tcant catch: catch objects Z position too low')
		return False
	
	# is it falling down?
	# - Note, dont do this. once its hit your head its velovcity changes so we cant rely on it
	'''
	if ob_carry.getLinearVelocity()[2] > 0.0:
		print("\tcarry? not falling")
		return False
	'''
	# Is it close enough to the center?
	# - Note, dont do this. if it touches we can carry, otherwise stuff sits on your head and nothing happens.
	'''
	if abs(ob_carry_pos[1] - pos_ray_sens[1]) + abs(ob_carry_pos[0] - pos_ray_sens[0]) > 0.5:
		return False
	'''
	
	# Cannot carry a dead animal
	if ob_carry.get('life', 1) <= 0:
		print("\tcant catch: cant carry dead")
		return False
	
	
	# Ok, Checks are done, now execute the catch
	
	# Orient the carry objects Z axis to the -Z of the sheep,
	# since it should be upside down
	if ob_carry.get('type', '') == 'shp':
		ob_catch_bonechild.alignAxisToVect(ob_carry.getAxisVect((0.0, 0.0,-1.0)), 2)
		pos = ob_catch_bonechild.worldPosition
	else:
		# ob_catch_bonechild.alignAxisToVect(ob_carry.getAxisVect([0,1,0]), 2)
		#pos = ob_catch_bonechild.worldPosition
		#pos[2] += 1
		
		ob_catch_bonechild.alignAxisToVect(ob_carry.getAxisVect((0.0, 0.0, -1.0)), 2)
		#ob_catch_bonechild.alignAxisToVect(ob_carry.getAxisVect([0,1,0]), 1)
		ob_carry.alignAxisToVect(own.getAxisVect((0.0, -1.0, 0.0)), 1)
		pos = ob_catch_bonechild.worldPosition
		
		# Only for carrying frankie
		if 'predator' in ob_carry:
			pos[2] -= 0.15
	
	
	# Set the parent
	# ob_catch_bonechild.alignAxisToVect([0,0,1], 2)
	
	ob_carry.localPosition = pos
	# Dont touch transformation after this!
	ob_carry.setParent(ob_catch_bonechild)
	own['force_walk'] = -1.0
	own['carrying'] = 1
	ob_carry['carried'] = 1
	cont.activate('catch')
	cont.activate('carry_constrain_up')


def main(cont):
	own = cont.owner
	
	# This object is a child of the wrist bone, it is used as the parent so the animations control the object motion
	
	
	# We are alredy carrying
	if own['carrying']:
		return # Alredy carrying
	
	ob_catch_bonechild = cont.sensors['carry_pos_linkonly'].owner	
	if ob_catch_bonechild.children:
		print('\tcarry warning, carrying was not set but had an object in hand! - should never happen, correcting')
		own['carrying'] = 1
		return

	# Do some sanity checks
	if own['grounded'] == 0:
		print('\tcant catch anything: we are not on the ground')
		dontCatch(cont)
		return
	
	# Are we falling or doing an action?
	#	Note! use own['action_done'] so carrying only stops when the throwing part of the action is done.
	#	otherwise youll drop the object before throwing
	

	
	if own['action_done'] != 0:
		# Kicking is ok to catch
		if own['action_name'] in ('', 'kick'):
			pass
		else:
			print('\tcant catch anything: midst other action, not doing action', own['action_name'], own['action_name'])
			dontCatch(cont)
			return
	
	if own['action_name'] != '':
		dontCatch(cont)
		return	
	
	sens_collideCarry = cont.sensors['carry_collider']
	
	if not sens_collideCarry.positive:
		print('\tcant catch anything: carry collider false')
		dontCatch(cont)
		return
	
	
	# Now we know we are in a fine state to catch an object
	# look through all catch collisions and catch the first one we can.
	# its unlikely there will ever be more then 2 or 3 but this is safest.
	
	for ob_carry in sens_collideCarry.hitObjectList:
		if do_catch(cont, own, ob_carry, ob_catch_bonechild):
			return
	
	# If we are still here it means we couldnt catch anything
	dontCatch(cont)
