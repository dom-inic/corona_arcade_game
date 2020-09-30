import pygame.font

class Button():
	"""button class """
	def __init__(self, ai_settings, screen, msg, posx, posy):
		""" initialize button attributes"""
		self.screen = screen
		self.posx = posx
		self.posy = posy
		self.screen_rect = screen.get_rect()


		# set the dimensions and properties of the button
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# Build the button's rect object and center it 
		self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)

		# the button message needs to be prepped only once 
		self.prep_msg(msg)

	def prep_msg(self, msg):
		""" turn msg into a rendered image and center text on the button"""
		self.msg_image= self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center


	def draw_button(self):
		""" draw button method that we can call to display the button onscreen"""
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
		
