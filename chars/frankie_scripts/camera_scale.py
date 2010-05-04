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
Scale the cameras parent when there is an object infront of the camera
'''

def main(cont):
	MAX = 4.0
	MIN = 0.6
	THRESH = 0.6 # Ignore anything under this distance, frankie is probably carrying somthing.
	
	own = cont.owner
	
	# For sone annoying reason this happens when the scene is initialized
	sens_wall = cont.sensors['camera_ray']
	
	ob = sens_wall.hitObject
	#if ob:	print('\tcamera: rayhit object -', ob.name)
	
	sorig = own.localScale[0] # assume uniform scale
	
	if not ob:
		scale = MAX # 1.0
	else:
		
		carry_obstructor = False
		# incase we are carrying an object, see if its logic 
		parent = ob.parent
		while parent:
			ob = parent
			parent = ob.parent
			
			if ob.get('carried', 0) != 0:
				carry_obstructor = True
				break
		
		if carry_obstructor:
			scale = MAX # this is not quite correct, we should really shoot another ray incase there is an obstructor
		else:
			scale = own.getDistanceTo(sens_wall.hitPosition)
			
			if scale < THRESH: scale = sorig
			elif scale > MAX: scale = MAX
			elif scale < MIN: scale = MIN
	
	# Let slow parent deal with interpolation
	own.localScale = [scale,scale,scale]

