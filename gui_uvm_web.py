# uvm_web.py
import streamlit as st
import tempfile
import subprocess
import uvm23_inter as uvm
import pandas as pd
import os

st.title("UVM23 Web IDE")

# Текстовая область для ввода ассемблерной программы
program_text = st.text_area("Ассемблерная программа", height=300, 
                            value="""const(12, 10)
write(95, 0)
const(12, 20)
write(95, 1)
const(12, 30)
write(95, 2)
const(12, 0)
write(95, 3)""")

if st.button("Собрать и выполнить"):
    # Временные файлы для исходного кода и бинарного файла
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "program.txt")
        binf = os.path.join(tmp, "program.bin")

        # Сохраняем программу во временный файл
        with open(src, "w", encoding="utf-8") as f:
            f.write(program_text)

        # Запускаем ассемблер
        proc = subprocess.run(
            ["python", "uvm23_text.py", "-i", src, "-o", binf],
            capture_output=True,
            text=True
        )

        # Если есть ошибки сборки — показываем их
        if proc.returncode != 0:
            st.error(proc.stderr or "Ошибка сборки")
        else:
            # Читаем бинарный файл
            with open(binf, "rb") as f:
                bytecode = f.read()

            # Сброс памяти и регистра
            for i in range(len(uvm.memory)):
                uvm.memory[i] = 0
            uvm.reg = 0

            # Выполняем программу
            uvm.execute(bytecode)

            # Выводим значение регистра
            st.write(f"REG = {uvm.reg}")

            # Выводим дамп памяти (0..200) через pandas DataFrame
            df = pd.DataFrame([[i, uvm.memory[i]] for i in range(200)], columns=["Address", "Value"])
            st.dataframe(df)
