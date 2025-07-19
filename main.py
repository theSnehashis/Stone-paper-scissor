import customtkinter as ctk
import random
from tkinter import messagebox

class StonePaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stone Paper Scissors")
        self.root.geometry("620x640")
        self.root.resizable(False, False)

        # Game State
        self.options = ["stone", "paper", "scissors"]
        self.emoji = {"stone": "🪨", "paper": "📄", "scissors": "✂"}
        self.reset_game_vars()

        self.create_widgets()
        self.disable_buttons()  # Disable at start

    def reset_game_vars(self):
        self.player_name = "Player 1"
        self.opponent_name = "Player 2"
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.max_rounds = 3
        self.round_history = []

    def create_widgets(self):
        # Name & Rounds Input
        top_frame = ctk.CTkFrame(self.root)
        top_frame.pack(pady=10, padx=10, fill="x")

        self.p1_entry = ctk.CTkEntry(top_frame, placeholder_text="Player 1", width=130)
        self.p1_entry.grid(row=0, column=0, padx=5)

        self.p2_entry = ctk.CTkEntry(top_frame, placeholder_text="Player 2", width=130)
        self.p2_entry.grid(row=0, column=1, padx=5)

        self.round_menu = ctk.CTkOptionMenu(top_frame, values=["3", "5", "10"])
        self.round_menu.set("3")
        self.round_menu.grid(row=0, column=2, padx=5)

        set_btn = ctk.CTkButton(top_frame, text="Set Names & Rounds", command=self.set_names_and_rounds)
        set_btn.grid(row=0, column=3, padx=5)

        # Labels
        self.status_label = ctk.CTkLabel(self.root, text="🪨📄✂ Let's Begin!", font=ctk.CTkFont(size=18, weight="bold"))
        self.status_label.pack(pady=5)

        self.user_label = ctk.CTkLabel(self.root, text=f"{self.player_name} Picked:", font=ctk.CTkFont(size=14))
        self.user_label.pack()

        self.comp_label = ctk.CTkLabel(self.root, text=f"{self.opponent_name} Picked:", font=ctk.CTkFont(size=14))
        self.comp_label.pack()

        self.result_label = ctk.CTkLabel(self.root, text=f"Result:", font=ctk.CTkFont(size=15, weight="bold"))
        self.result_label.pack(pady=5)

        self.score_label = ctk.CTkLabel(self.root, text="Score: 0 | 0", font=ctk.CTkFont(size=13))
        self.score_label.pack()

        self.round_label = ctk.CTkLabel(self.root, text="Round 0/3", font=ctk.CTkFont(size=13))
        self.round_label.pack(pady=2)

        # Buttons
        btn_frame = ctk.CTkFrame(self.root)
        btn_frame.pack(pady=10)

        self.stone_btn = ctk.CTkButton(btn_frame, text="🪨 Stone", width=120, command=lambda: self.play("stone"))
        self.paper_btn = ctk.CTkButton(btn_frame, text="📄 Paper", width=120, command=lambda: self.play("paper"))
        self.scissors_btn = ctk.CTkButton(btn_frame, text="✂ Scissors", width=120, command=lambda: self.play("scissors"))

        self.stone_btn.grid(row=0, column=0, padx=5, pady=5)
        self.paper_btn.grid(row=0, column=1, padx=5, pady=5)
        self.scissors_btn.grid(row=0, column=2, padx=5, pady=5)

        # Scoreboard
        self.log_box = ctk.CTkTextbox(self.root, height=180)
        self.log_box.pack(pady=10, padx=15, fill="both")
        self.log_box.insert("0.0", "Round History:\n")
        self.log_box.configure(state="disabled")

        # Reset Button
        reset_btn = ctk.CTkButton(self.root, text="🔄 Reset Game", command=self.reset_all)
        reset_btn.pack(pady=10)

    def set_names_and_rounds(self):
        p1 = self.p1_entry.get().strip()
        p2 = self.p2_entry.get().strip()
        self.player_name = p1 if p1 else "Player 1"
        self.opponent_name = p2 if p2 else "Player 2"
        self.max_rounds = int(self.round_menu.get())
        self.update_labels(force=True)
        self.enable_buttons()  # Enable buttons only after name input

    def play(self, user_choice):
        if self.rounds_played >= self.max_rounds:
            return

        self.disable_buttons()
        comp_choice = random.choice(self.options)

        if user_choice == comp_choice:
            result = "Draw"
        elif (user_choice == "stone" and comp_choice == "scissors") or \
             (user_choice == "paper" and comp_choice == "stone") or \
             (user_choice == "scissors" and comp_choice == "paper"):
            result = f"{self.player_name} Won"
            self.user_score += 1
        else:
            result = f"{self.opponent_name} Won"
            self.computer_score += 1

        self.rounds_played += 1
        self.user_label.configure(text=f"{self.player_name} Picked: {self.emoji[user_choice]} {user_choice.capitalize()}")
        self.comp_label.configure(text=f"{self.opponent_name} Picked: {self.emoji[comp_choice]} {comp_choice.capitalize()}")
        self.result_label.configure(text=f"Result: {result}")

        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"Round {self.rounds_played}: {self.emoji[user_choice]} vs {self.emoji[comp_choice]} → {result}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

        self.update_labels()

        if self.rounds_played == self.max_rounds:
            self.root.after(3000, self.show_final_result)
        else:
            self.root.after(3000, self.clear_feedback_and_enable)

    def clear_feedback_and_enable(self):
        self.user_label.configure(text=f"{self.player_name} Picked:")
        self.comp_label.configure(text=f"{self.opponent_name} Picked:")
        self.result_label.configure(text="Result:")
        self.enable_buttons()

    def update_labels(self, force=False):
        self.score_label.configure(text=f"Score: {self.user_score} | {self.computer_score}")
        self.round_label.configure(text=f"Round {self.rounds_played}/{self.max_rounds}")
        if force:
            self.user_label.configure(text=f"{self.player_name} Picked:")
            self.comp_label.configure(text=f"{self.opponent_name} Picked:")

    def show_final_result(self):
        if self.user_score > self.computer_score:
            msg = f"🎉 {self.player_name} Wins the Game!"
        elif self.computer_score > self.user_score:
            msg = f"🎉 {self.opponent_name} Wins the Game!"
        else:
            msg = "🤝 It's a Draw!"

        messagebox.showinfo("Game Over", f"Final Score:\n{self.player_name}: {self.user_score}\n{self.opponent_name}: {self.computer_score}\n\n{msg}")

    def reset_all(self):
        self.reset_game_vars()
        self.p1_entry.delete(0, "end")
        self.p2_entry.delete(0, "end")
        self.p1_entry.focus_set()
        self.round_menu.set("3")
        self.user_label.configure(text="Player 1 Picked:")
        self.comp_label.configure(text="Player 2 Picked:")
        self.result_label.configure(text="Result:")
        self.status_label.configure(text="🪨📄✂ Let's Begin!")
        self.score_label.configure(text="Score: 0 | 0")
        self.round_label.configure(text="Round 0/3")
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.insert("0.0", "Round History:\n")
        self.log_box.configure(state="disabled")
        self.disable_buttons()  # Keep buttons disabled until user sets names

    def disable_buttons(self):
        self.stone_btn.configure(state="disabled")
        self.paper_btn.configure(state="disabled")
        self.scissors_btn.configure(state="disabled")

    def enable_buttons(self):
        self.stone_btn.configure(state="normal")
        self.paper_btn.configure(state="normal")
        self.scissors_btn.configure(state="normal")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = StonePaperScissorsApp(root)
    root.mainloop()
