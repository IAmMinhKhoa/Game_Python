import random
import time
import sys
import pygame
# sys.path.insert(0,'objects_2.py')
from objects_2 import *
	# Player, Balls, Dot, Shadow, Particle, Message, BlinkingText, Button

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

info = pygame.display.Info()
width = info.current_w
height = info.current_h

win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
# win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60
path_score= 'score/score_2.txt'
# COLORS **********************************************************************


RED = (255,0,0)
GREEN = (0,177,64)
BLUE = (30, 144,255)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)
AQUA = (0,103,127)
WHITE = (255,255,255)
BLACK = (0,0,0)

color_list = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]
color_index = 0
color = color_list[color_index]

# FONTS ***********************************************************************

title_font = "Arc Dash/Fonts/Aladin-Regular.ttf"
tap_to_play_font = "Arc Dash/Fonts/BubblegumSans-Regular.ttf"
score_font = "Arc Dash/Fonts/DalelandsUncialBold-82zA.ttf"
game_over_font = "Arc Dash/Fonts/ghostclan.ttf"

# MESSAGES ********************************************************************

arc = Message(WIDTH-90, 200, 80, "Arc", title_font, WHITE, win)
dash = Message(80, 300, 60, "Dash", title_font, WHITE, win)
tap_to_play = BlinkingText(WIDTH//2, HEIGHT-60, 20, "Choose Ball And Tap To Play", tap_to_play_font, WHITE, win)
game_msg = Message(80, 150, 40, "GAME", game_over_font, BLACK, win)
over_msg = Message(210, 150, 40, "OVER!", game_over_font, WHITE, win)
score_text = Message(90, 230, 20, "SCORE", None, BLACK, win)
best_text = Message(200, 230, 20, "BEST", None, BLACK, win)
noob = Message(90, 275, 30,"NOOB", None, BLACK, win)

score_msg = Message(WIDTH-60, 50, 50, "0", score_font, WHITE, win)

final_score_msg = Message(90, 280, 40, "0", tap_to_play_font, BLACK, win)
high_score_msg = Message(200, 280, 40, "0", tap_to_play_font, BLACK, win)

# SOUNDS **********************************************************************

score_fx = pygame.mixer.Sound('Arc Dash/Sounds/point.mp3')
death_fx = pygame.mixer.Sound('Arc Dash/Sounds/dead.mp3')
score_page_fx = pygame.mixer.Sound('Arc Dash/Sounds/score_page.mp3')

pygame.mixer.music.load('Arc Dash/Sounds/hk.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0)

# Button images

home_img = pygame.image.load('Arc Dash/Assets/homeBtn.png')
replay_img = pygame.image.load('Arc Dash/Assets/replay.png')
sound_off_img = pygame.image.load("Arc Dash/Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Arc Dash/Assets/soundOnBtn.png")
ball1_img = pygame.image.load("Arc Dash\\Assets\\ball_1.png")
ball2_img = pygame.image.load("Arc Dash\\Assets\\ball_2.png")
exit_img = pygame.image.load("exit.png")
# Buttons

home_btn = Button(home_img, (24, 24), WIDTH // 4 - 18, 390)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, 382)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, 390)
ball1_btn =Button(ball1_img,(50,50),WIDTH/2+20 , 380)
ball2_btn =Button(ball2_img,(50,50),WIDTH/2-50 , 380)
exit_btn =Button(exit_img,(50,50),5 , 5)
# GAME VARIABLES **************************************************************

MAX_RAD = 120#điểm tối đa ngoài rìa, khi chạm nó thì tính điểm
rad_delta = 50
#1 là ball 1,2 là ball 2 m, -1 là chưa chọn bâll
val_ball=-1


# OBJECTS *********************************************************************

ball_group = pygame.sprite.Group()
dot_group = pygame.sprite.Group()
shadow_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

p = Player(win)


#center[0] là width, [1] là height
ball_positions = [(CENTER[0]-105, CENTER[1]),
				  (CENTER[0]+105, CENTER[1]),
					(CENTER[0]-45, CENTER[1]),
				  (CENTER[0]+45, CENTER[1]),
					(CENTER[0], CENTER[1]-75),
				  (CENTER[0], CENTER[1]+75)]

#hàm enumerate() cho phép bạn truy nhập vòng lặp lần lượt qua các thành phần của một collection trong khi nó vẫn giữ index của item hiện tại.
#https://viblo.asia/p/tim-hieu-ham-enumerate-trong-python-translated-YWOZrgerlQ0
for index, pos in enumerate(ball_positions):
	if index in (0,1):
		type_ = 1
		inverter = 5
	if index in (2,3):
		type_ = 1
		inverter = 3
	if index in (4,5):
		type_ = 2
		inverter = 1
	ball = Balls(pos, type_, inverter, win)
#inverter là hệ số khi click vào là đổi chiều bóng enemi
# ball = Balls(ball_positions[0], 1, 5, win)
# print(ball_positions[5])
	ball_group.add(ball)


dot_list = [(CENTER[0], CENTER[1]-MAX_RAD+3), (CENTER[0]+MAX_RAD-3, CENTER[1]),
			(CENTER[0], CENTER[1]+MAX_RAD-3), (CENTER[0]-MAX_RAD+3, CENTER[1])]
dot_index = random.choice([1,2,3,4])
#có thể bỏ khúc này
# dot_pos = dot_list[dot_index-1]
# dot = Dot(*dot_pos, win)
# dot_group.add(dot)
#
# shadow = Shadow(dot_index, win)
# shadow_group.add(shadow)


# VARIABLES *******************************************************************

clicked = False
num_clicks = 0
player_alive = True
sound_on = True

score = 0
highscore = 0

home_page = True
game_page = False
score_page = False
with open(path_score) as f:
	high_score=int(f.read())
	highscore=high_score

running = True
while running:
	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 5)
	clock.tick(FPS)
	pygame.display.update()
	win.fill(color)
	# if score >2 :
	# 	FPS=100

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			#khi ấn esc hoặc q thì sẽ out game
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False
		if event.type == pygame.MOUSEMOTION:
			if ball1_btn.rect.collidepoint(pygame.mouse.get_pos()):
				ball1_btn = Button(ball1_img, (60, 60), WIDTH / 2 + 10, 380)
			elif ball2_btn.rect.collidepoint(pygame.mouse.get_pos()):
				ball2_btn = Button(ball2_img, (60, 60), WIDTH / 2 - 60, 380)
			elif exit_btn.rect.collidepoint(pygame.mouse.get_pos()):
				exit_btn = Button(exit_img, (55, 55), 5, 5)
			else:
				exit_btn = Button(exit_img, (50, 50), 5, 5)
				ball2_btn = Button(ball2_img, (50, 50), WIDTH / 2 - 50, 380)
				ball1_btn = Button(ball1_img, (50, 50), WIDTH / 2 + 20, 380)
		if home_page==True and val_ball>0:

			home_page = False
			game_page = True
			score_page = False

			rad_delta 	= 50
			clicked = True
			score = 0
			num_clicks = 0
			player_alive = True


		if event.type == pygame.MOUSEBUTTONDOWN and game_page==True :
			clicked = False
		if event.type == pygame.MOUSEBUTTONDOWN and game_page==True:

			if clicked==False:
				clicked = True
				for ball in ball_group:
					if num_clicks % ball.inverter == 0:
						ball.dtheta *= -1

				p.set_move(dot_index)

				num_clicks += 1
				if num_clicks % 5 == 0:
					color_index += 1
					if color_index > len(color_list) - 1:
						color_index = 0

					color = color_list[color_index]



	if home_page==True:

		#vẽ các vòng tròn và các khe rảnh ngoài home
		for radius in [30, 60, 90, 120]:
			pygame.draw.circle(win, (0,0,0), CENTER, radius, 8)
			pygame.draw.circle(win, (255,255,255), CENTER, radius, 5)

		pygame.draw.rect(win, color, [CENTER[0]-10, CENTER[1]-MAX_RAD, MAX_RAD+50, MAX_RAD])
		pygame.draw.rect(win, color, [CENTER[0]-MAX_RAD, CENTER[1]-10, MAX_RAD, MAX_RAD+50])

		arc.update()
		dash.update()

		tap_to_play.update()


		if ball1_btn.draw(win):
			val_ball=1
			# game_page=True

		if ball2_btn.draw(win):
			val_ball=2
			# game_page = True
		if exit_btn.draw(win):

			exec(open("Main_Game.py", encoding="utf8").read())


#giao diện sau khi thuâ hiện cái bảng điẻm ra
	if score_page==True:
		with open(path_score) as f:
			high_score = int(f.read())
			highscore = high_score

		game_msg.update()
		over_msg.update()
		score_text.update()
		best_text.update()

		if score==0:
			noob.update()
		else:
			final_score_msg.update(score, shadow=False)
		high_score_msg.update(highscore, shadow=False)





		if home_btn.draw(win):

			home_page = True
			score_page = False
			game_page = False
			score_msg = Message(WIDTH - 60, 50, 50, "0", score_font, WHITE, win)
			score = 0
			val_ball=-1

		if replay_btn.draw(win):

			home_page = False
			score_page = False
			game_page = True

			FPS=60
			player_alive = True
			score = 0
			score_msg = Message(WIDTH-60, 50, 50, "0", score_font, WHITE, win)
			p = Player(win)


		if sound_btn.draw(win):
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if game_page==True :

		#vẽ 4 vòng tròn trong game
		for radius in [30 + rad_delta, 60 + rad_delta, 90 + rad_delta, 120 + rad_delta]:
			if rad_delta > 0:
				radius -= 1
				rad_delta -= 0.3
			# vẽ các vòng tròn trong game
			pygame.draw.circle(win, (0,0,0), CENTER, radius, 5)

		#vẽ chòng lên màu để tưởng có các rảnh khe hở
		pygame.draw.rect(win, color, [CENTER[0]-10, CENTER[1]-MAX_RAD, 20, MAX_RAD*2])
		pygame.draw.rect(win, color, [CENTER[0]-MAX_RAD, CENTER[1]-10, MAX_RAD*2, 20])

		if rad_delta <= 0 :
			# vẽ ra đường dẫn bóng
			shadow_group.update()
			p.update(player_alive, color, shadow_group,val_ball)
			#show ra các enemi
			ball_group.update()
			#in ra dot phía đối diện
			dot_group.update()
			#hiệu ứng vở bóng khi chết
			particle_group.update()
			#in ra điểm
			score_msg.update(score)

			#kiểm tra khi player chạm vào bóng đối diện thì sẽ tăng điểm
			for dot in dot_group:
				#sử lý khi va chạm với bóng trắng ngoài rìa
				if dot.rect.colliderect(p):
					dot.kill()
					score_fx.play()

					score += 1
					if score >highscore :
						highscore = score

						with open(path_score, mode='w') as f:
							str_sc = str(highscore)
							f.write(str_sc)


			#kiểm tra xem player chạm vào các ball enemi
			if pygame.sprite.spritecollide(p, ball_group, False) and player_alive==True:
				death_fx.play()
				#lấy vị trí bóng vỡ (die)
				x, y = p.rect.center
				for i in range(20):
					#vị trí mà khi bóng vở tạo effect bóng vở
					particle = Particle(x, y, WHITE, win)
					particle_group.add(particle)
				player_alive = False
				p.reset()


			if p.can_move==True and len(dot_group) == 0 and player_alive==True :
				dot_index = random.randint(1,4)
				dot_pos = dot_list[dot_index-1]
				dot = Dot(*dot_pos, win,dot_index,val_ball)
				dot_group.add(dot)

				shadow_group.empty()
				shadow = Shadow(dot_index, win)
				shadow_group.add(shadow)

			if not player_alive and len(particle_group) == 0:
				game_page = False
				score_page = True



				# dot_group.empty()
				# shadow_group.empty()
				for ball in ball_group:
					ball.reset()
				score_page_fx.play()





pygame.quit()