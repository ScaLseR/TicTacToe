import copy
import random
EMPTY_SYMBOL = ' '


class Board:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.board = [[EMPTY_SYMBOL] * n for i in range(n)]

    #отображение игровой доски в консоли
    def viev_board(self, board):
        for i in range(self.n):
            print('-' * (self.n * 3 + (self.n + 1)))
            for j in range(self.n):
                print('|', board[i][j], end=' ')
            print('|')
        print('-' * (self.n * 3 + (self.n + 1)))

    # подсчитываем количество определенных символов в списке всех диагоналей
    def count_sybmol_diag(self, list_diag, symbol):
        for diag in list_diag:
            if diag.count(symbol) == self.m:
                return True

    #подсчитываем количество определенных символов в списке
    def count_symbol_list(self, list_symbol, symbol):
        if list_symbol.count(symbol) == self.m:
            return True

    #пподсчитываем количество определенных символов по строке
    def is_win_row(self, x, symbol, board):
        if self.count_symbol_list(board[x], symbol):
            return True

    #подсчитываем количество определенных символов по столбцу
    def is_win_column(self, y, symbol, board):
        if self.count_symbol_list([col[y] for col in board], symbol):
            return True

    # подсчитываем количество определенных символов по диагоналям
    def is_win_diagon(self, symbol, board):
        #если n = m смотрим только основную и побочную диагональ
        if self.n == self.m:
            mdiag = []; sdiag = []
            for i in range(self.n):
                mdiag.append(board[i][i])
                sdiag.append(board[i][self.n - i - 1])
            if self.count_symbol_list(mdiag, symbol) or self.count_symbol_list(sdiag, symbol):
                return True
        #смотрим все возможные диагонали
        if self.n > self.m:
            diag_dn = []; diag_up = []
            for p in range(2 * self.n - 1):
                diag_dn.append([board[p - q][q] for q in range(max(0, p - self.n + 1), min(p, self.n - 1) + 1)])
                diag_up.append([board[self.n - p + q - 1][q] for q in range(max(0, p - self.n + 1), min(p, self.n - 1) + 1)])
                if self.count_sybmol_diag(diag_dn, symbol) or self.count_sybmol_diag(diag_up, symbol):
                    return True

    #основная проверка на выйгрыш
    def is_win(self, x, y, symbol, board):
        if self.is_win_row(x, symbol, board) or self.is_win_column(y, symbol, board) or self.is_win_diagon(symbol, board):
            return True

    #размещение символа на игровой доске
    def put_symbol(self, x, y, symbol):
        if x >= self.n or y >= self.n:
            print('Введены координаты за пределами поля. Введите корректные координаты!')
            return False
        else:
            if self.is_empty(x, y):
                self.board[x][y] = symbol
                if self.is_win(x, y, symbol, self.board):
                    self.viev_board(self.board)
                    print('*' * 44)
                    print('* Внимание!!! Победил игрок играющий за:', symbol, '*')
                    print('*' * 44)
                    exit()
                else:
                    count = self.count_empty_cells()
                    if len(count) <= 1:
                        self.viev_board(self.board)
                        print('*' * 10)
                        print('* Ничья! *')
                        print('*' * 10)
                        exit()
            else:
                print('Данная клетка занята! Введите координаты пустой клетки!')
                return False
        self.viev_board(self.board)
        return True

    #проверка клетки на наличие символов
    def is_empty(self, x, y):
        if self.board[x][y] == EMPTY_SYMBOL:
            return True

    #получение копии игровой доски
    def board_copy(self):
        c_board = copy.deepcopy(self.board)
        return c_board

    #получаем список кординат свободных клеток
    def count_empty_cells(self):
        count = []
        for i in range(self.n):
            for j in range(self.n):
                if self.is_empty(i, j):
                    count.append([i, j])
        return count

        # получаем список кординат свободных клеток
    def count_empty_corner(self):
        count = []
        if self.n == 3 and (self.is_empty(0, 0)):
            count.append([0, 0])
        if self.n == 3 and (self.is_empty(0, 2)):
            count.append([0, 2])
        if self.n == 3 and (self.is_empty(2, 0)):
            count.append([2, 0])
        if self.n == 3 and (self.is_empty(2, 2)):
            count.append([2, 2])
        return count

    #проверяем является ли следующий ход победным
    def if_win_hod(self, symbol):
        hod = []
        for i in range(self.n):
            for j in range(self.n):
                c_board = self.board_copy()
                if self.is_empty(i, j):
                    c_board[i][j] = symbol
                    if self.is_win(i, j, symbol, c_board):
                        hod.append([i, j])
        return hod

    #вычисляем координаты хода АИ
    def AI_get_xy(self, symbol):
        if symbol == 'X':
            pl_symbol = 'O'
        else:
            pl_symbol = 'X'
        #проверка на возможность победы ИИ
        hod_c = self.if_win_hod(symbol)
        if len(hod_c) > 0:
            return hod_c[0][0], hod_c[0][1]
        #проверка на возможность победы игрока
        hod_p = self.if_win_hod(pl_symbol)
        if len(hod_p) > 0:
            return hod_p[0][0], hod_p[0][1]
        #если играем на поле 3*3 и не занят центр, то занимаем
        if self.n == 3 and self.is_empty(1, 1):
            return 1, 1
        # если играем на поле 3*3 первым делом занимаем углы
        hod = self.count_empty_corner()
        if len(hod) > 0:
            pos = random.randint(0, len(hod) - 1)
            return hod[pos][0], hod[pos][1]
        #ходим на любую свободную клетку
        hod = self.count_empty_cells()
        if len(hod) > 0:
            pos = random.randint(0, len(hod)-1)
            return hod[pos][0], hod[pos][1]


