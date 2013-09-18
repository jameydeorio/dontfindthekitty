import ConfigParser


class Constants:
    CONFIG = ConfigParser.ConfigParser()
    CONFIG.read('data/config.ini')

    ZOO_WIDTH = 10
    ZOO_HEIGHT = 10

    ADJECTIVES = [line.strip('\n') for line in open('data/adjectives.txt', 'r')]
    CREATURES = [line.strip('\n') for line in open('data/creatures.txt', 'r')]
