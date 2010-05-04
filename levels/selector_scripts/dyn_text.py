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



def main(cont):
	own = cont.owner
	text = own.parent['portal_blend']
	
	if 'level_selector' in text:
		own['Text'] = 'extra levels'
		return
	
	# only needed for the other level selctor
	# text = text.replace('minilevel_', '')
	
	# Nice formatting from filename 
	text = text.split('.')[0].lower() # remove extension
	
	# remove un-needed text
	for c in ('-', '_', '/', 'minilevel'):
		text = text.replace(c, ' ')
	
	text = ' '.join(text.split())
	
	# Capitalize first letters
	# ...Secodn thaughts, lets not, our upper case
	#    letters are crap
	'''
	text_split = text.split()
	for i, word in enumerate(text_split):
		text_split[i] = word[:1].upper() + word[1:]
	
	text = ' '.join(text_split)
	'''
	
	own['Text'] = text
