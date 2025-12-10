from textual.app import App, ComposeResult
from textual.widgets import (
    Static,
    TextArea,
    Button,
    DataTable,
    Label,
)
from textual.containers import Horizontal, Vertical
from textual.message import Message
import subprocess
import tempfile
import os
import csv

from uvm23_inter import execute, memory, reg


class ErrorMessage(Message):
    def __init__(self, text: str):
        super().__init__()
        self.text = text


class UVMApp(App):
    CSS = """
    Screen {
        layout: horizontal;
    }

    #left {
        width: 60%;
        border: solid green;
    }

    #right {
        width: 40%;
        border: solid blue;
    }

    #dump {
        height: 100%;
    }

    .title {
        padding: 1;
        background: $accent;
        color: black;
        text-align: center;
    }

    #error-box {
        padding: 1;
        color: red;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="left"):
                yield Static("Ассемблерная программа", classes="title")
                self.editor = TextArea()
                yield self.editor
                yield Button("Собрать и выполнить", id="run")
                self.error_label = Label("", id="error-box")
                yield self.error_label

            with Vertical(id="right"):
                yield Static("Дамп памяти (0..200)", classes="title")
                self.dump = DataTable(id="dump")
                self.dump.add_columns("Адрес", "Значение")
                yield self.dump

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "run":
            await self.run_program()

    async def run_program(self):
        program_text = self.editor.text
        self.error_label.update("")

        # Очищаем дамп перед запуском
        self.dump.clear()
        self.dump.add_columns("Адрес", "Значение")

        # Временные файлы
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "program.txt")
            binf = os.path.join(tmp, "program.bin")
            dumpf = os.path.join(tmp, "dump.csv")

            # Пишем исходный код
            with open(src, "w", encoding="utf-8") as f:
                f.write(program_text)

            # Сборка (ассемблер)
            proc = subprocess.run(
                ["python", "uvm23_text.py", "-i", src, "-o", binf],
                capture_output=True,
                text=True
            )

            if proc.returncode != 0:
                self.error_label.update(proc.stderr or "Ошибка сборки")
                return

            # Читаем бинарный код и выполняем УВМ
            with open(binf, "rb") as f:
                bytecode = f.read()

            # Сбрасываем память перед каждым запуском
            for i in range(len(memory)):
                memory[i] = 0
            global reg
            reg = 0

            execute(bytecode)

            # Дамп 0..200
            with open(dumpf, "w") as f:
                f.write("Address,Value\n")
                for addr in range(0, 200):
                    f.write(f"{addr},{memory[addr]}\n")

            # Загружаем дамп в таблицу
            with open(dumpf) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.dump.add_row(row["Address"], row["Value"])


if __name__ == "__main__":
    UVMApp().run()
    
    
#python -m textual run gui_uvm.py

