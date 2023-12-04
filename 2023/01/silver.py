kalibratiewaarde = 0

with open("input.txt", "r") as bestand:
    for lijn in bestand:
        tekens = list(lijn)
        cijfers = list(filter(lambda teken: teken in "0123456789", tekens))
        getal = int(cijfers[0] + cijfers[-1])
        kalibratiewaarde = kalibratiewaarde + getal

print(kalibratiewaarde)
