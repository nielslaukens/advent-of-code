"""
Too slow
Runtime sample: 30s
Runtime input: 34s
"""

import dataclasses
import functools
import typing

from tools.graph.dijkstra import dijkstra


class IllegalMove(Exception):
    pass


CHAMBER_DEPTH = 2
CHAMBER_POS = [2, 4, 6, 8]
HALLWAY_LEN = 11
ENERGY_MAP = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
class GameState:
    @dataclasses.dataclass(frozen=True)
    class Position:
        chamber: typing.Optional[int]
        x: int

    def __init__(
            self,
            players: typing.Mapping[str, typing.Set[Position]],
    ):
        self.players = players

    def __hash__(self) -> int:
        return hash((
            frozenset(self.players['A']),
            frozenset(self.players['B']),
            frozenset(self.players['C']),
            frozenset(self.players['D']),
        ))

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.players == other.players

    def copy(self):
        return GameState(
            players={
                k: {
                    e
                    for e in v
                }
                for k, v in self.players.items()
            },
        )

    @functools.lru_cache()
    def _hallway_chambers(self, empty=None) -> typing.Tuple[typing.List[typing.Optional[str]], typing.List[typing.List[typing.Optional[str]]]]:
        hallway = [empty] * HALLWAY_LEN
        chambers = [
            [empty] * CHAMBER_DEPTH
            for chamber in CHAMBER_POS
        ]
        for a_type, positions in self.players.items():
            for pos in positions:
                if pos.chamber is None:
                    hallway[pos.x] = a_type
                else:
                    chambers[pos.chamber][pos.x] = a_type
        return hallway, chambers

    def __str__(self) -> str:
        hallway, chambers = self._hallway_chambers('.')

        o = ''.join(hallway) + "\n"
        p = 0
        format_string = ""
        for pos in CHAMBER_POS:
            format_string += " " * (pos - p)
            format_string += "{}"
            p = pos+1
        format_string += "\n"

        for d in range(CHAMBER_DEPTH):
            o += format_string.format(*[chambers[c][d] for c in range(len(CHAMBER_POS))])

        return o

    @classmethod
    def from_string(cls, s: str) -> "GameState":
        lines = s.split('\n')
        while lines[-1] == "":
            lines = lines[:-1]

        assert lines[0] == "#############"
        assert lines[1] == "#...........#"
        #                  "###:#:#:#:###"
        #                  "  #:#:#:#:#"

        chamber_occupants = [[], [], [], []]
        for line in lines[2:-1]:
            chamber_occupants[0].append(line[3:4])
            chamber_occupants[1].append(line[5:6])
            chamber_occupants[2].append(line[7:8])
            chamber_occupants[3].append(line[9:10])

        players = {'A': set(), 'B': set(), 'C': set(), 'D': set()}
        for ch_num, chamber in enumerate(chamber_occupants):
            for pos, occ in enumerate(chamber):
                players[occ].add(GameState.Position(ch_num, pos))
        assert len(chamber_occupants[0]) == CHAMBER_DEPTH
        return GameState(
            players=players,
        )

    def _top_of_chamber(self, ch_num: int) -> typing.Optional[typing.Tuple[str, Position]]:
        hallway, chambers = self._hallway_chambers()
        for depth, occ in enumerate(chambers[ch_num]):
            if occ is not None:
                return occ, GameState.Position(ch_num, depth)
        return None

    def _exit(self, ch_num: int, hallway_pos: int) -> typing.Tuple["GameState", int]:
        """
        Exit an amphipod from its chamber into the hallway.
        Does NOT check if the path is free, only if the destination is free.
        Returns new state and delta-energy
        """
        toc = self._top_of_chamber(ch_num)
        if toc is None:
            raise ValueError(f"Chamber {ch_num} is empty. Can't exit another amphipod")
        hallway, chambers = self._hallway_chambers()
        if hallway[hallway_pos] is not None:
            raise IllegalMove(f"Hallway position {hallway_pos} is already occupied by {hallway[hallway_pos]}")

        a, pos = toc
        state = self.copy()
        state.players[a].remove(pos)
        state.players[a].add(GameState.Position(None, hallway_pos))
        energy = ENERGY_MAP[a] * (pos.x+1 + abs(CHAMBER_POS[ch_num] - hallway_pos))
        #print(f"Exitting amphipod {a} from chamber {ch_num} to hallway position {hallway_pos}, E={energy}")
        return state, energy

    def _enter(self, hallway_pos: int) -> typing.Tuple["GameState", int]:
        """
        Enter a amphipod into its chamber.
        Does not check the path, only if the destination is acceptable
        """
        hallway, chambers = self._hallway_chambers()
        a = hallway[hallway_pos]
        if a is None:
            raise ValueError(f"No amphipod at hallway {hallway_pos}")

        target_chamber = ord(a) - ord('A')
        for depth in reversed(range(CHAMBER_DEPTH)):
            if chambers[target_chamber][depth] is None:  # free slot
                break
            elif chambers[target_chamber][depth] != a:
                raise IllegalMove(f"Moving amphipod {a} into chamber {target_chamber} "
                                  f"would block amphipod {chambers[target_chamber][depth]} currently still there")
        else:
            raise AssertionError(f"Would overfill chamber {target_chamber} with amphipod {a} "
                                 f"from hallway {hallway_pos}. Should not be possible.")

        state = self.copy()
        state.players[a].remove(GameState.Position(None, hallway_pos))
        state.players[a].add(GameState.Position(target_chamber, depth))
        energy = ENERGY_MAP[a] * (abs(hallway_pos - CHAMBER_POS[target_chamber]) + depth+1)
        #print(f"Entering amphipod {a} from hallway {hallway_pos} intto chamber {target_chamber} depth {depth}, E={energy}")
        return state, energy

    def range_ch_left(self, ch_num: int) -> typing.Iterable:
        return range(CHAMBER_POS[ch_num]-1, 0-1, -1)

    def range_ch_right(self, ch_num: int) -> typing.Iterable:
        return range(CHAMBER_POS[ch_num]+1, HALLWAY_LEN)

    @staticmethod
    @functools.lru_cache
    def done_state() -> "GameState":
        p = {}
        for ch_num in range(len(CHAMBER_POS)):
            s = set()
            for depth in range(CHAMBER_DEPTH):
                s.add(GameState.Position(ch_num, depth))
            p[chr(ord('A') + ch_num)] = s
        return GameState(p)

    def possible_next_states(self) -> typing.Generator[typing.Tuple["GameState", int], None, None]:
        """
        Returns (new_state, delta_energy) tuples
        """
        if self == self.done_state():
            return

        hallway, chambers = self._hallway_chambers()

        # we can either exit a new amphipod from a chamber into the hallway
        for ch_num in range(len(CHAMBER_POS)):
            toc = self._top_of_chamber(ch_num)
            if toc is None:  # chamber empty
                continue

            # do left and right separately. So we can break if we hit something
            for hallway_position in self.range_ch_left(ch_num):
                # possible positions to the left
                if hallway_position in CHAMBER_POS:  # not above chambers
                    continue
                if hallway[hallway_position] is not None:  # we bumped in to something
                    break
                yield self._exit(toc[1].chamber, hallway_position)

            for hallway_position in self.range_ch_right(ch_num):
                # possible positions to the right
                if hallway_position in CHAMBER_POS:  # not above chambers
                    continue
                if hallway[hallway_position] is not None:  # we bumped in to something
                    break
                yield self._exit(toc[1].chamber, hallway_position)

        # or move an amphipod from the hallway into its chamber
        for ch_num in range(len(CHAMBER_POS)):
            desired_amphipod = chr(ord('A') + ch_num)
            for hallway_pos in self.range_ch_left(ch_num):
                if hallway[hallway_pos] is None:
                    continue
                if hallway[hallway_pos] == desired_amphipod:
                    try:
                        yield self._enter(hallway_pos)
                    except IllegalMove:
                        pass
                else:
                    break  # encountered something, would block entry
            for hallway_pos in self.range_ch_right(ch_num):
                if hallway[hallway_pos] is None:
                    continue
                if hallway[hallway_pos] == desired_amphipod:
                    try:
                        yield self._enter(hallway_pos)
                    except IllegalMove:
                        pass
                else:
                    break  # encountered something, would block entry


with open("23.input.txt", "r") as f:
    start_state = GameState.from_string(f.read())

print(start_state)
known_states = {start_state}
newly_discovered_states = {start_state}
edges = dict()
while len(newly_discovered_states):
    to_investigate = newly_discovered_states
    newly_discovered_states = set()
    for state in to_investigate:
        for next_state, energy in state.possible_next_states():
            assert (state, next_state) not in edges
            edges[(state, next_state)] = energy
            if next_state not in known_states:
                known_states.add(next_state)
                newly_discovered_states.add(next_state)
    print(f"Found {len(known_states)} states ({len(newly_discovered_states)} new ones to investigate)")

total_costs = dijkstra(edges, start_state.done_state())
solution = total_costs[start_state]
print(solution.cost)
