# Ariel Morandy - Fev 2023
import declaration as d
from declaration import *
import classes as c
import random
import method as m
import pygame

# Overall algo


# Prey reproduce
# Predator reproduce
# Plant reproduce

# Prey eat Plant
# Predators eat Prey

# Prey move
# Predator move

# Energy consumption for everyone &  Death for everyone if no energy


def gameupdate(game):

	newanimal_list = []

	for animal in d.animal_list:

		# step 1: Reproduction
		go = True
		if isinstance(animal, c.Prey):
			# Most important, animal tries to reproduce
			if animal.energy_reserve > animal.energy_reproduction:
				#generation of an animal.
				x, y = animal.rect.centerx+random.randint(-tile_size,tile_size),animal.rect.centery+random.randint(-tile_size,tile_size)
				newanimal = c.Prey (x,y,random.randint(0,360))
				# cost for reproduction.
				animal.energy_reserve = animal.energy_reserve - animal.energy_reproduction_cost
				# we add to the list of new animal
				newanimal_list.append(newanimal)
				newanimal.generation = animal.generation + 1
				go = False
				animal.move = False

		elif isinstance(animal, c.Predator) and game.mode == "Priority Reproduce":
			if animal.energy_reserve > animal.energy_reproduction:
				print ("Predator Reproducing")
				#generation of an animal.
				x, y = animal.rect.centerx+random.randint(-tile_size,tile_size),animal.rect.centery+random.randint(-tile_size,tile_size)
				newanimal = c.Predator(x,y,random.randint(0,360))
				# cost for reproduction.
				animal.energy_reserve = animal.energy_reserve - animal.energy_reproduction_cost
				# we add to the list of new animal
				newanimal_list.append(newanimal)
				newanimal.generation = animal.generation + 1
				go = False
				animal.move = False

		# step 2: Food
		if go:
			#check if the animal can eat within a circle <= tilesize
			# Predator --> Prey
			# Prey --> Plant
			lunch = False
			lunch,food = m.capture_food (animal)

			if (isinstance(animal, c.Prey) and lunch) or (isinstance(animal, c.Predator) and lunch and game.mode == "Priority Eat"):

				# the animal is eating
				animal.move = False
				animal.state = "Eating"
				print("Animal Eating")
				animal.energy_reserve = animal.energy_reserve + food.energy_reserve

				# we kill the Plant or the Prey
				food.energy_reserve = 0

				go = False

				if animal.energy_reserve > animal.energy_reserve_max:
					animal.energy_reserve = animal.energy_reserve_max

		# step 3: Move
		# if the animal has finished its step we recompute a direction
		if  animal.move is False and animal.state =="Hunting" :
			#if Predator has locked the prey, we don't change direction
			if isinstance(animal,c.Predator) and animal.vision_lock:
				print ("Predator hunting")
			else:
				# we recompute an angle, randomly.
				angle = random.randint(animal.angle -animal.direction_change_angle, animal.angle+ animal.direction_change_angle)
				angle = angle % 360
				animal.angle = angle
				animal.rotate()

		if isinstance(animal, c.Prey) or ((isinstance(animal, c.Predator) and (game.mode == "Priority Move" or game.mode == "Priority Eat" or game.mode == "Priority Reproduce"))):
			animal.move = True

	# cleaning up for Plant and Aninal
	for plant in d.plant_list:
		plant.energy_reserve = plant.energy_reserve -plant.energy_per_cycle

		if plant.energy_reserve <0 and plant.state == "Alive":
			plant.update()
			plant.state = "Dead"

		if plant.state == "Dead":
			plant.regeneration_step = plant.regeneration_step + 1

			if plant.regeneration_step == plant.regeneration_time:
				plant.state = "Alive"
				plant.regeneration_step = 0
				plant.energy_reserve = plant.energy_reserve_max
				plant.update()


	for animal in d.animal_list:

		# each animal loses energy
		animal.energy_reserve = animal.energy_reserve -animal.energy_per_cycle

		# and more if it moves
		if animal.move:
			animal.energy_reserve = animal.energy_reserve - animal.energy_per_move

		# and dies if no energy
		if animal.energy_reserve <0 :
			print("Animal died")
			d.animal_list.remove(animal)
			pygame.sprite.Sprite.kill(animal)

		if animal.state == "Eating":
			animal.state = "Hunting"
			animal.move = False

	#adding newanimal in the regular list.
	for newanimal in newanimal_list:
		d.animal_list.append(newanimal)
		d.all_sprites_animal_list.add(newanimal)
		newanimal.state = "Hunting"
		newanimal.move = False

	newanimal_list.clear()





