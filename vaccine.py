import pygame
# class Sprite from pygame to help group related elements and act on all the grouped elements at once
from pygame.sprite import Sprite

class Bullet(Sprite):
	""" a class to manage bullets shot from the ship"""

	def __init__(self,ai_settings, screen, ship):
		""" create an instance of bullet at the ship'c curren position."""
		# super function to inherit properly from the Sprite class
		super(Bullet, self).__init__()
		self.screen = screen

		# create a bullet rect at cordinates (0, 0) and then set current position
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		# store the bullet's position using a decimal value instead of an int
		self.y = float(self.rect.y)

		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor

	def update(self):
		""" move the bullets up the screen."""
		# update the decimal position of the bullet
		self.y -= self.speed_factor
		# update the rect position
		self.rect.y = self.y

	def draw_bullet(self):
		""" draw the bullet to the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)