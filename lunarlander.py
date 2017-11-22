#!/usr/bin/python

# original lander graphic from Flaticon: www.flaticon.com

import sys
import time
from enum import Enum
import pygame
from pygame.locals import *


class State(Enum):
    paused, countdown, playing, end = range(4)


def display_centered(screen, text):
    text = big_font.render(text, 1, WHITE)
    text_pos = text.get_rect()
    text_pos.move_ip((SCREEN_WIDTH - text_pos.w)/2 , (SCREEN_HEIGHT - text_pos.h)/2)
    screen.blit(text, text_pos)


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = 0, 0, 0
WHITE = 255, 255, 255

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Lunar Lander')
clock = pygame.time.Clock()

lander = pygame.image.load('lander.png').convert_alpha()
lander_start = lander.get_rect().move((SCREEN_WIDTH - lander.get_rect().w)/2, 100)
lander_pos = lander_start.copy()

small_font = pygame.font.Font(None, 18)
big_font = pygame.font.Font(None, 36)

thrusting = False
left = False
right = False
fuel = 100
speed = 0
gravity = 0.5
state = State.countdown
countdown_start = None
timer_text = None

while True:
    time_passed = clock.tick(50)

    horiz = 0
    thrust = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_UP:
                thrusting = True
            elif event.key == K_LEFT:
                left = True
            elif event.key == K_RIGHT:
                right = True
            elif event.key == K_SPACE:
                if state == State.paused:
                    state = State.playing
                elif state == State.playing:
                    state = State.paused
            elif event.key == K_RETURN and state is not State.countdown:
                # reset
                speed = 0
                fuel = 100
                lander_pos = lander_start.copy()
                state = State.countdown
        elif event.type == KEYUP:
            if event.key == K_UP:
                thrusting = False
            elif event.key == K_LEFT:
                left = False
            elif event.key == K_RIGHT:
                right = False

    if state is State.countdown:
        if countdown_start:
            timer = time.time() - countdown_start
            if timer < 1:
                timer_text = 'Ready...'
            elif timer < 2:
                timer_text = 'Set...'
            elif timer < 3:
                timer_text = 'Go!'
            else:
                countdown_start = None
                state = State.playing
        else:
            countdown_start = time.time()
            continue
    elif state is State.playing:
        if fuel > 0:
            if thrusting:
                thrust = 1
                fuel -= 1
            if left:
                horiz -= 4
                fuel -= 1
            if right:
                horiz += 4
                fuel -= 1

        accel = gravity - thrust
        speed += accel

    if state == State.playing and lander_pos.y + lander_pos.h < SCREEN_HEIGHT:
        lander_pos.move_ip(horiz, speed)
        if lander_pos.y + lander_pos.h > SCREEN_HEIGHT:
            state = State.end
            lander_pos.y = SCREEN_HEIGHT - lander_pos.h


    screen.fill(BG_COLOR)

    fuel_label = small_font.render('fuel', 1, WHITE)
    fuel_label_pos = fuel_label.get_rect()
    fuel_label_pos.move_ip(10, 25)
    screen.blit(fuel_label, fuel_label_pos)

    speed_label = small_font.render('speed', 1, WHITE)
    speed_label_pos = speed_label.get_rect()
    speed_label_pos.move_ip(SCREEN_WIDTH - speed_label_pos.w - 10, 25)
    screen.blit(speed_label, speed_label_pos)

    if state is State.end:
        result_text = 'Final speed: {v}'.format(v=speed)
        display_centered(screen, result_text)
    elif state is State.countdown:
        display_centered(screen, timer_text)
    elif state is State.paused:
        display_centered(screen, 'Paused')

    fuel_bar_box = pygame.Rect(10, 10, 100, 10)
    fuel_bar = pygame.Rect(10, 10, fuel, 10)
    pygame.draw.rect(screen, WHITE, fuel_bar_box, 1)
    pygame.draw.rect(screen, WHITE, fuel_bar)

    speed_box = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 10)
    speed_bar = pygame.Rect(SCREEN_WIDTH - 60, 10, max(-50, min(speed, 50)), 10)
    pygame.draw.rect(screen, WHITE, speed_box, 1)
    pygame.draw.rect(screen, WHITE, speed_bar)

    screen.blit(lander, lander_pos)
    pygame.display.flip()
