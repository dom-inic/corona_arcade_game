# main file for running the game.
import sys
import pygame
# A Group class to help group the bullets
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from ufo import Ufo
import game_functions as gf
from game_stats import Gamestats, Gameover
from time import sleep
from button import Button
from scoreboard import Scoreboard
def run_game():
	# initialize game and create a screen object.
	pygame.init()
	# make an instance of the class Settings 
	ai_settings= Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("corona virus pandemic")
	# lets create an instance to stor game statistics and create a scoreboard
	stats = Gamestats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	# make a ship
	ship = Ship(ai_settings, screen)
	# make a group to store the bullets in 
	# bullets an instance of the class Group. created outside the loop to avoid repetition
	bullets = Group()
	# make a group of ufos 
	startreks = Group()

	# create the fleet of startreks
	gf.create_fleet(ai_settings, screen, ship, startreks)
	# make an instance of a ufo
	startrek= Ufo(ai_settings, screen)
	# start the mainloop for the game.
	#  lets create an instance of gameover 
	gameover = Gameover(screen)
	# creatign an instance of the class button for the play button
	play_button = Button(ai_settings, screen, "Play", 0 , 0)

	# creating a restart button 
	restart_button = Button(ai_settings, screen, "Restart", 800, 0)

	# gameover button to be displayed when the player runs out ships
	gameover_button = Button(ai_settings, screen, "Gameover", 200, 0)

	class Backround(pygame.sprite.Sprite):
		"""a Background class for the background image of the game"""
		def __init__(self, image_file, location):
			# call the sprite initializer
			pygame.sprite.Sprite.__init__(self) 
			self.image = pygame.image.load(image_file)
			self.rect = self.image.get_rect()
			self.rect.left, self.rect.top = location

	background = Backround('images/background.bmp', [0,0])

	screen.fill([255, 255, 255])
	screen.blit(background.image, background.rect)

	# boolean for quiting the game and setting the while loop to true
	running = True
			
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				if event.key == pygame.K_RIGHT:
					ship.moving_right = True

				if event.key == pygame.K_LEFT:
					ship.moving_left = True
				if event.key == pygame.K_SPACE:
					gf.fire_bullet(ai_settings, screen, ship, bullets)
				if event.key == pygame.K_p and  K_BACKSPACE:
					gf.p_keyboardplay(ai_settings, screen, stats, ship, startreks, bullets)
				# if event.key== pygame.K_BACKSPACE:
				# 	sleep(2)
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					ship.moving_right = False

				if event.key == pygame.K_LEFT:
					ship.moving_left = False

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				gf.check_play_button(ai_settings, screen, stats,sb,  play_button,ship, startreks, bullets, mouse_x, mouse_y)
				gf.check_restart_button(ai_settings, screen, stats, restart_button, ship, startreks, bullets, mouse_x, mouse_y)

		# keyboard and mouse events
		# gf.check_events(ai_settings ,screen,ship, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, startreks, bullets)
			gf.update_startreks(ai_settings,stats, screen, ship, startreks, bullets)

		gf.update_screen(ai_settings,screen,stats,sb ,ship, startreks, bullets, play_button, restart_button, gameover_button)

	


run_game()



