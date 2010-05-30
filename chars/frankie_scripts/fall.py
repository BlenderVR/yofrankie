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
When frankie is airboure he can double jump and glide
This script checks for conditions where this is ok and changes the state.

It also clamps the fall speed and detects when he is going to land so it can play the animation
'''
from bge import logic

from mathutils import Vector

DBL_JUMP_KEYHELD = 0
DBL_JUMP_OK = 1
DBL_JUMP_DONE = 2
DBL_JUMP_MISSED = 3
DBL_JUMP_DELAY = 4 # Delayed jumping means double jump wes pressed really fast and we have to delay before applying


DBL_JUMP_FALL_MARGIN = -1.4 # how fast you can be falling before you cant double jump anymore
DBL_JUMP_BEGIN_TIME = 0.3 # How long after jumping your allowed to double jump
	

def do_pradict_land(own, cont, velocity):
	# Check if we should land?
	if velocity[2] < -2.0: # Check downward falling velocity, 0.0 could be used but -2.0 seems good enough
		ray_to = own.worldPosition[:]
		ray_to[2] -= 10.0
		if own.rayCastTo(ray_to, 0.6, 'ground'):
			cont.activate('landing')
			cont.activate('landing_snd')


def do_clamp_speed(own, cont, velocity):		
	'''
	Clamp the x/y velocity, we can do speedups etc here
	but for now just clamping at around run speed is fine.
	'''
	velocity_vec = Vector([velocity[0], velocity[1]])
	l = velocity_vec.length


	if own['boosted']:
		MAX_SPEED = 3.0	
	else:
		MAX_SPEED = 6.0	
	
	if l < MAX_SPEED:
		return
	
	velocity_vec.length = MAX_SPEED
	
	velocity[0] = velocity_vec[0]
	velocity[1] = velocity_vec[1]
	
	own.setLinearVelocity(velocity)

def do_double_jump(own, cont, dropping_dir, actu_dbl_jump_anim, actu_dbl_jump_force):
	if dropping_dir > DBL_JUMP_FALL_MARGIN: # 0.2 to allow SOME falling
		if own['jump_time'] < DBL_JUMP_BEGIN_TIME:
			own['double_jump'] = DBL_JUMP_DELAY
		else:
			# Do the double jump
			# print("Reset Actuator 2", actu_dbl_jump_anim.getStart())
			# actu_dbl_jump_anim.setFrame( actu_dbl_jump_anim.getStart() )
			
			cont.activate(actu_dbl_jump_anim)
			actu_dbl_jump_anim = None
			
			cont.activate(actu_dbl_jump_force)
			actu_dbl_jump_force = None # Dont disable this
			
			own['double_jump'] = DBL_JUMP_DONE
			own['jump_time'] = 100.0 # So we know how long we have jumped for before gliding
			return True
	else:
		# We are falling so set the double jump done so we can glide.
		own['double_jump'] = DBL_JUMP_MISSED
		return False
	# Even if we  didnt double jump, tag as done. this way glide works
	return False


def do_glide_state(own, cont, velocity):
	# We know this cant be done before double jumping or missing a double jump
	# print(cont.sensors['any_collide'].positive, cont.sensors['any_collide'].hitObjectList,)
	###print([o.name for o in cont.sensors['any_collide'].hitObjectList])
	
	if velocity[2] > 0.0: # we must be falling
		return
	
	if cont.sensors['collide_any'].positive:
		return
	
	# print(dir(cont.sensors['any_collide']))
	if	own['double_jump'] == DBL_JUMP_MISSED  or  \
		(own['double_jump'] == DBL_JUMP_DONE  and  own['jump_time'] > 100.3): # and \
		# Note, own['jump_time'] over 100.0 will give a limit so you cant double jump right away
		
		
		# Other logic that didnt work so well
		# (not cont.sensors['any_collide'].positive):
		# (own['double_jump'] == DBL_JUMP_DONE and (actu_dbl_jump_anim.frame > actu_dbl_jump_anim.endFrame-1.0)):
		
		cont.activate('glide_state')

def main(cont):
	
	own = cont.owner
	
	# own.restoreDynamics() # WE SHOULDNT HAVE TO CALL THIS HERE
	
	
	# print([o.name for o in cont.sensors['any_collide'].hitObjectList])
	
	velocity = own.getLinearVelocity()
	
	
	# Done by an actuator now. we could add this back and remove the actuator.
	# but nicer to use user visible logic bricks.
	# own.alignAxisToVect([0,0,1], 2, 0.1)
	
	do_clamp_speed(own, cont, velocity)
	do_pradict_land(own, cont, velocity)
	
	KEY_JUMP = cont.sensors['key_jump'].positive
	
	
	
	actu_dbl_jump_anim = cont.actuators['doublejump']
	actu_dbl_jump_force = cont.actuators['double_jump_force']
	double_jump_done = False
	
	# Did we just enter this state?
	if cont.sensors['generic_true_pulse'].positive:
		if own['jump_time'] < 0.3:
			if not KEY_JUMP: # This is very unlikely since we only JUST sstarted jumping. in cases where we fall off a ledge its possible still.
				own['double_jump'] = DBL_JUMP_OK # Key is released, we can double jump next time its pressed.
			else:
				own['double_jump'] = DBL_JUMP_KEYHELD # We are not sure they were jumping so be sure to check the timer.
	else:		
		# Not bouncing
		if KEY_JUMP or own['double_jump'] == DBL_JUMP_DELAY:
			
			# Cant double jump or glide while carrying.
			if not own['carrying']:
				
				if own['double_jump'] == DBL_JUMP_OK or own['double_jump'] == DBL_JUMP_DELAY:
					double_jump_done =  do_double_jump(own, cont, velocity[2], actu_dbl_jump_anim, actu_dbl_jump_force)
				else:
					do_glide_state(own, cont, velocity)
		else:
			if own['double_jump'] == DBL_JUMP_KEYHELD:
				own['double_jump'] = DBL_JUMP_OK # Key is released, we can double jump next time its pressed.
	
	# If actions are not None, assume we didint want to suse them
	
	if not double_jump_done:
		cont.deactivate(actu_dbl_jump_force)
	
	# Add falling animations
	# print('%.4f' % velocity[2])
	# Use the right falling animation, falling up or down?
	if velocity[2] > 0.0:
		cont.deactivate('fall_down')
		cont.activate('fall_up')
	else:
		cont.deactivate('fall_up')
		cont.activate('fall_down')
