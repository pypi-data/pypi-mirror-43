# I didn't like two python card deck library options so I decided to make my own which I'm calling "pythoncards".
import random


# Deck class for creating a deck list that will work with the card class.
class Deck:

    def __init__(self, name: str, size: int, jokers: bool):
        self.name = name
        self.size = size
        if jokers:
            self.deck = [('joker', 'red'), ('joker', 'black')]
            self.size += 2
        elif not jokers:
            self.deck = []
        else:
            raise ValueError('pythoncards doesn\'t know whether or not to add jokers to the deck: didn\'t provide boolean for the jokers attribute.')

    def fill_standard_cards(self):
        suits = ['spades', 'hearts', 'clubs', 'diamonds']
        for i in range(2, 11):
            for suit in suits:
                self.deck.append((i, suit))
        face_cards = ['jack', 'queen', 'king', 'ace']
        for face in face_cards:
            for suit in suits:
                self.deck.append((face, suit))


class Card:

    def __init__(self, face_value: str or int, suit: str):
        self.suit = suit
        self.face_value = face_value
