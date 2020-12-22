from utils import *
from collections import deque
from collections.abc import Iterable
from copy import *


def calculate_score(cards: deque) -> int:
    factor = 1
    total = 0
    while len(cards) > 0:
        bottom = cards.popleft()
        total += factor * bottom
        factor += 1

    return total


def init_queue(it: Iterable) -> deque:
    q = deque()
    for el in it:
        q.appendleft(el)
    return q


def new_deck(nr_cards: int, deck: deque) -> deque:
    working_copy = deepcopy(deck)
    new_deck = deque()
    for i in range (0, nr_cards):
        new_deck.appendleft(working_copy.pop())  # TODO check appendleft

    return new_deck


def play_game(pl1: deque, pl2: deque) -> bool:
    # Returns true if pl1 won else false
    # Modifies both deques!
    earlier_decks = set()
    player1_won = None

    print('==== New Game ====')

    while player1_won is None:
        print('Player 1: ' + str(pl1))
        print('Player 2: ' + str(pl2))
        # determine if game ends
        if (str(pl1), str(pl2)) in earlier_decks:
            player1_won = True
            break
        if len(pl1) == 0:
            player1_won = False
            break
        if len(pl2) == 0:
            player1_won = True
            break
        earlier_decks.add((str(pl1), str(pl2)))
        # determine round winner
        p1c = pl1.pop()
        print('Player 1 drew card: ' + str(p1c))
        p2c = pl2.pop()
        print('Player 2 drew card: ' + str(p2c))

        if len(pl1) >= p1c and len(pl2) >= p2c:
            # subgame
            p1_wins_round = play_game(new_deck(p1c, pl1), new_deck(p2c, pl2))
        else:
            # highest card wins
            p1_wins_round = p1c > p2c

        if p1_wins_round:
            print('Player 1 won round!')
            pl1.appendleft(p1c)
            pl1.appendleft(p2c)
        else:
            print('Player 2 won round!')
            pl2.appendleft(p2c)
            pl2.appendleft(p1c)

    if player1_won:
        print('=== Player 1 won game! ===')
    else:
        print('=== Player 2 won game! ===')
    return player1_won


if __name__ == '__main__':
    inputs = open('input_day22.txt', 'r')
    blocks = inputs.read().split('\n\n')
    inputs.close()

    player1_deck = init_queue(map(int, non_empty_lines(blocks[0])[1:]))
    player2_deck = init_queue(map(int, non_empty_lines(blocks[1])[1:]))

    player1 = deepcopy(player1_deck)
    player2 = deepcopy(player2_deck)
    while len(player1) > 0 and len(player2) > 0:
        # draw top cards
        p1c = player1.pop()
        p2c = player2.pop()
        # determine winner
        # place top cards under stack winner, own card first
        if p1c > p2c:
            player1.appendleft(p1c)
            player1.appendleft(p2c)
        else:
            player2.appendleft(p2c)
            player2.appendleft(p1c)

    if len(player1) > 0 :
        score = calculate_score(player1)
    else:
        score = calculate_score(player2)

    print('Part 1: {}'.format(score))

    # start game from initial deck and play until end
    # end:
    #    earlier round existed in the same game with same decks for both players (player 1 wins)
    #    or one player has all the cards (winner)
    # play: keep playing rounds until end
    # round: winner can be determined straight away or by playing a sub-game
    # if nr(remaining deck) >= current card for both players: determine round winner by subgame
    # otherwise the player with the highest card wins the round
    # as before, the round winner gets the 2 cards

    player1 = deepcopy(player1_deck)
    player2 = deepcopy(player2_deck)

    player1_won = play_game(player1, player2)

    if player1_won:
        score = calculate_score(player1)
    else:
        score = calculate_score(player2)

    print('Part 2: {}'.format(score))
