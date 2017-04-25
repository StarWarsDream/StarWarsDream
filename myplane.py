# coding=UTF-8

import pygame
#定义MyPlane,继承pygame.sprite.Sprite
class MyPlane(pygame.sprite.Sprite): 
    def __init__(self,bg_size):
        #初始化sprite
        pygame.sprite.Sprite.__init__(self)
        #导入飞机图片
        self.image1=pygame.image.load("images/me1.png").convert_alpha()
        self.image2=pygame.image.load("images/me2.png").convert_alpha()
        self.destroy_images=[]
        #active属性表示飞机生存状态，当发生碰撞时变为faulse
        self.active=True
        #导入飞机撞毁图片
        self.destroy_images.extend([\
            pygame.image.load("images/me_destroy_1.png").convert_alpha(),\
            pygame.image.load("images/me_destroy_2.png").convert_alpha(),\
            pygame.image.load("images/me_destroy_3.png").convert_alpha(),\
            pygame.image.load("images/me_destroy_4.png").convert_alpha()\
        ])
        
        #获取图片的限定矩形
        self.rect=self.image1.get_rect()
        #本地化图片尺寸
        self.width,self.height=bg_size[0],bg_size[1]
        self.rect.left,self.rect.top=\
                        (self.width-self.rect.width)//2,\
                        self.height-self.rect.height-60
        #定义移动速度
        self.speed=10
        #无敌属性，默认为FALSE，当重生时变为TRUE
        self.invincible=False
        #mask属性，将图片的空白部分设置为空白，碰撞检测时就会只检测非空白部分
        self.mask=pygame.mask.from_surface(self.image1)


    def moveUp(self):
        if self.rect.top>0:
            self.rect.top-=self.speed
        else:
            self.rect.top=0

    def moveDown(self):
        if self.rect.bottom<self.height-60:
            self.rect.top+=self.speed
        else:
            self.rect.bottom=self.height-60

    def moveLeft(self):
        if self.rect.left>0:
            self.rect.left-=self.speed
        else:
            self.rect.left=0

    def moveRight(self):
        if self.rect.right<self.width:
            self.rect.left+=self.speed
        else:
            self.rect.right=self.width


    def reset(self):
        self.rect.left,self.rect.top=\
                        (self.width-self.rect.width)//2,\
                        self.height-self.rect.height-60
        self.active=True
        self.invincible=True




    
    
            

        
