names = []

while True:
    name_add = input("Adj meg egy nevet ")
    if name_add == "":
        break
    names.append(name_add)

print(names)