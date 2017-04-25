# coding=UTF-8
import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *  #导入常量模块
from random import *

#初始化pygame
pygame.init()
pygame.mixer.init()

#设置游戏窗口
bg_size=width,height=400,700
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")

background=pygame.image.load("images/background.png").convert()
BLACK=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)
WHITE=(255,255,255)

# 载入游戏音乐
pygame.mixer.music.load("sound/music.mp3")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1=enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2=enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3=enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target,inc):
    for each in target:
        each.speed+=inc

#主模块的主函数
def main():

    #播放背景音乐
    pygame.mixer.music.play(-1)

    #生成我方飞机
    me=myplane.MyPlane(bg_size)

    #中弹图片索引
    e1_destroy_index=0
    e2_destroy_index=0
    e3_destroy_index=0
    me_destroy_index=0
    
    enemies=pygame.sprite.Group()
    #生成敌方小型飞机
    small_enemies=pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)
    #生成敌方中型飞机
    mid_enemies=pygame.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,4)
    #生成敌方大型飞机
    big_enemies=pygame.sprite.Group()
    add_big_enemies(big_enemies,enemies,2)

    #统计得分
    score=0
    score_font=pygame.font.Font("font/font.ttf",36)

    #标志是否暂停游戏
    paused=False
    paused_nor_image=pygame.image.load("images/pause_nor.png").convert_alpha()
    paused_pressed_image=pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image=pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image=pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect=paused_nor_image.get_rect()
    paused_rect.left,paused_rect.top=width-paused_rect.width-10,10
    paused_image=paused_nor_image

    #游戏结束画面
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    #设置难度级别
    level=1

    #全屏炸弹
    bomb_image=pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect=bomb_image.get_rect()
    bomb_font=pygame.font.Font("font/font.ttf",48)
    bomb_num=3

    #超级子弹定时器
    DOUBLE_BULLET_TIME=USEREVENT+1

    #标志是否使用超级子弹
    is_double_bullet=False

    #解除我方无敌状态定时器
    INVINCIBLE_TIME=USEREVENT+2    

    #每30秒发送一个补给包
    bullet_supply=supply.Bullet_Supply(bg_size)
    bomb_supply=supply.Bomb_Supply(bg_size)
    SUPPLY_TIME=USEREVENT
    pygame.time.set_timer(SUPPLY_TIME,30*1000)
    
    
    #生成普通子弹
    bullet1=[]
    bullet1_index=0
    BULLET1_NUM=4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

     #生成超级子弹
    bullet2=[]
    bullet2_index=0
    BULLET2_NUM=8
    for i in range(BULLET2_NUM):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33,me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+30,me.rect.centery)))
      
    clock=pygame.time.Clock()

    #用于替换图片，绘制我方飞机时变换图片
    switch_image=True

    #用于延迟
    delay=100

    #生命数量
    life_image=pygame.image.load("images/life.png").convert_alpha()
    life_rect=life_image.get_rect()
    life_num=3

    #用于限制重复打开记录文件
    recorded=False
    
    running=True
    
    while running:
        for event in pygame.event.get():

            if event.type==QUIT: #退出游戏
                pygame.quit()
                sys.exit()
            #暂停事件
            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1 and paused_rect.collidepoint(event.pos):
                    paused=not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME,30*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type==MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image=resume_pressed_image
                    else:
                        paused_image=paused_pressed_image
                else:
                    if paused:
                        paused_image=resume_nor_image
                    else:
                        paused_image=paused_nor_image

            #全屏炸弹事件           
            elif event.type==KEYDOWN:
                if event.key==K_SPACE:
                    if bomb_num > 0:
                        bomb_num-=1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom>0:
                                each.active=False
            #补给包事件
            elif event.type==SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            #超级子弹事件
            elif event.type==DOUBLE_BULLET_TIME:
                is_double_bullet=False
                pygame.time.set_timer(DOUBLE_BULLET_TIME,0)

            elif event.type==INVINCIBLE_TIME:
                me.invincible=False
                pygame.time.set_timer(INVINCIBLE_TIME,0)
                            
        #根据用户的得分增加难度
        if level==1 and score>50000:
            level=2
            upgrade_sound.play()
            #增加3加小型敌机、2加中型敌机、1加大型敌机
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies,enemies,1)
            #提升小型敌机的速度
            inc_speed(small_enemies,1)
        elif level==2 and score>200000:
            level=3
            upgrade_sound.play()
            #增加3加小型敌机、2加中型敌机、1加大型敌机
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            #提升小型敌机的速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        elif level==3 and score>6400000:
            level=4
            upgrade_sound.play()
            #增加3加小型敌机、2加中型敌机、1加大型敌机
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            #提升小型敌机的速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        elif level==4 and score>1000000:
            level=5
            upgrade_sound.play()
            #增加3加小型敌机、2加中型敌机、1加大型敌机
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            #提升小型敌机的速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        
        #画出屏幕背景
        screen.blit(background,(0,0))

        if life_num and not paused:
            # 检测用户的键盘操作
            key_pressed=pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    if bomb_num<3:
                        bomb_num+=1
                    bomb_supply.active=False

            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move() 
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    #发射超级子弹
                    is_double_bullet=True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,20*1000)
                    bullet_supply.active=False
                    
            #发射子弹
            if not(delay%10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets=bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33,me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx+30,me.rect.centery))
                    bullet2_index=(bullet2_index+2)%BULLET2_NUM
                else:
                    bullets=bullet1 
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index=(bullet1_index+1)%BULLET1_NUM


            #检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit=pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active=False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.energy-=1
                                e.hit=True
                                if e.energy==0:
                                    e.active=False
                            else:
                                e.active=False

            #绘制大型敌机
            for each in big_enemies:
                if each.active:            
                    each.move()
                    if each.hit:
                        #绘制被打到的特效
                        screen.blit(each.image_hit,each.rect)
                        each.hit=False
                    else:    
                        if switch_image:
                            screen.blit(each.image1,each.rect)
                        else:
                            screen.blit(each.image2,each.rect)

                    #绘制血槽
                    pygame.draw.line(screen,BLACK,\
                                     (each.rect.left,each.rect.top-5),\
                                     (each.rect.right,each.rect.top-5),\
                                     2)
                    #当生命大于20%，显示绿色，否则显示红色
                    energy_remain=each.energy/enemy.BigEnemy.energy
                    if energy_remain>0.2:
                        energy_color=GREEN
                    else:
                        energy_color=RED
                    pygame.draw.line(screen,energy_color,\
                                    (each.rect.left,each.rect.top-5),\
                                    (each.rect.left+each.rect.width*energy_remain,each.rect.top-5),2)
                        
                    #即将出现在画面中，播放音效
                    if each.rect.bottom==-50:
                        enemy3_fly_sound.play(-1)      
                else:
                    #毁灭
                    if not(delay%3):
                        screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                        if e3_destroy_index==0:
                            enemy3_down_sound.play()
                        e3_destroy_index=(e3_destroy_index+1)%6
                        if e3_destroy_index==0:
                            each.reset()
                            score+=10000
                            enemy3_fly_sound.stop()
                        
            #绘制中型敌机
                for each in mid_enemies:
                    if each.active:
                        each.move()
                        if each.hit:
                            #绘制被打到的特效
                            screen.blit(each.image_hit,each.rect)
                            each.hit=False
                
                        else:
                            screen.blit(each.image,each.rect)
                        #绘制血槽
                        pygame.draw.line(screen,BLACK,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),2)
                        #当生命大于20%，显示绿色，否则显示红色
                        energy_remain=each.energy/enemy.MidEnemy.energy
                        if energy_remain>0.2:
                            energy_color=GREEN
                        else:
                            energy_color=RED
                        pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5),(each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),2)
                    else:
                        #毁灭
                        if not(delay%3):
                            if e2_destroy_index==0:
                                enemy2_down_sound.play()
                            screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                            e2_destroy_index=(e2_destroy_index+1)%4
                            if e2_destroy_index==0:
                                score+=6000
                                each.reset()
                            
                                
             #绘制小型敌机
                for each in small_enemies:
                    if each.active:
                        each.move()
                        screen.blit(each.image,each.rect)
                    else:
                        #毁灭                    
                        if not(delay%3):
                            if e1_destroy_index==0:
                                enemy1_down_sound.play()
                            screen.blit(each.destroy_images[e1_destroy_index],each.rect)
                            e1_destroy_index=(e1_destroy_index+1)%4
                            if e1_destroy_index==0:
                                score+=1000
                                each.reset()