import pytest
from hypothesis import given
from hypothesis.strategies import random_module
from pytest import fixture

from game import Deck, Card


class TestGame:
    class TestAtStart:
        def test_player1_starts(self):
            # TODO: Make random
            #
            # Pass a mock player_1 and Test that the GameStatus is equal
            # to the player_1 values
            pass

    class TestDuringTurn:
        class TestPlayCard:
            def test_current_player_attacks_the_other_one(self):
                pass

            def test_invalid_card__throw_error(self):
                pass

            def test_no_mana_left__automatically_finish_turn(self):
                pass

            def test_other_player_health_gets_to_zero__game_won(self):
                pass

            def test_can_not_play_after_game_finished(self):
                pass

            class TestAutomaticallyFinishTurn:
                def test_when_no_mana_left(self):
                    pass

                def test_when_no_cards_in_hand(self):
                    pass

    class TestFinishTurn:
        def test_switch_current_player(self):
            pass

        def test_init_new_turn_on_next_player(self):
            pass


class TestPlayer:
    # def test_new_turn
    class TestAtInit:
        def test_initial_values(self):
            pass

        def test_draws_3_cards(self):
            pass

    class TestNewTurn:
        class TestDrawNewCard:
            def test_deck_not_empty__draw(self):
                pass

            def test_deck_empty__do_not_draw(self):
                pass

        class TestManaSlots:
            def test_increases(self):
                pass

            def test_can_only_increase_up_to_a_max_value(self):
                pass

        class TestRefillMana:
            def test_refill_after_slot_number_increased(self):
                pass

            def test_when_max_number_of_slot_reached(self):
                pass

    class TestAttack:
        class TestInvalidCases:
            def test_not_enough_mana(self):
                pass

            def test_can_not_attack_self(self):
                pass

            def test_card_not_in_hand(self):
                pass

        def test_uses_mana_equal_to_card_cost(self):
            pass

        def test_damages_victim_with_dmg_equal_to_card_cost(self):
            pass

        def test_remove_card_from_hand(self):
            pass

    def test_health_below_zero__set_automatically_to_zero(self):
        pass


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
