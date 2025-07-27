import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Initialize Data ---
genders = ['Male', 'Female', 'Other']
population = [700, 650, 50]
ages = np.random.normal(loc=35, scale=15, size=1000)

# --- GUI Setup ---
window = tk.Tk()
window.title("Population Visualizer")
window.geometry("950x650")
window.configure(bg="#1e1e1e")

# --- Menu Functions ---
def show_about():
    messagebox.showinfo("About", "Population Visualizer v1.0\nCreated by Joe Allwin\nUsing Tkinter & Matplotlib")

def exit_app():
    window.quit()

# --- Styles ---
def apply_dark_mode():
    window.configure(bg="#1e1e1e")
    header.configure(bg="#1e1e1e", fg="white")
    summary_label.configure(bg="#1e1e1e", fg="white")
    chart_frame.configure(bg="#1e1e1e")
    btn_frame.configure(bg="#1e1e1e")
    theme_btn.configure(text="🌞 Light Mode", bg="#252525", fg="white")
    save_btn.configure(bg="#252525", fg="white")

def apply_light_mode():
    window.configure(bg="white")
    header.configure(bg="white", fg="black")
    summary_label.configure(bg="white", fg="black")
    chart_frame.configure(bg="white")
    btn_frame.configure(bg="white")
    theme_btn.configure(text="🌙 Dark Mode", bg="#e0e0e0", fg="black")
    save_btn.configure(bg="#e0e0e0", fg="black")

# --- Chart Drawing ---
def draw_chart(chart_type):
    fig = plt.Figure(figsize=(7, 4.5), dpi=100)
    ax = fig.add_subplot(111)

    if chart_type == "Bar Chart (Gender)":
        ax.bar(genders, population, color=['#00aaff', '#ff69b4', '#a17ef8'])
        ax.set_title("Gender Distribution")
        ax.set_ylabel("Population (millions)")
        summary_text = f"Total Population: {sum(population)} million"
    elif chart_type == "Histogram (Age)":
        ax.hist(ages, bins=20, color='#00c896', edgecolor='black', alpha=0.75)
        ax.set_title("Age Distribution")
        ax.set_xlabel("Age")
        ax.set_ylabel("Frequency")
        summary_text = f"Average Age: {np.mean(ages):.2f} | Std Dev: {np.std(ages):.2f}"

    ax.grid(axis='y', linestyle='--', alpha=0.6)

    for widget in chart_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    summary_label.config(text=summary_text)

    global current_fig
    current_fig = fig

# --- Save Chart ---
def save_chart():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if file_path and current_fig:
        current_fig.savefig(file_path)

# --- Toggle Theme ---
is_dark = True
def toggle_theme():
    global is_dark
    if is_dark:
        apply_light_mode()
    else:
        apply_dark_mode()
    is_dark = not is_dark

# --- Menu Bar ---
menubar = tk.Menu(window)

# File Menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Save Chart", command=save_chart)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

# View Menu
view_menu = tk.Menu(menubar, tearoff=0)
view_menu.add_command(label="Toggle Theme", command=toggle_theme)
menubar.add_cascade(label="View", menu=view_menu)

# Help Menu
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)

window.config(menu=menubar)

# --- Widgets ---
header = tk.Label(window, text="📊 Population Distribution Visualizer",
                  font=("Segoe UI", 20, "bold"), bg="#1e1e1e", fg="white")
header.pack(pady=20)

chart_option = tk.StringVar()
chart_option.set("Bar Chart (Gender)")

dropdown = ttk.Combobox(window, textvariable=chart_option, state="readonly",
                        values=["Bar Chart (Gender)", "Histogram (Age)"],
                        font=("Segoe UI", 12), width=30)
dropdown.pack()

# On dropdown change, update chart automatically
dropdown.bind("<<ComboboxSelected>>", lambda e: draw_chart(chart_option.get()))

# Button Row
btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack(pady=10)

save_btn = tk.Button(btn_frame, text="💾 Save Chart", command=save_chart,
                     font=("Segoe UI", 11, "bold"), bg="#252525", fg="white", padx=15, pady=6)
save_btn.grid(row=0, column=0, padx=10)

theme_btn = tk.Button(btn_frame, text="🌙 Dark Mode", command=toggle_theme,
                      font=("Segoe UI", 11, "bold"), bg="#252525", fg="white", padx=15, pady=6)
theme_btn.grid(row=0, column=1, padx=10)

# Chart Area
chart_frame = tk.Frame(window, bg="#1e1e1e")
chart_frame.pack(pady=20)

# Data Summary
summary_label = tk.Label(window, text="", font=("Segoe UI", 11), bg="#1e1e1e", fg="white")
summary_label.pack(pady=10)

# Start with chart
current_fig = None
draw_chart(chart_option.get())

# Apply default theme
apply_dark_mode()

# Run App
window.mainloop()
