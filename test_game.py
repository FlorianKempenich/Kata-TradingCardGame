from unittest.mock import patch

import pytest
from hypothesis import given
from hypothesis.strategies import random_module
from pytest import fixture

from game import Deck, Card, Player, InvalidMove, Game, GameError


class TestGame:
    @fixture
    def p0(self):
        return Player('First', Deck())

    @fixture
    def p1(self):
        return Player('Second', Deck())

    @fixture
    def game(self, p0, p1):
        return Game(p0, p1)

    class TestAtStart:
        def test_player1_starts(self, game):
            # TODO: Make random
            assert game.status['current_player'] == 'First'

    class TestDuringTurn:
        class TestStatus:
            def test_list_players_by_name(self, game):
                assert 'First' in game.status['players']
                assert 'Second' in game.status['players']

            def test_describe_key_attributes_of_players(self, game, p0: Player):
                p0.health = 22
                p0.mana_slots = 8
                p0.mana = 3
                p0_hand = [Card(3), Card(5), Card(1)]
                p0.hand = p0_hand

                assert game.status['players']['First']['health'] == 22
                assert game.status['players']['First']['mana_slots'] == 8
                assert game.status['players']['First']['mana'] == 3
                assert game.status['players']['First']['hand'] == p0_hand

        class TestPlayCard:
            def test_current_player_attacks_the_other_one(self, game, p0, p1):
                game.attacker = p1
                some_card_in_p1_hand = game.status['players']['Second']['hand'][1]

                with patch.object(p1, 'attack') as p1_attack_mock:
                    game.play_card(some_card_in_p1_hand)
                    p1_attack_mock.assert_called_with(p0, some_card_in_p1_hand)

            def test_invalid_card__throw_error(self, game):
                card_not_in_game = Card(3)
                with pytest.raises(GameError, match=r'(?i).*not in hand.*'):
                    game.play_card(card_not_in_game)

            def test_other_player_health_gets_to_zero__game_won(self):
                attacker = Player('attacker', Deck())
                victim = Player('victim', Deck())
                game = Game(attacker, victim)

                victim.health = 2
                kill_card = Card(4)
                attacker.mana_slots = 8
                attacker.mana = 4
                attacker.hand = [Card(2), kill_card, Card(8)]
                game.attacker = attacker

                assert game.status['finished'] is False
                game.play_card(kill_card)
                assert game.status['finished'] is True
                assert game.status['winner'] == 'attacker'

            def test_can_not_play_after_game_finished(self, game, p1):
                game.attacker = p1
                some_card_in_p1_hand = game.status['players']['Second']['hand'][1]

                game.game_finished = True
                with pytest.raises(GameError, match=r'(?i).*game is finished'):
                    game.play_card(some_card_in_p1_hand)

            class TestAutomaticallyFinishTurn:
                @patch.object(Game, 'finish_turn')
                def test_when_no_mana_left(self, finish_turn_mock, game, p0):
                    game.attacker = p0

                    p0.mana = 3
                    card_that_cost_3_mana = Card(3)
                    p0.hand = [Card(1), card_that_cost_3_mana, Card(7)]

                    finish_turn_mock.assert_not_called()
                    game.play_card(card_that_cost_3_mana)
                    finish_turn_mock.assert_called_once()

                @patch.object(Game, 'finish_turn')
                def test_when_no_cards_in_hand(self, finish_turn_mock, game, p0):
                    game.attacker = p0

                    p0.mana = 7
                    last_card_in_hand = Card(3)
                    p0.hand = [last_card_in_hand]

                    finish_turn_mock.assert_not_called()
                    game.play_card(last_card_in_hand)
                    finish_turn_mock.assert_called_once()

    class TestFinishTurn:
        def test_switch_current_player(self, game, p0: Player, p1):
            game.attacker = p0
            assert game.status['current_player'] == p0.name
            game.finish_turn()
            assert game.status['current_player'] == p1.name

        def test_init_new_turn_on_next_player(self, game, p0, p1: Player):
            game.attacker = p0
            with patch.object(p1, 'new_turn') as p1_new_turn_mock:
                p1_new_turn_mock.assert_not_called()
                game.finish_turn()
                p1_new_turn_mock.assert_called_once()


