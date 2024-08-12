#POLE = [[0, 1, 2, 3],
#        [1, 2, 3, 4],
#        [2, 3, 4, 5],
#        [3, 4, 5, 6]
#        ]
print("ПОИГРАЕМ?")

# Создаём матрицу 4x4 с нумерацией.
POLE = [[' ' if i == 0 or j == 0 else '-' for j in range(4)] for i in range(4)]

# Заполняем первую строку и первый столбец номерами.
for i in range(1, 4):
    POLE[i][0] = str(i)
    POLE[0][i] = str(i)

# Функция: Ход игрока "X".
def STEP_X(POLE):
    i = int(input("Игрок Х, введите номер строки (1-3): "))
    j = int(input("Игрок Х, введите номер столбца (1-3): "))
    if all([1 <= i < len(POLE),
            1 <= j < len(POLE[0]),
            POLE[i][j] != "X",
            POLE[i][j] != "O"
            ]):
        POLE[i][j] = "X"
    else:
        print("Ход недоступен")
    for row in POLE:
        print(*row)
    return POLE
# Функция: Ход игрока "O".
def STEP_O(POLE):
    i = int(input("Игрок О, введите номер строки (1-3): "))
    j = int(input("Игрок О, введите номер столбца (1-3): "))

    if all([1 <= i < len(POLE),
            1 <= j < len(POLE[0]),
            POLE[i][j] != "X",
            POLE[i][j] != "O"
            ]):
        POLE[i][j] = "O"
    else:
        print("Ход недоступен!!!")
    for row in POLE:
        print(*row)
    return POLE
# Функция: Проверка выигрыша игрока Х.
def check_win_X(POLE):
    # Проверка по горизонтали:
    for row in POLE[1:]:
        if len(set(row[1:])) == 1 and row[1] == 'X':
            return True
    # Проверка по вертикали:
    tr_POLE = [list(row) for row in zip(*POLE)]
    for col in tr_POLE[1:]:
        if len(set(col[1:])) == 1 and col[1] == 'X':
            return True
    # Проверка по диагонали 1:
    diag = [POLE[i][i] for i in range(1, len(POLE))]
    if len(set(diag)) == 1 and diag[0] == 'X':
        return True
    # Проверка по диагонали 2:
    diag_anti = [POLE[i][len(POLE) - i] for i in range(1, len(POLE))]
    if len(set(diag_anti)) == 1 and diag_anti[0] == 'X':
        return True

    return False
# Функция: Проверка выигрыша игрока O.
def check_win_O(POLE):
    # Проверка по горизонтали:
    for row in POLE[1:]:
        if len(set(row[1:])) == 1 and row[1] == 'O':
            return True
    # Проверка по вертикали:
    tr_POLE = [list(row) for row in zip(*POLE)]
    for col in tr_POLE[1:]:
        if len(set(col[1:])) == 1 and col[1] == 'O':
            return True
    # Проверка по диагонали 1:
    diag = [POLE[i][i] for i in range(1, len(POLE))]
    if len(set(diag)) == 1 and diag[0] == 'O':
        return True
    # Проверка по диагонали 2:
    diag_anti = [POLE[i][len(POLE) - i] for i in range(1, len(POLE))]
    if len(set(diag_anti)) == 1 and diag_anti[0] == 'O':
        return True

    return False
# Делаем ходы и проверяем условия выигрыша.
while True:
    STEP_X(POLE)
    if check_win_X(POLE):
        print('Игрок Х, Вы победили!!!')
        break
    STEP_O(POLE)
    if check_win_O(POLE):
        print('Игрок O, Вы победили!!!')
        break