import tkinter as tk
from tkinter import scrolledtext
from googletrans import Translator
import time

# Translator object
translator = Translator()

# Supported Indian languages
all_languages = {
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Punjabi": "pa",
}

# Animate gradient background
def animate_bg():
    global color_index
    colors = ["#e6f2ff", "#cce6ff", "#b3daff", "#99ceff", "#80c1ff"]
    root.configure(bg=colors[color_index])
    header.configure(bg=colors[color_index])
    input_label.configure(bg=colors[color_index])
    checkbox_frame.configure(bg=colors[color_index])
    button_frame.configure(bg=colors[color_index])
    output_label.configure(bg=colors[color_index])
    color_index = (color_index + 1) % len(colors)
    root.after(400, animate_bg)

# Translate selected languages with animation
def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        return
    output_text.delete("1.0", tk.END)
    for lang, code in all_languages.items():
        if language_vars[lang].get():
            translated = translator.translate(text, dest=code)
            output_text.insert(tk.END, f"{lang} Translation: {translated.text}\n\n")
            output_text.update()
            time.sleep(0.3)  # Small delay for animation effect

# Clear input/output
def clear_text():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

# Main window
root = tk.Tk()
root.title("English → Indian Languages Translator")
root.geometry("850x650")
color_index = 0

# Header
header = tk.Label(root, text="🈳 English → Indian Languages Translator", font=("Helvetica", 16, "bold"))
header.pack(pady=10)

# Input label
input_label = tk.Label(root, text="Enter English text:", font=("Helvetica", 12))
input_label.pack(pady=5)

# Input box
input_text = scrolledtext.ScrolledText(root, height=6, width=100, font=("Helvetica", 12))
input_text.pack(pady=5)

# Language selection
tk.Label(root, text="Select Languages:", font=("Helvetica", 12)).pack(pady=5)
language_vars = {}
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(pady=5)
for i, lang in enumerate(all_languages):
    var = tk.IntVar(value=1)
    chk = tk.Checkbutton(checkbox_frame, text=lang, variable=var, font=("Helvetica", 10))
    chk.grid(row=i//5, column=i%5, padx=5, pady=2, sticky="w")
    language_vars[lang] = var

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
tk.Button(button_frame, text="Translate", command=translate_text, bg="#4da6ff", fg="white",
          width=15, font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Clear", command=clear_text, bg="#ff6666", fg="white",
          width=15, font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=10)

# Output label
output_label = tk.Label(root, text="Translations:", font=("Helvetica", 12))
output_label.pack(pady=5)

# Output box
output_text = scrolledtext.ScrolledText(root, height=20, width=100, font=("Helvetica", 12), bg="#f0f0f0")
output_text.pack(pady=5)

# Start gradient background animation
animate_bg()

# Run GUI
root.mainloop()
