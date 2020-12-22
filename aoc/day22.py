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
    deck1 = _deck1.copy()
    deck2 = _deck2.copy()

    while True:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)

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


def play_recursive_combat(_deck1, _deck2):
    deck1 = _deck1.copy()
    deck2 = _deck2.copy()
    rounds = set()

    while True:
        # Check for identical previous round.
        signature = tuple(deck1), tuple(deck2)
        if signature in rounds:
            return 1, deck1
        rounds.add(signature)

        # Draw cards and play.
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            winner, _ = play_recursive_combat(deck1[:card1], deck2[:card2])
        elif card1 > card2:
            winner = 1
        else:
            winner = 2

        # Assign winnings and check for termination conditions.
        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
            if not deck2:
                return 1, deck1
        else:
            deck2.append(card2)
            deck2.append(card1)
            if not deck1:
                return 2, deck2


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
