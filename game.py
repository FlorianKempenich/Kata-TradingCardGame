"""

Preparation
[X] Each player starts the game with 30 Health and 0 Mana slots
[X] Each player starts with a deck of 20 Damage cards with the following
  Mana costs: 0,0,1,1,2,2,2,3,3,3,3,4,4,4,5,5,6,6,7,8
[X] From the deck each player receives 3 random cards has his initial hand

Gameplay

[X] The active player receives 1 Mana slot up to a maximum of 10 total slots
[X] The active player’s empty Mana slots are refilled
[X] The active player draws a random card from his deck
[X] The active player can play as many cards as he can afford. Any played card empties
  Mana slots and deals immediate damage to the opponent player equal to its Mana cost.
[X] If the opponent player’s Health drops to or below zero the active player wins the game
[X] If the active player can’t (by either having no cards left in his hand or lacking
  sufficient Mana to pay for any hand card) or simply doesn’t want to play another card,
  the opponent player becomes active

Special Rules
[X] Bleeding Out: If a player’s card deck is empty before the game is over he receives
    1 damage instead of drawing a card when it’s his turn.
[X] Overload: If a player draws a card that lets his hand size become >5 that card is
    discarded instead of being put into his hand.

GameStatus
{
    current_player: 'Frank',
    players: {
        'Frank': {
            health: 23,
            mana_slots: 8
            hand: [Card(4), Card(2), Card(6)],
            mana: 5
        },
        'Patrick': {
            health: 21,
            mana_slots: 7
            hand: [Card(1), Card(8)],
            mana: 2
        }
    finished: false,
    winner: null
}

Basic Logic for UI:

1. Call `get_status` on `Game`
2. Display status and ask current player to play
   For each card played:
     2.1 Call `play_card(card)` on `Game`
     2.2 Call `get_status` on `Game`
     2.3 If `current_player changed, display: "Turn finished, new player!"
     2.4 If game not finished, go to 2. else go to 3.
3. Display: "Game finished! Winner is {winner}"

"""
import random
from uuid import uuid4, UUID


class InvalidMove(Exception):
    pass


class GameError(Exception):
    pass


class Card:
    mana_cost: int
    attack_power: int
    uuid: UUID

    def __init__(self, mana_cost):
        self.mana_cost = mana_cost
        self.attack_power = mana_cost
        self.uuid = uuid4()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.uuid == other.uuid

    def __repr__(self):
        return f'Card<{self.mana_cost}>'


class Deck:
    START_CARDS_COST = [0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 8]

    def __init__(self):
        self.cards = []
        for cost in self.START_CARDS_COST:
            self.cards.append(Card(cost))

    def draw_card(self):
        if not self.cards:
            raise RuntimeError('Can not draw card! Deck is empty')

        rand_index = random.randint(0, len(self.cards) - 1)
        return self.cards.pop(rand_index)

    def cards_left(self) -> int:
        return len(self.cards)


class Player:
    MAX_MANA_SLOTS = 10
    MAX_HAND_SIZE = 5

    def __init__(self, name, deck):
        self.deck = deck

        self.name = name
        self.mana_slots = 0
        self.mana = 0
        self._health = 30
        self.hand = []

        for _ in range(0, 3):
            self._draw_card()

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health):
        if new_health < 0:
            new_health = 0

        self._health = new_health

    def _draw_card(self):
        if self.deck.cards_left():
            card = self.deck.draw_card()
            if len(self.hand) < self.MAX_HAND_SIZE:
                self.hand.append(card)
        else:
            # 'Bleeding out' special rule
            self.health -= 1

    def _increment_mana_slots(self):
        if self.mana_slots < self.MAX_MANA_SLOTS:
            self.mana_slots += 1

    def _refill_mana(self):
        self.mana = self.mana_slots

    def new_turn(self):
        self._draw_card()
        self._increment_mana_slots()
        self._refill_mana()

    def attack(self, victim: 'Player', card: Card):
        if victim == self:
            raise InvalidMove('Can not attack self')
        if card not in self.hand:
            raise InvalidMove('Card is not in Hand!')
        if self.mana < card.mana_cost:
            raise InvalidMove('Not enough Mana!')

        self.mana -= card.mana_cost
        victim.health -= card.attack_power
        self.hand.remove(card)


class Game:
    def __init__(self, player_0: Player, player_1: Player):
        self.player_0 = player_0
        self.player_1 = player_1

        self.game_finished = False
        self.attacker = self.player_0

    @property
    def victim(self):
        if self.attacker == self.player_0:
            return self.player_1
        else:
            return self.player_0

    @property
    def status(self):
        def player_status(player: Player):
            return {'health'    : player.health,
                    'mana_slots': player.mana_slots,
                    'mana'      : player.mana,
                    'hand'      : player.hand}

        def winner():
            if self.game_finished:
                return self.attacker.name
            return None

        return {'current_player': self.attacker.name,
                'players'       : {self.player_0.name: player_status(self.player_0),
                                   self.player_1.name: player_status(self.player_1)},
                'finished'      : self.game_finished,
                'winner'        : winner()}

    def play_card(self, card: Card):
        if self.game_finished:
            raise GameError('Can not play after game is finished!')

        try:
            self.attacker.attack(self.victim, card)
        except InvalidMove as e:
            raise GameError(e)

        if self.victim.health == 0:
            self.game_finished = True

        if self.attacker.mana == 0 or self.attacker.hand == []:
            self.finish_turn()

    def finish_turn(self):
        if not self.game_finished:
            self.attacker = self.victim
            self.attacker.new_turn()
