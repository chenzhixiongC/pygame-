#-*-coding:utf-8 -*-
import pygame, sys
import random
import logging
import time
logging.basicConfig(filename='./log/实验结果.log', level=logging.INFO)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen.get_rect()
pygame.display.set_caption("打气球游戏")

balloon_width = 0.18*screen_rect.width
start_button_width = 0.2*screen_rect.width
blow_button_width = 0.14*screen_rect.width
end_button_width = 0.2*screen_rect.width

class BALOON(object):

    def __init__(self, screen, balloon_width, bottom_bias):
        self.baloon = pygame.image.load('./picture/气球.png')
        self.rect = self.baloon.get_rect()
        self.rate = balloon_width/self.rect.width

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.flat_rate = 1.1
        self.bottom_bias = bottom_bias
        self.limit = 10
        self.broken = pygame.image.load('./picture/爆炸.png')
        self.broken_rect = self.broken.get_rect()
        self.broken_rate = 2*balloon_width/self.broken_rect.width
        self.baloon = pygame.transform.scale(self.baloon,
                                             (int(self.rate * self.rect.width), int(self.rate * self.rect.height)))
        self.rect = self.baloon.get_rect()
        self.default_rect = self.baloon.get_rect()
        self.broken = pygame.transform.scale(self.broken,(int(self.broken_rate * self.broken_rect.width), int(self.broken_rate * self.broken_rect.height)))
        self.broken_rect = self.broken.get_rect()
        print(self.default_rect, self.rect)

    def reset(self):
        self.baloon = pygame.image.load('./picture/气球.png')
        self.rect = self.baloon.get_rect()
        # self.rate = 150 / self.rect.width

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.flat_rate = 1.1
        self.limit = 10
        self.broken = pygame.image.load('./picture/爆炸.png')
        self.broken_rect = self.broken.get_rect()
        # self.broken_rate = 300 / self.broken_rect.width
        self.baloon = pygame.transform.scale(self.baloon,
                                             (int(self.rate * self.rect.width), int(self.rate * self.rect.height)))
        self.rect = self.baloon.get_rect()
        self.default_rect = self.baloon.get_rect()
        self.broken = pygame.transform.scale(self.broken, (
        int(self.broken_rate * self.broken_rect.width), int(self.broken_rate * self.broken_rect.height)))
        self.broken_rect = self.broken.get_rect()


    def show(self):
        print('show:', self.rect)
        self.screen.blit(self.baloon, ((self.screen_rect.width - self.rect.width)//2, (self.screen_rect.height - self.rect.height - self.bottom_bias)))

    def inflation(self):
        self.rect.width = (self.rect.width) * (self.flat_rate)
        self.rect.height = (self.rect.height) * (self.flat_rate)
        self.baloon = pygame.transform.smoothscale(self.baloon, (self.rect.width, self.rect.height))
        self.rect = self.baloon.get_rect()



    def is_blowout(self):
        if random.random() < 1/self.limit:
            return True
        self.limit -= 1
        return False

    def blowout(self):
        pygame.mixer.init()
        pygame.mixer.music.load('./music/explosionMax_22k16bMono.wav')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=0, start=0.0)
        self.screen.blit(self.broken, ((self.screen_rect.width - self.broken_rect.width) // 2,
                                       (self.screen_rect.height - self.broken_rect.height - self.bottom_bias*2)))


class BOARD(object):

    def __init__(self, screen, bias, info):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.score = 0
        self.info = info
        self.bias = bias
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('songtittc', 48)
        self.score_str = self.info + "：{:,}".format(self.score)

    def reset(self):
        self.score = 0
        self.get_scores(0)



    def get_scores(self, x):
        self.score += x
        self.score_str = self.info + "：{:,}".format(self.score)

    def show_board(self):
        self.score_image = self.font.render(self.score_str, True, self.text_color,
                                            (0, 0, 0))
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - self.bias[0]
        self.score_rect.top = self.bias[1]
        self.screen.blit(self.score_image, self.score_rect)

    def get_score(self):
        return self.score

    def clear(self):
        pass


class BUTTON(object):
    def __init__(self, screen, path, size=None):
        """初始化按钮属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.button = pygame.image.load(path)
        self.rect = self.button.get_rect()
        self.rate = 200/self.rect.width
        if size:
            self.rate = size / self.rect.width
        # self.rect.width *= self.rate
        # self.rect.height *= self.rate
        self.button = pygame.transform.scale(self.button, (int(self.rate*self.rect.width), int(self.rate*self.rect.height)))
        self.rect = self.button.get_rect()

        # 创建按钮的rect对象，并使其居中
        self.rect.center = self.screen_rect.center
        self.rect.bottom = self.screen_rect.bottom


    def show_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        print(self.rect)
        self.screen.blit(self.button, self.rect)

    def is_click(self, pos):
        return self.rect.collidepoint(pos)

class ENDBUTTON(BUTTON):
    def __init__(self, screen, path, size=None):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.button = pygame.image.load(path)
        self.rect = self.button.get_rect()
        self.rate = 180 / self.rect.width
        if size:
            self.rate = size / self.rect.width
        # self.rect.width *= self.rate
        # self.rect.height *= self.rate
        self.button = pygame.transform.scale(self.button,
                                             (int(self.rate * self.rect.width), int(self.rate * self.rect.height)))
        self.rect = self.button.get_rect()

        # 创建按钮的rect对象，并使其居中
        self.rect.left = self.screen_rect.left + 20
        self.rect.centery = self.screen_rect.centery

class ROUNDBOARD(BOARD):
    def __init__(self, screen, bias, info):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.score = 10
        self.info = info
        self.bias = bias
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('songtittc', 48)
        self.score_str = self.info + "：{:,}".format(self.score)

    def reset(self):
        self.score = 10
        self.get_scores(0)

    def min_one(self):
        self.score -= 1
        self.get_scores(0)

    def get_score(self):
        return self.score

class END(object):
    def __init__(self):
        self.draw_text = "游戏结束！最终得分：{}！感谢！"
        self.font = pygame.font.SysFont('songtittc', 48)

    def show(self, score):
        text = self.font.render(self.draw_text.format(score), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = screen.get_rect().center
        screen.blit(text, text_rect)






def refresh(cur_board=None, total_board=None, blow_button=None, baloon=None, end_button=None, start_button=None, round_board=None):
    if cur_board:
        cur_board.show_board()
    if total_board:
        total_board.show_board()
    if blow_button:
        blow_button.show_button()
    if baloon:
        baloon.show()
    if end_button:
        end_button.show_button()
    if start_button:
        start_button.show_button()
    if round_board:
        round_board.show_board()
# baloon_ = BALOON(screen, balloon_width, 80)
# cur_board = BOARD(screen, (30, 90), u"本轮得分")
# total_board = BOARD(screen, (30, 20), u"总得分")
# round_board = ROUNDBOARD(screen, (30, 160), u"剩余轮次")
# blow_button = BUTTON(screen, './picture/1.png', size=blow_button_width)
# end_button = ENDBUTTON(screen, './picture/结束2号.png', size=end_button_width)
# start_button = BUTTON(screen, './picture/开始3.png', size=start_button_width)
# end_scene = END()
# refresh(cur_board=cur_board, total_board=total_board, start_button=start_button, end_button=end_button,
#         baloon=baloon_, round_board=round_board)

rebuild = False
restart = True
count = 1
while True:
    for event in pygame.event.get():
        # 需要开始下一件事情前
        if count > 1 and restart:
            time.sleep(3)

        # 这是一件不需要触发的事情
        if restart:
            logging.info('第 %d 个同学开始实验, 实验结果如下：' % count)
            restart = False
            screen.fill((0, 0, 0))
            baloon_ = BALOON(screen, balloon_width, 80)
            cur_board = BOARD(screen, (30, 90), u"本轮得分")
            total_board = BOARD(screen, (30, 20), u"总得分")
            round_board = ROUNDBOARD(screen, (30, 160), u"剩余轮次")
            blow_button = BUTTON(screen, './picture/1.png', size=blow_button_width)
            end_button = ENDBUTTON(screen, './picture/结束2号.png', size=end_button_width)
            start_button = BUTTON(screen, './picture/开始3.png', size=start_button_width)
            end_scene = END()
            refresh(cur_board=cur_board, total_board=total_board, start_button=start_button, end_button=end_button,
                    baloon=baloon_, round_board=round_board)
            pygame.display.flip()
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 重建画布

            if rebuild:
                screen.fill((0, 0, 0))
                if round_board.get_score() == 0:
                    end_scene.show(total_board.get_score())
                    pygame.display.flip()
                    logging.info('第 {} 个同学结束实验, 总得分为 {}'.format(count, total_board.get_score()))
                    count += 1
                    restart = True
                    clock = pygame.time.Clock()
                    time_counter = clock.tick()
                    time_counter = 0
                    continue
                else:
                    baloon_.reset()

                    refresh(cur_board=cur_board, total_board=total_board, start_button=start_button, baloon=baloon_,
                            end_button=end_button, round_board=round_board)
                    # 终于点击了
                    if event.type == pygame.MOUSEBUTTONDOWN and start_button.is_click(event.pos):
                        # 终于可以开始吹气了
                        screen.fill((0, 0, 0))
                        baloon_.reset()
                        round_board.min_one()
                        refresh(cur_board=cur_board, total_board=total_board, blow_button=blow_button, baloon=baloon_,
                                end_button=end_button, round_board=round_board)
                        rebuild = False
                    else:
                        continue
            elif blow_button.is_click(event.pos):
                screen.fill((0, 0, 0))
                refresh(end_button=end_button)
                # 气球爆炸的情况
                if baloon_.is_blowout():
                    logging.info('气球爆炸，得分0')
                    # 重新绘制画面并进行气球爆炸
                    baloon_.blowout()
                    refresh(start_button=start_button, cur_board=cur_board, total_board=total_board, round_board=round_board)
                    cur_board.reset()
                    rebuild = True
                else:
                    baloon_.inflation()
                    baloon_.show()
                    cur_board.get_scores(1)
                    refresh(cur_board=cur_board, total_board=total_board, blow_button=blow_button, round_board=round_board)
            elif end_button.is_click(event.pos):
                logging.info('主动获取分数，得分%d'%cur_board.score)
                screen.fill((0, 0, 0))
                total_board.get_scores(cur_board.score)
                cur_board.reset()
                rebuild = True
                refresh(cur_board=cur_board, total_board=total_board, start_button=start_button, baloon=baloon_,
                        end_button=end_button, round_board=round_board)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        pygame.display.flip()