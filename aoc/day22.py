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
                return deck1
        else:
            deck2.append(card2)
            deck2.append(card1)
            if not deck1:
                return deck2


CACHE = {}

def play_recursive_combat(_deck1, _deck2, depth=1):
    deck1 = collections.deque(_deck1)
    deck2 = collections.deque(_deck2)

    history = set()
    round = 0
    while True:
        signature = calculate_signature(deck1, deck2)

        # Check for identical previous game.
        if signature in CACHE:
            return CACHE[signature]

        # Check for identical previous round.
        if signature in history:
            CACHE[signature] = 1, deck1
            return 1, deck1
        history.add(signature)

        card1 = deck1.popleft()
        card2 = deck2.popleft()

        # Draw cards and play.
        if len(deck1) >= card1 and len(deck2) >= card2:
            winner, _ = play_recursive_combat(list(deck1)[:card1], list(deck2)[:card2], depth+1)
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
                return 1, deck1
        else:
            deck2.append(card2)
            deck2.append(card1)
            if not deck1:
                CACHE[signature] = 2, deck2
                return 2, deck2



def calculate_score(deck):
    return sum(card * (len(deck) - idx) for idx, card in enumerate(deck))


def calculate_signature(deck1, deck2):
    sig1 = ",".join(str(card) for card in deck1)
    sig2 = ",".join(str(card) for card in deck2)
    return sig1 + ":" + sig2


def run():
    inputlines = util.get_input_lines("22.txt")
    decks = {p: cs for p, cs in get_decks(inputlines)}

    winning = play_combat(decks[1], decks[2])
    score1 = calculate_score(winning)

    _, winning = play_recursive_combat(decks[1], decks[2])
    score2 = calculate_score(winning)

    return score1, score2
