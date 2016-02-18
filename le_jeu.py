#!/usr/bin/python

import sys, os, random, math

import pygame
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

SCREENSIZE  = (3840,2160)

SCREEN = pygame.display.set_mode(SCREENSIZE,FULLSCREEN)


#la_souris_flipped   = pygame.image.load("SuperSourisSmall.png").convert_alpha()
#la_souris_flipped   = pygame.transform.flip(la_souris_flipped, 1, 0)
#la_souris_mask   = pygame.mask.from_surface(la_souris)
#la_souris_mask   = pygame.mask.from_surface(la_souris)
#le_fond   = pygame.image.load("data/le_fond.png").convert()
#le_fond   = pygame.transform.scale(le_fond,(SCREENSIZE[0],SCREENSIZE[1]))
#la_motte  = pygame.image.load("data/la_motte.png").convert_alpha()
#la_motte  = pygame.transform.scale(la_motte,(SCREENSIZE[0]/2,SCREENSIZE[1]/2))

class Un_Objet(pygame.sprite.Sprite):
	#image = None
	mask = None
	son = None
	state = ""

	def __init__(self, name, ratio):
		pygame.sprite.Sprite.__init__(self, self.containers)

		self.image = pygame.image.load("data/"+name+".png").convert_alpha()
		if ratio > 0:
			self.image = pygame.transform.scale(self.image,(self.image.get_width()/ratio,self.image.get_height()/ratio))
		else:
			self.image = pygame.transform.scale(self.image,(SCREENSIZE[0],SCREENSIZE[1]))
		self.rect  = self.image.get_rect()
		self.mask  = pygame.mask.from_surface(self.image)
		self.son   = [ pygame.mixer.Sound("data/"+name+"1.wav"), pygame.mixer.Sound("data/"+name+"2.wav") ]
		self.screen = SCREEN
		self.x = random.randint(0, SCREENSIZE[0]  - self.image.get_width())
		self.y = random.randint(0, SCREENSIZE[1]  - self.image.get_height())
		self.dx = random.randint(0, 20)
		self.dy = random.randint(0, 20)
		self.state = "RUN"
	
	def update(self):
		#control flow     
		if self.state == "QUIT":
			pygame.quit();sys.exit()
		self.event_loop()
		self.update_position()
		pygame.event.pump()



class Souris( Un_Objet ):
	
	start_rect = None
	dest_rect = None

	number_of_steps = 0
	current_step = 0
	speed = 15

	def __init__(self):
		Un_Objet.__init__(self, "la_souris", 20)
		self.state = "WHEREDOIGO"
		self.start_rect = self.rect.copy()
		self.dest_rect = self.rect.copy()

	
	def event_loop(self):
		pass

	def distance_to(self, to_rect):
		x=self.rect.center[0]
		y=self.rect.center[1]
		dx=to_rect.center[0]
		dy=to_rect.center[1]

		return math.sqrt( (x-dx)*(x-dx) + (y-dy)*(y-dy) )

	def update_position(self):
		if self.state == "WHEREDOIGO":

			self.start_rect.center = self.rect.center

			self.dest_rect.center = (random.randint(self.start_rect.x, self.start_rect.x + SCREENSIZE[0]/3), random.randint(self.start_rect.y - SCREENSIZE[1]/2, self.start_rect.y))

			print("I'm going from", self.start_rect, "to", self.dest_rect, "distance=",self.distance_to( self.dest_rect ))
			self.number_of_steps = self.distance_to( self.dest_rect )/self.speed

			i=random.randint(0,len(self.son)-1)
			self.son[i].play()
			self.state = "GOOUT"

		elif self.state == "GOOUT":

			self.rect.x = self.start_rect.x + ((self.dest_rect.x-self.start_rect.x)*self.current_step)/self.number_of_steps
			self.rect.y = self.start_rect.y + ((self.dest_rect.y-self.start_rect.y)*self.current_step)/self.number_of_steps

			self.current_step += 1

			if self.current_step >= self.number_of_steps:
				self.state = "GOIN"

		elif self.state == "GOIN":

			self.rect.x = self.start_rect.x + ((self.dest_rect.x-self.start_rect.x)*self.current_step)/self.number_of_steps
			self.rect.y = self.start_rect.y + ((self.dest_rect.y-self.start_rect.y)*self.current_step)/self.number_of_steps

			self.current_step -= 1

			if self.current_step == 0:
				self.state = "WHEREDOIGO"





