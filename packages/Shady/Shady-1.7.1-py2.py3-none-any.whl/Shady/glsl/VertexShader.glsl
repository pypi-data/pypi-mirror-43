/*
# $BEGIN_SHADY_LICENSE$
# 
# This file is part of the Shady project, a Python framework for
# real-time manipulation of psychophysical stimuli for vision science.
# 
# Copyright (c) 2017-2019 Jeremy Hill, Scott Mooney
# 
# Shady is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/ .
# 
# $END_SHADY_LICENSE$
*/

// Inherits GLSL version from prepended Version.glsl.

//@MODERN #define varying       out
//@MODERN #define gl_Vertex     vPosition
//@MODERN in      vec3          vPosition;

varying vec3      vFragCoordinateInEnvelope;

uniform mat4      uMatrixAnchorTranslation;
uniform mat4      uMatrixEnvelopeScaling;
uniform mat4      uMatrixEnvelopeRotation;
uniform mat4      uMatrixEnvelopeTranslation;
uniform mat4      uMatrixWorldProjection;

void main(void)
{
	vFragCoordinateInEnvelope = vec3( gl_Vertex.xy, 1.0 );
	
	gl_Position =
		uMatrixWorldProjection *
		uMatrixEnvelopeTranslation *
		uMatrixEnvelopeRotation *
		uMatrixEnvelopeScaling *
		uMatrixAnchorTranslation *
		vec4( gl_Vertex.xyz, 1.0 );
}
