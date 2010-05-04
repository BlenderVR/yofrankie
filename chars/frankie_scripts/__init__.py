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


# All frankies scripts

# Initialize game stuff, on the MainCam object
import init
# on the Camera_Scaler object
import camera_scale


# Run, State 3
import run_speed
import run_wall

# Fall, State 4
import fall
import fall_bounce

# Ledge grab, used in multiple states
import ledge_collide
import ledge_hang
# import ledge_test <- used by modules above

# Carry, State 11
import carry_drop

# Health and stats, State 15
import stat_health
import stat_hit
import stat_pickup
import stat_portal
import stat_ground_pos

# Action State 16
import action_all
import action_carry
import action_ground_test

# Others
import idle_anim		# state 8
import glide			# state 19
import respawn			# state 26
import drown_revive	# state 28
