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

import sys
import math
import enum

from PnmPicture import PnmPicture
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class MouseButton(enum.IntEnum):
	LeftButton = 0
	MiddleButton = 1
	RightButton = 2
	WheelUp = 3
	WheelDown = 4

class MouseButtonAction(enum.IntEnum):
	ButtonDown = 0
	ButtonUp = 1

class GlutApplication(object):
	def __init__(self, window_title = "Unnamed Window", initial_size = (640, 480), initial_pos = (200, 200)):
		(self._width, self._height) = initial_size

		glutInit(1, "None")
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE)
		glEnable(GL_MULTISAMPLE)
		glutInitWindowSize(self.width, self.height)
		glutInitWindowPosition(*initial_pos)

		window = glutCreateWindow(window_title.encode("latin1"))

		glutDisplayFunc(self._draw_gl_scene)
		glutIdleFunc(self._idle)
		glutKeyboardFunc(self._gl_keyboard)
		glutMouseFunc(self._gl_mouse_raw)
		glutMotionFunc(self._gl_motion)
		glutReshapeFunc(self._gl_reshape)
		self._init_gl(*initial_size)

	@property
	def width(self):
		return self._width

	@property
	def height(self):
		return self._height

	def run(self):
		glutMainLoop()

	def _draw_gl_scene(self):
		pass

	def _idle(self):
		pass

	def _gl_keyboard(self, key, pos_x, pos_y):
		pass

	def _gl_mouse(self, mouse_button, mouse_button_action, pos_x, pos_y):
		pass

	def _gl_mouse_raw(self, mouse_button, mouse_button_action, pos_x, pos_y):
		mouse_button = MouseButton(mouse_button)
		mouse_button_action = MouseButtonAction(mouse_button_action)
		return self._gl_mouse(mouse_button, mouse_button_action, pos_x, pos_y)

	def _gl_motion(self, pos_x, pos_y):
		pass

	def _gl_reshape(self, new_width, new_height):
		self._width = new_width
		self._height = new_height
		self._draw_gl_scene()

	def _init_gl(self, width, height):
		glClearColor(1.0, 1.0, 1.0, 0.0)
		glClearDepth(1.0)
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glShadeModel(GL_SMOOTH)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0, width / height, 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)

	def load_texture_2d(self, pnm_image):
		pnm = PnmPicture().readfile(pnm_image)
		texture_id = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture_id)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, pnm.width, pnm.height, 0, GL_RGB, GL_UNSIGNED_BYTE, pnm.data)
		return texture_id
