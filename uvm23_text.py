# uvm23_text.py — Ассемблер для УВМ, Вариант 23 (текстовый файл)

import argparse  # Импортируем библиотеку для обработки аргументов командной строки

import re

# ==========================
# Функции для формирования команд УВМ
# ==========================

def mask(n):
    # Создаёт маску из n битов (например, n=7 => 0b1111111 = 127)
    return 2**n - 1

# Загрузка константы в аккумулятор (команда const)
def asm_const(A: int, B: int):
    cmd = 0
    cmd |= A & mask(7)           # Биты 0-6 — поле A
    cmd |= (B & mask(15)) << 7   # Биты 7-21 — поле B
    return cmd.to_bytes(4, 'little')  # Преобразуем в 4 байта в порядке little-endian

# Чтение значения из памяти (команда read)
def asm_read(A: int, B: int):
    cmd = 0
    cmd |= A & mask(7)           # Биты 0-6 — поле A
    cmd |= (B & mask(25)) << 7   # Биты 7-31 — адрес памяти
    return cmd.to_bytes(4, 'little')

# Запись значения в память (команда write)
def asm_write(A: int, B: int):
    cmd = 0
    cmd |= A & mask(7)           # Биты 0-6 — поле A
    cmd |= (B & mask(25)) << 7   # Биты 7-31 — адрес памяти
    return cmd.to_bytes(4, 'little')

# Унарная операция abs() (команда abs)
def asm_abs(A: int, B: int):
    cmd = 0
    cmd |= A & mask(7)           # Биты 0-6 — поле A
    cmd |= (B & mask(8)) << 7    # Биты 7-14 — смещение
    return cmd.to_bytes(4, 'little')




# ==========================
# Функция сборки всей программы
# ==========================
def asm(program):
    mass = b""  # Инициализация пустой бинарной строки
    for cmd in program:
        op = cmd["op"]            # Определяем тип операции (const, read, write, abs)
        A = cmd.get("A", 0)       # Получаем значение A, если есть, иначе 0
        B = cmd.get("B", 0)       # Получаем значение B, если есть, иначе 0
        if op == "const":
            mass += asm_const(A, B)
        elif op == "read":
            mass += asm_read(A, B)
        elif op == "write":
            mass += asm_write(A, B)
        elif op == "abs":
            mass += asm_abs(A, B)
        else:
            raise ValueError(f"Неизвестная операция: {op}")
    return mass  # Возвращаем всю программу в виде бинарного кода


# ==========================
# Этап 1
# ==========================

def test():
    # Проверка правильности формирования команд
    assert list(asm_const(12, 208)) == [0x0C, 0x68, 0x00, 0x00]   # const
    assert list(asm_read(106, 225)) == [0xEA, 0x70, 0x00, 0x00]   # read
    assert list(asm_write(95, 421)) == [0xDF, 0xD2, 0x00, 0x00]   # write
    assert list(asm_abs(85, 90)) == [0x55, 0x2D, 0x00, 0x00]      # abs
test()  # Запуск теста сразу при запуске программы

parser = argparse.ArgumentParser(description="Ассемблер для УВМ — Вариант 23")
parser.add_argument("-i", "--input", required=True, help="Входной текстовый файл программы")  # Путь к исходному текстовому файлу
parser.add_argument("-o", "--output", required=True, help="Выходной бинарный файл")           # Путь к бинарному выходу
parser.add_argument("-t", "--test", type=int, default=0, help="Режим тестирования (1=on)")   # Флаг тестирования
args = parser.parse_args()  # Разбор аргументов командной строки


program = []
with open(args.input, "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Парсим строки вида: name(A, B) с поддержкой отрицательных чисел
        match = re.match(r"(\w+)\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", line)
        if not match:
            raise ValueError(f"Неверный формат строки: {line}")

        op = match.group(1).lower()
        A = int(match.group(2))
        B = int(match.group(3))

        program.append({"op": op, "A": A, "B": B})


# вывод промежуточного представления 
if args.test:
    print("Промежуточное представление программы:")
    for cmd in program:
        print(cmd)  # Выводим словари вида 
        




# ==========================
# Этап 2: формирование машинного кода
# ==========================
asm_result = asm(program)  # Генерация бинарного кода всей программы

# Запись бинарного кода в файл
with open(args.output, "wb") as f:
    f.write(asm_result)

# Вывод размера бинарного файла
print(f"Размер бинарного файла: {len(asm_result)} байт")

# Печать  команд в тестовом режиме
if args.test:
    print("Машинный код")
    print(" ".join(f"{b:02X}" for b in asm_result))
    
    
    

    
    
    



# python uvm23_text.py -i uvm23-test.txt -o uvm23-output.bin -t 1 запуск программы этой командой