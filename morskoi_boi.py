from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

#################################


class Ship:
    def __init__(self, nachalo, ln, orient):  # nachalo = Dot(x, y)  orient = 0 or 1
        self.nachalo = nachalo
        self.ln = ln
        self.orient = orient
        self.live = ln

    @property
    def dots(self):
        ship_dots = []
        for n in range(self.ln):
            ship_dot_x = self.nachalo.x
            ship_dot_y = self.nachalo.y

            if self.orient == 0:
                ship_dot_x += n
            else:
                ship_dot_y += n

            ship_dots.append(Dot(ship_dot_x, ship_dot_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


######################################
class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Точка с данными координатми находятся за пределами игрового поля"


class BoardUsedException(BoardException):
    def __str__(self):
        return "В точку с данными координатми вы стреляли ранее"


class BoardShipException(BoardException):
    pass

######################################


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size
        self.pole = [['-'] * size for _ in range(size)]
        self.busy = []
        self.ships = []
        self.shot_busy = []
        self.ships_kill = 0

    def __str__(self):
        pole_fin = "   |"

        for i in range(self.size):
            pole_fin += f" {i+1} |"

        for i, j in enumerate(self.pole):
            pole_fin += f"\n {i+1} | " + " | ".join(j) + " |"

        if self.hid:
            pole_fin = pole_fin.replace("■", "-")

        return pole_fin

    def out(self, dot):
        if 0 <= dot.x < self.size and 0 <= dot.y < self.size:
            return False
        else:
            return True

    def contour(self, ship):
        for dot in ship.dots:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    cont_dot = Dot(dot.x + i, dot.y + j)

                    if not(self.out(cont_dot) or cont_dot in self.busy):
                        self.busy.append(cont_dot)
                        #  self.pole[cont_dot.x][cont_dot.y] = "•"

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardShipException()
            else:
                self.pole[dot.x][dot.y] = "■"
                self.busy.append(dot)

        self.ships.append(ship)   # .dots
        self.contour(ship)

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()

        if dot in self.shot_busy:
            raise BoardUsedException()

        self.shot_busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.live -= 1
                self.pole[dot.x][dot.y] = "X"
                if ship.live > 0:
                    print("Корабль подбит")
                    return True
                else:
                    print("Корабль уничтожен")
                    self.ships_kill += 1
                    return False

        self.pole[dot.x][dot.y] = "•"
        print("Вы промахнулись")
        return False


class Player:
    def __init__(self, mein_board, enemi_board):
        self.mein_board = mein_board
        self.enemi_board = enemi_board

    def ask(self):
            pass

    def move(self):
        while True:
            try:
                coord_vist = self.ask()
                otvet = self.enemi_board.shot(coord_vist)
                return otvet
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        dot = Dot(randint(0, 5), randint(0, 5))
        print(f"Координаты выстрела компьютера: {dot.x+1}  {dot.y+1}")
        return dot


class User(Player):
    def ask(self):
        while True:
            shot = input("Введите координаты выстрела: ").split()
            if len(shot) == 2:
                if shot[0].isdigit and shot[1].isdigit():
                    return Dot(int(shot[0]) - 1, int(shot[1]) - 1)
                else:
                    print("Введите цифры")
            else:
                print("Введите 2 значения")


class Game:
    def privet(self):
        print("---------------- ")
        print("      ИГРА       ")
        print("   морской бой   ")
        print("---------------- ")
        print("формат координат ")
        print("х - номер строки ")
        print("у - номер столбца")

    def r_board(self):
        board = None
        while board is None:
            ship_lens = [3, 2, 2, 1, 1, 1, 1]

            board = Board()
            for lens in ship_lens:

                if board is None:
                    break
                n = 0
                while True:
                    n += 1
                    if n > 2000:
                        board = None
                        break
                    ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), lens, randint(0, 1))
                    try:
                        board.add_ship(ship)
                        break
                    except BoardShipException:
                        board = None
                        break

        return board

    def __init__(self, size=6):
        self.size = size
        pole1 = self.r_board()
        pole2 = self.r_board()
        pole1.hid = True
        self.ai = AI(pole1, pole2)
        self.user = User(pole2, pole1)

    def game(self):
        n = 0
        while True:
            """print("_" * 28)
            print("  Поле игрока  ")
            print(self.user.mein_board)
            print("_" * 28)
            print("Поле компьютера")
            print(self.ai.mein_board)
            print("_" * 28)"""

            if n % 2 == 0:
                print("_" * 28)
                print("  Поле игрока  ")
                print(self.user.mein_board)
                print("_" * 28)
                print("Поле компьютера")
                print(self.ai.mein_board)
                print("_" * 28)

                print(" Выстрел игрока ")
                otvet = self.user.move()
            else:
                print(" Выстрел компьютера ")
                otvet = self.ai.move()

            if self.user.mein_board.ships_kill == 7:
                print("_" * 28)
                print("  Компьютер выиграл  ")
                break

            if self.ai.mein_board.ships_kill == 7:
                print("_" * 28)
                print("  Игрок выиграл  ")
                break

            if not otvet:
                n += 1

    def start(self):
        self.privet()
        self.game()


h = Game()
h.start()





















