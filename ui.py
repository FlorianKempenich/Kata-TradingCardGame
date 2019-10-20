from pprint import pprint

from game import Game, Player, Deck

if __name__ == '__main__':
    p1_name = input('Player 1:')
    p2_name = input('Player 2:')

    p1 = Player(p1_name, Deck())
    p2 = Player(p2_name, Deck())
    game = Game(p1, p2)

    while not game.status['finished']:
        pprint(game.status)
        print('')
        print(f"It's {game.status['current_player']}'s turn")
        card_index = int(input('Which card? (index (<0 to pass))'))
        if card_index < 0:
            game.finish_turn()
        else:
            card = game.status['players'][game.status['current_player']]['hand'][card_index]
            game.play_card(card)
            print(f"You planed {card}")
        print('')
        print('')

    print("Game Finished!! :D :D")
    pprint(game.status)
