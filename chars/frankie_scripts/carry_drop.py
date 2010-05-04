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


# mostly copied from action_all.py, do_throw_carry() , since dropping and throwing are similar

'''
run this script if we die or drown while carrying
'''

def main(cont):
	'''
	Throw items your carrying ontop of your head
	'''
	own = cont.owner
	
	ob_parent = cont.sensors['carry_pos_linkonly'].owner
	
	try:
		own_carry = ob_parent.children[0]
	except:
		# was nothing to carry
		own['carrying'] = 0
		return
	
	own_carry.removeParent()
	own['carrying'] = 0
	own_carry['carried'] = 0
	
	# Tell the object we threw it. so we cant hurt ourselves
	if 'projectile_id' in own_carry:
		own_carry['projectile_id'] = own['id']
	
	own_y = own.getAxisVect((0.0, 2.0, 0.0))
	own_y[2] = 0.0
	own_carry.setLinearVelocity([own_y[0],own_y[1], 3.0], 0) # We are carrying sideways
	
	# Notes 
	# * set upright while in the falling with interpolation or landing.
	# * dont need to turn the carry animation off, its done via a property check.

	