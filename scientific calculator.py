
import tkinter as tk
from tkinter import *
import math   # for sin, cos, sqrt, log, etc.
import re 
from datetime import datetime , timedelta
from tkinter import messagebox
import operator as op

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("300x400")
        self.resizable(False, False)
        
        # Display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        display_label = tk.Label(self, textvariable=self.display_var, font=("Arial", 28, "bold"), 
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
                
                # Replace symbolic functions → Python math functions
                expr = expr.replace("sin(", "math.sin(")
                expr = expr.replace("cos(", "math.cos(")
                expr = expr.replace("tan(", "math.tan(")
                expr = expr.replace("√(", "math.sqrt(")
                expr = expr.replace("√", "math.sqrt(")
                expr = expr.replace("log(", "math.log10(")
                expr = expr.replace("ln(", "math.log(")
                expr = expr.replace("π", str(math.pi))
                expr = expr.replace("e", str(math.e))
                expr = expr.replace("^", "**")
                
                # Handle cases like "2sin(30)" → "2*sin(30)"
                expr = re.sub(r'(\d)\s*(sin|cos|tan|math\.sin|math\.cos|math\.tan|math\.sqrt|math\.log)', r'\1*\2', expr)
                
                result = eval(expr)
                
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
        
        # Row 2: More Scientific Functions
        sci_buttons_row2 = [
            ("√", 2, 0), ("^", 2, 1), ("e", 2, 2), ("(", 2, 3), (")", 2, 4), ("%", 2, 5),
        ]
        
        for text, row, col in sci_buttons_row2:
            if text == "√":
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("Arial", 12, "bold"),
                               command=lambda: add_function("sqrt"), bg="lightyellow")
            elif text == "(":
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("Arial", 12, "bold"),
                               command=add_opening_bracket, bg="lightyellow")
            elif text == ")":
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("Arial", 12, "bold"),
                               command=add_closing_bracket, bg="lightyellow")
            else:
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("Arial", 12, "bold"),
                               command=lambda t=text: update_display(t), bg="lightyellow")
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Row 3-6: Number and Operation buttons
        buttons = [
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("/", 3, 3), ("*", 3, 4), ("←", 3, 5),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3), ("+", 4, 4), ("1/x", 4, 5),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), (".", 5, 3), ("00", 5, 4), ("0", 5, 5),
        ]
        
        for text, row, col in buttons:
            if text == "ac":
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("Arial", 12, "bold"),
                               bg="lightyellow", fg="white", command=delete_last)
            elif text == "1/x":
                btn = tk.Button(self, text=text, padx=10, pady=12, font=("Arial", 11, "bold"),
                               command=lambda: update_display("1/"), bg="lightyellow")
            else:
                btn = tk.Button(self, text=text, padx=12, pady=12, font=("Arial", 12, "bold"),
                               command=lambda t=text: update_display(t))
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Row 7: Equals and Clear buttons (side by side)
        eq_btn = tk.Button(self, text="=", padx=12, pady=12, font=("Arial", 12, "bold"),
                          bg="orange", fg="white", command=calculate_result)
        eq_btn.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=2, pady=2)
        
        clear_btn = tk.Button(self, text="C", padx=12, pady=12, font=("Arial", 12, "bold"),
                             bg="orange", fg="white", command=clear_display)
        clear_btn.grid(row=6, column=3, columnspan=3, sticky="nsew", padx=2, pady=2)
        
        # Grid config
        for i in range(7): 
            self.grid_rowconfigure(i, weight=1)
        for i in range(6): 
            self.grid_columnconfigure(i, weight=1)
    
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
            
            # Replace symbolic functions → Python math functions
            expr = expr.replace("sin(", "math.sin(")
            expr = expr.replace("cos(", "math.cos(")
            expr = expr.replace("tan(", "math.tan(")
            expr = expr.replace("√(", "math.sqrt(")
            expr = expr.replace("√", "math.sqrt(")
            expr = expr.replace("log(", "math.log10(")
            expr = expr.replace("ln(", "math.log(")
            expr = expr.replace("π", str(math.pi))
            expr = expr.replace("e", str(math.e))
            expr = expr.replace("^", "**")
            
            # Handle cases like "2sin(30)" → "2*sin(30)"
            expr = re.sub(r'(\d)\s*(sin|cos|tan|math\.sin|math\.cos|math\.tan|math\.sqrt|math\.log)', r'\1*\2', expr)
            
# Function to calculate trigonometric numbers of an angle
    def trig_sin():
     global calc_operator
    result = str(math.sin(math.radians(int(calc_operator))))
    calc_operator = result    
    text_input.set(result)

    def trig_cos():
     global calc_operator
    result = str(math.cos(math.radians(int(calc_operator))))
    calc_operator = result
    text_input.set(result)

    def trig_tan():
        global calc_operator
    result = str(math.tan(math.radians(int(calc_operator))))
    calc_operator = result
    text_input.set(result)

result = eval(expr)
result = round(result, 10)
self.display_var.set(str(result))
except Exception as e:
    self.display_var.set("Error")

    if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()