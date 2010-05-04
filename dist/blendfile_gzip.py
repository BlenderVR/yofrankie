#!/usr/bin/python

# --------------------------------------------------------------------------
# Blendfile compresser
# --------------------------------------------------------------------------

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

# root_dir= '/somedir'
import sys
root_dir = sys.argv[-1]

import os
import os.path

def isblend_nogz(path):
	try:
		f= open(path, 'r')
		is_blend= f.read(7) == 'BLENDER'
		f.close()
		return is_blend
		
	except:
		return False
	
def fileList(path):
	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			yield os.path.join(dirpath, filename)

def main():
	
	if not os.path.isdir(root_dir):
		print 'Expected a dir to search for blendfiles as a final arg. aborting.'
		return
	
	print 'Searching "%s"...' % root_dir
	files= [f for f in fileList(root_dir)]
	files.sort()
	print 'done.'
	#print files
	tot_files= len(files)
	tot_compressed= tot_blends= tot_alredy_compressed= 0
	tot_blend_size= 0
	tot_blend_size_saved= 0
	for f in files:
		if len(f) >= 6: # .blend is 6 chars
			f_lower= f.lower()
			if f_lower.endswith('.blend') or\
			f_lower[:-1].endswith('.blend') or\
			f_lower[:-2].endswith('.blend'): # .blend10 +
				
				print f,'...',
				tot_blends+=1
				# allows for dirs with .blend, will just be false.
				if isblend_nogz(f):
					print 'compressing ...',
					tot_compressed+= 1
					orig_size= os.path.getsize(f)
					tot_blend_size+= orig_size
					os.system('gzip --best "%s"' % f)
					os.system('mv "%s.gz" "%s"' % (f,f)) # rename the gz file to the original.
					new_size= os.path.getsize(f)
					tot_blend_size_saved += orig_size-new_size
					print 'saved %.2f%%' % (100-(100*(float(new_size)/orig_size)))
				else:
					print 'alredy compressed.'
					tot_alredy_compressed+=1
					
	
	print '\nTotal files:', tot_files
	print 'Total Blend:', tot_blends
	print 'Total Blend Compressed:', tot_compressed
	print 'Total Alredy Compressed:', tot_alredy_compressed
	print '\nTotal Size in Blends: %sMB' % (((tot_blend_size)/1024)/1024)
	print 'Total Saved in Blends: %sMB' % (((tot_blend_size_saved)/1024)/1024)

if __name__=='__main__':
	main()
