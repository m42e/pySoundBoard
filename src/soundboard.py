#!/usr/bin/env python3
# Place sounds in sounds folder in sound_ij.wav format
# being i row number and j column number (starting at 0)

import pygame
import json
from pygame.locals import *

# variables
size = [800, 480]

with open('config.json') as cf:
    config = json.load(cf)

# colors
red = (237, 85, 101)
orange = (252, 110, 81)
yellow = (255, 206, 84)
yellow2 = (246, 187, 66)
green = (160, 212, 104)
green2 = (140, 193, 82)
turquoise = (72, 207, 173)
blue = (79, 193, 233)
purple = (93, 156, 236)
black = (0, 0, 0)
white = (255, 255, 255)
dark = (30, 30, 30)
grey = (150, 150, 150)
grey2 = (20, 20, 20)

# initialize game engine
pygame.mixer.pre_init(44100, -16, 2, 512)  # fixes delay in play
pygame.init()

# init channels
pygame.mixer.set_num_channels(len(config['sounds']))

# set screen width/height and caption
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.display.set_caption('pySoundBoard')

# init fonts
#fontObj = pygame.font.Font('res/Hyperspace.otf', int(spacing/2.5))
#fontnames = pygame.font.Font('res/pragmata.otf', 12)

def get_button_size(config, extra=0):
    button_x = (config['ui']['size'][0] - (config['ui']['columns']+1)*config['ui']['spacing'])/config['ui']['columns']
    button_y = (config['ui']['size'][1] - (config['ui']['rows']+1)*config['ui']['spacing'])/config['ui']['rows']
    return button_x+extra, button_y+extra

def get_button_coordinates(config, i):
    bx, by = get_button_size(config)
    offset_x = bx + config['ui']['spacing']
    offset_y = by + config['ui']['spacing']

    x = (i%config['ui']['columns'])*offset_x + config['ui']['spacing']
    y = (i//config['ui']['columns'])*offset_y + config['ui']['spacing']
    return (x,y)


def makebuttons(config):
    '''generate sound button objects according to the number of
    rows'''
    data = []
    for j, sound in enumerate(config['sounds']):
        data.append({
            'soundchannel': pygame.mixer.Channel(j),
            'soundobj': pygame.mixer.Sound(sound['sound']),
            'coord': get_button_coordinates(config, j),
            'size': get_button_size(config),
            'path': sound['sound'],
            'rectobj': pygame.Rect(*get_button_coordinates(config, j), *get_button_size(config)),
            'color': grey,
            'loop': False
        })
    return data



# make the initial set of objects
buttons = makebuttons(config)

# initialize clock. used later in the loop.
clock = pygame.time.Clock()

paused = False

# Loop until the user clicks close button
done = False
while done == False:
    # clear the screen before drawing
    screen.fill(dark)
    # draw border
    pygame.draw.rect(screen, grey2, (0, 0, size[0], size[1]), 1)
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for elem in data:
                if elem['rectobj'].collidepoint(pos):
                    if elem['soundchannel'].get_busy():
                        elem['soundchannel'].stop()
                        pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                       elem['coord'][1]-6, *get_button_size(config, 12)), 5)
                    else:
                        elem['soundchannel'].play(elem['soundobj'])
                        pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                       elem['coord'][1]-6, *get_button_size(config, 12)), 5)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == rightB:
            pos = pygame.mouse.get_pos()
            for elem in data:
                if elem['rectobj'].collidepoint(pos):
                    if elem['soundchannel'].get_busy():
                        elem['soundchannel'].fadeout(fadeout)
                        pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                       elem['coord'][1]-6, *get_button_size(config, 12)), 5)
                    else:
                        elem['soundchannel'].play(
                            elem['soundobj'], fade_ms=fadein)
                        pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                       elem['coord'][1]-6, *get_button_size(config, 12)), 5)
    # write game logic here
    pos = pygame.mouse.get_pos()
    for elem in data:
        if elem['soundchannel'].get_busy():
            elem['color'] = yellow
        else:
            if elem['path'] == 'sounds/fallback.wav':
                elem['color'] = grey
            else:
                elem['color'] = green
        if elem['rectobj'].collidepoint(pos):
            pygame.draw.rect(screen, orange, (elem['coord'][0]-6,
                                              elem['coord'][1]-6, *get_button_size(config, 12)), 1)
    # write draw code here
    for elem in data:
        pygame.draw.rect(screen, elem['color'], elem['rectobj'])

    # display what’s drawn. this might change.
    pygame.display.update()
    # run at 20 fps
    clock.tick(20)

# close the window and quit
pygame.quit()
