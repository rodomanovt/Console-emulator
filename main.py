import tkinter as tk
from typing import TextIO
import Sus
from tkinter import scrolledtext
import getpass
import platform
from VFSBuilder import *


class CommandLineEmulator:
    def __init__(self):
        self.username = getpass.getuser()
        self.hostname = platform.node()

        self.root = tk.Tk()
        self.root.title(f"Эмулятор - [{self.username}@{self.hostname}]")
        self.root.geometry("800x600")
        self.root.configure(bg='black')

        self.text_area = scrolledtext.ScrolledText(
            self.root,
            bg='black',
            fg='white',
            insertbackground='white',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # теги форматирования цвета текста
        self.text_area.tag_configure("prompt", foreground="lime")
        self.text_area.tag_configure("output", foreground="white")

        vfs_builder = VFSBuilder("vfs.json")
        self.VFSROOT = vfs_builder.getRoot()

        self.prompt = f"{self.username}@{self.hostname}: ~$ "  # строка вида username@hostname: ~$
        self.current_directory = self.VFSROOT
        self.directoryString = ""
        self.change_directory("")

        self.first_prompt = True

        # Для пропуска ошибочных строк скрипта без вывода сообщения об ошибке
        self.isScriptRunning = False

        # Выводим начальное приглашение
        self.show_prompt()

        # Привязываем обработчики событий
        self.text_area.bind('<KeyPress>', self.on_key_press)

        # Фокус на текстовое поле
        self.text_area.focus_set()


    def show_prompt(self):
        """Выводит приглашение ко вводу"""
        if self.first_prompt:
            # Первое приглашение выводим без перевода строки
            self.text_area.insert(tk.END, self.prompt, "prompt")
            self.first_prompt = False
        else:
            # Последующие приглашения выводим с новой строки
            self.text_area.insert(tk.END, "\n" + self.prompt, "prompt")

        # Прокручиваем вниз
        self.text_area.see(tk.END)


    def change_directory(self, path: str):
        if path:
            pathSequence = path.split("/")
            for folder in pathSequence:
                if folder in self.current_directory.childrenNames:
                    self.directoryString += f"/{folder}"
                    self.current_directory = self.current_directory.getChild(folder)
                    # TODO: неправильно обрабатывает случай вида folder2/fgdsgdfgssdfs
                else:
                    raise FileNotFoundError("Cannot find child directory")
            self.prompt = f"{self.username}@{self.hostname}: ~{self.directoryString}$ "
        else:
            self.current_directory = self.VFSROOT
            self.prompt = f"{self.username}@{self.hostname}: ~$ "
            self.directoryString = ""



    def print_output(self, text):
        """Функция вывода строки в консоль"""
        self.text_area.insert(tk.END, "\n" + text, "output")
        self.text_area.see(tk.END)


    def get_current_line(self):
        """Получает текущую команду из последней строки"""
        # Получаем весь текст
        full_text = self.text_area.get(1.0, tk.END).rstrip('\n')
        lines = full_text.split('\n')

        if lines:
            last_line = lines[-1]
            if last_line.startswith(self.prompt):
                return last_line[len(self.prompt):]
            else:
                # Если приглашение было удалено, возвращаем всю строку
                return last_line
        return ""


    def execute_command(self, line):
        """Выполняет команду и выводит результат"""
        if not line:
            return

        line = line.strip().split()
        command, args = line[0], line[1:]
        print(command, args)

        if command == "exit":
            self.root.quit()
        elif command == "clear":
            self.clear_screen()

        elif command == "neofetch": Sus.sus(self)
        elif command == "help":
            self.print_output("Доступные команды:")
            self.print_output("  help - показать эту справку")
            self.print_output("  clear - очистить экран")
            self.print_output("  exit - выйти из эмулятора")
            self.print_output("  echo - вывести текст")
            self.print_output("  ls - перечислить файлы")
            self.print_output("  cd - сменить директорию")

        elif command == "echo":
            self.print_output(" ".join(args))

        elif command == "ls":
            file_list = self.current_directory.children
            res = ""
            for el in file_list: res += el.name + " "
            self.print_output(res)

        elif command == "cd":
            if len(args) == 0:
                self.change_directory("")
                return
            try:
                self.change_directory(args[0])
            except FileNotFoundError:
                self.print_output(f"{args[0]}: файл или путь не найден")

        elif  ".sheesh" in command:
            try:
                with open(command, "r") as script:
                    self.run_script(script)
            except FileNotFoundError:
                self.print_output(f"{command}: команда не найдена")

        else:
            if not self.isScriptRunning:
                self.print_output(f"{command}: команда не найдена")


    def print_script_command(self, command):
        """
        Для запуска sheesh-скриптов
        Вывод промпта с командой для имитации диалога с пользователем
        """
        self.text_area.insert(tk.END, "\n" + self.prompt, "prompt")
        self.text_area.insert(tk.END, command, "output")


    def run_script(self, script: TextIO):
        lines = script.readlines()
        self.isScriptRunning = True
        for line in lines:
            line = line.strip()
            if line: # в скрипте можно оставлять пустые строки
                if line[0] != "#": # можно делать комментарии
                    self.print_script_command(line)
                    self.execute_command(line)
        self.isScriptRunning = False


    def clear_screen(self):
        self.text_area.delete(1.0, tk.END)
        self.first_prompt = True


    def on_key_press(self, event):
        """Обработчик нажатия клавиш"""
        if event.keysym == 'Return':
            line = self.get_current_line()
            self.execute_command(line)
            self.show_prompt()
            return "break"

        return None


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    emulator = CommandLineEmulator()
    emulator.run()