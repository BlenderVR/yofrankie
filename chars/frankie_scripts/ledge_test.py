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


# This module is used in 2 places.
# ledge_collide.py -	To detect if we can grab a ledge
# ledge_hang.py -		To keep us attached to the edge

# Since we cant import modules in the blenderplayer assign to 
# GameLogic.frankTestLedge = frankTestLedge
# import debug
# reload(debug)

import GameLogic, mathutils
from mathutils import Vector

CLIMB_HANG_Y_OFFSET = -0.25
CLIMB_HANG_Z_OFFSET = -0.35

RAY_LENGTH = 1.0
RAY_CAST_Z_OFFSET = 0.2

# This module is importedm, not used directly
def frankTestLedge(own, cont, hit_object, CORRECTION_RAY):
	
	'''
	hit_object is the ledge we are colliding,
		if its None then just look for all objects
		with 'ledge' property
	
	Return: ray_hit, ray_nor, z_pos
	'''

	if own['carrying'] or own['carried']:
		print("cant grab - carry!")
		return None, None, None

	own_pos = own.worldPosition
	'''
	own_pos = own.worldPosition
	own_pos_ofs = own_pos[:]
	[2] += RAY_CAST_Z_OFFSET
	'''	

	
	# Ok we are colliding and pressing up		
	y_axis = own.getAxisVect( (0.0, 1.0, 0.0) )
	
	ray_dir = own_pos[:]
	ray_dir[0] += y_axis[0]
	ray_dir[1] += y_axis[1]
	
	if hit_object:
		# print("HITUP!!!")
		#ob_ledge, hit_first, nor_first = own.rayCast(ray_dir, hit_object, RAY_LENGTH)
		ob_ledge, hit_first, nor_first = own.rayCast(ray_dir, own_pos, RAY_LENGTH)
		if ob_ledge and ob_ledge != hit_object:
			print("Hit Wrong Object, was %s should be %s" % (ob_ledge.name, hit_object.name)) # should never happen
			return None, None, None			
	else:
		# print("NO HITOB!!!")
		ob_ledge, hit_first, nor_first = own.rayCast(ray_dir, own_pos, RAY_LENGTH, 'ledge')
	
	if not hit_first:
		print("FirstLedgeRay Missed!", ray_dir, y_axis)
		return None, None, None
	
	# debug.setpos( hit_first )
	
	# Not strictly needed but makes for better results, shoot a ray allong the normal of the ray ray you just hit
	# This prevents moving too far when latching onto a ledge.
	
	y_axis_corrected = [-nor_first[0], -nor_first[1], 0.0]
	ray_dir_first = ray_dir[:]
	
	
	# Should we re-shoot a ray that is corrected based on the normal from the surface of what we hit?
	if CORRECTION_RAY:
		ray_dir_closer = own_pos[:]
		ray_dir_closer[0] += y_axis_corrected[0]
		ray_dir_closer[1] += y_axis_corrected[1]
		
		if hit_object:
			ob_closer, hit_closer, nor_closer = own.rayCast(ray_dir_closer, hit_object, RAY_LENGTH,  'ledge')
		else:
			ob_closer, hit_closer, nor_closer = own.rayCast(ray_dir_closer, None, RAY_LENGTH, 'ledge')
		
		if ob_closer:
			### print("CAST !!!!!!!!2nd ray")
			AXIS = ((hit_closer, y_axis_corrected, nor_closer), (hit_first, y_axis, nor_first))
		else:
			### print("Can only castr 1 ray")
			AXIS = ((hit_first, y_axis, nor_first),)
	else:
		# Simple, dont pradict best second ray
		ob_closer = None
		AXIS = ((hit_first, y_axis, nor_first),)
	
	
	# Do Z Ray Down.
	Y_OFFSET = 0.6 # length of the Y ray forward.
	Z_OFFSET = 0.6 # length of the Z ray up.
	
	for hit_new, y_axis_new, nor_new in AXIS:
		
		# Set the 2D length of this vector to Y_OFFSET
		y_axis_new = Vector([y_axis_new[0],y_axis_new[1]])
		y_axis_new.length = Y_OFFSET
		
		# Now cast a new ray down too see the Z posuition of the ledge above us
		new_ray_pos= [own_pos[0]+y_axis_new[0], own_pos[1]+y_axis_new[1], own_pos[2]+Z_OFFSET]
		new_ray_pos_target = new_ray_pos[:]
		new_ray_pos_target[2] -= 0.5 # This dosnt matter, just lower is fine
		
		### debug.setpos( new_ray_pos )
		### debug.setpos( new_ray_pos_target )
		
		
		ob_ledge, hit_down, nor_down = own.rayCast(new_ray_pos_target, new_ray_pos, 0.5) # Can hit objects of any property, MAYBE should choose ground.
		
		if ob_ledge:
			own['can_climb'] = 1
			###print("Round nice RAY at pt", hit_down[2])
			# debug.setpos( hit_down )
			return hit_new, nor_new, hit_down[2]

	# Could not hit it vertically...
	# Ok we will try to find the bugger!
	# Cast multiple rays, this is not pretty
	### print("BUGGER, cant climb", ob_closer)
	own['can_climb'] = 0
	
	new_ray_pos = own_pos[:] # we only need to adjust its z value
	if ob_closer:
		# print("Closer")
		new_ray_pos_target = ray_dir_closer[:]
	else:
		# print("NotCloser")
		new_ray_pos_target = ray_dir_first[:]

	target_z = own_pos[2]-CLIMB_HANG_Z_OFFSET
	inc = 0.05 # Watch this, some numbers may cause jitter
	
	# z_ray_search_origin
	sss = z_ray_search_origin = own_pos[2]-0.2 # Tested this to be a good and correct starting location for searching the ray.
	
	z_ray_search_limit = own_pos[2]-(CLIMB_HANG_Z_OFFSET*1.8)
	
	test_ok = None # False
	i = 0
	
	# Ray cast with an increasingly higher Z origin to find the top of the ledge
	while z_ray_search_origin < z_ray_search_limit:
		i+=1
		# print(i, z_ray_search_origin, (own_pos[2]-(CLIMB_HANG_Z_OFFSET*1.8))-z_ray_search_origin)
		z_ray_search_origin += inc
		new_ray_pos[2] = new_ray_pos_target[2] = z_ray_search_origin
		
		test = own.rayCast(new_ray_pos_target, new_ray_pos, RAY_LENGTH, 'ledge') # Can hit objects of any property, MAYBE should choose ground.
		
		if test[0]:
			test_ok = test
		elif test[0]==None and test_ok: # If we have hit 
			# no hit, return the last hit
			# print("Found", i)
			'''
			crap = test_ok[1][:]
			crap[2] = z_ray_search_limit
			debug.setpos( crap )
			'''
			
			return test_ok[1], test_ok[2], z_ray_search_origin
	
	print("Missed VRAY")
	# crap = hit_first[:]
	# crap[2] = own_pos[2]-CLIMB_HANG_Z_OFFSET
	# debug.setpos( crap )
	return hit_first, nor_first, own_pos[2]-CLIMB_HANG_Z_OFFSET
