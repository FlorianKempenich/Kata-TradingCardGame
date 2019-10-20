# Kata - Trading Card Game

(Not so) Simple Kata in Python from [CodingDojo - Trading Card Game](http://codingdojo.org/kata/TradingCardGame/)  
Without special rules

## Rules

### Preparation

- Each player starts the game with 30 Health and 0 Mana slots
- Each player starts with a deck of 20 Damage cards with the following Mana costs: 0,0,1,1,2,2,2,3,3,3,3,4,4,4,5,5,6,6,7,8
- From the deck each player receives 3 random cards has his initial hand

### Gameplay

- The active player receives 1 Mana slot up to a maximum of 10 total slots
- The active player’s empty Mana slots are refilled
- The active player draws a random card from his deck
- The active player can play as many cards as he can afford. Any played card empties Mana slots and deals immediate damage to the opponent player equal to its Mana cost.
- If the opponent player’s Health drops to or below zero the active player wins the game
- If the active player can’t (by either having no cards left in his hand or lacking sufficient Mana to pay for any hand card) or simply doesn’t want to play another card, the opponent player becomes active


## Solution

The goal of the Kata was to practice TDD, the best way to understand the solution is simply to [read the tests](/test_game.py).


### Test outline
#### Game
![Tests outline for Game](/img/test_game.png)
#### Player
![Tests outline for Player](/img/test_player.png)
#### Deck
![Tests outline for Deck](/img/test_deck.png)
#### Card
![Tests outline for Card](/img/test_card.png)

### Domain Model
![UML representation of the domain](/img/model.png)
