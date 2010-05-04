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


import GameLogic

def main(cont):
	own = cont.owner
	hud_dict = GameLogic.globalDict['HUD']
	
	sens_msg = cont.sensors['health_change_msg']
	
	if not sens_msg.positive:
		return
	
	# Get all messages and update the ID's we need to.
	messages_player_ids = sens_msg.bodies

	if not messages_player_ids or len(messages_player_ids ) == 0:
		return
	
	for player_id in messages_player_ids:
		
		# The message will be an ID. 0 or 1
		id = str(int(player_id) + 1)
		
		replace_mesh = cont.actuators['replace_mesh_p' + id]
		life = min(max(hud_dict['life_p'+id], 0), 13)
		
		# each player has their own mesh
		mesh = 'life_%.2d_p%s' % (life, id)
		
		replace_mesh.mesh = mesh
		replace_mesh.instantReplaceMesh() # both work
		# cont.activate(replace_mesh)