class Player:
    def __init__(self, symbol, board):
        self.board = board
        self.symbol = symbol

    #ввод правильных координат игроком
    def valid_coord(self):
        while True:
            try:
                x, y = input('Введите координаты (X,Y) - куда поставим: ' + self.symbol + '? ').split()
                x = int(x); y = int(y)
                if x >= 0 and y >= 0:
                    return x, y
            except:
                print('Введите верные координаты! Число пробел число')

    #ход игрока, отправка символа игрока на доску
    def p_move(self):
        rez = False
        while not rez:
            x, y = self.valid_coord()
            rez = self.board.put_symbol(x, y, self.symbol, self.board)


class AIPlayer:
    def __init__(self, symbol, board):
        self.board = board
        self.symbol = symbol

    def p_move(self):
        print('---Ход ИИ---')
        x, y = self.board.AI_get_xy(self.symbol)
        _ = self.board.put_symbol(x, y, self.symbol, self.board)


class Game:
    players = []

    #обработка ввода правильных цифровых значений
    def valid_input_dig(self, text, n=0):
        while True:
            vvod = input(text)
            if vvod.isdigit() and int(vvod) >= n:
                return int(vvod)
            else:
                if n == 0:
                    print('Введите число!')
                elif n == 2:
                    print('Введите число игроков 2 и больше!')

    #обработка ввода правильных буквенных ответов на диалоги
    def valid_input_let(self, text, zn1, zn2):
        while True:
            vvod = input(text + '"' + zn1 + '" или "' + zn2 + '": ')
            if vvod.isalpha() and (vvod == zn1 or vvod == zn2):
                return vvod
            else:
                print('Введите ' + '"' + zn1 + '" или "' + zn2 + '"!')

    #основная конфигурация игры
    def config(self):
        n = self.valid_input_dig('Введите размер поля N*N: ')
        m = self.valid_input_dig('Введите длину выигрышной линии M: ')
        board = Board(n, m)
        col_players = self.valid_input_dig('Введите количество игроков(2 и больше): ', 2)
        if col_players == 2:
            xod = self.valid_input_let('Вы хотите ходить первыми? - ', 'y', 'n')
            if xod == 'y':
                p1 = Player('X', board)
                game.add_players(p1)
                otv = self.valid_input_let('Вторым игроком будет ИИ или человек? - ', 'ii', 'p')
                if otv == 'ii':
                    p2 = AIPlayer('O', board)
                elif otv == 'p':
                    p2 = Player('O', board)
                game.add_players(p2)
            elif xod == 'n':
                otv = self.valid_input_let('Первым игроком будет ИИ или человек? - ', 'ii', 'p')
                if otv == 'ii':
                    p1 = AIPlayer('X', board)
                elif otv == 'p':
                    p1 = Player('X', board)
                game.add_players(p1)
                p2 = Player('O', board)
                game.add_players(p2)
        elif col_players > 2:
            pl = Player('X', board)
            game.add_players(pl)
            print('Первый игрок ставит "X" ')
            for i in range(col_players - 1):
                symbol = input(f'Введите символ игрока {i+2} : ')
                pl = Player(symbol, board)
                game.add_players(pl)
        game.start()

    #добавление игроков
    def add_players(self, player):
        self.players.append(player)

    #старт игры
    def start(self):
        while True:
            for player in self.players:
                player.p_move()

if __name__ == '__main__':
    game = Game()
    game.config()