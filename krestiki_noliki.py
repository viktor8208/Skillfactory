dannie = [[' ' for _ in range(3)]for _ in range(3)]


def vivod(z):
    print("   | 0 | 1 | 2 |")
    print("----------------")
    print(f" 0 | {z[0][0]} | {z[0][1]} | {z[0][2]} |")
    print(f" 1 | {z[1][0]} | {z[1][1]} | {z[1][2]} |")
    print(f" 2 | {z[2][0]} | {z[2][1]} | {z[2][2]} |")
    print("----------------")


vivod(dannie)


def prov_vvod():
    while True:
        vvod = (input("введите координаты через пробел: ")).split()
        if len(vvod) == 2:
            x, y = vvod
            if x.isdigit() and y.isdigit():
                x, y = map(int, vvod)
                if 0 <= x <= 2 and 0 <= y <= 2:
                    if dannie[x][y] == " ":
                        return x, y
                    else:
                        print("Клетка занята")
                        continue
                else:
                    print("Значение координат должно быть от 0 до 2")
            else:
                print("Необходимо ввести цифры")
                continue
        else:
            print("Координат должно быть две")
            continue


def prov_viigr(dan):
    comb_v = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
              ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
              ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0))]

    for comb in comb_v:
        c = []
        for c_v in comb:
            c.append(dan[c_v[0]][c_v[1]])
        if c == ["X", "X", "X"]:
            print("Крестики выиграли")
            return True
        if c == ["0", "0", "0"]:
            print("Нолики выиграли")
            return True
    return False


hod = 1
while True:
    print("Ходят нолики" if hod % 2 != 0 else "Ходят крестики")
    q, w = prov_vvod()
    if hod % 2 == 0:
        dannie[q][w] = 'X'
        vivod(dannie)

    else:
        dannie[q][w] = '0'
        vivod(dannie)

    if prov_viigr(dannie):
        print("Игра окончена")
        break
    elif hod == 9:
        print("Ничья \n Игра окончена")
        break
    hod += 1
