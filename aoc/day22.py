import collections
from . import util


def get_decks(lines):
    player = 0
    cards = collections.deque()
    for line in lines:
        if line.startswith("Player"):
            player = int(line[-2])
        elif line:
            cards.append(int(line))
        else:
            yield player, cards
            player = 0
            cards = collections.deque()


def play(deck1, deck2):
    card1 = deck1.popleft()
    card2 = deck2.popleft()

    if card1 > card2:
        deck1.append(card1)
        deck1.append(card2)
    else:
        deck2.append(card2)
        deck2.append(card1)


def calculate_score(deck):
    return sum(card * (len(deck) - idx) for idx, card in enumerate(deck))


def run():
    inputlines = util.get_input_lines("22.txt")
    decks = {p: cs for p, cs in get_decks(inputlines)}

    while decks[1] and decks[2]:
        play(decks[1], decks[2])

    if decks[1]:
        score = calculate_score(decks[1])
    else:
        score = calculate_score(decks[2])

    return (score,)
