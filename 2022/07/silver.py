from __future__ import annotations
import dataclasses
import typing


@dataclasses.dataclass
class File:
    size: int


@dataclasses.dataclass
class Dir:
    parent: Dir
    content: dict[str, Dir | File] = dataclasses.field(default_factory=dict)

    @property
    def name(self) -> str:
        if self.parent is None:
            return None
        for k, v in self.parent.content.items():
            if v == self:
                return k
        raise KeyError("Not found in parent, orphan dir")

    @property
    def path(self) -> str:
        e = self
        l = [self.name]
        while e.parent is not None:
            e = e.parent
            l.insert(0, e.name)
        assert l[0] is None
        del l[0]
        return '/' + '/'.join(l)

    def pretty_print(self, indent: int = 0):
        for k, v in self.content.items():
            print(f"{' ' * indent}{k} ({'dir' if isinstance(v, Dir) else v.size})")
            if isinstance(v, Dir):
                v.pretty_print(indent+2)

    def total_size(self) -> int:
        s = 0
        for k, v in self.content.items():
            if isinstance(v, Dir):
                s += v.total_size()
            else:
                s += v.size
        return s

    def dir_iter(self) -> typing.Generator[Dir, None, None]:
        yield self
        for k, v in self.content.items():
            if isinstance(v, Dir):
                for i in v.dir_iter():
                    yield i


tree = Dir(parent=None, content=[])
state = None
pwd = None
ls = {}
with open("input.txt", 'r') as f:
    for line in f:
        line = line.rstrip()
        if line[0:2] == '$ ':
            if state == 'ls':
                #print(f"Listing {pwd.path} done; {len(ls)} entries")
                pwd.content = ls
                ls = {}
            state = 'prompt'

        if state == 'prompt':
            assert line[0:2] == "$ "
            args = line[2:].split()
            #print(f"command: {args[0]}, args: {args[1:]}")
            if args[0] == 'cd':
                if args[1] == '/':
                    pwd = tree
                    #print(f"Moving to /")
                elif args[1] == '..':
                    #print(f"Moving from {'/'.join(pwd)} up 1")
                    pwd = pwd.parent
                    #print(f"Now in {'/'.join(pwd)}")
                else:
                    #print(f"Moving from {'/'.join(pwd)} into {args[1]}")
                    if args[1] not in pwd.content:
                        print(f"Discovered dir {args[1]} in `{pwd.path}` by cd, not by ls")
                        pwd.content[args[1]] = Dir(parent=pwd)
                    pwd = pwd.content[args[1]]
                    #print(f"Now in {'/'.join(pwd)}")
            elif args == ['ls']:
                state = 'ls'
            else:
                raise ValueError("Unknown command")
        elif state == 'ls':
            a, b = line.split(' ')
            if a == 'dir':
                e = Dir(parent=pwd)
            else:
                e = File(size=int(a))
            ls[b] = e
        else:
            raise ValueError("unknown state")

    if state == 'ls':
        pwd.content = ls


#tree.pretty_print()
#print(tree.total_size())
s = 0
for d in tree.dir_iter():
    size = d.total_size()
    if size <= 100000:
        s += size
print(s)
