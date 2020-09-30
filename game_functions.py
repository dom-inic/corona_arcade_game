# game functions file for functions in the game  to reduce the longetivity of the game and make it easy to debug
import sys
import pygame
from bullet import Bullet
from ufo import Ufo
from time import sleep
from button import Button
# from gameover import Gameover

# gameover = Gameover(screen)

# def check_keydown_events(event,ai_settings, screen,ship, bullets):
# 	"""respond to keypresses """

# 	if event.key == pygame.K_RIGHT:
# 		# move the ship to thhe right
# 		ship.moving_right = True
# 	elif event.key == pygame.K_LEFT:
# 		# move the ship to the left
# 		ship.moving_left = True

# 	if event.key == pygame.K_ESCAPE:
# 		sys.exit()
# 	elif  event.key == pygame.K_SPACE:
# 		fire_bullet(ai_settings, screen, ship, bullets)
		

def fire_bullet(ai_settings, screen, ship, bullets):
	""" fire a bullet if limit not yet reached"""
	# create a new bullet and add it to the bullet's group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet =Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
# def check_keyup_events(event,ship):
# 	"""respond to key releases"""
# 	if event.key == pygame.K_RIGHT: 
# 		ship.moving_right = False
# 	elif event.type == pygame.K_LEFT:
# 		ship.moving_left = False



# def check_events(ai_settings,screen, ship, bullets):
# 	""" respond to keypresses and mouse events"""
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			sys.exit()
# 		elif event.type == pygame.KEYDOWN:
# 			check_keydown_events(event,ai_settings, screen,ship, bullets)

# 		elif event.type == pygame.KEYUP:
# 			check_keyup_events(event,ship)


				
def update_screen(ai_settings,screen, stats, sb, ship, startreks, bullets, play_button, restart_button, gameover_button):
	"""update images on the screen and flip to the new screen"""
	screen.fill(ai_settings.bg_color)
	# redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	ship.blitme()
	startreks.draw(screen)

	# draw the score  information
	sb.show_score()

	# Draw the play button if the game is inactive 
	if not stats.game_active:
		play_button.draw_button()

	elif stats.game_active:
		restart_button.draw_button()

	if stats.ships_left == 0:
		gameover_button.draw_button()


	# make the most recently drawn screen visible
	pygame. display.flip()
def update_bullets(ai_settings, screen,stats, sb, ship, startreks, bullets):
	""" update the position of bullets and get rid of old bullets"""
	# update the bullet's position
	bullets.update()
	# check for any bullets that have hit the startreks and get rid of the bullet and the startrek
	collisions = pygame.sprite.groupcollide(bullets, startreks, True, True)

	if collisions:
		for startreks in collisions.values():
			stats.score += ai_settings.startrek_points * len(startreks)
			sb.prep_score()
		check_high_score(stats, sb)

	# a for loop to get rid of bullets that have dissappere to avoid slowing down the game
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	if len(startreks) == 0:
		# start a new level
		# destroy existing bullets, speed up game and create new fleet
		bullets.empty()
		ai_settings.increase_speed()

		# increase level 
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, startreks)

def create_fleet(ai_settings, screen,ship, startreks):
	"""create a full fleet of startreks"""
	# create a startrek and find the number of startreks in a row
	# spacing between each startrek is equal to one ufo width
	startrek = Ufo(ai_settings, screen)
	number_startreks_x = get_number_startreks(ai_settings, startrek.rect.width )
	number_rows = get_number_rows(ai_settings, ship.rect.height, startrek.rect.height)



	# create the fleet of startreks
	for row_number in range(number_rows):
		for startrek_number in range(number_startreks_x):
		# create a startrek and place it in the row
			create_startrek(ai_settings, screen, startreks, startrek_number, row_number)




def get_number_startreks(ai_settings, startrek_width):
	""" determins the number of startreks that fit in a row."""
	available_space_x = ai_settings.screen_width -2 *startrek_width
	number_startreks_x = int(available_space_x / (2 * startrek_width))
	return number_startreks_x

