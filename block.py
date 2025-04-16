import pygame as pg
from random import random

class Block:
    __block = pg.image.load("block.png")
    __block = pg.transform.scale(__block, (60, 60))
    __block_list = []
    __count = 0

    def __init__(self):
        Block.__count += 1
        if Block.__count == 1:
            self.__position = [200,200]
        elif Block.__count == 2:
            self.__position = [600,200]
        elif Block.__count == 3:
            self.__position = [200, 400]
        else:
            self.__position = [600, 400]

    @classmethod
    def get_block(cls):
        return cls.__block

    def get_position(self):
        return self.__position
    
    @staticmethod
    def get_block_list():
        return Block.__block_list
    @staticmethod
    def add_block_list(block):
        Block.__block_list.append(block)
    @staticmethod
    def clear_block_list():
        Block.__block_list.clear()