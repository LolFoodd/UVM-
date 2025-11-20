#Вариант 23
# Загрузка константы 


import argparse

def mask(n):
    return 2**n - 1


def asm_const(A: int, B: int):
    cmd = 0
    cmd |= A & mask(7)
    cmd |= (B & mask(15)) << 7
    return cmd.to_bytes(4, 'little')



def asm_read(A: int, B: int):
    cmd = 0
    cmd |= A & mask(7)
    cmd |= (B & mask(25)) << 7
    return cmd.to_bytes(4, 'little')


def asm_write(A: int, B: int):
    cmd = 0
    cmd |= A & mask(7)
    cmd |= (B & mask(25)) << 7
    return cmd.to_bytes(4, 'little')


def asm_abs(A: int, B: int):
    cmd = 0
    cmd |= A & mask(7)
    cmd |= (B & mask(8)) << 7
    return cmd.to_bytes(4, 'little')


def asm(program):
    mass = b""
    for cmd in program:
        mass += cmd
    return mass



#Этап 1. Перевод программы в промежуточное представление




print("Перво. запись константы")
print([f"0x{i:02x}" for i in asm_const(12,208)])



print("Второе. чтение значения из памяти")
print([f"0x{i:02x}" for i in asm_read(106,225)])



print("Третье. запись значения в память")
print([f"0x{i:02x}" for i in asm_write(95,421)])

print("Третье. запись значения в память")
print([f"0x{i:02x}" for i in asm_write(85,90)])





