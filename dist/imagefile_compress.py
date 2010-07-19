#!/usr/bin/python

# --------------------------------------------------------------------------
# Imagefile compresser
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

# run this command with...
# imagefile_compress ~/somepath/blender.bin /someplace/project_tree

# Bug in blender in 2.48 where G.curscreen is left empty causing the blenderplayer to crash
# until its fixed this needs to run in forground mode
BACKGROUND = True
USE_JPEG = True

# not nice but fixes index color image being converted
EXCEPTIONS = ['font_peach.tga']

# root_dir= '/somedir'
import sys
root_dir = sys.argv[-1]
blend_bin = sys.argv[-2]

if "--nojpeg" in sys.argv:
	USE_JPEG = False

import os
import os.path
	
def fileList(path):
	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			yield os.path.join(dirpath, filename)

def isimage_noalpha(path):
	# Parse image magick output
	# Will look somthing like this
	'''
Image: textures/stone_cliff_tile_001_nor.png
  Format: PNG (Portable Network Graphics)
  Class: DirectClass
  Geometry: 1024x256+0+0
  Resolution: 28.35x28.35
  Print size: 36.1199x9.02998
  Units: PixelsPerCentimeter
  Type: TrueColorMatte
  Endianess: Undefined
  Colorspace: RGB
  Depth: 8-bit
  Channel depth:
    red: 8-bit
    green: 8-bit
    blue: 8-bit
    alpha: 1-bit
  Channel statistics:
    red:
      min: 3 (0.0117647)
      max: 252 (0.988235)
      mean: 126.877 (0.497559)
      standard deviation: 51.1924 (0.200754)
    green:
      min: 3 (0.0117647)
      max: 252 (0.988235)
      mean: 127.292 (0.499182)
      standard deviation: 49.4588 (0.193956)
    blue:
      min: 145 (0.568627)
      max: 254 (0.996078)
      mean: 219.27 (0.859882)
      standard deviation: 21.1571 (0.0829692)
    alpha:
      min: 255 (1)
      max: 255 (1)
      mean: 255 (1)
      standard deviation: 0 (0)
  Rendering intent: Saturation
  Gamma: 0.45455
  Chromaticity:
    red primary: (0.64,0.33)
    green primary: (0.3,0.6)
    blue primary: (0.15,0.06)
    white point: (0.3127,0.329)
  Interlace: None
  Background color: rgba(1,1,1,1)
  Border color: rgba(223,223,223,1)
  Matte color: grey74
  Transparent color: none
  Page geometry: 1024x256+0+0
  Dispose: Undefined
  Iterations: 0
  Compression: Zip
  Orientation: Undefined
  Properties:
    create-date: 2008-12-06T18:46:56+00:00
    modify-date: 2008-12-06T18:46:56+00:00
    signature: 000de7e23b96507141109445ad1a8208d0467bbd7c8b24ce7312b6d1f6e2e825
  Artifacts:
    verbose: true
  Tainted: False
  Filesize: 798kb
  Number pixels: 256kb

	'''
	
	lines = [l.strip() for l in os.popen('identify -verbose "%s"' % path).read().split('\n')]
	chan_ok = False
	for i,l in enumerate(lines):
		
		if l == 'alpha:':
			#print "\tFound ALPHA"
			min_str = lines[i+1] # min: 145 (0.568627)
			#print "\t\tMinSTR", min_str
			if min_str.startswith('min:'):
				if min_str.split()[1] == '255':
					return True
				else:
					return False
	
	return True

def replace_ext(path, ext):
	return '.'.join( path.split('.')[:-1] ) + ext

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
	tot_compressed= tot_images= tot_alredy_compressed= 0
	tot_blend_size= 0
	tot_blend_size_saved= 0
	for f in files:
		
		if f.split('/')[-1].split('\\')[-1] in EXCEPTIONS:
			continue
		
		f_lower= f.lower()
		if f_lower.endswith('.png') or f_lower.endswith('.tga'):
			print f,'...',
			tot_images+=1
			# allows for dirs with .blend, will just be false.
			has_no_alpha = isimage_noalpha(f)
			if has_no_alpha or not USE_JPEG:
				print 'compressing ...',
				tot_compressed+= 1
				orig_size= os.path.getsize(f)
				tot_blend_size+= orig_size

				if USE_JPEG:
					f_new = replace_ext(f, '.jpg')
					os.system('convert "%s" "%s"' % (f, f_new))
				else:
					f_new = replace_ext(f, '_temp_' + os.path.splitext(f)[1])
					if has_no_alpha:
						os.system('convert +matte -quality 100 "%s" "%s"' % (f, f_new))
					else:
						os.system('convert -quality 100 "%s" "%s"' % (f, f_new))

				new_size= os.path.getsize(f_new)

				if new_size < orig_size:
					os.system('rm "%s"' % f) # remove the uncompressed image
					tot_blend_size_saved += orig_size-new_size
					print 'saved %.2f%%' % (100-(100*(float(new_size)/orig_size)))

					if not USE_JPEG:
						os.system('mv "%s" "%s"' % (f_new, f))
					
				else:
					os.system('rm "%s"' % f_new) # jpeg image isnt smaller, remove it
					print 'no space saved, not using compressed file'

			else:
				print 'has alpha, cannot compress.'
				tot_alredy_compressed+=1
	
	print '\nTotal files:', tot_files
	print 'Total Images:', tot_images
	print 'Total Images Compressed:', tot_compressed
	print 'Total Alredy Compressed:', tot_alredy_compressed
	print '\nTotal Size in Images: %sMB' % (((tot_blend_size)/1024)/1024)
	print 'Total Saved in Images: %sMB' % (((tot_blend_size_saved)/1024)/1024)

	if USE_JPEG:
		# Now relink images
		for f in files:
			f_lower = f.lower()
			if f_lower.endswith('.blend'):
				if BACKGROUND:
					bg = '-b'
				else:
					bg = ''
				
				os.system('%s %s "%s" -P dist/imagefile_relink.py' % (blend_bin, bg, f))



if __name__=='__main__':
	main()
