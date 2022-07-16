from model import Unit
from model.game import Game
from model.order import Order
from model.unit_order import UnitOrder
from model.constants import Constants
from model.vec2 import Vec2
from model.action_order import ActionOrder
from typing import Optional, Tuple, List
from debug_interface import DebugInterface


class MyStrategy:
    def __init__(self, constants: Constants):
        pass

    def process_units(self, game: Game) -> Tuple[Unit, List[Unit]]:
        me, opponents = None, []
        for unit in game.units:
            if unit.player_id != game.my_id:
                opponents.append(unit)
            else:
                me = unit
        assert me is not None
        return me, opponents

    def get_default_order(self, my_unit: Unit):
        return UnitOrder(
            target_velocity=Vec2(-my_unit.position.x, -my_unit.position.y),
            target_direction=Vec2(-my_unit.direction.y, my_unit.direction.x),
            action=ActionOrder.Aim(False)
        )

    def see_opponents_order(self, my_unit: Unit, opponents: List[Unit]):
        return UnitOrder(
            target_velocity=Vec2(-my_unit.position.x, -my_unit.position.y),
            target_direction=Vec2(-my_unit.direction.y, my_unit.direction.x),
            action=ActionOrder.Aim(True)
        )

    def get_self_score(self, game: Game) -> float:
        my_player = [player for player in game.players if player.id == game.my_id][0]
        return my_player.score

    def get_order(self, game: Game, debug_interface: Optional[DebugInterface]) -> Order:
        my_unit, opponents = self.process_units(game)

        if opponents:
            my_order = self.see_opponents_order(my_unit, opponents)
        else:
            my_order = self.get_default_order(my_unit)

        return Order({my_unit.id: my_order})

    def debug_update(self, displayed_tick: int, debug_interface: DebugInterface):
        pass

    def finish(self):
        pass
