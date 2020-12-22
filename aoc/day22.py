import collections
from . import util


def get_decks(lines):
    player = 0
    cards = []
    for line in lines:
        if line.startswith("Player"):
            player = int(line[-2])
        elif line:
            cards.append(int(line))
        else:
            yield player, cards
            player = 0
            cards = []


def play_combat(_deck1, _deck2):
    deck1 = collections.deque(_deck1)
    deck2 = collections.deque(_deck2)

    while True:
        card1 = deck1.popleft()
        card2 = deck2.popleft()

        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
            if not deck2:
                return 1, deck1
        else:
            deck2.append(card2)
            deck2.append(card1)
            if not deck1:
                return 2, deck2


CACHE = {}


def play_recursive_combat(_deck1, _deck2):
    deck1 = collections.deque(_deck1)
    deck2 = collections.deque(_deck2)
    history = set()

    while True:
        signature = tuple(deck1), tuple(deck2)

        # Check for identical previous game.
        if signature in CACHE:
            break

        # Check for identical previous round.
        if signature in history:
            CACHE[signature] = 1, deck1
            break
        history.add(signature)

        # Draw cards and play.
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if len(deck1) >= card1 and len(deck2) >= card2:
            subdeck1 = list(deck1)[:card1]
            subdeck2 = list(deck2)[:card2]
            winner, _ = play_recursive_combat(subdeck1, subdeck2)
        elif card1 > card2:
            winner = 1
        else:
            winner = 2

        # Assign winnings and check for termination conditions.
        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
            if not deck2:
                CACHE[signature] = 1, deck1
                break
        else:
            deck2.append(card2)
            deck2.append(card1)
            if not deck1:
                CACHE[signature] = 2, deck2
                break

    return CACHE[signature]


def calculate_score(deck):
    return sum(card * (len(deck) - idx) for idx, card in enumerate(deck))


def run():
    inputlines = util.get_input_lines("22.txt")
    decks = {p: cs for p, cs in get_decks(inputlines)}

    _, winning = play_combat(decks[1], decks[2])
    score1 = calculate_score(winning)

    _, winning = play_recursive_combat(decks[1], decks[2])
    score2 = calculate_score(winning)

    return score1, score2
