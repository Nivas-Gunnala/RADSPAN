from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random


class CheckerPiece(Agent):
    def __init__(self, unique_id, model, color, is_king=False):
        super().__init__(unique_id, model)
        self.color = color  # "red" or "black"
        self.is_king = is_king

    def possible_moves(self):
        """Return a list of valid moves (including captures) following Checkers rules."""
        directions = []
        if self.color == "red" or self.is_king:
            directions.extend([(1, 1), (-1, 1)])
        if self.color == "black" or self.is_king:
            directions.extend([(1, -1), (-1, -1)])

        moves = []
        captures = []
        x, y = self.pos

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Simple move
            if self.model.grid.out_of_bounds((nx, ny)) is False and self.model.grid.is_cell_empty((nx, ny)):
                moves.append((nx, ny))
            # Capture
            elif not self.model.grid.out_of_bounds((nx, ny)):
                cell_contents = self.model.grid.get_cell_list_contents((nx, ny))
                if cell_contents and cell_contents[0].color != self.color:
                    jump_x, jump_y = nx + dx, ny + dy
                    if not self.model.grid.out_of_bounds((jump_x, jump_y)) and self.model.grid.is_cell_empty((jump_x, jump_y)):
                        captures.append((jump_x, jump_y, cell_contents[0]))

        return captures if captures else moves  # Captures take priority

    def step(self):
        moves = self.possible_moves()
        if moves:
            move = random.choice(moves)
            if isinstance(move, tuple) and len(move) == 3:
                # Capture
                target_pos = (move[0], move[1])
                captured_piece = move[2]
                self.model.grid.remove_agent(captured_piece)
                self.model.schedule.remove(captured_piece)
                self.model.grid.move_agent(self, target_pos)
            else:
                self.model.grid.move_agent(self, move)

            # King me
            if (self.color == "red" and self.pos[1] == self.model.height - 1) or \
               (self.color == "black" and self.pos[1] == 0):
                self.is_king = True


class CheckersModel(Model):
    def __init__(self, width=8, height=8):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.running = True

        # Place red pieces
        uid = 0
        for y in range(3):
            for x in range(width):
                if (x + y) % 2 == 1:
                    piece = CheckerPiece(uid, self, "red")
                    self.grid.place_agent(piece, (x, y))
                    self.schedule.add(piece)
                    uid += 1

        # Place black pieces
        for y in range(height - 3, height):
            for x in range(width):
                if (x + y) % 2 == 1:
                    piece = CheckerPiece(uid, self, "black")
                    self.grid.place_agent(piece, (x, y))
                    self.schedule.add(piece)
                    uid += 1

    def step(self):
        self.schedule.step()

        # Check win condition
        colors = {agent.color for agent in self.schedule.agents}
        if len(colors) == 1:
            self.running = False


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 0.4
    }

    portrayal["Color"] = "red" if agent.color == "red" else "black"
    if agent.is_king:
        portrayal["r"] = 0.5  # Bigger size for king

    return portrayal


# Visualization
grid = CanvasGrid(agent_portrayal, 8, 8, 500, 500)
server = ModularServer(CheckersModel, [grid], "Checkers Game", {})
server.port = 8600  # Change if needed

if __name__ == "__main__":
    server.launch()