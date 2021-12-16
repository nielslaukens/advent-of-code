import dataclasses
import enum
import io
import typing


def hex_to_bin(h: str) -> str:
    out = ""
    for ch in h:
        i = int(ch, 16)
        b = ('0' * 4 + format(i, 'b'))[-4:]
        out += b
    return out


def read_int(bit_reader: typing.TextIO, num_bits: int) -> int:
    b = bit_reader.read(num_bits)
    if len(b) < num_bits:
        raise BufferError(f"Requested {num_bits} from BitReader, but got onl {len(b)}")
    return int(b, 2)


class LiteralPacketData(int):
    @classmethod
    def from_bit_reader(cls, bit_reader: typing.TextIO) -> "LiteralPacketData":
        value_bits = ""
        while True:
            chunk = bit_reader.read(5)
            value_bits += chunk[1:]
            if chunk[0] == '0':
                break
        return cls(int(value_bits, 2))

@dataclasses.dataclass()
class Operator:
    operands: typing.List

    class LengthType(enum.Enum):
        TotalLength = 0
        NumSubPackets = 1

    @classmethod
    def from_bit_reader(cls, bit_reader: typing.TextIO) -> "Operator":
        mode = Operator.LengthType(int(bit_reader.read(1), 2))
        if mode == Operator.LengthType.TotalLength:
            total_length = read_int(bit_reader, 15)
            sub_packets_bit_string = io.StringIO(bit_reader.read(total_length))
            sub_packets = []
            try:
                while True:
                    p = Packet.from_bit_reader(sub_packets_bit_string)
                    sub_packets.append(p)
            except BufferError:
                pass
        elif mode == Operator.LengthType.NumSubPackets:
            num_subpackets = read_int(bit_reader, 11)
            sub_packets = []
            for i in range(num_subpackets):
                p = Packet.from_bit_reader(bit_reader)
                sub_packets.append(p)
        else:
            raise ValueError("Unrecognized mode")

        return cls(
            operands=sub_packets,
        )


@dataclasses.dataclass
class Packet:
    class PacketType(enum.Enum):
        def __new__(cls, value, data_type):
            obj = object.__new__(cls)
            obj._value_ = value
            obj.data_type = data_type
            return obj
        Oper0 = (0, Operator)
        Oper1 = (1, Operator)
        Oper2 = (2, Operator)
        Oper3 = (3, Operator)
        Literal = (4, LiteralPacketData)
        Oper5 = (5, Operator)
        Oper6 = (6, Operator)
        Oper7 = (7, Operator)

    version: int
    packet_type: int
    data: typing.Any

    @classmethod
    def from_bit_reader(cls, bit_reader: typing.TextIO) -> "Packet":
        version = read_int(bit_reader, 3)
        packet_type = read_int(bit_reader, 3)
        packet_type = Packet.PacketType(packet_type)
        try:
            data = packet_type.data_type.from_bit_reader(bit_reader)
        except AttributeError:
            data = None

        return cls(
            version=version,
            packet_type=packet_type,
            data=data,
        )


def test_literal():
    bit_reader = io.StringIO(hex_to_bin("D2FE28"))
    p = Packet.from_bit_reader(bit_reader)
    assert p.version == 6
    assert p.packet_type == Packet.PacketType.Literal
    assert p.data == 2021
test_literal()


def test_oper_len():
    bit_reader = io.StringIO(hex_to_bin("38006F45291200"))
    p = Packet.from_bit_reader(bit_reader)
    assert p.version == 1
    assert p.packet_type == Packet.PacketType.Oper6
    assert len(p.data.operands) == 2
    assert p.data.operands[0].packet_type == Packet.PacketType.Literal
    assert p.data.operands[0].data == 10
    assert p.data.operands[1].packet_type == Packet.PacketType.Literal
    assert p.data.operands[1].data == 20
test_oper_len()

def test_oper_num():
    bit_reader = io.StringIO(hex_to_bin("EE00D40C823060"))
    p = Packet.from_bit_reader(bit_reader)
    assert p.version == 7
    assert p.packet_type == Packet.PacketType.Oper3
    assert len(p.data.operands) == 3
    assert p.data.operands[0].packet_type == Packet.PacketType.Literal
    assert p.data.operands[0].data == 1
    assert p.data.operands[1].packet_type == Packet.PacketType.Literal
    assert p.data.operands[1].data == 2
    assert p.data.operands[2].packet_type == Packet.PacketType.Literal
    assert p.data.operands[2].data == 3
test_oper_num()


def sum_versions(tree: Packet):
    s = tree.version
    if isinstance(tree.data, Operator):
        for op in tree.data.operands:
            s += sum_versions(op)
    return s

def test_sum_1():
    bit_reader = io.StringIO(hex_to_bin("8A004A801A8002F478"))
    p = Packet.from_bit_reader(bit_reader)
    s = sum_versions(p)
    assert s == 16
test_sum_1()

def test_sum_2():
    bit_reader = io.StringIO(hex_to_bin("620080001611562C8802118E34"))
    p = Packet.from_bit_reader(bit_reader)
    s = sum_versions(p)
    assert s == 12
test_sum_2()

def test_sum_3():
    bit_reader = io.StringIO(hex_to_bin("C0015000016115A2E0802F182340"))
    p = Packet.from_bit_reader(bit_reader)
    s = sum_versions(p)
    assert s == 23
test_sum_3()

def test_sum_4():
    bit_reader = io.StringIO(hex_to_bin("A0016C880162017C3686B18A3D4780"))
    p = Packet.from_bit_reader(bit_reader)
    s = sum_versions(p)
    assert s == 31
test_sum_4()

with open("16.input.txt", "r") as f:
    bit_reader = io.StringIO(hex_to_bin(f.read().strip()))
p = Packet.from_bit_reader(bit_reader)
print(f"Sum of versions: {sum_versions(p)}")