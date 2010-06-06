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


# import frank_ledge_module
from bge import logic
from mathutils import Vector, Matrix, RotationMatrix
from ledge_test import frankTestLedge, CLIMB_HANG_Y_OFFSET, CLIMB_HANG_Z_OFFSET

def do_reset_timeofs(cont):
	own_rig = cont.sensors['rig_linkonly'].owner # The rig owns this! - cheating way ti get the rig/
	own_rig.timeOffset = own_rig['defTimeOffset']


def do_fall_state(own, cont):
	cont.activate('fall_state')
	own.setLinearVelocity((0.0, 0.0, 2.0))
	own['ledge_regrip_timer'] = 0.0
	do_reset_timeofs(cont)


def main(cont):
	
	HANG_COUNTER_GRAVITY = 0.17
	# HANG_TIMEOFFSET = 20.0
	
	own = cont.owner
		
	# 3rd arg gets a corrected ray when its thr first ray for the state
	# This can only run the first time otherwise it makes shimmy jitter baddly.
	#	since correcting the axis can rotate frankie back and fourth.
	if cont.sensors['true_init_pulse_ledge'].positive:
		ledge_hit, ledge_nor, zpos = frankTestLedge(own, cont, None, False)
	else:
		
		# Drop on purpose
		sens_keyDown = cont.sensors['key_down']
		if sens_keyDown.positive and sens_keyDown.triggered:
			do_fall_state(own, cont)
			return
		
		
		ledge_hit, ledge_nor, zpos = frankTestLedge(own, cont, None, True)
		
		# set the timeoffset so hanging gets nice smooth movement for free.
		# cont.sensors['rig_linkonly'].owner.timeOffset = HANG_TIMEOFFSET
	
	if not ledge_hit:
		do_fall_state(own, cont)
		return
	
	sens_up = cont.sensors['key_up']
	if sens_up.positive and sens_up.triggered and own['can_climb']:
		# own.suspendDynamics()
		do_reset_timeofs(cont)
		cont.activate('climb_state')
		return
	
	own.setLinearVelocity((0.0, 0.0, HANG_COUNTER_GRAVITY))
	
	# Make sure frankie is upright. especially if he was just gliding this can happen!
	own.alignAxisToVect((0.0, 0.0, 1.0), 2)
	
	# We need to do somthing a bit extra tricky here, move the position of frankie around the ray intersect pivot,
	# This avoids jittering
	new_dir = Vector([-ledge_nor[0], -ledge_nor[1], 0.0])
	new_z = zpos + CLIMB_HANG_Z_OFFSET
	own_y = Vector( own.getAxisVect((0.0, 1.0, 0.0)) )
	ledge_hit = Vector(ledge_hit)
	cross =own_y.cross(new_dir)
	ang = own_y.angle(new_dir)
	
	# Set Frankies distance from the hit position
	
	if ang > 0.0001:
		if cross.z < 0:
			ang = -ang
		
		pos_orig = Vector(own.worldPosition)
		####pos_new = ((pos_orig-ledge_hit) * rot) + ledge_hit
		# Do this instead.

		d = (pos_orig-ledge_hit)
		d.z = 0.0
		d.length = -CLIMB_HANG_Y_OFFSET

		pos_new = (d*RotationMatrix(ang, 3, 'Z')) + ledge_hit
		
	else:
		# Simple but not good enough
		# own.localPosition = (pos_orig-ledge_hit) + ledge_hit

		# Location, use CLIMB_HANG_Y_OFFSET to offset ourselves from the ledges hit point
		d = Vector(ledge_nor)
		d.z = 0.0
		d.length = -CLIMB_HANG_Y_OFFSET
		pos_new = d + ledge_hit
	
	own.alignAxisToVect([-ledge_nor[0], -ledge_nor[1], 0.0], 1)
	pos_new.z = new_z
	own.localPosition = pos_new
	
