from seneca.libs.math import random
from seneca.libs.storage.datatypes import List

cards = List('cards')
cardinal_values = List('cardinal_values')
suits = List('suits')
cities = List('cities')

@seed
def initialize():
    random.seed()
    cards.extend([1, 2, 3, 4, 5, 6, 7, 8])
    cardinal_values.extend(['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'])
    suits.extend(['S', 'C', 'H', 'D'])
    cities.extend(['Cleveland', 'Detroit', 'Chicago', 'New York', 'San Francisco'])

@export
def shuffle_cards(**kwargs):
    random.shuffle(cards)
    return cards

@export
def random_number(k):
    return random.randrange(k)

@export
def random_number_2(k):
    # adjust the random state by calling another random function
    shuffle_cards()
    return random.randrange(k)

@export
def random_bits(k):
    shuffle_cards()
    shuffle_cards()
    shuffle_cards()
    return random.getrandbits(k)

@export
def int_in_range(a, b):
    shuffle_cards()
    shuffle_cards()
    return random.randint(a, b)

@export
def deal_card():
    random.shuffle(cardinal_values)
    random.shuffle(cardinal_values)
    random.shuffle(cardinal_values)

    random.shuffle(suits)
    random.shuffle(suits)
    random.shuffle(suits)

    c = ''
    c += random.choice(cardinal_values)
    c += random.choice(suits)

    return c

@export
def pick_cities(k):
    return random.choices(cities, k)

