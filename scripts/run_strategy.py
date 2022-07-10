from main import Runner
from codegame.server_message import ServerMessage
from codegame.client_message import ClientMessage
from debug_interface import DebugInterface
import sys
from my_strategy import MyStrategy as Strat


class StrategyRunner(Runner):
    def __init__(self, StratClass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.StratClass = StratClass

    def run(self):
        strategy = None
        debug_interface = DebugInterface(self.reader, self.writer)
        while True:
            message = ServerMessage.read_from(self.reader)
            if isinstance(message, ServerMessage.UpdateConstants):
                strategy = self.StratClass(message.constants)
            elif isinstance(message, ServerMessage.GetOrder):
                order = strategy.get_order(message.player_view, debug_interface if message.debug_available else None)
                ClientMessage.OrderMessage(order).write_to(self.writer)
                self.writer.flush()
            elif isinstance(message, ServerMessage.Finish):
                strategy.finish()
                break
            elif isinstance(message, ServerMessage.DebugUpdate):
                strategy.debug_update(message.displayed_tick, debug_interface)
                ClientMessage.DebugUpdateDone().write_to(self.writer)
                self.writer.flush()
            else:
                raise Exception("Unexpected server message")


if __name__ == "__main__":
    host = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
    port = 31001 if len(sys.argv) < 3 else int(sys.argv[2])
    token = "0000000000000000" if len(sys.argv) < 4 else sys.argv[3]
    StrategyRunner(Strat, host, port, token).run()
