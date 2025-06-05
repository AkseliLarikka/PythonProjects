import tkinter as tk
from tkinter import messagebox
from tkinter import TclError
import random
import time
import json
import os

# Miinaharavan kilpailustandardien mukaiset asetukset
DIFFICULTY_SETTINGS = {
    "Aloittelija": {"size": (9, 9), "mines": 10},
    "Keskitaso": {"size": (16, 16), "mines": 40},
    "Asiantuntija": {"size": (30, 16), "mines": 99},
    "Mukautettu": {"size": None, "mines": None},  # Placeholder mukautetulle
}
SCOREBOARD_FILE = "./Minesweeper/scoreboard.json"
HIGHLIGHT_COLOR = "#b0e0e6" # Vaalea sinivihreä korostusväri

class Minesweeper:
    def __init__(self, master_frame, game_manager, difficulty, custom_settings=None):
        self.master_frame = master_frame
        self.game_manager = game_manager
        self.difficulty = difficulty
        
        if difficulty == "Mukautettu" and custom_settings:
            self.width, self.height = custom_settings["size"]
            self.num_mines = custom_settings["mines"]
            self.custom_settings = custom_settings
        else:
            settings = DIFFICULTY_SETTINGS[difficulty]
            self.width, self.height = settings["size"]
            self.num_mines = settings["mines"]
            self.custom_settings = None

        self.first_click = True
        self.game_over = False
        self.flags_placed = 0
        self.start_time = None
        self.timer_running = False

        self.board_buttons = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.mine_map = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.revealed = [[False for _ in range(self.width)] for _ in range(self.height)]
        
        self.highlighted_buttons = [] # Lista korostetuista napeista
        self.default_btn_bg = self.master_frame.cget('bg') # Oletusnappien väri

        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self.master_frame)
        top_frame.pack()

        self.mine_label = tk.Label(top_frame, text=f"Miinat: {self.num_mines - self.flags_placed}", font=("Arial", 12))
        self.mine_label.pack(side=tk.LEFT, padx=10, pady=5)

        restart_button = tk.Button(top_frame, text="Päävalikkoon", command=self.game_manager.show_menu)
        restart_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.time_label = tk.Label(top_frame, text="Aika: 0", font=("Arial", 12))
        self.time_label.pack(side=tk.LEFT, padx=10, pady=5)

        board_frame = tk.Frame(self.master_frame)
        board_frame.pack()

        for r in range(self.height):
            for c in range(self.width):
                button = tk.Button(board_frame, width=2, height=1, relief=tk.RAISED, font=("Arial", 9))
                button.grid(row=r, column=c, padx=1, pady=1)
                button.bind('<Button-1>', lambda e, r=r, c=c: self.on_left_click(r, c))
                button.bind('<Button-3>', lambda e, r=r, c=c: self.on_right_click(r, c))
                self.board_buttons[r][c] = button
    
    # --- Pelin logiikka ---
    
    def place_mines(self, first_r, first_c):
        # Miinojen asettelu turvallisen ensiklikkauksen jälkeen
        placed_mines = 0
        while placed_mines < self.num_mines:
            r = random.randint(0, self.height - 1)
            c = random.randint(0, self.width - 1)
            if not self.mine_map[r][c] and (abs(r - first_r) > 1 or abs(c - first_c) > 1):
                self.mine_map[r][c] = True
                placed_mines += 1

    def reveal_cell(self, r, c, by_chord=False):
    # Muutettu ehto estämään liputettujen ruutujen avaamisen
        if self.revealed[r][c] or self.board_buttons[r][c]['text'] == '🚩':
            return
        if by_chord:
            print("Pika-avattu ruutu")

        self.revealed[r][c] = True
        button = self.board_buttons[r][c]
        
        if self.mine_map[r][c]:
            self.lose_game(button)
            return

        adjacent_mines = self.count_adjacent_mines(r, c)
        
        button.config(relief=tk.SUNKEN, bg='light gray', state='disabled')
        button.unbind('<Button-1>')
        button.unbind('<Button-3>')
        
        if adjacent_mines > 0:
            # Numeroiden väritys standardien mukaisesti
            colors = {1: 'blue', 2: 'green', 3: 'red', 4: '#000080', 5: '#800000', 6: '#008080', 7: 'black', 8: 'gray'}
            button.config(text=str(adjacent_mines), fg=colors.get(adjacent_mines, 'black'))
            # Sidotaan uudet toiminnot numeronappeihin (korostus & pika-avaus)
            button.bind('<ButtonPress-1>', lambda e, r=r, c=c: self.on_number_press(r, c))
            button.bind('<ButtonRelease-1>', lambda e, r=r, c=c: self.on_number_release_and_chord(r, c))
        else:
            # Tyhjien ruutujen rekursiivinen avaus
            for neighbor_r, neighbor_c in self.get_neighbors(r, c):
                self.reveal_cell(neighbor_r, neighbor_c, by_chord=True)
        
        self.check_win_condition()

    # --- Hiiren tapahtumien käsittelijät ---

    def on_left_click(self, r, c):
        if self.game_over or self.board_buttons[r][c]['text'] == '🚩': return

        if self.first_click:
            self.start_timer()
            self.place_mines(r, c)
            self.first_click = False

        self.reveal_cell(r, c)

    def on_right_click(self, r, c):
        if self.game_over or self.revealed[r][c]: return
            
        button = self.board_buttons[r][c]
        if button['text'] == '🚩':
            button.config(text='')
            self.flags_placed -= 1
        else:
            button.config(text='🚩', fg='red')
            self.flags_placed += 1
        
        self.mine_label.config(text=f"Miinat: {self.num_mines - self.flags_placed}")

    def on_number_press(self, r, c):
        """Korostaa naapurit, kun numeronappia painetaan."""
        if self.game_over: return
        self.clear_highlights()
        
        for neighbor_r, neighbor_c in self.get_neighbors(r, c):
            button = self.board_buttons[neighbor_r][neighbor_c]
            if not self.revealed[neighbor_r][neighbor_c]:
                button.config(bg=HIGHLIGHT_COLOR)
                self.highlighted_buttons.append(button)

    def on_number_release_and_chord(self, r, c):
        """Poistaa korostuksen ja yrittää pika-avausta, kun nappi vapautetaan."""
        if self.game_over: return
        self.clear_highlights()

        adjacent_flags = 0
        for neighbor_r, neighbor_c in self.get_neighbors(r, c):
            if self.board_buttons[neighbor_r][neighbor_c]['text'] == '🚩':
                adjacent_flags += 1
        
        try:
            number_on_cell = int(self.board_buttons[r][c]['text'])
            if adjacent_flags == number_on_cell:
                for neighbor_r, neighbor_c in self.get_neighbors(r, c):
                    self.reveal_cell(neighbor_r, neighbor_c, by_chord=True)
        except (ValueError, TclError):
            pass # Ei tehdä mitään, jos napissa ei ole numeroa

    # --- Apu- ja tilafunktiot ---

    def get_neighbors(self, r, c):
        """Palauttaa listan naapurikoordinaateista."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    neighbors.append((nr, nc))
        return neighbors
        
    def count_adjacent_mines(self, r, c):
        return sum(1 for nr, nc in self.get_neighbors(r, c) if self.mine_map[nr][nc])

    def clear_highlights(self):
        for button in self.highlighted_buttons:
            try:
                button.config(bg=self.default_btn_bg)
            except tk.TclError:
                pass # Nappi on jo tuhottu
        self.highlighted_buttons = []

    def start_timer(self):
        if not self.timer_running:
            self.start_time = time.perf_counter()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.perf_counter() - self.start_time
            self.time_label.config(text=f"Aika: {elapsed_time:.2f} s")
            self.master_frame.after(100, self.update_timer)

    def lose_game(self, clicked_button):
        self.game_over = True
        self.timer_running = False
        self.clear_highlights()
        clicked_button.config(text='💣', bg='red', state='disabled')
        for r in range(self.height):
            for c in range(self.width):
                button = self.board_buttons[r][c]
                button.unbind('<Button-1>')
                button.unbind('<ButtonPress-1>')
                button.unbind('<ButtonRelease-1>')
                button.unbind('<Button-3>')
                if self.mine_map[r][c] and button['text'] != '🚩':
                    button.config(text='💣', bg='gray', state='disabled')
        messagebox.showinfo("Miinaharava", "Osuit miinaan! Peli päättyi.")
    
    def check_win_condition(self):
        if self.game_over: return
        
        revealed_count = sum(row.count(True) for row in self.revealed)
        if revealed_count == self.width * self.height - self.num_mines:
            self.game_over = True
            self.timer_running = False
            final_time = round(time.perf_counter() - self.start_time, 2)
            
            # Tallenna tulos
            if self.difficulty == "Mukautettu":
                self.game_manager.save_custom_score(self.custom_settings, final_time)
            else:
                self.game_manager.save_score(self.difficulty, final_time)
            
            # Näytä mukautettu voittoviesti
            self.show_win_dialog(final_time)

    def show_win_dialog(self, final_time):
        """Näyttää mukautetun voittoviestin valintoineen."""
        win_dialog = tk.Toplevel(self.master_frame)
        win_dialog.title("Onnittelut!")
        win_dialog.geometry("450x250")
        win_dialog.resizable(False, False)
        
        # Keskitä ikkuna näytön keskelle
        win_dialog.update_idletasks()
        screen_width = win_dialog.winfo_screenwidth()
        screen_height = win_dialog.winfo_screenheight()
        x = (screen_width // 2) - (450 // 2)
        y = (screen_height // 2) - (250 // 2)
        win_dialog.geometry(f'450x250+{x}+{y}')
        
        win_dialog.transient(self.master_frame)
        win_dialog.grab_set()
        
        # Sisältö
        congratulations = tk.Label(win_dialog, text="🎉 Onneksi olkoon, voitit pelin! 🎉", 
                                 font=("Arial", 14, "bold"), fg="green")
        congratulations.pack(pady=20)
        
        time_label = tk.Label(win_dialog, text=f"Aikasi: {final_time} sekuntia", 
                            font=("Arial", 12))
        time_label.pack(pady=10)
        
        # Painikkeet - kaksi riviä
        button_frame1 = tk.Frame(win_dialog)
        button_frame1.pack(pady=10)
        
        button_frame2 = tk.Frame(win_dialog)
        button_frame2.pack(pady=5)
        
        # Ensimmäinen rivi
        view_game_btn = tk.Button(button_frame1, text="Tarkastele peliä", 
                                command=lambda: self.view_game_and_close(win_dialog))
        view_game_btn.pack(side=tk.LEFT, padx=10)
        
        view_scores_btn = tk.Button(button_frame1, text="Tarkastele tuloksia", 
                                  command=lambda: self.view_scores_and_close(win_dialog))
        view_scores_btn.pack(side=tk.LEFT, padx=10)
        
        # Toinen rivi
        new_game_btn = tk.Button(button_frame2, text="Uusi peli", 
                               command=lambda: self.new_game_and_close(win_dialog))
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        menu_btn = tk.Button(button_frame2, text="Päävalikko", 
                           command=lambda: self.menu_and_close(win_dialog))
        menu_btn.pack(side=tk.LEFT, padx=10)
        
        # Aseta ensisijainen fokus
        view_game_btn.focus()

    def view_game_and_close(self, dialog):
        """Sulkee voittoviestin ja jättää pelikentän näkyviin voittotilanteessa."""
        dialog.destroy()
        # Ei tehdä mitään muuta - pelikenttä jää näkyviin voittotilanteessa

    def view_scores_and_close(self, dialog):
        """Sulkee voittoviestin ja näyttää tulostaulukon."""
        dialog.destroy()
        self.game_manager.show_scoreboard()

    def new_game_and_close(self, dialog):
        """Sulkee voittoviestin ja aloittaa uuden pelin samalla vaikeustasolla."""
        dialog.destroy()
        if self.difficulty == "Mukautettu":
            self.game_manager.start_game(self.difficulty, self.custom_settings)
        else:
            self.game_manager.start_game(self.difficulty)

    def menu_and_close(self, dialog):
        """Sulkee voittoviestin ja palaa päävalikkoon."""
        dialog.destroy()
        self.game_manager.show_menu()

class GameManager:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.scores = self.load_scores()
        self.custom_scores = self.load_custom_scores()
        self.show_menu()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

    def show_menu(self):
        self.root.title("Miinaharava - Valikko")
        self.clear_frame()
        
        tk.Label(self.current_frame, text="Valitse vaikeustaso", font=("Arial", 16, "bold")).pack(pady=20)
        
        for difficulty in DIFFICULTY_SETTINGS.keys():
            if difficulty == "Mukautettu":
                button = tk.Button(self.current_frame, text=difficulty, font=("Arial", 12), 
                                 command=self.show_custom_dialog)
            else:
                button = tk.Button(self.current_frame, text=difficulty, font=("Arial", 12), 
                                 command=lambda d=difficulty: self.start_game(d))
            button.pack(fill='x', padx=50, pady=6)
        
        scoreboard_button = tk.Button(self.current_frame, text="Tulostaulukko", font=("Arial", 12), command=self.show_scoreboard)
        scoreboard_button.pack(fill='x', padx=50, pady=(15, 6))

        self.center_window(320, 350)

    def show_custom_dialog(self):
        """Näyttää mukautetun pelin asetukset -dialogin."""
        custom_dialog = tk.Toplevel(self.root)
        custom_dialog.title("Mukautettu peli")
        custom_dialog.geometry("300x250")
        custom_dialog.resizable(False, False)
        
        # Keskitä ikkuna
        custom_dialog.update_idletasks()
        screen_width = custom_dialog.winfo_screenwidth()
        screen_height = custom_dialog.winfo_screenheight()
        x = (screen_width // 2) - (300 // 2)
        y = (screen_height // 2) - (250 // 2)
        custom_dialog.geometry(f'300x250+{x}+{y}')
        
        custom_dialog.transient(self.root)
        custom_dialog.grab_set()
        
        tk.Label(custom_dialog, text="Mukautettu peli", font=("Arial", 14, "bold")).pack(pady=15)
        
        # Leveys
        width_frame = tk.Frame(custom_dialog)
        width_frame.pack(pady=5)
        tk.Label(width_frame, text="Leveys (5-50):").pack(side=tk.LEFT)
        width_var = tk.StringVar(value="16")
        width_entry = tk.Entry(width_frame, textvariable=width_var, width=10)
        width_entry.pack(side=tk.RIGHT, padx=10)
        
        # Korkeus
        height_frame = tk.Frame(custom_dialog)
        height_frame.pack(pady=5)
        tk.Label(height_frame, text="Korkeus (5-30):").pack(side=tk.LEFT)
        height_var = tk.StringVar(value="16")
        height_entry = tk.Entry(height_frame, textvariable=height_var, width=10)
        height_entry.pack(side=tk.RIGHT, padx=10)
        
        # Miinat
        mines_frame = tk.Frame(custom_dialog)
        mines_frame.pack(pady=5)
        tk.Label(mines_frame, text="Miinat (1-999):").pack(side=tk.LEFT)
        mines_var = tk.StringVar(value="40")
        mines_entry = tk.Entry(mines_frame, textvariable=mines_var, width=10)
        mines_entry.pack(side=tk.RIGHT, padx=10)
        
        # Napit
        button_frame = tk.Frame(custom_dialog)
        button_frame.pack(pady=20)
        
        def start_custom_game():
            try:
                width = int(width_var.get())
                height = int(height_var.get())
                mines = int(mines_var.get())
                
                # Validointi
                if not (5 <= width <= 50):
                    messagebox.showerror("Virhe", "Leveyden tulee olla 5-50 välillä!")
                    return
                if not (5 <= height <= 30):
                    messagebox.showerror("Virhe", "Korkeuden tulee olla 5-30 välillä!")
                    return
                if not (1 <= mines <= min(999, width * height - 1)):
                    messagebox.showerror("Virhe", f"Miinojen määrä tulee olla 1-{min(999, width * height - 1)} välillä!")
                    return
                
                custom_settings = {"size": (width, height), "mines": mines}
                custom_dialog.destroy()
                self.start_game("Mukautettu", custom_settings)
                
            except ValueError:
                messagebox.showerror("Virhe", "Syötä kelvollisia numeroita!")
        
        start_btn = tk.Button(button_frame, text="Aloita peli", command=start_custom_game)
        start_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(button_frame, text="Peruuta", command=custom_dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        width_entry.focus()

    def start_game(self, difficulty, custom_settings=None):
        self.clear_frame()
        if difficulty == "Mukautettu":
            self.root.title(f"Miinaharava - Mukautettu ({custom_settings['size'][0]}x{custom_settings['size'][1]}, {custom_settings['mines']} miinaa)")
            Minesweeper(self.current_frame, self, difficulty, custom_settings)
            w, h = custom_settings["size"]
        else:
            self.root.title(f"Miinaharava - {difficulty}")
            Minesweeper(self.current_frame, self, difficulty)
            settings = DIFFICULTY_SETTINGS[difficulty]
            w, h = settings["size"]
        
        # Lasketaan ikkunan koko riittävän suureksi
        button_size = 30  # Kasvatettu nappien kokoa
        win_w = max(w * button_size + 60, 400)  # Minimum leveys 400
        win_h = h * button_size + 120  # Lisää tilaa yläreunan kontrolleille
        self.center_window(win_w, win_h)

    def show_scoreboard(self):
        self.root.title("Miinaharava - Tulostaulukko")
        self.clear_frame()
        
        # Scrollattava sisältö
        canvas = tk.Canvas(self.current_frame)
        scrollbar = tk.Scrollbar(self.current_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        tk.Label(scrollable_frame, text="Parhaat ajat", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Tavalliset vaikeustasot
        for difficulty, times in self.scores.items():
            if difficulty != "Mukautettu":  # Mukautettu käsitellään erikseen
                frame = tk.LabelFrame(scrollable_frame, text=difficulty, padx=10, pady=10, font=("Arial", 12))
                frame.pack(padx=15, pady=5, fill="x")
                if not times:
                    tk.Label(frame, text="Ei tuloksia.").pack()
                else:
                    for i, time in enumerate(times):
                        tk.Label(frame, text=f"{i+1}. {time:.2f} sekuntia").pack(anchor="w")
        
        # Mukautetut pelit
        if self.custom_scores:
            custom_frame = tk.LabelFrame(scrollable_frame, text="Mukautettu", padx=10, pady=10, font=("Arial", 12))
            custom_frame.pack(padx=15, pady=5, fill="x")
            
            if not self.custom_scores:
                tk.Label(custom_frame, text="Ei tuloksia.").pack()
            else:
                # Järjestä tulokset ajan mukaan
                sorted_scores = sorted(self.custom_scores, key=lambda x: x['time'])
                for i, score in enumerate(sorted_scores[:10]):  # Näytä top 10
                    size_text = f"{score['width']}x{score['height']}"
                    mines_text = f"{score['mines']} miinaa"
                    time_text = f"{score['time']:.2f}s"
                    result_text = f"{i+1}. {time_text} ({size_text}, {mines_text})"
                    tk.Label(custom_frame, text=result_text, font=("Arial", 10)).pack(anchor="w")
        
        back_button = tk.Button(scrollable_frame, text="Takaisin valikkoon", command=self.show_menu)
        back_button.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.center_window(400, 600)

    # --- Ikkunan- ja tulostenhallinta ---
    
    def center_window(self, width, height):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def load_scores(self):
        if not os.path.exists(SCOREBOARD_FILE):
            return {d: [] for d in DIFFICULTY_SETTINGS.keys() if d != "Mukautettu"}
        try:
            with open(SCOREBOARD_FILE, 'r') as f:
                scores = json.load(f)
                # Varmista, että kaikki vaikeustasot ovat olemassa (paitsi Mukautettu)
                for d in DIFFICULTY_SETTINGS.keys():
                    if d != "Mukautettu" and d not in scores:
                        scores[d] = []
                return scores
        except (json.JSONDecodeError, IOError):
            return {d: [] for d in DIFFICULTY_SETTINGS.keys() if d != "Mukautettu"}

    def load_custom_scores(self):
        custom_file = "./Minesweeper/custom_scores.json"
        if not os.path.exists(custom_file):
            return []
        try:
            with open(custom_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_score(self, difficulty, time):
        scores_for_difficulty = self.scores.get(difficulty, [])
        scores_for_difficulty.append(round(time, 2))
        self.scores[difficulty] = sorted(scores_for_difficulty)[:5]
        try:
            with open(SCOREBOARD_FILE, 'w') as f:
                json.dump(self.scores, f, indent=4)
        except IOError as e:
            messagebox.showerror("Virhe", f"Tuloksia ei voitu tallentaa: {e}")

    def save_custom_score(self, custom_settings, time):
        score_entry = {
            "width": custom_settings["size"][0],
            "height": custom_settings["size"][1],
            "mines": custom_settings["mines"],
            "time": round(time, 2)
        }
        self.custom_scores.append(score_entry)
        
        try:
            custom_file = "./Minesweeper/custom_scores.json"
            with open(custom_file, 'w') as f:
                json.dump(self.custom_scores, f, indent=4)
        except IOError as e:
            messagebox.showerror("Virhe", f"Mukautetun pelin tulosta ei voitu tallentaa: {e}")

def main():
    root = tk.Tk()
    try:
        root.iconbitmap("./Minesweeper/bomb.ico")  # .ico-tiedosto
    except tk.TclError:
        try:
            img = tk.PhotoImage(file="./Minesweeper/bomb.png")
            root.iconphoto(True, img)  # Käytä PNG:ää varasuunnitelmana
        except tk.TclError:
            pass  # Ei kuvaketta, jos tiedostoja ei löydy
    
    GameManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()