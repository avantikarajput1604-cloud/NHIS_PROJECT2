from ast import expr
from operator import eq
import tkinter as tk
from tkinter import messagebox
import math
import re

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("scientific calculator")
        self.geometry("300x400")
        self.resizable(False, False)
        
        # Display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        display_label = tk.Label(self, textvariable=self.display_var, font=("times new roman", 28, "bold"), 
                                anchor="e", bg="lightgray", padx=10, pady=10)
        display_label.grid(row=0, column=0, columnspan=6, sticky="ew")
        
        # Bind keyboard events
        self.bind("<Key>", self.on_key_press)
        self.focus()
        
        # Button functions
        def update_display(value):
            current = self.display_var.get()
            if current == "0" or current == "Error":
                self.display_var.set(value)
            else:
                self.display_var.set(current + value)
        
        def clear_display():
            self.display_var.set("0")
        
        def delete_last():
            current = self.display_var.get()
            if len(current) > 1:
                self.display_var.set(current[:-1])
            else:
                self.display_var.set("0")
        
        def calculate_result():
            try:
                expr = self.display_var.get()
                
                # Create a custom namespace with math functions
                namespace = {
                    'sin': lambda x: math.sin(math.radians(x)),
                    'cos': lambda x: math.cos(math.radians(x)),
                    'tan': lambda x: math.tan(math.radians(x)),
                    'asin': lambda x: math.degrees(math.asin(x)),
                    'acos': lambda x: math.degrees(math.acos(x)),
                    'atan': lambda x: math.degrees(math.atan(x)),
                    'sqrt': math.sqrt,
                    'log': math.log10,
                    'ln': math.log,
                    'pi': math.pi,
                    'e': math.e,
                    '__builtins__': {}
                }
                
                # Replace symbolic functions with function calls
                expr = expr.replace("√", "sqrt")
                expr = expr.replace("π", "pi")
                expr = expr.replace("^", "**")
                
                # Handle implicit multiplication (e.g., "2sin(30)" → "2*sin(30)")
                expr = re.sub(r'(\d)\s*(sin|cos|tan|asin|acos|atan|sqrt|log|ln|pi|e)', r'\1*\2', expr)
                expr = re.sub(r'(sin|cos|tan|asin|acos|atan|sqrt|log|ln)\s*\(', r'\1(', expr)
                
                result = eval(expr, namespace)
                
                # Round to avoid floating point errors
                result = round(result, 10)
                self.display_var.set(str(result))
            except Exception as e:
                self.display_var.set("Error")
        
        def add_function(func_name):
            current = self.display_var.get()
            if current == "0":
                self.display_var.set(func_name + "(")
            else:
                self.display_var.set(current + func_name + "(")
        
        def add_opening_bracket():
            current = self.display_var.get()
            if current == "0":
                self.display_var.set("(")
            else:
                self.display_var.set(current + "(")
        
        def add_closing_bracket():
            current = self.display_var.get()
            open_count = current.count("(")
            close_count = current.count(")")
            if open_count > close_count:
                self.display_var.set(current + ")")
        
        # Row 1: Scientific Functions (Trig)
        sci_buttons_row1 = [
            ("sin", 1, 0), ("cos", 1, 1), ("tan", 1, 2), ("ln", 1, 3), ("log", 1, 4), ("π", 1, 5),
        ]
        
        for text, row, col in sci_buttons_row1:
            if text in ["sin", "cos", "tan","ln", "log"]:
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("Arial", 12, "bold"),
                               command=lambda t=text: add_function(t), bg="lightgray", fg="black")
            else:
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("Arial", 12, "bold"),
                               command=lambda t=text: update_display(t), bg="lightgray", fg="black")
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Row 2: More Scientific Functions
        sci_buttons_row2 = [
            ("√", 2, 0), ("^", 2, 1), ("e", 2, 2), ("(", 2, 3), (")", 2, 4), ("%", 2, 5),
        ]
        
        for text, row, col in sci_buttons_row2:
            if text == "√":
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("times new roman", 15, "bold"),
                               command=lambda: add_function("sqrt"), bg="lightgray", fg="black")
            elif text == "(":
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("times new roman", 15, "bold"),
                               command=add_opening_bracket, bg="lightgray", fg="black")
            elif text == ")":
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("times new roman", 15, "bold"),
                               command=add_closing_bracket, bg="lightgray", fg="black")
            else:
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("times new roman", 15, "bold"),
                               command=lambda t=text: update_display(t), bg="lightgray", fg="black")
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Row 3-6: Number and Operation buttons
        buttons = [
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("/", 3, 3), ("*", 3, 4), ("ac", 3, 5),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3), ("+", 4, 4), ("1/x", 4, 5),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), (".", 5, 3), ("0", 5, 4), ("00", 5, 5),
        ]
        
        for text, row, col in buttons:
            if text == "ac":
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("times new roman", 15, "bold"),
                               bg="lightgray", fg="black", command=delete_last)
            elif text == "1/x":
                btn = tk.Button(self, text=text, padx=10, pady=12, font=("times new roman", 15, "bold"),
                               command=lambda: update_display("1/"), bg="lightgray", fg="black")
            else:
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("times new roman", 15, "bold"),
                               command=lambda t=text: update_display(t))
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Row 7: Equals and Clear buttons (side by side)
        eq_btn = tk.Button(self, text="=", padx=12, pady=12, font=("times new roman", 15, "bold"),
                           bg="orange", fg="white", command=calculate_result)
        eq_btn.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=2, pady=2)
        
        clear_btn = tk.Button(self, text="C", padx=12, pady=12, font=("times new roman", 12, "bold"),
                              bg="orange", fg="white", command=clear_display)
        clear_btn.grid(row=6, column=3, columnspan=3, sticky="nsew", padx=2, pady=2)
        
        self.history = []  # Stores (expr, result)


        # Grid config
        for i in range(7): 
            self.grid_rowconfigure(i, weight=1)
        for i in range(5): 
            self.grid_columnconfigure(i, weight=1)

        def add_to_history(self, expr, result):
         if not self.history or (expr, result) != self.history[-1]:
            self.history.append((expr, result))

    def show_history_popup(self):
        popup = tk.Toplevel(self)
        popup.title("History")
        popup.geometry("320x350")
        tk.Label(popup, text="Calculation History", font=("Arial", 14, "bold")).pack(pady=8)
        listbox = tk.Listbox(popup, height=15, font=("Arial", 12), activestyle="dotbox")
        listbox.pack(fill="both", expand=True, padx=10)
        for expr, res in self.history:
            listbox.insert(tk.END, f"{expr} = {res}")
        def on_select(event):
            sel = listbox.curselection()
            if sel:
                val = listbox.get(sel[0])
                eq_idx = val.find('=')
                expr_val = val[:eq_idx].strip()
                self.display_var.set(expr_val)
                popup.destroy()
        listbox.bind("<<ListboxSelect>>", on_select)
        tk.Button(popup, text="Close", font=("Arial", 12), command=popup.destroy).pack(pady=8)

    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        # Number keys
        if key.isdigit():
            current = self.display_var.get()
            if current == "0" or current == "Error":
                self.display_var.set(key)
            else:
                self.display_var.set(current + key)
        
        # Operators
        elif key in "+-*/.":
            current = self.display_var.get()
            if current != "0" and current != "Error":
                self.display_var.set(current + key)
            elif key == ".":
                self.display_var.set(current + key)
        
        # Opening bracket
        elif key == "(":
            current = self.display_var.get()
            if current == "0":
                self.display_var.set("(")
            else:
                self.display_var.set(current + "(")
        
        # Closing bracket
        elif key == ")":
            current = self.display_var.get()
            open_count = current.count("(")
            close_count = current.count(")")
            if open_count > close_count:
                self.display_var.set(current + ")")
        
        # Power operation
        elif key == "^":
            current = self.display_var.get()
            if current != "0" and current != "Error":
                self.display_var.set(current + key)
        
        # Enter key or = for calculation
        elif event.keysym in ("Return", "Equal"):
            self.calculate_result_keyboard()
        
        # Backspace for delete
        elif event.keysym == "BackSpace":
            current = self.display_var.get()
            if len(current) > 1:
                self.display_var.set(current[:-1])
            else:
                self.display_var.set("0")
            
        
        # Clear with 'c' or 'C'
        elif key.lower() == "c":
            self.display_var.set("0")
        
        # Escape to clear
        elif event.keysym == "Escape":
            self.display_var.set("0")
    
    def calculate_result_keyboard(self):
        """Calculate result (for keyboard input)"""
        try:
            expr = self.display_var.get()

            
            # Create a custom namespace with math functions
            namespace = {
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                'asin': lambda x: math.degrees(math.asin(x)),
                'acos': lambda x: math.degrees(math.acos(x)),
                'atan': lambda x: math.degrees(math.atan(x)),
                'sqrt': math.sqrt,
                'log': math.log10,
                'ln': math.log,
                'pi': math.pi,
                'e': math.e,
                '__builtins__': {}
            }
            
            # Replace symbolic functions with function calls
            expr = expr.replace("√", "sqrt")
            expr = expr.replace("π", "pi")
            expr = expr.replace("^", "**")
            
            # Handle implicit multiplication
            expr = re.sub(r'(\d)\s*(sin|cos|tan|asin|acos|atan|sqrt|log|ln|pi|e)', r'\1*\2', expr)
            expr = re.sub(r'(sin|cos|tan|asin|acos|atan|sqrt|log|ln)\s*\(', r'\1(', expr)
            
            result = eval(expr, namespace)
            result = round(result, 10)
            self.display_var.set(str(result))
        except Exception as e:
            self.display_var.set("Error")

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()