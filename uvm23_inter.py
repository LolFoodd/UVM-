import argparse
# uvm23_inter.py — Интерпретатор УВМ, вариант 23

reg = 0
memory = [0] * 1000  # память данных


def execute(bytecode: bytes):
    """
    Выполняет машинный код УВМ-23.
    Формат команды: 4 байта, little endian
    Поля:
        A = биты 0..6
        B = биты 7..31
    """

    global reg, memory

    for i in range(0, len(bytecode), 4):
        cmd_bytes = bytecode[i:i+4]
        if len(cmd_bytes) < 4:
            break

        cmd = int.from_bytes(cmd_bytes, "little")

        A = cmd & 0b1111111              # биты 0–6
        B = cmd >> 7                     # остальное

        # ================= Команды УВМ 23 =================

        # const(A=12): reg = B
        if A == 12:
            reg = B

        # read(A=106): reg = memory[B]
        elif A == 106:
            reg = memory[B]

        # write(A=95): memory[B] = reg
        elif A == 95:
            memory[B] = reg

        # abs(A=85): reg = abs(memory[reg + B])
        elif A == 85:
            addr = reg + B
            if 0 <= addr < len(memory):
                reg = abs(memory[addr])
            else:
                reg = 0  # защита от выхода за пределы

        # неизвестная команда
        else:
            # Можно игнорировать или бросать исключение
            pass


# ================= CLI-режим =================
# (запускается только вручную из консоли)
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Интерпретатор УВМ-23")
    parser.add_argument("-i", "--input", required=True, help="Входной бинарный файл")
    parser.add_argument("-d", "--dump", required=True, help="Файл дампа CSV")
    parser.add_argument("-r", "--range", required=True, help="Диапазон дампа, например 0-50")
    args = parser.parse_args()

    with open(args.input, "rb") as f:
        bytecode = f.read()

    execute(bytecode)

    print("REG =", reg)

    start, end = args.range.split("-")
    start = int(start)
    end = int(end)

    with open(args.dump, "w") as f:
        f.write("Address,Value\n")
        for addr in range(start, end + 1):
            f.write(f"{addr},{memory[addr]}\n")

    print("Дамп сохранён в:", args.dump)
