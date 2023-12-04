kalibratiewaarde = 0

cijfers_in_woorden = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

with open("input.txt", "r") as bestand:
    for lijn in bestand:
        lijn = lijn.strip()

        eerste_gevonden: tuple[int, int] = None
        for woord, cijfer in cijfers_in_woorden.items():
            index = lijn.find(woord)
            if index >= 0 and (eerste_gevonden is None or index < eerste_gevonden[0]):
                eerste_gevonden = (index, cijfer)

            index = lijn.find(str(cijfer))
            if index >= 0 and (eerste_gevonden is None or index < eerste_gevonden[0]):
                eerste_gevonden = (index, cijfer)

        eerste_cijfer = eerste_gevonden[1]

        laatst_gevonden: tuple[int, int] = None
        for woord, cijfer in cijfers_in_woorden.items():
            index = lijn.rfind(woord)
            if index >= 0 and (laatst_gevonden is None or index > laatst_gevonden[0]):
                laatst_gevonden = (index, cijfer)

            index = lijn.rfind(str(cijfer))
            if index >= 0 and (laatst_gevonden is None or index > laatst_gevonden[0]):
                laatst_gevonden = (index, cijfer)

        laatste_cijfer = laatst_gevonden[1]

        getal = int(str(eerste_cijfer) + str(laatste_cijfer))
        print(f"{lijn} {getal}")

        kalibratiewaarde += getal


print(kalibratiewaarde)
