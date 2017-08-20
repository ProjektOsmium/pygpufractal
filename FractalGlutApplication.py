#!/usr/bin/python3
#       pygpufractal - Fractal computation on GPU using GLSL.
#       Copyright (C) 2017-2017 Johannes Bauer
#
#       This file is part of pygpufractal.
#
#       pygpufractal is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; this program is ONLY licensed under
#       version 3 of the License, later versions are explicitly excluded.
#
#       pygpufractal is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with pygpufractal; if not, write to the Free Software
#       Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#       Johannes Bauer <JohannesBauer@gmx.de>

from GlutApplication import GlutApplication
from GLFragmentShader import GLFragmentShaderProgram
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from ColorMixer import ColorMixer

class MandelbrotFragmentShaderProgram(GLFragmentShaderProgram):
	def __init__(self):
		GLFragmentShaderProgram.__init__(self, """\
		uniform sampler1D tex;
		uniform vec2 center, size;
		uniform int max_iterations;
		uniform float cutoff;

		void main() {
			vec2 c;
			c.x = center.x + (size.x * (gl_TexCoord[0].x - 0.5));
			c.y = center.y + (size.y * (gl_TexCoord[0].y - 0.5));

			int iteration;
			vec2 z = c;
			for (iteration = 0; iteration < max_iterations; iteration++) {
				float x = (z.x * z.x - z.y * z.y) + c.x;
				float y = (z.y * z.x + z.x * z.y) + c.y;

				float abs_value = x * x + y * y;
				if (abs_value > cutoff) {
					break;
				}
				z.x = x;
				z.y = y;
			}

			float flt_iteration = iteration / float(max_iterations - 1);
			gl_FragColor = texture1D(tex, flt_iteration);
		}
		""")

class FractalGlutApplication(GlutApplication):
	def __init__(self):
		GlutApplication.__init__(self, window_title = "Python Fractals")
#		self._lut_texture = self.load_texture_2d("texture.pnm")
#		self._lut_texture = self.create_texture_1d_rgb(b"aaabbbcccdddeeefffggghhhiii")
		self._lut_texture = self._create_gradient_texture("rainbow", 256)
		self._shader_pgm = MandelbrotFragmentShaderProgram()
		self._center = (-0.4, 0)
		self._zoom = 1 / 250
		self._max_iterations = 20
		self._cutoff = 10.0;

	def _create_gradient_texture(self, palette, data_points):
		data = bytearray()
		color_mixer = ColorMixer(palette)
		for i in range(data_points):
			pixel = color_mixer[i / (data_points - 1)]
			data += bytes(pixel)
		return self.create_texture_1d_rgb(data)

	def _gl_keyboard(self, key, pos_x, pos_y):
		if key == b"\x1b":
			sys.exit(0)

	def _draw_gl_scene(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glViewport(0, 0, self.width, self.height)
		glClearDepth(1)
		glClearColor(0, 0, 0, 0)
		glClear(GL_COLOR_BUFFER_BIT)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, 1, 0, 1, -1, 1)

		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity()

		glUseProgram(self._shader_pgm.program)
		self._shader_pgm.set_uniform("center", self._center)
		size = (self.width * self._zoom, self.height * self._zoom)
		self._shader_pgm.set_uniform("size", size)
		self._shader_pgm.set_uniform("max_iterations", self._max_iterations)
		self._shader_pgm.set_uniform("cutoff", self._cutoff)
		glBindTexture(GL_TEXTURE_1D, self._lut_texture)
		glEnable(GL_TEXTURE_1D)
		glBegin(GL_QUADS)
		glTexCoord2f(-1, -1)
		glVertex2f(-1, -1)
		glTexCoord2f(1, -1)
		glVertex2f(1, -1)
		glTexCoord2f(1, 1)
		glVertex2f(1, 1)
		glTexCoord2f(-1, 1)
		glVertex2f(-1, 1)
		glEnd()

		glutSwapBuffers()
