import tkinter as tk
import random

WORD_BANKS = {
    "Normal": ["apple", "banana", "kiwi", "melon", "window", "keyboard"],
    "Hard": ["binary search", "linked list", "cloud storage"],
    "Nightmare": [
        "Practice makes perfect.",
        "Accuracy is more important than speed."
    ]
}

class SpeedTypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Typing Challenge")
        self.root.geometry("600x450")
        self.root.config(bg="#1E2A38")

        self.remaining = 0
        self.round = 0
        self.now_round = 0
        self.answer = ""
        self.score = 0
        self.playing = False

        tk.Label(root, text="Speed Typing Challenge",
                 font=("Arial", 22, "bold"), fg="white", bg="#1E2A38").pack(pady=10)

        frame_top = tk.Frame(root, bg="#1E2A38")
        frame_top.pack(pady=5)

        tk.Label(frame_top, text="Rounds:", fg="white", bg="#1E2A38",
                 font=("Arial", 14)).grid(row=0, column=0, padx=5)

        self.round_entry = tk.Entry(frame_top, width=5, font=("Arial", 14))
        self.round_entry.insert(0, "5")
        self.round_entry.grid(row=0, column=1, padx=5)

        difficulty_frame = tk.Frame(root, bg="#1E2A38")
        difficulty_frame.pack()

        self.difficulty = tk.StringVar(value="Normal")

        self.btn_normal = tk.Button(difficulty_frame, text="Normal", width=10,
                                    command=lambda: self.set_difficulty("Normal"))
        self.btn_normal.grid(row=0, column=0, padx=5, pady=5)

        self.btn_hard = tk.Button(difficulty_frame, text="Hard", width=10,
                                  command=lambda: self.set_difficulty("Hard"))
        self.btn_hard.grid(row=0, column=1, padx=5)

        self.btn_nm = tk.Button(difficulty_frame, text="Nightmare", width=10,
                                command=lambda: self.set_difficulty("Nightmare"))
        self.btn_nm.grid(row=0, column=2, padx=5)

        self.highlight_difficulty()

        self.start_btn = tk.Button(root, text="Start Game",
                                   font=("Arial", 14), width=12,
                                   command=self.start_game)
        self.start_btn.pack(pady=10)

        self.word_label = tk.Label(root, text="", font=("Arial", 28),
                                   fg="#6DFF6B", bg="#1E2A38")
        self.word_label.pack(pady=20)

        self.timer_label = tk.Label(root, text="",
                                    font=("Arial", 14), fg="white", bg="#1E2A38")
        self.timer_label.pack()

        self.input_entry = tk.Entry(root, font=("Arial", 18), width=25, justify="center")
        self.input_entry.pack()
        self.input_entry.bind("<Return>", self.check_answer)

    def set_difficulty(self, lv):
        if self.playing:
            return
        self.difficulty.set(lv)
        self.highlight_difficulty()

    def highlight_difficulty(self):
        buttons = [self.btn_normal, self.btn_hard, self.btn_nm]
        for b in buttons:
            b.config(bg="lightgray")

        if self.difficulty.get() == "Normal":
            self.btn_normal.config(bg="#FFE28A")
        elif self.difficulty.get() == "Hard":
            self.btn_hard.config(bg="#FFB86C")
        else:
            self.btn_nm.config(bg="#FF6E6E")

    def start_game(self):
        try:
            self.round = int(self.round_entry.get())
        except ValueError:
            self.timer_label.config(text="⚠ 請輸入正確的回合數")
            return

        self.playing = True
        self.score = 0
        self.now_round = 0
        self.start_btn.config(state="disabled")

        for b in [self.btn_normal, self.btn_hard, self.btn_nm]:
            b.config(state="disabled")

        self.next_question()

    def next_question(self):
        if self.now_round >= self.round:
            self.end_game()
            return

        self.now_round += 1
        bank = WORD_BANKS[self.difficulty.get()]
        self.answer = random.choice(bank)

        self.word_label.config(text=self.answer)
        self.input_entry.delete(0, tk.END)

        if self.difficulty.get() in ["Normal", "Hard"]:
            self.remaining = 10.0
        else:
            self.remaining = 15.0

        self.update_timer()

    def update_timer(self):
        if self.remaining <= 0:
            self.timer_label.config(text="Time: 0.0s")
            self.root.after(800, self.next_question)
            return

        self.timer_label.config(text=f"Time: {self.remaining:.1f}s")
        self.remaining -= 0.1
        self.root.after(100, self.update_timer)

    def check_answer(self, event):
        if not self.playing:
            return

        if self.input_entry.get() == self.answer:
            self.score += 1

        self.next_question()

    def end_game(self):
        self.playing = False
        self.word_label.config(text="")
        self.input_entry.delete(0, tk.END)

        self.timer_label.config(text=f"🎉 完成！成績：{self.score}/{self.round}")

        self.start_btn.config(state="normal")

        for b in [self.btn_normal, self.btn_hard, self.btn_nm]:
            b.config(state="normal")


def main():
    root = tk.Tk()
    SpeedTypingGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()