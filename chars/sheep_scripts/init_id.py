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


from bge import logic

def main(cont):
	# Give the sheep a unique ID
	try:
		ID = logic.ID = logic.ID + 1
	except:
		ID = logic.ID = 0
	
	own = cont.owner
	# For respawning.
	own['x_orig'], own['y_orig'], own['z_orig'] = own.worldPosition
	own['id'] = ID
	# print("setting ID", ID


	# Warning!!! This only works when inside dupliGroups
	#   since objects in hidden layers will still show up as a sensor.

	# Assign dummy value
	own['own_rig'] = 0
	for ob in own.children:
		name = ob.name[2:]
		
		if 'rig_ram' in name:
			own['type'] = 'ram'
			del own['carried'], own['projectile'], own['kickable']
			break
		elif 'rig_sheep' in name:
			own['type'] = 'shp'
			break
		elif 'rig_rat' in name:
			own['type'] = 'rat'
			#del own.carried
			break
		
		# Theres an an odd bug with flawsh_death object adder
		# set the object by name and it should help
		# This should not be needed
		'''
		actu = cont.actuators['create_poof']
		actu.object = 'flash_death'
		'''
	
	cont.activate('default_state')
