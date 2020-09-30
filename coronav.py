import pygame 
from pygame.sprite import Sprite

# a class ufo to represent a single ufo to create the instance of ufo
# we inherit the class sprite to help us create a group of ufos 

class Ufo(Sprite):
	""" a class to represent a single ufo in the fleet"""

	def __init__(self, ai_settings, screen):
		""" initialize the ufo and set its starting position"""
		# a super function to inherit properly from the Sprite class
		super(Ufo, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# load the ufo image and set its rect attribute
		self.image = pygame.image.load('assets/images/covid50.BMP')
		self.rect = self.image.get_rect()

		# start each new ufo near the top left of the screen 
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# store the ufo's exact position using a decimal value
		self.x = float(self.rect.x)

	def blitme(self):
		""" blitme method to draw the ufo's position at its current location"""
		self.screen.blit(self.image, self.rect)

	def update(self):
		""" move the startrek to the right or left"""
		self.x += (self.ai_settings.startrek_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x

	def check_edges(self):
		""" return true if a startrek hits the edge of the screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <=0:
			return True

