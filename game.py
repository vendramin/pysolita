#!/usr/bin/python
import sys
import random
import pygame
import sys
import config

from pygame.locals import *
from copy import copy

class Mouse(pygame.sprite.DirtySprite):
    def __init__(self, filename):
        super(Mouse, self).__init__()
        pygame.mouse.set_visible(False)
        self.load_image(filename)
        self.default = self.image
        self.rect = self.image.get_rect()
        self.dirty = 2 

    def load_image(self, filename=None):
        if filename == None:
            self.image = self.default
        else:
            self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()

    def set_image(self, image=None):
        if image != None:
            self.image = image 
            self.rect = self.image.get_rect()
        else:
            self.image = self.default
            self.rect = self.image.get_rect()

    def get_pos(self):
        return pygame.mouse.get_pos()

    def set_pos(self, position):
        pygame.mouse.set_pos(position)

    def update(self):
        self.rect.center = self.get_pos()

class Text(pygame.sprite.DirtySprite):
    def __init__(self, filename=None, size=40):
        super(Text, self).__init__()
        self.font = pygame.font.Font(filename, size)
        self.msg = None
        self.color = Color('black')
        self.antialias = True
        self.update()
        self.rect = self.image.get_rect()
        self.dirty = 2

    def set_color(self, color):
        self.color = color

    def update(self):
        if not self.msg == None: 
            self.rect = self.image.get_rect(centerx=config.w/2)
        self.image = self.font.render(self.msg, self.antialias, self.color)

class Game(object):
    def __init__(self): 
        pygame.init()
           
        self.screen = pygame.display.set_mode((config.w, config.h), HWSURFACE|DOUBLEBUF)
        pygame.display.set_caption("PySolita")
   
        self.text = Text('gui/font.ttf')
        self.mouse = Mouse('gui/cursor.png')

        self.background = pygame.image.load(config.path + 'background.png').convert()
        self.screen.blit(self.background, (0, 0))
        
        pygame.display.flip()

        self.xray_mode = False
        self.message = Message()
        
    def init(self):

        self.looser = False
        self.played = 0
        self.bad = 0

        self.mycard = None
        self.deck = Deck(False) 
        self.table = Table(self.deck)

        self.sprites = pygame.sprite.LayeredDirty()
        self.mycards = pygame.sprite.LayeredDirty()

        self.cols = {}

        for i in range(4):
            card = self.deck.pickup_one_card()
            posx = (config.w-(config.n-1)*config.card_w)/2
            card.set_position(posx+i*config.card_w, 2*posx+4*config.card_h)
            card.set_as_mine()
            self.mycards.add(card)
            self.sprites.add(card)

        for y in range(1, config.n):
            self.cols[y] = []

        for x in range(1,5):
            for y in range(1, config.n):
                card = self.deck.pickup_one_card()
                card.set_position(posx+(y-1)*config.card_w, posx+config.card_h*(x-1))
                self.cols[y].append(card.rect)
                self.table.add(card)
                self.sprites.add(card)

        self.sprites.add(self.text, layer=self.sprites.get_top_layer()+1)
        self.sprites.add(self.mouse, layer=self.sprites.get_top_layer()+1)

    def run(self, screen=None):
        self.quit = 0
        clock = pygame.time.Clock()
        while not self.quit:
            clock.tick(60)
            self.loop()

    def bad_card(self, card):
        self.bad = self.bad+1
        posx = (config.w-(config.n-1)*config.card_w)/2
        card.set_position(config.w-posx-self.bad*config.card_w, 2*posx+4*config.card_h)
        self.sprites.add(card)
 
    def loop(self):

        if self.played == 13*4-4:
            self.message.set_message('winner')
            self.sprites.add(self.message)
        else:
            if self.bad==4:
                self.looser = True
                self.message.set_message('looser')
                self.sprites.add(self.message)

        if self.mycard != None:
            if self.mycard.number == config.n:
                tmp = self.mycard
                self.mycard.kill()
                self.mycard = None
                print 'sonaste'
                self.mouse.set_image()
                self.bad_card(tmp)
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                pass
            elif event.type == MOUSEBUTTONDOWN:
                self.on_mouse_button_down()
            elif event.type == MOUSEBUTTONUP:
                pass
            elif event.type == KEYUP:
                pass
            elif event.type == KEYDOWN:
                if event.key == K_t:
                    self.text.visible = not self.text.visible
                if event.key == K_f:
                    self.sprites.add(self.message)
                if event.key == K_r or event.key == K_SPACE:
                    self.mouse.set_image()
                    self.init()
                if event.key == K_RETURN:
                    for card in self.table.sprites():
                        card.flip()
                if event.key == K_x:
                    self.xray_mode = not self.xray_mode
                if event.key == K_w:
                    x, y = self.mouse.get_pos()
                    for card in self.table.sprites():
                        if pygame.Rect(card.rect).collidepoint(x,y):
                            print card.number, card.suit
 
        self.on_mouse_motion()
        self.text.update()
        self.draw()

    def on_mouse_motion(self):
        if self.xray_mode:
            x, y = self.mouse.get_pos()
            for card in self.table.sprites():
                        if pygame.Rect(card.rect).collidepoint(x,y):
                            self.text.msg = 'X-ray mode: {0}{1}'.format(card.number, card.suit)
        
    def on_mouse_button_down(self):
        x, y = self.mouse.get_pos()
        if self.mycard != None:
            for r in self.cols[self.mycard.number]:
                if r.collidepoint(x,y):
                    for card in self.table.sprites():
                        if pygame.Rect(card.rect).collidepoint(x,y):
                            for n, r in self.table.lines.items():
                                if r.collidepoint(x,y):
                                    if not n in self.table.suits.keys():
                                        if not self.mycard.suit in self.table.suits.values():
                                            self.table.suits[n] = self.mycard.suit
                                        else:
                                            return
                                    else:
                                        if self.mycard.suit != self.table.suits[n]:
                                            return

                            card.kill()
                            card.flip()
                            self.mycard.kill()
            
                            tmp = card
                            card = self.mycard
                            card.rect = copy(tmp.rect)
            
                            self.mycard = tmp
            
                            self.table.add(card)
                            self.mycards.add(self.mycard)
                            self.sprites.add(card)
            
                            self.mouse.set_image(self.mycard.image)
                            self.played = self.played + 1

        for card in self.mycards:
            if pygame.Rect(card.rect).collidepoint(x,y) and self.mycard == None:
                self.mycard = card
                self.mycard.flip()
                self.mycards.remove(self.mycard)
                self.mouse.set_image(self.mycard.image)
                self.mycard.kill()

        self.draw()

    def draw(self):
        self.sprites.clear(self.screen, self.background)
        self.sprites.update()
        pygame.display.update(self.sprites.draw(self.screen))

