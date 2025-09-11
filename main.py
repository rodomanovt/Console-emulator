import tkinter as tk
import Sus
from tkinter import scrolledtext
import getpass
import platform


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

        # теги форматирования
        self.text_area.tag_configure("prompt", foreground="green")
        self.text_area.tag_configure("output", foreground="white")
        self.text_area.tag_configure("error", foreground="red")

        self.first_prompt = True

        # Выводим начальное приглашение
        self.show_prompt()

        # Привязываем обработчики событий
        self.text_area.bind('<KeyPress>', self.on_key_press)

        # Фокус на текстовое поле
        self.text_area.focus_set()


    def show_prompt(self):
        """Выводит приглашение ко вводу"""
        prompt = f"{self.username}@{self.hostname}: ~$ "

        if self.first_prompt:
            # Первое приглашение выводим без перевода строки
            self.text_area.insert(tk.END, prompt, "prompt")
            self.first_prompt = False
        else:
            # Последующие приглашения выводим с новой строки
            self.text_area.insert(tk.END, "\n" + prompt, "prompt")

        # Прокручиваем вниз
        self.text_area.see(tk.END)



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
            prompt = f"{self.username}@{self.hostname}: ~$ "
            if last_line.startswith(prompt):
                return last_line[len(prompt):]
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
            self.print_output("  ls - заглушка")
            self.print_output("  cd - заглушка")
        elif command == "ls":
            self.print_output(f"ls args: {args}")
        elif command == "cd":
            self.print_output(f"cd args: {args}")

        else:
            self.print_output(f"Команда не найдена: {command}")
            self.print_output("Введите 'help' для списка доступных команд")


    def clear_screen(self):
        self.text_area.delete(1.0, tk.END)
        self.prompt_positions = []
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