class TestPlayer:
    @fixture
    def deck(self):
        return Deck()

    @fixture
    def player(self, deck):
        return Player('Frank', deck)

    @fixture
    def other_player(self):
        return Player('Opponent', Deck())

    class TestAtInit:
        def test_initial_values(self):
            player = Player('Frank', Deck())
            assert player.name == 'Frank'
            assert player.health == 30
            assert player.mana_slots == 0
            assert player.mana == 0

        @patch.object(Player, '_draw_card')
        def test_draws_3_cards(self, draw_card_mock):
            _player = Player('Frank', Deck())
            assert draw_card_mock.call_count == 3

    class TestDrawCard:
        @patch.object(Deck, 'draw_card')
        def test_deck_not_empty__draw(self, deck_draw_card_mock, player, deck):
            assert deck.cards != []

            card_to_be_drawn = Card(4)
            deck_draw_card_mock.return_value = card_to_be_drawn

            player._draw_card()

            deck_draw_card_mock.assert_called_once()
            assert card_to_be_drawn in player.hand

        @patch.object(Deck, 'draw_card')
        def test_deck_empty__do_not_draw(self, deck_draw_card_mock, player, deck):
            deck.cards = []
            player._draw_card()
            deck_draw_card_mock.assert_not_called()

    class TestNewTurn:
        @patch.object(Player, '_draw_card')
        def test_draw_a_card(self, draw_card_mock, player):
            player.new_turn()
            draw_card_mock.assert_called_once()

        class TestManaSlots:
            def test_increases(self, player):
                mana_slots_before_new_turn = player.mana_slots
                player.new_turn()
                assert player.mana_slots == mana_slots_before_new_turn + 1

            def test_can_only_increase_up_to_a_max_value(self, player):
                for _ in range(0, 200):
                    player.new_turn()

                assert player.mana_slots == Player.MAX_MANA_SLOTS

        class TestRefillMana:
            def test_refill_after_slot_number_increased(self, player):
                player.mana_slots = 7
                player.mana = 3

                player.new_turn()

                assert player.mana == 8

            def test_when_max_number_of_slot_reached(self, player):
                player.mana_slots = Player.MAX_MANA_SLOTS
                player.mana = 3

                player.new_turn()

                assert player.mana == Player.MAX_MANA_SLOTS

    class TestAttack:
        class TestInvalidCases:
            def test_not_enough_mana(self, player, other_player):
                player.mana = 4
                card_too_expensive = Card(7)
                player.hand = [Card(1), Card(3), card_too_expensive]
                with pytest.raises(InvalidMove, match=r'(?i).*not enough.*'):
                    player.attack(other_player, card_too_expensive)

            def test_can_not_attack_self(self, player):
                with pytest.raises(InvalidMove, match=r'(?i).*can not attack self.*'):
                    player.attack(player, Card(3))

            def test_card_not_in_hand(self, player, other_player):
                player.mana = 8
                card_not_in_hand = Card(7)
                player.hand = [Card(1), Card(3)]
                with pytest.raises(InvalidMove, match=r'(?i).*not in hand.*'):
                    player.attack(other_player, card_not_in_hand)

            def test_check_card_in_hand_before_cost(self, player, other_player):
                player.mana = 3
                card_not_in_hand_and_also_too_expensive = Card(7)
                player.hand = [Card(1), Card(3)]
                with pytest.raises(InvalidMove, match=r'(?i).*not in hand.*'):
                    player.attack(other_player, card_not_in_hand_and_also_too_expensive)

        @fixture
        def attack_card(self):
            return Card(3)

        @fixture
        def player_ready_to_attack(self, player, attack_card):
            player.mana_slots = 8
            player.mana = 6
            player.hand = [Card(1), attack_card, Card(7)]
            return player

        def test_uses_mana(self, player_ready_to_attack, attack_card, other_player):
            mana_before_attack = player_ready_to_attack.mana
            player_ready_to_attack.attack(other_player, attack_card)
            mana_after_attack = player_ready_to_attack.mana
            assert mana_after_attack == mana_before_attack - attack_card.mana_cost

        def test_damages_victim(self, player_ready_to_attack, attack_card, other_player):
            victim_health_before_attack = other_player.health
            player_ready_to_attack.attack(other_player, attack_card)
            victim_health_after_attack = other_player.health
            assert victim_health_after_attack == victim_health_before_attack - attack_card.attack_power

        def test_remove_card_from_hand(self, player_ready_to_attack, attack_card, other_player):
            hand_before_attack = player_ready_to_attack.hand.copy()
            player_ready_to_attack.attack(other_player, attack_card)
            hand_after_attack = player_ready_to_attack.hand
            assert attack_card in hand_before_attack
            assert attack_card not in hand_after_attack

    def test_health_below_zero__set_automatically_to_zero(self, player):
        player.health = -24
        assert player.health == 0


class TestDeck:
    @fixture
    def deck(self):
        return Deck()

    def test_new_deck(self, deck):
        def assert_there_are(expected_num_of_card):
            def get_cards_with_cost(mana_cost):
                return [card for card in deck.cards if card.mana_cost == mana_cost]

            class Wrapper:
                def cards_of_mana(self, mana_cost):
                    cards_with_given_cost = get_cards_with_cost(mana_cost)
                    assert len(cards_with_given_cost) == expected_num_of_card

            return Wrapper()

        assert_there_are(2).cards_of_mana(0)
        assert_there_are(2).cards_of_mana(1)
        assert_there_are(3).cards_of_mana(2)
        assert_there_are(4).cards_of_mana(3)
        assert_there_are(3).cards_of_mana(4)
        assert_there_are(2).cards_of_mana(5)
        assert_there_are(2).cards_of_mana(6)
        assert_there_are(1).cards_of_mana(7)
        assert_there_are(1).cards_of_mana(8)

    def test_can_not_draw_card_on_empty_deck(self, deck):
        deck.cards = []
        with pytest.raises(RuntimeError, match=r'.*empty.*'):
            deck.draw_card()

    @given(random_module())
    def test_draw_card_draws_random_card_from_deck(self, _random_module):
        deck = Deck()  # Not using fixture because of 'hypothesis'
        cards_in_deck_before_draw = deck.cards.copy()
        card = deck.draw_card()
        assert card in cards_in_deck_before_draw

    @given(random_module())
    def test_drawn_card_is_not_in_deck_anymore(self, _random_module):
        deck = Deck()  # Not using fixture because of 'hypothesis'
        card = deck.draw_card()
        cards_in_deck_after_draw = deck.cards.copy()
        assert card not in cards_in_deck_after_draw

    @given(random_module())
    def test_draw_all_cards(self, _random_module):
        deck = Deck()  # Not using fixture because of 'hypothesis'

        for _ in range(0, 20):
            deck.draw_card()

        with pytest.raises(RuntimeError, match=r'.*empty.*'):
            deck.draw_card()

    @given(random_module())
    def test_cards_left(self, _random_module):
        deck = Deck()
        deck.cards = [Card(0), Card(0), Card(8)]
        assert deck.cards_left() == 3
        deck.draw_card()
        assert deck.cards_left() == 2


class TestCard:
    def test_attack_power_equals_mana_cost(self):
        cost = 4
        card = Card(cost)
        assert card.mana_cost == cost
        assert card.attack_power == cost
