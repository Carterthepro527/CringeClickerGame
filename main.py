import tkinter as tk
import tkinter.messagebox
import subprocess
import os
from tkinter import ttk

game_window_open = False
SAVE_FILE = "clicker_game_save.txt"

class ClickerGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Clicker Game")
        self.master.geometry("300x200")  # Set initial window size

        self.load_game_data()

        self.label = tk.Label(master, text=f"Clicks: {self.click_count}")
        self.label.pack(pady=10)

        self.click_button = ttk.Button(master, text="Click me!", command=self.click)
        self.click_button.pack()

        # Create the shop button
        self.shop_button = ttk.Button(master, text="Shop", command=self.open_shop)
        self.shop_button.place(relx=1, anchor='ne', x=-10, y=10)  # Place button at top-right corner with a margin of 10 pixels

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_game_data(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as file:
                data = file.readlines()
                self.click_count = int(data[0].strip())
                self.upgrade_cost = int(data[1].strip())
                self.click_multiplier = int(data[2].strip())
                self.upgrade_count = int(data[3].strip())
        else:
            self.click_count = 0
            self.upgrade_cost = 10
            self.click_multiplier = 1
            self.upgrade_count = 0

    def save_game_data(self):
        with open(SAVE_FILE, "w") as file:
            file.write(f"{self.click_count}\n")
            file.write(f"{self.upgrade_cost}\n")
            file.write(f"{self.click_multiplier}\n")
            file.write(f"{self.upgrade_count}\n")

    def click(self):
        self.click_count += self.click_multiplier
        self.label.config(text=f"Clicks: {self.click_count}")

    def open_shop(self):
        global game_window_open
        if not game_window_open:
            game_window_open = True
            shop_window = tk.Toplevel()
            shop_window.title("Shop")
            shop_window.geometry("200x200")

            shop_label = tk.Label(shop_window, text="Welcome to the shop!")
            shop_label.pack(pady=10)

            # Display current upgrade count
            upgrade_count_label = tk.Label(shop_window, text=f"Current Upgrades: {self.upgrade_count}")
            upgrade_count_label.pack()

            # Create the "Buy Upgrade" button in the shop window
            upgrade_button_text = f"Buy Upgrade ({self.upgrade_cost} clicks)\n({self.upgrade_count} bought)"
            upgrade_button = ttk.Button(shop_window, text=upgrade_button_text, command=self.buy_upgrade)
            upgrade_button.pack()

            shop_window.protocol("WM_DELETE_WINDOW", self.close_shop)
        else:
            tk.messagebox.showinfo("Game Already Open", "The game window is already open.")

    def close_shop(self):
        global game_window_open
        game_window_open = False
        self.master.focus()

    def buy_upgrade(self):
        if self.click_count >= self.upgrade_cost:
            self.click_count -= self.upgrade_cost
            self.click_multiplier += 1
            self.upgrade_cost *= 2
            self.upgrade_count += 1
            self.label.config(text=f"Clicks: {self.click_count}")
            self.master.bell()  # Error noise
            self.save_game_data()  # Save the game data after buying the upgrade
            print("Upgrade bought successfully!!")
        else:
            self.master.bell()  # Error noise
            tk.messagebox.showinfo("Insufficient Clicks", f"You need {self.upgrade_cost - self.click_count} more clicks for this upgrade.")

    def on_closing(self):
        self.save_game_data()
        self.master.destroy()

def main():
    root = tk.Tk()
    game = ClickerGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
