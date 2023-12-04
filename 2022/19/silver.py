from __future__ import annotations

import enum
import math
import re
import typing
from copy import copy


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
            for material, num in needed_material.items():
                self.material[material] -= num
            print(f"t={self.t}: Spend {needed_material} to create {new_robot} "
                  f"=> {self.workers[new_robot]+1} total")

        for robot, num in self.workers.items():
            output_material = Material(robot.value)
            self.material[output_material] += num
            if num > 0:
                print(f"t={self.t}: {num} {robot} gathers {num} {output_material} "
                      f"=> {self.material[output_material]}")

        self.t += 1

        # Robot is ready at end of this minute
        if new_robot is not None:
            self.workers[new_robot] += 1
            print(f"t={self.t}: {new_robot} created => {self.workers[new_robot]} total")

    @staticmethod
    def div(material: dict[Material, int], bots: dict[Robot, int]) -> dict[Material, float]:
        out = {}
        for mat in Material:
            robot = Robot(mat.value)
            if bots.get(robot, 0) > 0:
                out[mat] = material.get(mat, 0) / bots[robot]
            elif material.get(mat, 0) > 0:
                out[mat] = math.inf
            else:
                out[mat] = 0
        return out

    def needed_time_to_gather_materials_for_bot(
            self,
            wanted_bot: Robot,
            margin: dict[Material, int] = None,
    ) -> dict[Material, float]:
        if margin is None:
            margin = {}

        needed_materials = copy(self.blueprint[wanted_bot])

        # subtract what we already have in stock, and include margin
        for mat in needed_materials.keys():
            needed_materials[mat] -= self.material[mat] - margin.get(mat, 0)

        needed_materials_ticks = self.div(needed_materials, self.workers)
        return needed_materials_ticks

    def argmax(self, m: dict[typing.Any, float]) -> typing.Any:
        positive = {
            k: v
            for k, v in m.items()
            if v > 0
        }
        if len(positive) == 0:
            return None

        s = sorted(m.keys(), key=lambda k: m[k], reverse=True)
        return s[0]

    def mostly_needed_bot(self, to_make_bot: Robot = Robot.Geode) -> list[Robot]:
        needed_time_to_gather_material = self.needed_time_to_gather_materials_for_bot(to_make_bot)
        print(f"    time to make {to_make_bot}: {needed_time_to_gather_material}")
        bottleneck_material = self.argmax(needed_time_to_gather_material)
        if bottleneck_material is None:
            return [to_make_bot]

        if needed_time_to_gather_material[bottleneck_material] == math.inf:
            # bottleneck is not made at all, start there
            return self.mostly_needed_bot(Robot(bottleneck_material.value))

        # Should we wait for the material for to_make_bot to be available?
        # Or should we increase the capacity there?

        bottleneck_bot = Robot(bottleneck_material.value)
        # If we'd make bottleneck_bot instead, would this push back to_make_bot?
        expected_start_time = max(needed_time_to_gather_material.values())
        needed_time_to_gather_material_2 = self.needed_time_to_gather_materials_for_bot(
            to_make_bot,
            self.blueprint[bottleneck_bot],
        )
        new_start_time = max(needed_time_to_gather_material_2.values())
        if new_start_time <= expected_start_time:  # no push back, go for it
            return [to_make_bot, *self.mostly_needed_bot(bottleneck_bot)]

        return [to_make_bot]


s = Simulation(blueprint[2])
for t in range(TIME):
    print(f"t={t}, mat at hand: {s.material}")
    print(f"     workers at hand: {s.workers}")
    mostly_needed_bots = s.mostly_needed_bot()
    print(f"     need most: {mostly_needed_bots}")
    while len(mostly_needed_bots):
        bot = mostly_needed_bots.pop(0)
        try:
            s.tick(bot)
            break
        except ValueError:
            mat = s.argmax(s.needed_time_to_gather_materials_for_bot(bot))
            #reserved_material[mat] = reserved_material.get(mat, 0) + s.blueprint[bot][mat]
            #print(f"    {bot} not available")
    else:
        s.tick(None)
    print()

assert s.t == TIME
print(s.material[Material.Geode])


# sample-1: [None, None, <Robot.Clay: 'clay'>, None, <Robot.Clay: 'clay'>, None, <Robot.Clay: 'clay'>, None, None, None, <Robot.Obsidian: 'obsidian'>, <Robot.Clay: 'clay'>, None, None, <Robot.Obsidian: 'obsidian'>, None, None, <Robot.Geode: 'geode'>, <Robot.Clay: 'clay'>, None, <Robot.Geode: 'geode'>, None, <Robot.Clay: 'clay'>, None, None] => 9
# sample-2: [None, None, <Robot.Ore: 'ore'>, None, <Robot.Ore: 'ore'>, <Robot.Clay: 'clay'>, <Robot.Clay: 'clay'>, <Robot.Clay: 'clay'>, <Robot.Clay: 'clay'>, <Robot.Clay: 'clay'>, <Robot.Obsidian: 'obsidian'>, <Robot.Clay: 'clay'>, <Robot.Obsidian: 'obsidian'>, <Robot.Obsidian: 'obsidian'>, <Robot.Obsidian: 'obsidian'>, <Robot.Clay: 'clay'>, <Robot.Obsidian: 'obsidian'>, <Robot.Geode: 'geode'>, <Robot.Obsidian: 'obsidian'>, <Robot.Geode: 'geode'>, <Robot.Obsidian: 'obsidian'>, <Robot.Geode: 'geode'>, <Robot.Obsidian: 'obsidian'>, <Robot.Geode: 'geode'>, None] => 12
