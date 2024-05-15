import pygame
from decimal import Decimal

def add_decimal(numToAdd, num):
    after_comma = Decimal(num).as_tuple()[-1]*-1
    add = Decimal(numToAdd) / Decimal(10**after_comma)
    return Decimal(num) + add
    
def sub_decimal(numToSub, num):
    after_comma = Decimal(num).as_tuple()[-1]*-1
    sub = Decimal(numToSub) / Decimal(10**after_comma)
    return Decimal(num) - sub

def rotate(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