class Chat( Un_Objet ):

	def __init__(self):
		Un_Objet.__init__(self, "le_chat", 5)

	def event_loop(self):

		for click in pygame.event.get():
			if click.type == MOUSEBUTTONDOWN:
				hit = pygame.mouse.get_pressed()
				if hit[0]:
					print click
					i=random.randint(0,len(self.son)-1)
					self.son[i].play()
			elif click.type == QUIT:
				self.state = "QUIT"
			elif click.type == KEYDOWN:
				if click.key in [ K_ESCAPE, K_q ]:
					self.state = "QUIT"
			
	def update_position(self):
		#(self.x, self.y) = pygame.mouse.get_pos()
		self.rect.center = pygame.mouse.get_pos()
		#self.x += self.dx
		#self.y += self.dy
		"""
		#if random.randint(0,5000) > 4990:
			#le_squeek.play()
		if self.x < 0:
			self.x = 0
			#le_squeek.play()
			#self.image = pygame.transform.flip(self.image, 1, 0)
		if self.y < 0:
			self.y = 0
			#le_squeek.play()
			#self.image = pygame.transform.flip(self.image, 0, 1)
		if self.x > (SCREENSIZE[0] - self.image.get_width()):
			self.x = (SCREENSIZE[0] - self.image.get_width())
			#le_squeek.play()
			#self.image = pygame.transform.flip(self.image, 1, 0)
		if self.y > (SCREENSIZE[1] - self.image.get_height()):
			self.y = (SCREENSIZE[1] - self.image.get_height())
			#le_squeek.play()
			#self.image = pygame.transform.flip(self.image, 0, 1)
		"""

		#self.screen.blit(self.image,(self.x-self.image.get_width()/2,self.y-self.image.get_height()/2))

class Motte( Un_Objet ):

	def __init__(self):
		Un_Objet.__init__(self, "la_motte", 2)
	
	def event_loop(self):
		pass

	def update_position(self):
		pass

class Fond( Un_Objet ):

	def __init__(self):
		Un_Objet.__init__(self, "le_fond", -1)
	
	def event_loop(self):
		pass

	def update_position(self):
		pass

#####           
def main():
	toutes_les_boites.clear(SCREEN, le_fond.image)

	la_souris.update()
	le_chat.update()
	la_motte.update()

        # Draw the scene
        dirty = toutes_les_boites.draw(SCREEN)
        pygame.display.update(dirty)  
       	#pygame.display.update()
	pygame.time.delay(10)

#####
if __name__ == "__main__":
	la_boite_du_fond = pygame.sprite.Group()
	la_boite_de_la_souris = pygame.sprite.Group()
	la_boite_du_chat = pygame.sprite.Group()
	la_boite_de_la_motte  = pygame.sprite.Group()
	toutes_les_boites = pygame.sprite.RenderUpdates()

	Fond.containers = la_boite_du_fond # , toutes_les_boites
	Motte.containers = la_boite_de_la_motte, toutes_les_boites
	Souris.containers = la_boite_de_la_souris, toutes_les_boites
	Chat.containers = la_boite_du_chat, toutes_les_boites

	le_fond   = Fond()
	le_chat   = Chat()
	la_souris = Souris()
	la_motte  = Motte()

	la_motte.rect.bottom = le_fond.rect.bottom
	la_souris.rect.center = la_motte.rect.center
	la_souris.rect.bottom = la_motte.rect.bottom
	
	SCREEN.blit(le_fond.image,(0,0))
        pygame.display.flip()  
	
	while 1:
		main()
