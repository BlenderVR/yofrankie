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
Use this script when running into a wall with the "slip" property
either run allongside the wall or reflect off it.
'''
from bge import logic

from mathutils import Vector, Matrix, RotationMatrix

def main(cont):
	own = cont.owner
	
	sens_wall_ray = cont.sensors['wall_ray']
	sens_wall_time = cont.sensors['wall_run_time']
	actu_motion = cont.actuators['wall_run_motion']
	
	if not sens_wall_time.positive:
		# We must turn off this actuator once the time limit sensor
		# is false, otherwise it will keep benig applied
		
		# This will happen when first touching the wall which is not needed
		# but there is no harm in it either.		
		# There is a small chance the time will run out but the ray will be hitting somthing.
		# so just to be sure, always remove motion when the wall timer is false.
		
		cont.deactivate(actu_motion)
		if not sens_wall_ray.positive:
			return
	
	# when to apply the rebound force from the wall and turn frankie
	# make sure its lower then the wall_run_time sensor maximum
	LIMIT_REBOUND_TIME = 0.25
	
	REBOUND_LINV = 1.0
	
	#if not sens_wall_ray.positive:
	#if 1:
	if not sens_wall_time.positive and sens_wall_ray.positive:
		# Either initialize a rebound, of if the angle is low, just run paralelle to the wall
		wall_nor = Vector(sens_wall_ray.hitNormal)
		wall_nor.z = 0.0
		
		own_neg_y = Vector(own.getAxisVect((0.0, -1.0, 0.0)))
		own_neg_y.z = 0.0
		
		ang = own_neg_y.angle(wall_nor)
		# 22.5 deg = 0.39269908169872 rad
		if ang > 0.39269908169872:
			cross = wall_nor.cross(own_neg_y)
			# 90 deg = 1.5707963267949 rad
			if cross.z > 0.0:
				paralelle_dir = wall_nor * RotationMatrix(-1.5707963267949, 3, 'Z')	
			else:
				paralelle_dir = wall_nor * RotationMatrix(1.5707963267949, 3, 'Z')	
			
			own.alignAxisToVect(paralelle_dir, 1, 0.1)
			return
		
		else:
			# Rebount! - we're running directly into it
			
			own['wall_run_timer'] = 0.0
			
			# Set the direction velocity, apply this later
			
			''' # Simple direct off wall, not that fun
			wall_nor = sens_wall_ray.hitNormal
			actu_motion.linV = (wall_nor[0]*REBOUND_LINV, wall_nor[1]*REBOUND_LINV, 0.0)
			'''
			
			# Nicer to reflect
			wall_nor.normalize()
			ref = -(own_neg_y.reflect(wall_nor))
			actu_motion.linV = (ref[0]*REBOUND_LINV, ref[1]*REBOUND_LINV, 0.0) # global linV
			
			cont.activate('run_wall')
		
	else:
		## We are not facing the wall anymore, just orient to the reflection vector
		# Apply rebound and face that direction
		if own['wall_run_timer'] > LIMIT_REBOUND_TIME:
			vel = actu_motion.linV.copy()
			own.alignAxisToVect(vel, 1, 0.2)
			cont.activate(actu_motion)
