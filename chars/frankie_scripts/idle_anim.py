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
Play an actuator randomly
this runs in its own state and is disabled when frankie does anything
'''
from bge import logic
import random

def main(cont):
	own = cont.owner
	
	# Positive pulse happens on entering the state,
	# In this case the timer is not set so ignore it.
	if cont.sensors['generic_true_pulse'].positive:
		return
	
	actu_list = cont.actuators
	
	i = random.randint(0, len(actu_list)-1)
	
	if i >= len(actu_list):
		i = len(actu_list) - 1 # unlikely but possible?
	
	for ii, actu in enumerate(actu_list):
		
		if ii==i:	cont.activate(actu)
		else:		cont.deactivate(actu)
		
