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
This script controlls frankies gliding angle, speed etc
'''
import GameLogic
from Mathutils import Vector

TIME_OFFSET = 1000.0
# Set the velocity when gliding		
# This is what we had early on, it even works!!!

GLIDE_PITCH_LIMIT_MAX =  0.8 # angle limit, compare with the Z of a unit length Y vector transformed by the objects world matrix.
GLIDE_PITCH_LIMIT_MIN = -0.8 # ...make sure these match up roughly with 45d constraint that is applied as an actuator

GLIDE_SPEED_LIMIT = 8.0 # Faster you can go the higher you can fly
GLIDE_SPEED_PITCH = 0.05 # set the DRot to this value when tilting
GLIDE_SPEED_FALL_ACCEL = 0.009 # How fast we drop when gliding
GLIDE_SPEED_FALL = -7.0 # -10 makes you fly!
GLIDE_SPEED_FALL_TIME_FAC = 0.05 # 2.66 # increase GLIDE_SPEED_FALL with the jump speed over time.
GLIDE_ACCEL = 0.7 # WATCH THIS ONE!
GLIDE_EASE_IN_TIME = 0.5  # Ease in from current velocity
GLIDE_SLOWPARENT_TIMEOFS = 20.0 # How much delay we should have, (avoids jitter when at maximum pitch)

def main(cont):
	
	own = cont.owner
	own_zpos = own.worldPosition[2]
	
	# If we touch ANYTHING, fall out of glide mode. except for a ledge.
	collide_any = cont.sensors['collide_any']
	if collide_any.positive:
		# If any of these are a bounce object, dont detect a hit.
		if not [ob_hit for ob_hit in cont.sensors['collide_any'].hitObjectList if ('bounce' in ob_hit)]:
			if own['grounded']:	cont.activate('glide_stop_ground')
			else:				cont.activate('glide_stop_air')
			return
	
	own_rig = cont.sensors['rig_linkonly'].owner # The rig owns this! - cheating way ti get the rig/
	
	# print(own.getLinearVelocity())
	# First check if we should quit gliding
	if cont.sensors['key_jump_off'].positive or own['grounded']:
		if own['grounded']:	cont.activate('glide_stop_ground')
		else:				cont.activate('glide_stop_air')
		
		own_rig.timeOffset = own_rig['defTimeOffset']
		return
	
	KEY_UP = cont.sensors['key_up'].positive
	if not KEY_UP:	KEY_DOWN = cont.sensors['key_down'].positive
	else:			KEY_DOWN = False
	
	# Initialize the height, so we can disallow ever getting higher
	if cont.sensors['true_init_pulse_rep'].positive:
		own['glide_z_init'] = own_zpos
		#### own.glide_swooped = 0
		jump_time = 0.0
		own['jump_time'] = TIME_OFFSET # Reuse this for timing our glide since we cant jump once gliding anyway
		
		own_rig.timeOffset = GLIDE_SLOWPARENT_TIMEOFS
	else:
		jump_time = own['jump_time'] - TIME_OFFSET
		if KEY_UP and jump_time > 1.0:
			jump_time = ((jump_time-1) * 0.5) + 1
			own['jump_time'] = jump_time + TIME_OFFSET
	
		# Scale down the timeoffset
		### own_rig.timeOffset *= 0.9
	
	# pprint(jump_time, 'jump_time')
	
	glide= cont.actuators['glide_py']
	
	# Rotation and aligning are now handled in actuators
	
	vel = own.getLinearVelocity()
	own_y = own.getAxisVect((0.0, 1.0, 0.0))
	
	# ------------------------- 
	# own_y[2] MUST BE BETWEEN GLIDE_PITCH_LIMIT_MIN and GLIDE_PITCH_LIMIT_MAX
	# not hard to ensure, but if adjusting the rotate constraint from 45d make sure these change too.
	speed = -(own_y[2]-GLIDE_PITCH_LIMIT_MIN) / (GLIDE_PITCH_LIMIT_MIN-GLIDE_PITCH_LIMIT_MAX)
	speed_inv = 1.0-speed
	
	if KEY_UP:		drot_x = -GLIDE_SPEED_PITCH
	elif KEY_DOWN:	drot_x =  GLIDE_SPEED_PITCH
	else:			drot_x = 0.0
	
	# Set the rotation to tilt forward or back
	glide.dRot = (drot_x, 0.0, 0.0) # set to local on the actuator
	
	# --------------------------
	
	# We COULD just use own_y, but better compensate for the existing 
	# Calculate XY!
	orig_xy_speed = Vector(vel[0], vel[1]).length
	
	fac = speed_inv * GLIDE_ACCEL
	
	orig_xy_speed += fac*fac
	
	if orig_xy_speed > GLIDE_SPEED_LIMIT:
		orig_xy_speed = GLIDE_SPEED_LIMIT
	# normalize and scale to original speed, use verbose python
	own_y_length = Vector(own_y[0], own_y[1]).length
	new_x = (own_y[0]/own_y_length) * orig_xy_speed
	new_y = (own_y[1]/own_y_length) * orig_xy_speed
	#new_xy = Vector(own_y[0], own_y[1])
	#new_xy.length = orig_xy_speed
	
	# Calculate Z, Heres the logic,
	# tilting down makes you go faster but also fall quicker
	# tiltin up makes fall slower but slows you down X/Y motion.
	# if your not moving fast and tilting back, you fall.
	
	# Calculate Z Offset
	fac = GLIDE_SPEED_FALL_TIME_FAC*jump_time
	zoffset = GLIDE_SPEED_FALL + fac*fac # jump time means start for gliding here
	# print(zoffset)
	if zoffset>10.0:
		zoffset=10.0
	
	if speed > 0.5:
		# slow down but go up
		fac = (speed-0.5)*(1800.0/(1+jump_time/20.0))
		zoffset -= (orig_xy_speed / GLIDE_SPEED_LIMIT) * fac
		
		
		fac = 1+(0.5-speed) # Raising above 0.5 is bad juju
		#if own.glide_swooped==2: fac = (fac*fac)
		
		new_x *= fac
		new_y *= fac
		
	else:
		# Falling
		fac = (speed)*30
		zoffset -= (orig_xy_speed / GLIDE_SPEED_LIMIT) * fac
		
		# This 0.98 dampens the forward speed, use the time stuff also
		fac = 0.98 / (1+(GLIDE_SPEED_FALL_TIME_FAC*jump_time))
		new_x *= fac
		new_y *= fac

	new_z = vel[2] -GLIDE_SPEED_FALL_ACCEL * zoffset

	z_over = own_zpos - own['glide_z_init']
	if z_over > 0.0:
		scaler = (1+(z_over*0.2))
		new_x = new_x / scaler
		new_y = new_y / scaler
		if new_z > 0.0: # only scale down if were riseing
			new_z = new_z / scaler
			
	
	# # Interpolate velocity if just started jumping!
	if jump_time < GLIDE_EASE_IN_TIME:
		fac = jump_time / GLIDE_EASE_IN_TIME
		faci = 1.0-fac
		
		new_x = new_x*fac + vel[0]*faci
		new_y = new_y*fac + vel[1]*faci
		new_z = new_z*fac + vel[2]*faci
		# print("Interpolate",fac)
		
	glide.linV = new_x, new_y, new_z # set to global on the actuator
	
	cont.activate(glide)
