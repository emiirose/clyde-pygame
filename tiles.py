import pygame, csv, os

PELLETIMG = "pac_man_egg.png"


class Pellet():

    def __init__(self, x, y):

        self.image = pygame.image.load(PELLETIMG)
        self.image.set_colorkey((84, 84, 84))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Tile(pygame.sprite.Sprite):

    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap():

    def __init__(self, filename, spritesheet):
        self.tile_size = 32
        self.spritesheet = spritesheet
        self.tiles, self.pellets = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)
        for pellet in self.pellets:
            pellet.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
            return map

    def load_tiles(self, filename):
        tiles = []
        pellets = []
        map = self.read_csv(filename)
        x, y = 0, 0
        z = 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '-1':
                    pellets.append(Pellet(x * self.tile_size, y * self.tile_size))
                elif tile == '0':
                    tiles.append(
                        Tile('yellowTop.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '1':
                    tiles.append(
                        Tile('redTop.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(
                        Tile('pinkTop.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '3':
                    tiles.append(
                        Tile('blueTop.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '4':
                    tiles.append(
                        Tile('purpleTop.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '5':
                    tiles.append(
                        Tile('greenTop.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '6':
                    tiles.append(
                        Tile('yellowBottom.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '7':
                    tiles.append(
                        Tile('redBottom.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '8':
                    tiles.append(
                        Tile('pinkBottom.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '9':
                    tiles.append(
                        Tile('blueBottom.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '10':
                    tiles.append(
                        Tile('purpleBottom.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                elif tile == '11':
                    tiles.append(
                        Tile('greenBottom.png', x * self.tile_size,
                             y * self.tile_size, self.spritesheet))
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        self.pmStartX = pellets[0].rect.x
        self.pmStartY = pellets[0].rect.y
        self.pcStartX = pellets[len(pellets)-1].rect.x
        self.pcStartY = pellets[len(pellets)-1].rect.y
        self.start_x = pellets[(len(pellets)-1)//2].rect.x
        self.start_y = pellets[(len(pellets)-1)//2].rect.y

        return tiles, pellets
