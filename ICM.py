import tkinter as tk
import json
import os
import keyboard
import time

class ModernSkillButton(tk.Frame):
    def __init__(self, parent, skill_name, combo_keys, bind_key, icon, bg_color, command, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.configure(bg=bg_color, height=28)
        
        self.skill_name = skill_name
        self.combo_keys = combo_keys
        self.bind_key = bind_key
        self.icon = icon
        self.command = command
        self.bg_color = bg_color
        
        self.create_widgets()
        
    def create_widgets(self):
        content = tk.Frame(self, bg=self.bg_color)
        content.pack(fill='both', expand=True, padx=0, pady=0)
        
        left_frame = tk.Frame(content, bg=self.bg_color)
        left_frame.pack(side='left', fill='both', expand=True)
        
        name_frame = tk.Frame(left_frame, bg=self.bg_color)
        name_frame.pack(fill='x')
        
        tk.Label(name_frame, text=self.icon, font=('Arial', 9), 
                fg='#ff4444', bg=self.bg_color).pack(side='left')
        
        tk.Label(name_frame, text=self.skill_name, font=('Arial', 8), 
                fg='#ffffff', bg=self.bg_color, anchor='w').pack(side='left', padx=(3, 0))
        
        tk.Label(left_frame, text=self.combo_keys, font=('Arial', 7), 
                fg='#888888', bg=self.bg_color, anchor='w').pack(fill='x')
        
        right_frame = tk.Frame(content, bg=self.bg_color)
        right_frame.pack(side='right')
        
        self.bind_label = tk.Label(right_frame, text=self.bind_key, font=('Arial', 8, 'bold'),
                                  fg='#ff4444', bg=self.bg_color, width=3)
        self.bind_label.pack(padx=(5, 0))
        
        self.bind_label.bind("<Button-1>", self.start_binding)
        
    def start_binding(self, event):
        self.bind_label.config(text="???", fg='#ffaa00')
        return self
        
    def update_bind(self, new_key):
        self.bind_key = new_key
        self.bind_label.config(text=new_key, fg='#ff4444')

class InvokerComboBinds:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Invoker Combo Master")
        self.root.geometry("280x449")
        self.root.configure(bg='#000000')
        self.root.resizable(False, False)
        
        self.root.attributes('-topmost', True)
        
        try:
            self.root.iconbitmap('invoker_icon.ico')
        except:
            pass
        
        self.center_window()
        
        self.colors = {
            'bg': '#000000',
            'accent': '#ff4444',
            'text_primary': '#ffffff',
            'text_secondary': '#888888'
        }
        
        self.delays = {
            'between_keys': 0.15,
            'last_key': 0.25,
            'before_r': 0.1
        }
        
        self.binding_index = None
        self.config_file = "invoker_binds_config.json"
        
        self.skill_data = [
            ("Chaos Meteor", "EEW", "q", "🔥"),
            ("EMP", "WWW", "w", "⚡"),
            ("Tornado", "WWQ", "e", "🌪️"),
            ("Cold Snap", "QQQ", "1", "❄️"),
            ("Sun Strike", "EEE", "2", "☀️"),
            ("Ghost Walk", "QQW", "3", "👻"),
            ("Ice Wall", "QQE", "4", "🧊"),
            ("Forge Spirit", "EEQ", "5", "🔥"),
            ("Deafening Blast", "QWE", "6", "💥"),
            ("Alacrity", "WWE", "7", "✨")
        ]
        
        self.load_binds()
        self.create_ui()
        self.setup_hotkeys()
        
        self.root.mainloop()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def load_binds(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_binds = json.load(f)
                    updated_skills = []
                    for name, combo, default_key, icon in self.skill_data:
                        saved_key = saved_binds.get(name.lower().replace(" ", "_"), default_key)
                        updated_skills.append((name, combo, saved_key, icon))
                    self.skill_data = updated_skills
            except:
                pass
    
    def save_binds(self):
        binds = {}
        for name, combo, key, icon in self.skill_data:
            binds[name.lower().replace(" ", "_")] = key
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(binds, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def setup_hotkeys(self):
        try:
            keyboard.unhook_all()
            
            for name, combo, key, icon in self.skill_data:
                func = getattr(self, f"cast_{name.lower().replace(' ', '_')}")
                keyboard.add_hotkey(key, func)
                
        except:
            pass
    
    def press_keys_with_delay(self, keys):
        delays = [self.delays['between_keys']] * len(keys)
        delays[-1] = self.delays['last_key']
        
        for key, delay in zip(keys, delays):
            keyboard.press_and_release(key)
            time.sleep(delay)
    
    def cast_chaos_meteor(self): 
        self._cast_spell(['e', 'e', 'w'])
    
    def cast_emp(self): 
        self._cast_spell(['w', 'w', 'w'])
    
    def cast_tornado(self): 
        self._cast_spell(['w', 'w', 'q'])
    
    def cast_cold_snap(self): 
        self._cast_spell(['q', 'q', 'q'])
    
    def cast_sun_strike(self): 
        self._cast_spell(['e', 'e', 'e'])
    
    def cast_ghost_walk(self): 
        self._cast_spell(['q', 'q', 'w'])
    
    def cast_ice_wall(self): 
        self._cast_spell(['q', 'q', 'e'])
    
    def cast_forge_spirit(self): 
        self._cast_spell(['e', 'e', 'q'])
    
    def cast_deafening_blast(self): 
        self._cast_spell(['q', 'w', 'e'])
    
    def cast_alacrity(self): 
        self._cast_spell(['w', 'w', 'e'])
    
    def _cast_spell(self, keys):
        self.press_keys_with_delay(keys)
        time.sleep(self.delays['before_r'])
        keyboard.press_and_release('r')
    
    def create_ui(self):
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=10, pady=6)
        
        header = tk.Frame(main_container, bg=self.colors['bg'], height=40)
        header.pack(fill='x', pady=(0, 5))
        
        tk.Label(header, text="INVOKER COMBO", font=('Arial', 11, 'bold'),
                fg=self.colors['accent'], bg=self.colors['bg']).pack()
        
        tk.Label(header, text="Click key to rebind", 
                font=('Arial', 7), fg=self.colors['text_secondary'], 
                bg=self.colors['bg']).pack()
        
        skills_frame = tk.Frame(main_container, bg=self.colors['bg'])
        skills_frame.pack(fill='both', expand=True)
        
        self.skill_buttons = []
        
        for i, (name, combo, key, icon) in enumerate(self.skill_data):
            btn = ModernSkillButton(skills_frame, name, combo, key, icon, 
                                  self.colors['bg'], getattr(self, f"cast_{name.lower().replace(' ', '_')}"))
            btn.pack(fill='x', pady=0)
            self.skill_buttons.append(btn)
            
            btn.bind_label.bind("<Button-1>", lambda e, idx=i: self.start_binding(idx))
        
        status_bar = tk.Frame(main_container, bg=self.colors['bg'], height=20)
        status_bar.pack(fill='x', pady=(5, 0))
        
        self.status_label = tk.Label(status_bar, text="Ready", font=('Arial', 7),
                                   fg=self.colors['text_secondary'], bg=self.colors['bg'])
        self.status_label.pack()
        
        self.root.bind('<Key>', self.key_press)
        self.root.focus_set()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def start_binding(self, index):
        self.binding_index = index
        self.skill_buttons[index].bind_label.config(text="???", fg='#ffaa00')
        self.status_label.config(text=f"Press new key for {self.skill_data[index][0]}...")
    
    def key_press(self, event):
        if self.binding_index is not None:
            index = self.binding_index
            new_key = event.keysym.lower()
            
            if new_key in ['shift_l', 'shift_r', 'control_l', 'control_r', 'alt_l', 'alt_r', 'caps_lock']:
                return
            
            name, combo, old_key, icon = self.skill_data[index]
            self.skill_data[index] = (name, combo, new_key, icon)
            
            self.skill_buttons[index].update_bind(new_key)
            
            self.save_binds()
            self.setup_hotkeys()
            
            self.status_label.config(text=f"✓ {name} bound to {new_key}")
            self.binding_index = None
    
    def on_closing(self):
        self.save_binds()
        self.root.destroy()

if __name__ == "__main__":
    app = InvokerComboBinds()