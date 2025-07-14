#phisics egnine
import math
import pygame



g=9.8*64
class projectile:
	def __init__(self,coords: tuple,speed: float,angle: float,t: float):
		if not all(isinstance(i, (int, float)) for i in coords):
			raise TypeError("All coordinates must be int or float")
		self.x0,self.y0=coords
		if not isinstance(speed, (int, float)):
			raise TypeError("speed must be int or float")
		self.speed=speed
		if not isinstance(angle, (int, float)):
			raise TypeError("angle must be int or float")
		self.angle=math.radians(angle)
		if not isinstance(t, (int, float)):
			raise TypeError("Starting time must be int or float")
		self.t=t

		self.pos = (self.x0, self.y0)  # current position

	def traj(self):
		x = self.x0 + self.speed * math.cos(self.angle) * self.t
		y = self.y0 + self.speed * math.sin(self.angle) * self.t + 0.5 * g * self.t**2
		return x, y

	def update(self, dt):
		self.t += dt
		self.pos = self.traj()  # update current position
	def position_at(self, t):
		x = self.x0 + self.speed * math.cos(self.angle) * t
		y = self.y0 + self.speed * math.sin(self.angle) * t + 0.5 * g * t**2
		return x, y