def create_startrek(ai_settings, screen, startreks, startrek_number, row_number):
	"""creaye a startrek and place it in the row"""
	startrek = Ufo(ai_settings, screen)
	startrek_width = startrek.rect.width
	startrek.x = startrek_width + 2 * startrek_width * startrek_number
	startrek.rect.x = startrek.x
	startrek.rect.y = startrek.rect.height + 2 * startrek.rect.height * row_number
	startreks.add(startrek)

def get_number_rows(ai_settings, ship_height, startrek_height):
	""" determine the number of rows of startreks that fit on the screen"""
	available_space_y = (ai_settings.screen_height -
							(3 * startrek_height) - ship_height)
	number_rows = int(available_space_y / (2 * startrek_height))
	return number_rows



def check_fleet_edges(ai_settings, startreks):
	""" respond appropraitely if any alien have reached an edge"""
	for startrek in startreks.sprites():
		if startrek.check_edges():
			change_fleet_direction(ai_settings, startreks)
			break

def change_fleet_direction(ai_settings, startreks):
	""" drop the entire fleet an change the fleet's direction"""
	for startrek in startreks.sprites():
		startrek.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def  ship_hit(ai_settings, stats, screen, ship, startreks, bullets):
	""" respond to ship being hit by a starttrek"""
	if stats.ships_left > 0:

		# decrement ship_left
		stats.ships_left -= 1

		# empty the list of startreks and bullets
		startreks.empty()
		bullets.empty()

		# create a new fleet and center the ship
		create_fleet(ai_settings,screen, ship, startreks)
		ship.center_ship()

		# pause
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		


def update_startreks(ai_settings,stats, screen, ship, startreks, bullets):
	check_fleet_edges(ai_settings, startreks)
	startreks.update()

	# look for startrek and ship collisions
	if pygame.sprite.spritecollideany(ship, startreks):
		ship_hit(ai_settings, stats, screen, ship, startreks, bullets)

	check_startreks_bottom(ai_settings, stats, screen, ship, startreks, bullets)
def check_startreks_bottom(ai_settings, stats, screen, ship, startreks, bullets):
	""" checking whether any startreks have reached the bottom of the screen """
	screen_rect = screen.get_rect()
	for startrek in startreks.sprites():
		if startrek.rect.bottom >= screen_rect.bottom:
			# treat this the same as if the ship got hit
			ship_hit(ai_settings, stats, screen, ship, startreks, bullets)
			break
		
def check_play_button(ai_settings, screen, stats, sb, play_button,ship, startreks, bullets, mouse_x, mouse_y):
	""" start a new game when the player clicks play """
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# reset the game settings
		ai_settings.initialize_dynamic_settings()
		# hide the mouse cursor
		pygame.mouse.set_visible(False)
		# reset the game statistics
		stats.reset_stats()
		stats.game_active = True

		# reset the scoreboard images 
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()

		# empty the list of starttreks and bullets 
		startreks.empty()
		bullets.empty()

		# create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, startreks)
		ship.center_ship()


def check_restart_button(ai_settings, screen, stats, restart_button, ship, startreks, bullets, mouse_x, mouse_y):
	""" restart a game when the player clicks the restart button """
	if restart_button.rect.collidepoint(mouse_x, mouse_y):
		# reset the game statistics 
		stats.reset_stats()
		stats.game_active = True

		# empty the list of startreks and bullets
		startreks.empty()
		bullets.empty()

		# create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, startreks)
		ship.center_ship()

def p_keyboardplay(ai_settings, screen, stats, ship, startreks, bullets):
	stats.reset_stats()
	stats.game_active = True

	# empty the list of startreks and bullets
	startreks.empty()
	bullets.empty()

	# create a new fleet and center the ship
	create_fleet(ai_settings, screen, ship, startreks)
	ship.center_ship()

def check_high_score(stats, sb):
	""" check to see if there is a new high score """
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()







