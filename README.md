# SurvivalAMD
This game is to observe how predators adopts strategy to eat prey. 
There are three objects
  a/ Plants who grow, die and reborn every X iterations , they hold calories 
  b/ Prey who are not smart, they randomly move and eat plant if they meet them, Prey die if no food, or too old, or eaten by predators
  c/Predators : they can see thru a cone of vision, move or not, and eat or not preys. They reproduce if enough energy, and die if no more energy 

#Edit declaration.py
  - number_plants = 200 , this is the original number of plants on the grid 

#Edit classes.py
/for predators
self.vision_angle = 20,
self.vision_distance = 200,
self.speed = 3,
		self.direction_change_angle = 20,
		self.energy_reserve_max = 1500,
		self.energy_reserve = 600,
		self.energy_reproduction= 1200,
		self.energy_reproduction_cost= 400,
		self.energy_per_move  = 30,
		self.energy_per_cycle = 2,
/for prey
		self.vision_angle = 180
		self.vision_distance = 150
		self.speed = 2
		self.direction_change_angle = 35
		self.energy_reserve_max = 1000
		self.energy_reserve = 700
		self.energy_reproduction= 800
		self.energy_reproduction_cost= 400
		self.energy_per_move  = 5
		self.energy_per_cycle = 1
/for plant
		self.energy_reserve_max = 300
		self.energy_reserve = 300
		self.energy_per_cycle = 1
		self.regeneration_time= 25
		self.regeneration_step= 0

  # run main01() to launch the game 
  1/Place more plants, preys and Predators 
  2/Hit the Simulation and observe 
  3/You can save and reload a particular game you like
