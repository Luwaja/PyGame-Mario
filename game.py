import pygame
import time

from pygame.locals import*
from time import sleep


#----------------------------------------------------------------
class Sprite():
	def __init__(self, x, y, image):
		self.x = x
		self.y = y

	def isPipe(self):
		return False
	def isGoomba(self):
		return False
	def isFireball(self):
		return False

#----------------------------------------------------------------
class Pipe(Sprite):
	def __init__(self, x, y, image):
		super().__init__(x, y, image)
		self.w = 55
		self.h = 400
		self.pipeImage = pygame.image.load("pipe.png")

	def isPipe(self):
		return True

	def drawYourself(self, screen, scrollPos):
		screen.blit(self.pipeImage, (self.x - scrollPos, self.y))

	def update(self):
		pass

#----------------------------------------------------------------
class Mario(Sprite):
	def __init__(self, x, y, image):
		super().__init__(x, y, image)
		self.w = 60
		self.h = 95
		self.vert_velocity = 0
		self.numFramesInAir = 0
		self.currentImage = 0
		#Loading in Mario images
		self.marioImages = []
		self.marioImages.append(pygame.image.load("mario1.png"))
		self.marioImages.append(pygame.image.load("mario1.png"))
		self.marioImages.append(pygame.image.load("mario2.png"))
		self.marioImages.append(pygame.image.load("mario3.png"))
		self.marioImages.append(pygame.image.load("mario4.png"))
		self.marioImages.append(pygame.image.load("mario5.png"))
		self.marioImages.append(pygame.image.load("mario6.png"))
		self.marioImages.append(pygame.image.load("mario7.png"))

	def changeImageState(self):
		self.currentImage += 1
		if self.currentImage > len(self.marioImages) - 1:
			self.currentImage = 0

	def setPreviousPosition(self):
		self.prevx = self.x
		self.prevy = self.y

	def getOutOfPipe(self, pipe):
		#Mario coming from top
		if(self.prevy + self.h) < pipe.y:
			self.y = pipe.y - self.h - 1
			self.vert_velocity = 0 #Stop Mario from falling
			self.numFramesInAir = 0 #Allow Mario to jump off pipe
		#Mario coming from bottom
		elif self.prevy > (pipe.y+pipe.h):
		    self.y = pipe.y + pipe.h
		else:
			#Mario coming from left
			if self.prevx < pipe.x:
				self.x = pipe.x - self.w - 1
			#Mario coming from right
			if self.prevx > pipe.x:
				self.x = pipe.x + pipe.w + 1
			
	def drawYourself(self, screen, scrollPos):
		screen.blit(self.marioImages[self.currentImage], (self.x - scrollPos, self.y))

	def update(self):
		self.vert_velocity += 2
		self.y += self.vert_velocity
		self.numFramesInAir += 1
		if self.y > 400 - self.h:
			self.vert_velocity = 0
			self.y = 400 - self.h
			self.numFramesInAir = 0

#----------------------------------------------------------------
class Goomba(Sprite):
	def __init__(self, x, y, image):
		super().__init__(x, y, image)
		self.w = 37
		self.h = 45
		self.horz_velocity = 2
		self.vert_velocity = 0
		self.framesOnFire = 0
		self.goombaImage = pygame.image.load("goomba.png")
		self.goombaFire = pygame.image.load("goomba_fire.png")

	def isGoomba(self):
		return True

	def onFire(self):
		self.goombaImage = self.goombaFire
		self.horz_velocity = 0
		self.framesOnFire += 1

	def drawYourself(self, screen, scrollPos):
		screen.blit(self.goombaImage, (self.x - scrollPos, self.y))

	def update(self):
		self.x += self.horz_velocity
		self.vert_velocity += 1.5
		self.y += self.vert_velocity
		if self.y > 400 - self.h:
			self.vert_velocity = 0
			self.y = 400 - self.h

#----------------------------------------------------------------
class Fireball(Sprite):
	def __init__(self, x, y, image):
		super().__init__(x, y, image)
		self.w = 47
		self.h = 47
		self.horz_velocity = 15
		self.vert_velocity = 0
		self.fireballImage = pygame.image.load("fireball.png")
		
	def isFireball(self):
		return True

	def drawYourself(self, screen, scrollPos):
		screen.blit(self.fireballImage, (self.x - scrollPos, self.y))

	def update(self):
		self.x += self.horz_velocity
		self.vert_velocity += 1
		self.y += self.vert_velocity
		if self.y > 400 - self.h:
			self.vert_velocity = -self.vert_velocity
			self.y = 400 - self.h

