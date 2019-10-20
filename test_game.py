from pytest import fixture

from game import Game


@fixture
def game():
    return Game()


def test_say_hi(game):
    assert game.return_hi() == 'hi'


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
    def test_new_deck(self):
        pass

    def test_can_not_draw_card_on_empty_deck(self):
        pass

    def test_draw_card_draws_random_card_from_deck(self):
        pass
