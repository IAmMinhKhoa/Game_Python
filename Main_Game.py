import math
import random
import pygame
import os
import sys

from objects_1 import *
pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
# win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
info = pygame.display.Info()
width = info.current_w
height = info.current_h

# if width >= height:
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
# else:
#     win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 90

# mã màu
BLACK = (20,20,20)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)
RED = (255,0,0)
GRAY = (128,128,128)
BLUE = (30, 144,255)
WHITE = (255, 255, 255)

# font chữ
title_font = 'Qircle Rush/Fonts/AvQest.ttf'

#gọi các ảnh vào
Button_game_img = pygame.image.load('Button_Game.png')
OutGame_img = pygame.image.load('out_game.png')
arc_dash_img = pygame.image.load('Arc Dash.png')

#set vị trí tên game TAP TAP
tap = Message(80, 150, 70, "Tap", title_font, WHITE, win)
tap2 = Message(210, 150, 70, "Tap", title_font, WHITE, win)

# thêm 30 ảnh animation backround vào mảng, sau đó cho mảng chạy lien tục để animation
ide_br=[]
for i in range(30):
    path="br/"+str(i+1)+".png"
    ide_br.append(path)

#set vị trí kích thước cho các button
Button_game_btn_1 = Button(Button_game_img, (120, 50), 10, HEIGHT//2 + 90)
arc_dash_btn = Button(arc_dash_img, (100, 25), 20, HEIGHT//2 + 100)
Button_game_btn_2 = Button(Button_game_img, (120, 50), 157, HEIGHT//2 + 90)
OutGame= Button(OutGame_img, (90, 60), WIDTH // 2-45, HEIGHT-80)

#các biến
k=1 #biến k này để biến chạy cho mảng ảnh animaiton chạy thôi
running = True

while running:
    pygame.draw.rect(win, BLUE, (0, 0,WIDTH, HEIGHT), 6)
    clock.tick(30)
    pygame.display.update()

    win.fill(BLACK)
    #tiến hành cho chạy mảng vẽ background
    chosen_img = pygame.image.load(ide_br[k])
    win.blit(chosen_img, ((0, 0)))
    k+=1
    if k>29:
        k=0

    #BẮT SỰ KIỆN
    for event in pygame.event.get():
        #NẾU ẤN ESC HOẶC NÚT Q THÌ 0UT GAME
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or \
                    event.key == pygame.K_q:
                running = False
        #hover nhé
        if event.type == pygame.MOUSEMOTION:
            if Button_game_btn_1.rect.collidepoint(pygame.mouse.get_pos()):
                Button_game_btn_1 = Button(Button_game_img, (105, 45), 15, HEIGHT//2 + 95)
            elif Button_game_btn_2.rect.collidepoint(pygame.mouse.get_pos()):
                Button_game_btn_2 = Button(Button_game_img, (105, 45), 162, HEIGHT // 2 + 95)
            elif OutGame.rect.collidepoint(pygame.mouse.get_pos()):
                OutGame = Button(OutGame_img, (85, 55), WIDTH // 2 - 42, HEIGHT - 82)
            else:
                Button_game_btn_1 = Button(Button_game_img, (120, 50), 10, HEIGHT // 2 + 90)
                Button_game_btn_2 = Button(Button_game_img, (120, 50), 157, HEIGHT // 2 + 90)
                OutGame = Button(OutGame_img, (90, 60), WIDTH // 2 - 45, HEIGHT - 80)
    #HOẶC NẾU ẤN BUTTON OUT MÀU ĐỎ TRONG GAME THÌ CŨNG OUT
    if OutGame.draw(win):
        running = False

    #IN RA TÊN GAME
    tap.update()
    tap2.update()


    #BẮT SỰ KIỆN NẾU NÚT GAME 1 HOẶC GAME 2 ĐƯỢC CLICK THÌ CHUYỂN SANG GAME ĐÓ
    if Button_game_btn_1.draw(win) :
        exec(open("main_1.py", encoding="utf8").read())
        running = False
    elif Button_game_btn_2.draw(win):
        exec(open("main_2.py", encoding="utf8").read())
        running = False



pygame.quit()