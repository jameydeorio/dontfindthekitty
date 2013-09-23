#!/usr/bin/env python

import os
import random
import sys
import urllib
import webbrowser
import pygame
import pygcurse
from classes.button import Button
from classes.message_panel import MessagePanel
from classes.panel import Panel

from helpers.constants import Constants
from classes.zookeeper import Zookeeper
from classes.creature import Creature
from classes.zoo_map import ZooMap


# TODO: End screen is too big and clunky. Refactor.


class Game(object):
    def __init__(self):
        self.window = pygcurse.PygcurseWindow(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Don't Find The Kitty")
        font_name = Constants.CONFIG.get('game', 'font')
        font_size = Constants.CONFIG.getint('game', 'font_size')
        self.window.font = pygame.font.Font(os.path.join(Constants.RES_DIR, font_name), font_size)
        self.window.autoupdate = False
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        self.zookeeper = Zookeeper(Constants.CONFIG.get('zookeeper', 'character'))
        self.creatures = [Creature() for n in range(5)]
        self.kitty = Creature(creature='kitty')
        self.zoo_map = ZooMap()
        self.zoo_map.place_creatures(self.creatures + [self.kitty])
        self.message_panel = MessagePanel(0, Constants.ZOO_HEIGHT)
        self.last_captured = Creature()

        self.lost = False

    def run(self):

        while 1:
            self.clock.tick(Constants.FPS)

            self.window.setscreencolors(None, 'black', clear=True)
            self.window.fill(bgcolor=Constants.ZOO_BG_COLOR, region=(1, 1, Constants.ZOO_WIDTH - 2, Constants.ZOO_HEIGHT - 2))

            # input
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    xpos, ypos = self.window.getcoordinatesatpixel(event.pos)
                    if 0 < xpos < Constants.ZOO_WIDTH and 0 < ypos < Constants.ZOO_HEIGHT:
                        captured = self.zookeeper.capture(self.zoo_map, xpos, ypos)
                        if captured:
                            self.last_captured = captured

            if self.last_captured and self.last_captured.creature == 'kitty':
                self.end_screen()

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

    def end_screen(self):
        kitty_panel = Panel(region=(12, 5, 36, 5), fgcolor='white', bgcolor='gray', border=True, shadow=True)
        kitty_panel.text = 'Play again?'

        buttons = []

        yes_button = Button(region=(18, 8, 6, 1), fgcolor=pygame.Color(0, 100, 0), bgcolor='white')
        yes_button.text = ' yes'
        buttons.append(yes_button)

        no_button = Button(region=(28, 8, 6, 1), fgcolor=pygame.Color(100, 0, 0), bgcolor='white')
        no_button.text = '  no'
        no_button.action = lambda: sys.exit(0)
        buttons.append(no_button)

        tweet_button = Button(region=(38, 8, 6, 1), fgcolor=pygame.Color(0, 0, 255), bgcolor='white')
        tweet_button.text = 'tweet'
        twitter_text = "I found the kitty! {sex} was {adjective}.".format(
            sex=self.kitty.sex.capitalize(),
            adjective=self.kitty.adjective,
        )
        twitter_url = 'https://twitter.com/intent/tweet?text={text}&hashtags={hashtags}&via={via}&url={url}'.format(
            text=urllib.quote(twitter_text),
            hashtags='dontfindthekitty',
            via='jameydeorio',
            url='http://jameydeorio.com',
        )
        tweet_button.action = lambda: webbrowser.open(twitter_url)
        buttons.append(tweet_button)

        while 1:
            self.clock.tick(Constants.FPS)

            self.window.setscreencolors(None, 'black', clear=True)
            self.window.fill(bgcolor=Constants.ZOO_BG_COLOR, region=(1, 1, Constants.ZOO_WIDTH - 2, Constants.ZOO_HEIGHT - 2))

            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    xpos, ypos = self.window.getcoordinatesatpixel(event.pos)
                    if 0 < xpos < Constants.ZOO_WIDTH and 0 < ypos < Constants.ZOO_HEIGHT:
                        for button in buttons:
                            if button.contains(xpos, ypos):
                                button.execute()

            self.zoo_map.draw(self.window)
            self.message_panel.write_captures(self.window, self.zookeeper.captures[-self.message_panel.length:])

            kitty_panel.draw(self.window)

            for button in buttons:
                button.draw(self.window)

            self.zookeeper.draw(self.window, pygame.mouse.get_pos())
            self.window.update()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
