import copy
EMPTY_SYMBOL = ' '


class Board:

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.board = [[EMPTY_SYMBOL] * n for i in range(n)]

    #отображение игровой доски в консоли
    def viev_board(self, *board):
        if len(board) == 0:
            board = self.board
        else:
            board = board[0]
        for i in range(self.n):
            print('-' * (self.n * 3 + (self.n + 1)))
            for j in range(self.n):
                print('|', board[i][j], end=' ')
            print('|')
        print('-' * (self.n * 3 + (self.n + 1)))

    #проверка на завершение игры
    def end_game(self):
        rez = self.is_win(self.board)
        if rez == EMPTY_SYMBOL:
            print('Ничья!')
            exit()
        elif rez:
            print('Победил игрок ', rez)
            exit()

    #подсчитываем количество определенных символов подряд в списке всех диагоналей
    def count_sybmol_diag(self, list_diag):
        for diag in list_diag:
            rez = self.count_symbol_list(diag)
            if rez:
                return rez

    #подсчитываем количество одинаковых символов подряд в списке
    def count_symbol_list(self, list_symbol):
        count = 1
        for i in range(len(list_symbol)-1):
            if list_symbol[i] != EMPTY_SYMBOL:
                if list_symbol[i+1] == list_symbol[i]:
                    count += 1
                    if count == self.m:
                        return list_symbol[i]
                else:
                    count = 1

    #пподсчитываем количество определенных символов подряд по строкам
    def is_win_row(self, board):
        for i in range(self.n):
            rez = self.count_symbol_list(board[i])
            if rez:
                return rez

    #подсчитываем количество одинаковых символов подряд по столбцам
    def is_win_column(self, board):
        for i in range(self.n):
            rez = self.count_symbol_list([col[i] for col in board])
            if rez:
                return rez

    # подсчитываем количество одинаковых символов подряд по диагоналям
    def is_win_diagon(self, board):
        #если n = m смотрим только основную и побочную диагональ
        if self.n == self.m:
            mdiag = []
            sdiag = []
            for i in range(self.n):
                mdiag.append(board[i][i])
                sdiag.append(board[i][self.n - i - 1])
                rez_m = self.count_symbol_list(mdiag)
                rez_s = self.count_symbol_list(sdiag)
                if rez_m:
                    return rez_m
                if rez_s:
                    return rez_s
        #смотрим все возможные диагонали
        if self.n > self.m:
            diag_dn = []; diag_up = []
            for p in range(2 * self.n - 1):
                diag_dn.append([board[p - q][q] for q in range(max(0, p - self.n + 1), min(p, self.n - 1) + 1)])
                diag_up.append([board[self.n - p + q - 1][q] for q in range(max(0, p - self.n + 1), min(p, self.n - 1) + 1)])
                rez_dn = self.count_sybmol_diag(diag_dn)
                rez_up = self.count_sybmol_diag(diag_up)
                if rez_dn:
                    return rez_dn
                if rez_up:
                    return rez_up

    #основная проверка на выйгрыш
    def is_win(self, board):
        row = self.is_win_row(board)
        col = self.is_win_column(board)
        diag = self.is_win_diagon(board)
        if row:
            return row
        elif col:
            return col
        elif diag:
            return diag
        if len(self.count_empty_cells(board)) > 0:
            return None
        return EMPTY_SYMBOL

    #размещение символа на игровой доске
    def put_symbol(self, x, y, symbol, board):
         board[x][y] = symbol

    #проверка клетки на наличие символов
    def is_empty(self, x, y, board):
        if board[x][y] == EMPTY_SYMBOL:
            return True

    #получение копии игровой доски
    def board_copy(self):
        c_board = copy.deepcopy(self.board)
        return c_board

    #получаем список кординат свободных клеток
    def count_empty_cells(self, board):
        count = []
        for i in range(self.n):
            for j in range(self.n):
                if self.is_empty(i, j, board):
                    count.append([i, j])
        return count

    #максимизация для ai
    def max(self, ai_symbol, c_board):
        if ai_symbol == 'X':
            pl_symbol = 'O'
        else:
            pl_symbol = 'X'
        max_v = (1 - self.m)
        px = None
        py = None
        result = self.is_win(c_board)
        if result == pl_symbol:
            return (-1, 0, 0)
        elif result == ai_symbol:
            return (1, 0, 0)
        elif result == EMPTY_SYMBOL:
            return (0, 0, 0)
        for i in range(self.n):
            for j in range(self.n):
                if self.is_empty(i, j, c_board):
                    c_board[i][j] = ai_symbol
                    #self.viev_board(c_board)
                    (m, min_i, min_j) = self.min(pl_symbol, c_board)
                    if m > max_v:
                        max_v = m
                        px = i
                        py = j
                    self.put_symbol(i, j, EMPTY_SYMBOL, c_board)
        return (max_v, px, py)

    #минимизация для игрока - человека
    def min(self, pl_symbol, c_board):
        if pl_symbol == 'X':
            ai_symbol = 'O'
        else:
            ai_symbol = 'X'
        min_v = self.m - 1
        qx = None
        qy = None
        result = self.is_win(c_board)
        if result == pl_symbol:
            return (-1, 0, 0)
        elif result == ai_symbol:
            return (1 , 0, 0)
        elif result == EMPTY_SYMBOL:
            return (0, 0, 0)
        for i in range(self.n):
            for j in range(self.n):
                if self.is_empty(i, j, c_board):
                    c_board[i][j] = pl_symbol
                    #self.viev_board(c_board)
                    (m, max_i, max_j) = self.max(ai_symbol, c_board)
                    if m < min_v:
                        min_v = m
                        qx = i
                        qy = j
                    self.put_symbol(i, j, EMPTY_SYMBOL, c_board)
        return (min_v, qx, qy)

    #проверка правильности введенных игроком координат
    def valid_coord(self, symbol, human, *coord):
        if human:
            try:
                x, y = input('Введите координаты (X,Y) - куда поставим: ' + symbol + '? ').split()
                x = int(x)
                y = int(y)
                if x < 0 or x > self.n or y < 0 or y > self.n:
                    print('Введены координаты вне области игрового поля')
                    return False
                elif not self.is_empty(x, y, self.board):
                    print('Данная клетка занята')
                    return False
                else:
                    self.put_symbol(x, y, symbol, self.board)
                    return True
            except:
                print('Введите координаты: число пробел число.')
        else:
            self.put_symbol(coord[0], coord[1], symbol, self.board)


class Player:
    def __init__(self, symbol, board):
        self.board = board
        self.symbol = symbol

    #ход игрока, отправка символа игрока на доску
    def p_move(self):
        rez = False
        while not rez:
            rez = self.board.valid_coord(self.symbol, True)


class AIPlayer:
    def __init__(self, symbol, board):
        self.board = board
        self.symbol = symbol

    #ход АИ(мин-макс)
    def p_move(self):
        print('---Ход ИИ---')
        c_board = self.board.board_copy()
        _, x, y = self.board.max(self.symbol, c_board)
        _ = self.board.valid_coord(self.symbol, False, x, y)


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
        game.start(board)

    #добавление игроков
    def add_players(self, player):
        self.players.append(player)

    #старт игры
    def start(self, board):
        board.viev_board()
        while True:
            for player in self.players:
                player.p_move()
                board.viev_board()
                board.end_game()

if __name__ == '__main__':
    game = Game()
    game.config()