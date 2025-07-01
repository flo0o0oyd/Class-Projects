import tkinter as tk
from tkinter import messagebox
import random


class PetGameApp:
    def __init__(self):
        self.rootWin = tk.Tk()
        self.rootWin.title("Pet Game")
        self.rootWin.geometry("600x500")
        self.rootWin.config(bg='light yellow')

        self.pet_health = 50
        self.pet_happiness = 50
        self.remaining_actions = 3
        self.event_triggered = False

        # Pet images
        self.pet_images = {
            "default": tk.PhotoImage(file="pic/cat.png"),
            "style1": tk.PhotoImage(file="pic/cat2.png"),
            "style2": tk.PhotoImage(file="pic/cat3.png")
        }

        self.pet_state = {
            "happy": tk.PhotoImage(file="pic/happycat.png"),
            "happy2": tk.PhotoImage(file="pic/happycat2.png"),
            "happy3": tk.PhotoImage(file="pic/happycat3.png"),
            "sad": tk.PhotoImage(file="pic/sadcat.png"),
            "sad2": tk.PhotoImage(file="pic/sadcat2.png"),
            "sad3": tk.PhotoImage(file="pic/sadcat3.png"),
        }

        self.pet_image_key = "default"

        # Enemy images
        self.enemy_images_normal = {
            "enemy1": tk.PhotoImage(file="pic/enemy1.png"),
            "enemy2": tk.PhotoImage(file="pic/paul.png"),
        }

        self.enemy_images_boss = {
            "enemy3": tk.PhotoImage(file="pic/enemy3.png")
        }

        # Background colors
        self.bg_default = "light yellow"
        self.bg_event_positive = "light green"
        self.bg_event_negative = "light coral"

        self.create_start_page()

    def create_start_page(self):
        self.clear_window()
        self.rootWin.config(bg=self.bg_default)

        tk.Label(self.rootWin, text="Pet Game", fg='black', bg='light blue',
                 font='Phosphate 95', pady=10, justify=tk.CENTER).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Button(self.rootWin, text="Start Game", font='Times 30', command=self.create_game_page).grid(
            row=1, column=0, columnspan=2, pady=20)

        tk.Button(self.rootWin, text="Quit", font="Times 30", command=self.quit_game).grid(
            row=2, column=0, columnspan=2, pady=20)

    def create_game_page(self):
        self.clear_window()
        self.rootWin.config(bg=self.bg_default)
        self.event_triggered = False

        self.health_label = tk.Label(self.rootWin, text=f"Health: {self.pet_health}", font="Courier 30", bg=self.bg_default)
        self.health_label.grid(row=0, column=0, pady=10)

        self.happiness_label = tk.Label(self.rootWin, text=f"Happiness: {self.pet_happiness}", font="Courier 30", bg=self.bg_default)
        self.happiness_label.grid(row=0, column=1, pady=10)

        self.actions_label = tk.Label(self.rootWin, text=f"Remaining Actions: {self.remaining_actions}", font="Courier 15", bg=self.bg_default)
        self.actions_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.pet_label = tk.Label(self.rootWin, image=self.pet_images[self.pet_image_key], bg=self.bg_default)
        self.pet_label.grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(self.rootWin, text="Feed", font="Courier 20", command=self.feed_pet).grid(row=3, column=0, pady=10)
        tk.Button(self.rootWin, text="Play", font="Courier 20", command=self.play_with_pet).grid(row=3, column=1, pady=10)

        tk.Button(self.rootWin, text="Dressing Room", font="Courier 20", command=self.create_dressing_room_page).grid(row=4, column=0, pady=10)
        tk.Button(self.rootWin, text="Battle Room", font="Courier 20", command=self.battle_haha).grid(row=4, column=1, pady=10)

        tk.Button(self.rootWin, text="Next Day", font="Courier 20", command=self.next_day).grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(self.rootWin, text="Back to Main Menu", font="Courier 15", command=self.create_start_page).grid(row=6, column=0, columnspan=2, pady=20)

        self.update_status()

    def create_dressing_room_page(self):
        self.clear_window()
        tk.Label(self.rootWin, text="Choose a Style for Your Pet", font="Courier 30", bg="light pink").pack(pady=10)

        for style, image in self.pet_images.items():
            tk.Button(self.rootWin, image=image, command=lambda s=style: self.set_pet_style(s)).pack(pady=5)

        tk.Button(self.rootWin, text="Back", font="Courier 20", command=self.create_game_page).pack(pady=20)

    def set_pet_style(self, style):
        self.pet_image_key = style
        self.create_game_page()

    def battle_haha(self):
        if self.remaining_actions > 0:
            self.remaining_actions -= 1
            self.update_action_label()
            self.create_battle_room_page()
        else:
            messagebox.showinfo("", "No actions left for today! Please go to the next day.")

    def create_battle_room_page(self):
        self.clear_window()
        choose_normal = random.random() > 0.2

        if choose_normal:
            enemy_image = self.enemy_images_normal[random.choice(list(self.enemy_images_normal.keys()))]
            bg_color = self.bg_default
            title = "Enemy Appeared!"
            attack_command = self.attack_enemy_normal
            font_size = 20
        else:
            enemy_image = self.enemy_images_boss[random.choice(list(self.enemy_images_boss.keys()))]
            bg_color = "light pink"
            title = "Oh! The Boss comes!"
            attack_command = self.attack_enemy_boss
            font_size = 35

        self.rootWin.config(bg=bg_color)
        tk.Label(self.rootWin, text="Battle Room", font="Courier 30 bold", bg=bg_color).pack(pady=10)
        tk.Label(self.rootWin, text=title, font="Courier 20", bg=bg_color).pack(pady=5)
        tk.Label(self.rootWin, image=enemy_image, bg=bg_color).pack(pady=10)

        self.battle_result_label = tk.Label(self.rootWin, text="", font="Courier 15", bg=bg_color)
        self.battle_result_label.pack(pady=5)

        self.battle_button = tk.Button(self.rootWin, text="Attack!", font=f"Courier {font_size}", command=attack_command)
        self.battle_button.pack(pady=10)

        tk.Button(self.rootWin, text="Back", font="Courier 20", command=self.create_game_page).pack(pady=20)

    def attack_enemy_normal(self):
        if random.random() > 0.3:
            self.pet_happiness = min(self.pet_happiness + 20, 100)
            self.pet_health = min(self.pet_health + 10, 100)
            self.battle_result_label.config(text="You Win! Happiness +20, Health +10", fg="dark green")
        else:
            self.pet_health = max(self.pet_health - 10, 0)
            self.battle_result_label.config(text="You Lose! Health -10", fg="red")
        self.battle_button.config(state=tk.DISABLED)

    def attack_enemy_boss(self):
        if random.random() > 0.7:
            self.pet_happiness = min(self.pet_happiness + 50, 100)
            self.pet_health = min(self.pet_health + 20, 100)
            self.battle_result_label.config(text="You Beat the Boss! Happiness +50, Health +20", fg="green")
        else:
            self.pet_health = max(self.pet_health - 15, 0)
            self.battle_result_label.config(text="You Lose! OMG! Health -15", fg="red")
        self.battle_button.config(state=tk.DISABLED)
        self.update_status()

    def feed_pet(self):
        if self.remaining_actions > 0:
            self.pet_health = min(self.pet_health + 10, 100)
            self.remaining_actions -= 1
            self.update_status()
            self.toggle_image()
            self.update_action_label()
        else:
            messagebox.showinfo("", "No actions left for today! Please go to the next day.")

    def play_with_pet(self):
        if self.remaining_actions > 0:
            self.pet_happiness = min(self.pet_happiness + 10, 100)
            self.remaining_actions -= 1
            self.update_status()
            self.toggle_image()
            self.update_action_label()
        else:
            messagebox.showinfo("", "No actions left for today! Please go to the next day.")

    def update_action_label(self):
        if hasattr(self, "actions_label"):
            self.actions_label.config(text=f"Remaining Actions: {self.remaining_actions}")

    def next_day(self):
        self.remaining_actions = 3
        self.pet_health = max(self.pet_health - 10, 0)
        self.pet_happiness = max(self.pet_happiness - 10, 0)
        self.event_triggered = False
        self.update_status()
        self.update_action_label()

        if self.pet_health <= 0:
            messagebox.showwarning("", "Your pet is starving!")
            self.create_start_page()
        elif self.pet_happiness <= 0:
            messagebox.showwarning("", "Your pet died of boredom!")
            self.create_start_page()

    def update_status(self):
        if hasattr(self, "health_label") and hasattr(self, "happiness_label"):
            self.health_label.config(text=f"Health: {self.pet_health}")
            self.happiness_label.config(text=f"Happiness: {self.pet_happiness}")

    def toggle_image(self):
        key_map = {
            "default": "happy",
            "style1": "happy2",
            "style2": "happy3"
        }
        if self.pet_image_key in key_map:
            self.pet_label.config(image=self.pet_state[key_map[self.pet_image_key]])
            self.pet_label.after(1000, lambda: self.pet_label.config(image=self.pet_images[self.pet_image_key]))

    def quit_game(self):
        self.rootWin.destroy()

    def clear_window(self):
        for widget in self.rootWin.winfo_children():
            widget.destroy()

    def run(self):
        self.rootWin.mainloop()


if __name__ == "__main__":
    myApp = PetGameApp()
    myApp.run()
