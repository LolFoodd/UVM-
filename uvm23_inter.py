import argparse
# python uvm23_inter.py -i uvm23-output.bin -d dump.csv -r "0-50"

reg = 0
memory = [0] * 1000   # память данных


def execute(bytecode):
    global reg

    for i in range(0, len(bytecode), 4):
        cmd = bytecode[i:i+4]
        cmd = int.from_bytes(cmd, "little")

        # Поля УВМ В23
        A = cmd & 0b1111111      # биты 0–6
        B = cmd >> 7             # остальное

        # ====== Команды УВМ 23 ======

        # const(A=12): загрузка константы B
        if A == 12:
            reg = B

        # read(A=106): регист = память[B]
        elif A == 106:
            reg = memory[B]

        # write(A=95): память[B] = регистр
        elif A == 95:
            memory[B] = reg

        # abs(A=85): регистр = abs(память[reg + B])
        elif A == 85:
            reg = abs(memory[reg + B])


# ================= CLI =================
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-d", "--dump", required=True)
parser.add_argument("-r", "--range", required=True)

args = parser.parse_args()

with open(args.input, "rb") as f:
    bytecode = f.read()

execute(bytecode)

print("REG =", reg)

# диапазон вида "0-100"
start, end = args.range.split("-")
start = int(start)
end = int(end)

# Дамп памяти в CSV
with open(args.dump, "w") as f:
    f.write("Address,Value\n")
    for addr in range(start, end + 1):
        f.write(f"{addr},{memory[addr]}\n")

print("Дамп сохранён в:", args.dump)
