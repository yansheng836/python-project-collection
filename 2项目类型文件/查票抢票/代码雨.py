# Python实现代码雨效果
import sys
import random
import pygame
from pygame.locals import *


# 屏幕大小
WIDTH = 800
HEIGHT = 600
# 下落速度范围
SPEED = [15, 30]
# 字母大小范围
SIZE = [5, 30]
# CODE长度范围
LEN = [1, 8]


# 随机生成一个颜色
def randomColor():
	return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# 随机生成一个速度
def randomSpeed():
	return random.randint(SPEED[0], SPEED[1])


# 随机生成一个大小
def randomSize():
	return random.randint(SIZE[0], SIZE[1])


# 随机生成一个长度
def randomLen():
	return random.randint(LEN[0], LEN[1])


# 随机生成一个位置
def randomPos():
	return (random.randint(0, WIDTH), -20)


# 随机生成一个字符串
def randomCode():
	return random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')


# 定义代码精灵类
class Code(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.Font('C:\Windows\Fonts\Font.ttf', randomSize())
		self.speed = randomSpeed()
		self.code = self.getCode()
		self.image = self.font.render(self.code, True, randomColor())
		self.image = pygame.transform.rotate(self.image, random.randint(87, 93))
		self.rect = self.image.get_rect()
		self.rect.topleft = randomPos()
	def getCode(self):
		length = randomLen()
		code = ''
		for i in range(length):
			code += randomCode()
		return code
	def update(self):
		self.rect = self.rect.move(0, self.speed)
		if self.rect.top > HEIGHT:
			self.kill()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('源码加微信mmp9972')
clock = pygame.time.Clock()
codesGroup = pygame.sprite.Group()
while True:
	clock.tick(24)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit(0)
	screen.fill((1, 1, 1))
	codeobject = Code()
	codesGroup.add(codeobject)
	codesGroup.update()
	codesGroup.draw(screen)
	pygame.display.update()