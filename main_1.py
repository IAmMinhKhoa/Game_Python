
import random
import pygame
# sys.path.insert(0,'objects_1.py')
from objects_1 import *
	# Circle, Player, Dot, Particle, Snowflake,ScoreCard, Button, Message, BlinkingText
 
pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2



# if width >= height:
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
# else:
# win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 70

# COLORS *********************************************************************

RED = (255,0,0)
GREEN = (0,177,64)
BLUE = (30, 144,255)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)
AQUA = (0,103,127)
WHITE = (255, 255, 255)
BLACK = (20,20,20)
GRAY = (128,128,128)
lightskyblue=(135,206,250)
color_list = [BLUE, GREEN, ORANGE, YELLOW]
color_index = 3
color = color_list[color_index]

#ĐÂY LÀ PATH FILE TXT CHỨA ĐIỂM CỦA GAME
path_score= 'score/score_1.txt'

# FONTS **********************************************************************

score_font = "Qircle Rush/Fonts/neuropol x rg.ttf"
title_font = 'Qircle Rush/Fonts/AvQest.ttf'

#IN RA ĐIỂM TRONG KHI CHƠI CÒN ĐANG CHẠY
score_msg = ScoreCard(WIDTH//2, 60, 35, score_font, WHITE, win)
#IN RA ĐIỂM CÓ ĐƯỢC KHI GAME OVER
final_score_msg = Message(90, 270, 50, "0", score_font, WHITE, win)
#IN RA ĐIỂM CAO NHẤT TỪ TRƯỚC TỚI GIỜ
high_score_msg = Message(200, 270, 50, "0", score_font, WHITE, win)
#ĐÂY LÀ 1 VĂN BẢNG IN RA THÔNG BÁO BẠN ĐÃ ĐƯỢC THÀNH TÍCH MỚI
new_high_msg = Message(WIDTH//2, 320, 25, "NEW HIGH!", score_font, lightskyblue, win)

#TÊN GAME IN BÊN NGOÀI
qircle_msg = Message(WIDTH-160, 150, 80, "Qircle", title_font, WHITE, win)
dash_msg = Message(WIDTH-100, 220, 60, "Rush", title_font, WHITE, win)

#VĂN BẢN TAP TO PLAY
tap_to_play = BlinkingText(WIDTH//2, HEIGHT-60, 20, "Tap To Play", None, WHITE, win)
#VĂN BẢN NOOB HIỆN RA KHI SCORE CHỈ CÓ 0 ĐIỂM
noob = Message(90, 270, 30,"NOOB", None, RED, win)

#IN RA ĐOẠN TEXT NHƯ TRONG HÌNH
game_msg = Message(80, 150, 40, "GAME ", title_font, WHITE, win)
over_msg = Message(210, 150, 40, "OVER!", title_font, WHITE, win)
score_text = Message(90, 230, 20, "SCORE", None, WHITE, win)
best_text = Message(200, 230, 20, "BEST", None, WHITE, win)

# SOUNDS *********************************************************************

dash_fx = pygame.mixer.Sound('Qircle Rush/Sounds/dash.mp3')
click_fx = pygame.mixer.Sound('Qircle Rush/Sounds/click.mp3')
dead_fx = pygame.mixer.Sound('Qircle Rush/Sounds/dead.mp3')
score_page_fx = pygame.mixer.Sound('Qircle Rush/Sounds/score_page.mp3')

pygame.mixer.music.load('Qircle Rush/Sounds/music.wav')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)

# IMAGES *********************************************************************

main_circle = pygame.image.load('Qircle Rush/Assets/main.png')
flake_img = 'Qircle Rush/Assets/flake.png'

close_img = pygame.image.load('Qircle Rush/Assets/closeBtn.png')
replay_img = pygame.image.load('Qircle Rush/Assets/replay.png')
sound_off_img = pygame.image.load("Qircle Rush/Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Qircle Rush/Assets/soundOnBtn.png")

ball1_img=pygame.image.load("Qircle Rush\\Assets\\ball_1.png");
ball2_img=pygame.image.load("Qircle Rush\\Assets\\ball_2.png");
exit_img = pygame.image.load("exit.png")


# Buttons ********************************************************************

close_btn = Button(close_img, (24, 24), WIDTH // 4 - 18, HEIGHT//2 + 120)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT//2 + 115)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT//2 + 120)
exit_btn =Button(exit_img,(50,50),5 , 5)
ball1_btn =Button(ball1_img,(50,50),WIDTH/2+20 , 380)
ball2_btn =Button(ball2_img,(50,50),WIDTH/2-50 , 380)
# GROUP & OBJECTS ************************************************************

flake_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
circle_group = pygame.sprite.Group()

p = Player()
d = Dot()
pos = random.randint(0, 11)

# VARIABLES ******************************************************************

clicked = False
rotate = True
shrink = True
sound_on = True

val_ball=-1
clicks = 0
count = 50
score = 0
high_score = 0
score_list = []

#biến set giao diện của game
home_page = True
game_page = False
score_page = False

#tiến học đọc điểm cao nhất từ file txt và gán cho biến hight_score
with open(path_score) as f:
	high_score=int(f.read())

#biến game chạy, nếu false là game dừng
running = True
while running:
	#vẽ khung viền màn hình
	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 8)
	#tốc độ game
	clock.tick(FPS)
	#này là hàm mặc định, tìm hiểu gg them đi giải thích mệt
	pygame.display.update()
	#backround màu đen
	win.fill(BLACK)
	#BẮT SỰ KIỆN KHI CLICK NÀY NỌ
	for event in pygame.event.get():
		if event.type == pygame.QUIT:

			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:

				running = False
		if event.type == pygame.MOUSEMOTION:
			if ball1_btn.rect.collidepoint(pygame.mouse.get_pos()):
				ball1_btn = Button(ball1_img, (60, 60), WIDTH / 2 + 10, 380)
			elif ball2_btn.rect.collidepoint(pygame.mouse.get_pos()):
				ball2_btn =Button(ball2_img,(60,60),WIDTH/2-60 , 380)
			elif exit_btn.rect.collidepoint(pygame.mouse.get_pos()):
				exit_btn = Button(exit_img, (55, 55), 5, 5)
			else:
				exit_btn = Button(exit_img, (50, 50), 5, 5)
				ball2_btn =Button(ball2_img,(50,50),WIDTH/2-50 , 380)
				ball1_btn = Button(ball1_img, (50, 50), WIDTH / 2 + 20, 380)

		if  val_ball!=-1:

			if home_page:
				home_page = False
				game_page = True

				# for i in range(12):
				circle_group.empty()

				for i in range(12):
					c = Circle(i)
					circle_group.add(c)

			elif  event.type == pygame.MOUSEBUTTONDOWN  and game_page:
				#nếu không click thì...
				if  clicked ==False:
					clicked = True
					rotate = False
					clicks += 1
					click_fx.play()

		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
			rotate = True

	if home_page:
		count += 1
		if count % 100 == 0:
			x = random.randint(40, WIDTH - 40)
			y = 0
			flake = Snowflake(x, y, flake_img)
			flake_group.add(flake)

			count = 0

		flake_group.update(win)
		qircle_msg.update()
		dash_msg.update()
		tap_to_play.update()
		if ball1_btn.draw(win):
			val_ball = 1
		if ball2_btn.draw(win):
			val_ball = 2
		if exit_btn.draw(win):

			exec(open("Main_Game.py", encoding="utf8").read())



	if score_page:

		if  score >= high_score:
			high_score = score
			new_high_msg.update()
			with open(path_score, mode='w') as f:
				str_sc=str(high_score)
				f.write(str_sc)

		if score == 0:
			noob.update()
		else:
			final_score_msg.update(score, YELLOW)

		high_score_msg.update(high_score, YELLOW)

		game_msg.update()
		over_msg.update()
		score_text.update()
		best_text.update()



		if close_btn.draw(win):

			clicks = 0
			score = 0
			p.reset()
			val_ball=-1
			home_page=True
			score_page = False
			game_page = False
		if replay_btn.draw(win):
			clicks = 0
			score = 0
			pos = random.randint(0, 11)

			p.reset()
			# final_score_msg = Message(144, HEIGHT//2-50, 100, "0", score_font, WHITE, win)

			score_page = False
			game_page = True

		if sound_btn.draw(win):
			pass
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if game_page:
		#vẽ trục giữa
		win.blit(main_circle, (CENTER[0] - 12.5, CENTER[1] - 12.5))

		score_msg.update(score)

		particle_group.update()

		circle_group.update(shrink)


		circle_group.draw(win)
		#giúp playẻ quay vòng trục
		# print(rotate)
		p.update(rotate,val_ball)
		p.draw(win,val_ball)

		if p.alive:
			if score and score % 7 == 0:
				if score not in score_list:
					score_list.append(score)
					shrink = not shrink

			if clicks and clicks % 5 == 0:
				color_index = (color_index + 1) % len(color_list)
				color = color_list[color_index]

				r = random.choice([-1, 1])
				for c in circle_group:
					c.dt *= -r
					c.rotate = True

				clicks = 0

			#tao ra bong ghi diem
			dot_circle = circle_group.sprites()[pos]
			x, y = dot_circle.rect.center
			d.update(x, y, win, color)

#bug hien tai la cham roi nhung ko phan hoi lai
			#kiem tra va cham
			for circle in circle_group:
				if circle.complete==True:

					if pygame.sprite.collide_mask(p, circle):
						# print("cham")

						if circle.i == pos:
							pos = random.randint(0, 11)

							x, y = circle.rect.center
							#tạo effect khi playẻ chạm bóng màu thì tạo effect vỡ
							for i in range(10):
								particle = Particle(x, y, color, win)
								particle_group.add(particle)

							score += 1
							dash_fx.play()
						p.dr *= -1

			#kiem tra khi biong bay ra ria man hinh thi vo ra
			x, y = p.rect.center
			if (x < 0 or x > WIDTH or y < 0 or y > HEIGHT):
				for i in range(10):
					particle = Particle(x, y, WHITE, win)
					particle_group.add(particle)
				p.alive = False
				dead_fx.play()
		#khi bóng vở thì game over
		if not p.alive and len(particle_group) == 0:
			particle_group.empty()

			game_page = False
			score_page = True
			score_page_fx.play()



running = False