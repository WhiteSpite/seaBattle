from exceptions import *
from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, bow_dot, length, orientation):
        self.bow_dot = bow_dot
        self.length = self.hp = length
        self.orientation = orientation

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow_dot.x
            cur_y = self.bow_dot.y
            if self.orientation == 0:
                cur_x += i
            elif self.orientation == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def contour(self, board, verb=False):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for d in self.dots:
                    cur = Dot(d.x + dx, d.y + dy)
                    if not (board.is_dot_out(cur) or cur in board.busy_dots):
                        if verb:
                            board.field[cur.y][cur.x] = '.'
                        board.busy_dots.append(cur)

    def is_hit(self, hit_dot):
        return hit_dot in self.dots


class Board:
    def __init__(self, size=6, hidden=False):
        self.hidden = hidden
        self.size = size
        self.defeated_ships_counter = 0
        self.busy_dots = []
        self.ships = []
        self.field = [['0'] * self.size for _ in range(self.size)]

    def __str__(self):
        res = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{1 + i} | " + " | ".join(row) + " |"
        if self.hidden:
            res = res.replace("█", '0')
        return res

    def is_dot_out(self, dot):
        return not all(0 <= getattr(dot, i) < self.size for i in dot.__dir__()[:2])

    def add_ship(self, ship):
        if any(self.is_dot_out(d) or d in self.busy_dots for d in ship.dots):
            raise ShipIncorrectPlacementExc()
        for d in ship.dots:
            self.field[d.y][d.x] = "█"
            self.busy_dots.append(d)
        ship.contour(self)
        self.ships.append(ship)

    def shot(self, dot):
        if self.is_dot_out(dot):
            raise OffBoardExc()
        if dot in self.busy_dots:
            raise DotAlreadyHitExc()
        self.busy_dots.append(dot)
        for ship in self.ships:
            if ship.is_hit(dot):
                ship.hp -= 1
                self.field[dot.y][dot.x] = 'X'
                if ship.hp == 0:
                    self.defeated_ships_counter += 1
                    ship.contour(self, verb=True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен!')
                    return True
        self.field[dot.y][dot.x] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy_dots = []


class Player:
    def __init__(self, self_board, enemy_board):
        self.self_board = self_board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except GameExc as e:
                print(e)


class AI(Player):
    def ask(self):
        dot = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {dot.x + 1} {dot.y + 1}')
        return dot


class User(Player):
    def ask(self):
        while True:
            coords = input('Ваш ход. Введите координаты через пробел:').split()
            if len(coords) != 2:
                print('Введите две координаты!')
                continue
            try:
                x, y = map(int, coords)
            except ValueError:
                print('Введите числа!')
                continue
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self):
        user_board = self.build_board()
        ai_board = self.build_board()
        ai_board.hidden = True

        self.ai = AI(ai_board, user_board)
        self.user = User(user_board, ai_board)

    def build_board(self):
        ship_lenths = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        for l in ship_lenths:
            while True:
                attempts += 1
                if attempts > 1000:
                    try:
                        return self.build_board()
                    except RecursionError:
                        return self.build_board()
                ship = Ship(Dot(randint(0, board.size), randint(0, board.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except ShipIncorrectPlacementExc:
                    pass
        board.busy_dots = []
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" Формат ввода: x y ")
        print(" x - номер столбца  ")
        print(" y - номер строки ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.user.self_board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.self_board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if not repeat:
                num += 1

            if self.ai.self_board.defeated_ships_counter == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.user.self_board.defeated_ships_counter == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break

    def start(self):
        self.greet()
        self.loop()


Game().start()
