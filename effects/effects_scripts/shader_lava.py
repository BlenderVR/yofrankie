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



MaterialIndexList = [0,1]
GlobalAmbient = [0.39,0.35,0.32,1]
AmbF = 0.5
# -------------------------------------

VertexShader = """
varying vec2 Texcoord;
void main( void )
{
    gl_Position = ftransform();
    Texcoord    = gl_MultiTexCoord0.xy;
    
}
"""

FragmentShader = """
uniform sampler2D Texture1;
uniform sampler2D Texture2;
uniform float time;

varying vec2 Texcoord;
void main( void )
{
vec4 noise = texture2D( Texture1,Texcoord);
vec2     T1=  Texcoord+vec2(1.5,-1.5)*time*0.02;
vec2     T2=  Texcoord+vec2(-0.15,1.0)*time*0.01;
T1.x+=(noise.x)*2.0;
T1.y+=(noise.y)*2.0;
T2.x-=(noise.y)*0.3;
T2.y+=(noise.z)*0.3;
float     p=  texture2D( Texture1,T1*3.0).a;  
vec4 color =  texture2D( Texture2, T2*3.0); 
vec4 temp= color*(vec4(p,p,p,p)*1.6)+(color*color-0.15);
if(temp.r > 1.0){temp.bg+=clamp(temp.r-2.0,0.0,100.0);}
if(temp.g > 1.0){temp.rb+=temp.g-1.0;}
if(temp.b > 1.0){temp.rg+=temp.b-1.0;}
    gl_FragColor = temp;
}
"""


def main(cont):
	# for each object
	own = cont.owner
	time = own['time'] * 3.0
	for mesh in own.meshes:
		for mat in mesh.materials:
			# regular TexFace materials do NOT have this function
			try:
				mat_index = mat.getMaterialIndex()
			except:
				return

			# find an index
			found = 0
			for i in range(len(MaterialIndexList)):
				if mat_index == MaterialIndexList[i]:
					found=1
					break
			if not found: continue

			shader = mat.getShader()
			if shader != None:
				if not shader.isValid():
					shader.setSource(VertexShader, FragmentShader,1)
				
				shader.setUniform1f('time', time)
				shader.setSampler('Texture1', 0)
				shader.setSampler('Texture2', 1)
				#shader.setSampler('det', 2)
