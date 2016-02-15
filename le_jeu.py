#!/usr/bin/python

import sys, os, random

import pygame
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

SCREENSIZE  = (3840,2160)

SCREEN = pygame.display.set_mode(SCREENSIZE,FULLSCREEN)

la_souris = pygame.image.load("data/la_souris.png").convert_alpha()
la_souris = pygame.transform.scale(la_souris,(la_souris.get_width()/20,la_souris.get_height()/20))

le_chat = pygame.image.load("data/le_chat.png").convert_alpha()
le_chat = pygame.transform.scale(le_chat,(le_chat.get_width()/5,le_chat.get_height()/5))
#la_souris_flipped   = pygame.image.load("SuperSourisSmall.png").convert_alpha()
#la_souris_flipped   = pygame.transform.flip(la_souris_flipped, 1, 0)
la_souris_mask   = pygame.mask.from_surface(la_souris)
#la_souris_mask   = pygame.mask.from_surface(la_souris)
le_fond   = pygame.image.load("data/le_fond.png").convert()
le_squeek = pygame.mixer.Sound("data/squeek1.wav")

class Souris:
	image = None
	def __init__(self, image):
		self.image = image
		self.screen = SCREEN
		self.x = random.randint(0, SCREENSIZE[0]  - la_souris.get_width())
		self.y = random.randint(0, SCREENSIZE[1]  - la_souris.get_height())
		self.dx = random.randint(0, 20)
		self.dy = random.randint(0, 20)
		self.init()
	
	def init(self):
		self.state = "RUN"
 
	def event_loop(self):
		self.target = pygame.mouse.get_pos()
		for click in pygame.event.get():
			if click.type == MOUSEBUTTONDOWN:
				hit = pygame.mouse.get_pressed()
				if hit[0]:
					print click
			elif click.type == QUIT:
				self.state = "QUIT"
			elif click.type == KEYDOWN:
				if click.key in [ K_ESCAPE, K_q ]:
					self.state = "QUIT"
				elif click.key == pygame.K_UP:
					self.dy -= 10
				elif click.key == pygame.K_DOWN:
					self.dy += 10
				elif click.key == pygame.K_LEFT:
					self.dx -= 10
				elif click.key == pygame.K_RIGHT:
					self.dx += 10
			
	def update_position(self):
		self.x += self.dx
		self.y += self.dy
		if random.randint(0,5000) > 4990:
			le_squeek.play()
		if self.x < 0:
			self.x = 0
			self.dx = -self.dx
			le_squeek.play()
			self.image = pygame.transform.flip(self.image, 1, 0)
		if self.y < 0:
			self.y = 0
			self.dy = -self.dy
			le_squeek.play()
			self.image = pygame.transform.flip(self.image, 0, 1)
		if self.x > (SCREENSIZE[0] - self.image.get_width()):
			self.x = (SCREENSIZE[0] - self.image.get_width())
			self.dx = -self.dx
			le_squeek.play()
			self.image = pygame.transform.flip(self.image, 1, 0)
		if self.y > (SCREENSIZE[1] - self.image.get_height()):
			self.y = (SCREENSIZE[1] - self.image.get_height())
			self.dy = -self.dy
			le_squeek.play()
			self.image = pygame.transform.flip(self.image, 0, 1)

		#if self.dx >= 0:
		self.screen.blit(self.image,(self.x,self.y))
		#else:
		#	self.screen.blit(la_souris_flipped,(self.x,self.y))

	def update(self):
		#control flow     
		if self.state == "QUIT":
			pygame.quit();sys.exit()
		self.event_loop()
		self.update_position()
		pygame.event.pump()


#####           
def main():
	SCREEN.blit(pygame.transform.scale(le_fond,(SCREENSIZE[0],SCREENSIZE[1])),(0,0))
	for l in MySouris:
		l.update()
       	pygame.display.update()
	pygame.time.delay(10)

#####
if __name__ == "__main__":
	MySouris = []
	MySouris.append( Souris(la_souris) )
	MySouris.append( Souris(le_chat) )
	while 1:
		main()