#----------------------------------------------------------------
class Model():
	def __init__(self, mario, goomba):
		self.mario = mario
		self.goomba = goomba
		
		self.spriteList = []
		#Create Mario
		self.mario = Mario(100,200, "mariojump.png")
		self.spriteList.append(self.mario)
		#Create pipes
		self.spriteList.append(Pipe(300,350,"pipe.png"))
		self.spriteList.append(Pipe(600,300,"pipe.png"))
		self.spriteList.append(Pipe(900,200,"pipe.png"))
		self.spriteList.append(Pipe(955,100,"pipe.png"))
		#Create goombas
		self.goomba1 = Goomba(400, 300, "goomba.png")
		self.spriteList.append(self.goomba1)
		self.goomba2 = Goomba(800, 300, "goomba.png")
		self.spriteList.append(self.goomba2)

	def throwFireball(self):
		self.spriteList.append(Fireball(self.mario.x + self.mario.w - 15, self.mario.y + 15, "fireball.png"))

	def checkCollision(self, s1, s2):
		if (s1.x+s1.w) < s2.x: #S1'S RIGHT is less than S2'S LEFT
			return False #S1 is NOT colliding
		if s1.x > (s2.x+s2.w): #S1'S LEFT is greater than S2'S RIGHT
			return False
		if (s1.y+s1.h) < s2.y: #S1'S BOTTOM is greater than S2'S TOP
			return False
		if s1.y > (s2.y+s2.h): #S1'S TOP is less than S2'S BOTTOM
			return False
		else:
			return True #S1 IS colliding
			
	def update(self):
		#Update sprites
		for sprite1 in self.spriteList:
			sprite1.update()

		#Sprite interactions
		for sprite1 in self.spriteList:
			#Pipe collision detection
			if sprite1.isPipe():
				#Mario-pipe detection
				checkMario = self.checkCollision(self.mario, sprite1)
				if checkMario == True:
					self.mario.getOutOfPipe(sprite1)

			#Goomba collision detection
			if sprite1.isGoomba():
				for sprite2 in self.spriteList:
					if sprite2.isPipe():
						checkGoomba = self.checkCollision(sprite1, sprite2)
						if checkGoomba == True:
							sprite1.horz_velocity = -(sprite1.horz_velocity)
					if sprite2.isFireball():
						checkFireball = self.checkCollision(sprite2, sprite1)
						if checkFireball:
							sprite1.onFire()
							self.spriteList.remove(sprite2)
							if sprite1.framesOnFire > 1:
								self.spriteList.remove(sprite1)

#----------------------------------------------------------------
class View():
	def __init__(self, model):
		#Screen
		self.model = model
		screen_size = (1000,500)
		self.screen = pygame.display.set_mode(screen_size)
		#Scroll
		self.scrollPos = 0

	def update(self):    
		self.screen.fill([98, 186, 240]) #Draw the sky
		pygame.draw.rect(self.screen, [28, 138, 23], Rect(0, 400, 1000, 100)) #Draws ground
		self.scrollPos = self.model.mario.x - 100

		for i in range(len(self.model.spriteList)):
			self.model.spriteList[i].drawYourself(self.screen, self.scrollPos)

		pygame.display.flip()
		

#----------------------------------------------------------------
class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.keep_going = True

	def update(self):
		self.model.mario.setPreviousPosition()
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
			elif event.type == KEYUP:
				if event.key == K_LCTRL:
					self.model.throwFireball()
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.mario.x -= 6
			self.view.scrollPos -= 6
			self.model.mario.changeImageState()
		if keys[K_RIGHT]:
			self.model.mario.x += 6
			self.view.scrollPos += 6
			self.model.mario.changeImageState()
		if keys[K_UP]:
			if self.model.mario.numFramesInAir < 5:
				self.model.mario.vert_velocity = -30
		if keys[K_DOWN]:
			pass
		if keys[K_SPACE]:
			if self.model.mario.numFramesInAir < 5:
				self.model.mario.vert_velocity = -30


			
#GAME---------------------------------------------------------------
print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
mar = Mario(300, 300,"mario1.png")
g = Goomba(400, 300, "goomba.png")
m = Model(mar, g)
v = View(m)
c = Controller(m, v)
while c.keep_going:
	mar.update()
	g.update()
	c.update()
	m.update()
	v.update()
	sleep(0.03)
print("Goodbye")
