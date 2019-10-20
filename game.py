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
[-] The active player can play as many cards as he can afford. Any played card empties
  Mana slots and deals immediate damage to the opponent player equal to its Mana cost.
[-] If the opponent player’s Health drops to or below zero the active player wins the game
[-] If the active player can’t (by either having no cards left in his hand or lacking
  sufficient Mana to pay for any hand card) or simply doesn’t want to play another card,
  the opponent player becomes active

class GameStatus {
    Cards[] cards_in_hand
    Int available_mana
    String current_player_name

    Boolean finished
    Player winner
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


class Player:
    MAX_MANA_SLOTS = 10

    def __init__(self, name, deck):
        self.deck = deck

        self.name = name
        self.mana_slots = 0
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
            self.hand.append(card)

    def _increment_mana_slots(self):
        if self.mana_slots < self.MAX_MANA_SLOTS:
            self.mana_slots += 1

    def _refill_mana(self):
        self.mana = self.mana_slots

    def new_turn(self):
        self._draw_card()
        self._increment_mana_slots()
        self._refill_mana()


class Card:
    mana_cost: int
    uuid: UUID

    def __init__(self, mana_cost):
        self.mana_cost = mana_cost
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
