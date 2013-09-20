#!/usr/bin/env python

import os
import random
import sys
import pygame
import pygcurse
from classes.message_panel import MessagePanel

from helpers.constants import Constants
from classes.zookeeper import Zookeeper
from classes.creatures import Creature
from classes.zoo_map import ZooMap


class Game:
    def __init__(self):
        self.window = pygcurse.PygcurseWindow(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Don't Find The Kitty")
        font_name = Constants.CONFIG.get('game', 'font')
        font_size = Constants.CONFIG.getint('game', 'font_size')
        self.window.font = pygame.font.Font(os.path.join(Constants.RES_DIR, font_name), font_size)
        self.window.autoupdate = False
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        self.zookeeper = Zookeeper(Constants.CONFIG.get('zookeeper', 'character'))
        self.creatures = [Creature() for n in range(29)]
        self.creatures.append(Creature(creature='kitty'))
        self.zoo_map = ZooMap()
        self.zoo_map.place_creatures(self.creatures)
        self.message_panel = MessagePanel(0, Constants.ZOO_HEIGHT)

    def run(self):
        while 1:
            self.clock.tick(Constants.FPS)

            self.window.setscreencolors(None, 'black', clear=True)

            # input
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    xpos, ypos = self.window.getcoordinatesatpixel(event.pos)
                    self.zookeeper.capture(self.zoo_map, xpos, ypos)

            # compute
            for row in self.zoo_map.grid:
                for thing in row:
                    if thing and random.choice(range(Constants.CONFIG.getint('creatures', 'chance_to_move'))) == 1:
                        thing.move(self.zoo_map)

            # draw
            self.render()

    def render(self):
        self.zoo_map.draw(self.window)
        self.message_panel.write_captures(self.window, self.zookeeper.captures[-self.message_panel.length:])
        self.zookeeper.draw(self.window, pygame.mouse.get_pos())
        self.window.update()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