class Table():
    def __init__(self, deck):
        self.deck = deck
        self.x = (config.w - (config.n-1)*config.card_w)/2
        self.y = config.h-self.x
        self.w = config.n*config.card_w
        self.h = 4*config.card_h

        self.lines = { 
            1: pygame.Rect(0, self.x, self.w, config.card_h), 
            2: pygame.Rect(0, config.card_h+self.x, self.w, config.card_h),
            3: pygame.Rect(0, config.card_h*2+self.x, self.w, config.card_h),
            4: pygame.Rect(0, config.card_h*3+self.x, self.w, config.card_h) 
        }

        self.suits = {}
        self.cards = pygame.sprite.LayeredDirty()

    def add(self, card):
        self.cards.add(card)
    def get_lines(self):
        return self.lines.values()
    def suit_of_line(self, n):
        return 
    def sprites(self):
        return self.cards.sprites()
        
class Deck():
    def __init__(self, classic=True):
        self.card_w = config.card_w
        self.card_h = config.card_h
        self.cards = []
        filename = config.path+'{0:02}{1}.gif'            

        for n in range(1,config.n+1):
            for s in config.suits:
                self.cards.append(Card(n, s, filename.format(n, s)))

    def pickup_one_card(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card
    
class Message(pygame.sprite.DirtySprite):
    def __init__(self):
        super(Message, self).__init__()
        self.images = { 
            'looser': pygame.image.load(config.path+'looser.png').convert_alpha(),
            'winner': pygame.image.load(config.path+'winner.png').convert_alpha()
        }
        self.set_message()
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    def set_message(self, message='looser'):
        self.image = self.images[message]
        self.rect = self.image.get_rect()
        self.rect.x = (config.w-self.rect.w)/2
        self.rect.y = (config.h-self.rect.h)/2
        self.dirty = 2

class Card(pygame.sprite.DirtySprite):
    def __init__(self, number, suit, filename):
        super(Card, self).__init__()
        self.filename = filename
        self.rect = pygame.Rect(0, 0, config.card_w, config.card_h)
        self.number = number
        self.suit = suit
        self.front = pygame.image.load(self.filename).convert_alpha()
        self.back = pygame.image.load(config.hidden_card_filename).convert_alpha()
        self.hidden = True
        self.image = self.back 
        self.mine = False
        self.row = 0
    def set_as_mine(self):
        self.mine = True
    def is_mine(self):
        return self.mine
    def set_visible(self):
        if self.hidden:
            self.flip()

    def flip(self):
        self.dirty = 2
        self.hidden = not self.hidden
        if self.hidden:
            self.image = self.back
        else:
            self.image = self.front
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y 

if __name__ == '__main__':

    if '-h' in sys.argv:
        print 'PySolita, version 0'
        print 'Usage: game.py <video_mode>, where <video_mode> is:'
        print '     -a   for 640x480'
        print '     -b   for 800x600 (default)'
        print '     -c   for 1024x768'
        sys.exit(0)

    config.init((800, 600))
    if '-a' in sys.argv:
            config.init((640, 480))
    if '-c' in sys.argv:
            config.init((1024, 768))
    
    game = Game()
    game.init()
    game.run()


