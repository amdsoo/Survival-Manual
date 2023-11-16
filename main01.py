# Ariel Morandy -  python! Fev 2023
import declaration as d
from declaration import *
import pygame
import classes as c
import userinterface as ui
import simulation as simu
import random

file = open('savefolder/statistic.txt', 'wt')

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Survival ML')

# basic font for Large Text
my_font = pygame.font.SysFont('Comic Sans MS', 30)
# small font for user typed
my_font_S = pygame.font.SysFont('Comic Sans MS', 12)

# show a long message
display_long_message = False
long_message = ""

# list to manage button activity
button_list = []

# create the main Objects
world  = c.World()
grid   = c.Grid()
game   = c.Game()

# create randomly plants
i=1
while i < number_plants:
	x = random.randint (tile_size,screen_width-2*tile_size)
	y = random.randint (2*tile_size, screen_height-2*tile_size)
	energy_reserve =  random.randint (175,300)
	plant= c.Plant (x,y,0)
	plant.energy_reserve = energy_reserve
	d.plant_list.append(plant)
	d.all_sprites_plant_list.add(plant)
	i+=1


# main creation of buttons
ui.menu_create(button_list)


# simulation and delete are independant
button_simulation = ui.Button("Simulation", 9 * tile_size, screen_height - tile_size)
button_delete = ui.Button("Delete", 10 * tile_size, screen_height - tile_size)
button_save = ui.Button("save", 11 * tile_size, screen_height - tile_size)
button_open = ui.Button("open", 12 * tile_size, screen_height - tile_size)

# game loop
inwork_mode = False
tmp_object = None
tmp_object_angle = 0
placement_type = ""


run = True
while run:
	clock.tick(60)

	for event in pygame.event.get():

		Mouse_x, Mouse_y = pygame.mouse.get_pos()

		# we show the properties in the lower right corner
		long_message = game.get_info()
		display_long_message = True


		if event.type == pygame.QUIT:
			run = False


		if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
			game.mode = "Priority Wait"
		if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
			game.mode = "Priority Move"
		if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
			game.mode = "Priority Eat"
		if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
			game.mode = "Priority Reproduce"


		if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
			print("Screen coord   = ", Mouse_x, Mouse_y)

			placement_type = ""
			button_simulation.click()
			button_delete.click()
			button_save.click()
			button_open.click()



			if button_delete.state == "pressed" or button_save.state == "pressed" or button_open.state == "pressed":
				placement_type = ""

			# check all the buttons from button list, if something is clicked, deactivate all
			placement_type = ui.menu_state_from_event(button_list)

			if placement_type != "":
				button_delete.state = "depressed"
				button_save.state = "depressed"
				button_open.state = "depressed"

		if button_save.state == "pressed":
			game.save_game ()
			button_save.state = "depressed"

		if button_open.state == "pressed":
			game.open_game ()
			button_open.state = "depressed"


		if placement_type != "":

			# a temporary object is created on left click if its button is active.
			if not inwork_mode:

				# creation of object based on category selected from the active button
				object_class = ui.menu_selection_frombutton(button_list)

				if object_class != "":

					if isinstance(tmp_object, c.Animal):
						tmp_object_angle = random.randint(0, 360)
					else:
						tmp_object_angle =0

					tmp_object = eval("c." + object_class)(Mouse_x, Mouse_y, tmp_object_angle)

				print("Object of class" + object_class + "is created in tmp", tmp_object)
				all_sprites_tmp.add(tmp_object)
				inwork_mode = True
				event.button = None

			# the temporary object moves with the mouse
			if inwork_mode:

				tmp_object.rect.x = Mouse_x
				tmp_object.rect.y = Mouse_y


				if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and \
				    tile_size < Mouse_y < (screen_height - tile_size) :

					print ("we enter the creation of " , tmp_object)

					# in Screen coordinates
					tmp_object.rect.x = Mouse_x
					tmp_object.rect.y = Mouse_y
					tmp_object.x = Mouse_x
					tmp_object.y = Mouse_y

					pygame.sprite.Sprite.kill(tmp_object)

					if isinstance(tmp_object,c.Animal):
						d.animal_list.append(tmp_object)
						d.all_sprites_animal_list.add(tmp_object)
					else:
						d.plant_list.append(tmp_object)
						d.all_sprites_plant_list.add(tmp_object)


					# we remove the sprite from the tmp group

					inwork_mode = False


		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			print("Escape button used")
			# delete the temporary object, remove the sprite
			if tmp_object is not None:
				pygame.sprite.Sprite.kill(tmp_object)
				tmp_object = None
			inwork_mode = False
			ui.menu_reset(button_list)
			button_delete.state = "depressed"
			button_save.state   = "depressed"
			button_open.state   = "depressed"
			placement_type      = ""


	# initialisation of world , with machines
	screen.fill(GREY)
	world.draw(screen)
	grid.draw(screen)
	game.draw(screen)


	game.draw_msg(screen,long_message)

	for button in button_list:
		button.draw(screen)

	d.all_sprites_plant_list.draw(screen)
	d.all_sprites_animal_list.draw(screen)


	d.all_sprites_animal_list.update()
	d.all_sprites_plant_list.update()
	all_sprites_tmp.draw(screen)

	button_simulation.draw(screen)
	button_delete.draw(screen)
	button_save.draw(screen)
	button_open.draw(screen)

	nb_prey     =0
	nb_predator =0
	prey_max_gen = game.prey_max_gen
	predator_max_gen = game.predator_max_gen

	for animal in d.animal_list:
		animal.draw_vision_line(screen)
		if isinstance(animal, c.Prey):
			nb_prey +=1
			prey_max_gen = max(game.prey_max_gen,animal.generation)
		else:
			nb_predator +=1
			predator_max_gen = max(game.predator_max_gen, animal.generation)
	game.nb_prey     = nb_prey
	game.nb_predator = nb_predator
	game.prey_max_gen = prey_max_gen
	game.predator_max_gen = predator_max_gen

	if button_simulation.state == "pressed":
		if game.iteration_index == game.iteration:
			simu.gameupdate(game)
			game.cycle = game.cycle + 1
			game.iteration_index = 0
			msg= 'cycle'+ "," + str(game.cycle)+ "," +str(game.nb_prey) +"," +str(game.nb_predator) + "\n"
			file.write (msg)
		game.iteration_index = game.iteration_index + 1

	pygame.display.update()


pygame.quit()
