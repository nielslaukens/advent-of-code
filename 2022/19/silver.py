from __future__ import annotations

import enum
import numbers
import re
import typing
from copy import copy

from tools import tree_pruning
from tools.tree_pruning import Tree


class Material(enum.Enum):
    Ore = 'ore'
    Clay = 'clay'
    Obsidian = 'obsidian'
    Geode = 'geode'


class Robot(enum.Enum):
    Ore = 'ore'
    Clay = 'clay'
    Obsidian = 'obsidian'
    Geode = 'geode'



TIME = 24  # minutes


blueprint = {}
with open("sample.txt", "r") as f:
    for line in f:
        match = re.match(r'^Blueprint (\d+): (.*)',
                         line)
        if not match:
            raise ValueError(line)
        blueprint_nr = int(match.group(1))
        blueprint[blueprint_nr] = {}
        factories = [_.strip()
                     for _ in match.group(2).split('.')
                     if _ != ""]
        for factory in factories:
            match = re.match(r'Each (\w+) robot costs (.*)', factory)
            if not match:
                raise ValueError(factory)
            output = Robot(match.group(1))
            inputs = match.group(2).split(' and ')
            parsed_inputs = {}
            for input in inputs:
                match = re.match(r'(\d+) (\w+)', input)
                material = Material(match.group(2))
                parsed_inputs[material] = int(match.group(1))

            blueprint[blueprint_nr][output] = parsed_inputs

# for bpn, bp in blueprint.items():
#     print(f"Blueprint {bpn}")
#     for r, i in bp.items():
#         print(f"  {r} : {i}")


class Simulation:
    def __init__(self, blueprint: dict[Robot, dict[Material, int]]):
        self.workers = {
            Robot.Ore: 1,
            Robot.Clay: 0,
            Robot.Obsidian: 0,
            Robot.Geode: 0,
        }
        self.material = {
            Material.Ore: 0,
            Material.Clay: 0,
            Material.Obsidian: 0,
            Material.Geode: 0,
        }
        self.blueprint = blueprint
        self.t = 0

    def __copy__(self) -> Simulation:
        c = Simulation(self.blueprint)
        c.workers = {**self.workers}
        c.material = {**self.material}
        c.t = self.t
        return c

    def tick(self, new_robot: Robot | None):
        if new_robot is not None:
            needed_material = self.blueprint[new_robot]
            for material, num in needed_material.items():
                if self.material[material] < num:
                    raise ValueError(f"Not enough {material} for {new_robot}: need {num}, have {self.material[material]}")
                self.material[material] -= num
            # print(f"t={self.t}: Spend {needed_material} to create {new_robot}."
            #       f"=> {self.workers[new_robot]+1} total")

        for robot, num in self.workers.items():
            output_material = Material(robot.value)
            self.material[output_material] += num
            # if num > 0:
            #     print(f"t={self.t}: {num} {robot} gathers {num} {output_material} "
            #           f"=> {self.material[output_material]}")

        self.t += 1

        # Robot is ready at end of this minute
        if new_robot is not None:
            self.workers[new_robot] += 1


class ChosenPath(tree_pruning.Tree):
    # For every tick, we can choose to do nothing, or create a new robot
    # This makes a decision tree, where we need to find the optimal path
    def __init__(self, blueprint, choices: list[Robot | None] = None):
        if choices is None:
            choices = []
        self.blueprint = blueprint
        self.choices = choices
        self._sim = None

    def simulate(self):
        if self._sim is None:
            self._sim = Simulation(self.blueprint)
            for c in self.choices:
                self._sim.tick(c)  # may raise
        return self._sim

    def do_choice(self, c: Robot | None) -> ChosenPath:
        cp = ChosenPath(self.blueprint, [*self.choices, c])
        cp._sim = copy(self._sim)
        cp._sim.tick(c)
        return cp

    def branches(self) -> typing.Collection[tuple[typing.Any, Tree]]:
        if len(self.choices) == TIME:
            try:
                return [(None, tree_pruning.Leaf(self.simulate().material[Material.Geode]))]
            except ValueError:
                return []

        b = []
        try:
            b.append((Robot.Geode, self.do_choice(Robot.Geode)))
        except ValueError:
            pass
        try:
            b.append((Robot.Obsidian, self.do_choice(Robot.Obsidian)))
        except ValueError:
            pass
        try:
            b.append((Robot.Clay, self.do_choice(Robot.Clay)))
        except ValueError:
            pass
        try:
            b.append((Robot.Ore, self.do_choice(Robot.Ore)))
        except ValueError:
            pass

        b.append((None, self.do_choice(None)))

        return b

    def score_guaranteed_below(self, score: numbers.Real) -> bool:
        sim = self.simulate()
        current_open_geodes = sim.material[Material.Geode]
        current_geode_bots = sim.workers[Robot.Geode]
        time_remaining = TIME - sim.t
        while time_remaining > 0:
            current_open_geodes += current_geode_bots
            current_geode_bots += 1
            time_remaining -= 1
        return current_open_geodes < score


cp = ChosenPath(blueprint[2])
best = cp.search_best_leaf()
print(best)
