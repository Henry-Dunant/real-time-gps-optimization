import tkinter as tk
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Elite Adaptive Traffic Intersection")
root.geometry("950x800")
root.configure(bg="#f4f6f7")

title = tk.Label(root, text="Intelligent Traffic Control Simulator",
                 font=("Arial", 16, "bold"), bg="#f4f6f7")
title.pack(pady=10)

# ---------------- SIGNAL CREATION ----------------
def create_signal(parent, lane_name):
    frame = tk.Frame(parent, bg="#f4f6f7")
    canvas = tk.Canvas(frame, width=60, height=180, bg="black")

    red = canvas.create_oval(10, 10, 50, 50, fill="red")
    yellow = canvas.create_oval(10, 65, 50, 105, fill="grey")
    green = canvas.create_oval(10, 120, 50, 160, fill="grey")

    canvas.pack()
    label = tk.Label(frame, text=lane_name, bg="#f4f6f7", font=("Arial", 12))
    label.pack()
    frame.pack(side="left", padx=40)

    return canvas, red, yellow, green

signal_frame = tk.Frame(root, bg="#f4f6f7")
signal_frame.pack(pady=10)

laneA_canvas, A_red, A_yellow, A_green = create_signal(signal_frame, "Lane A")
laneB_canvas, B_red, B_yellow, B_green = create_signal(signal_frame, "Lane B")
laneC_canvas, C_red, C_yellow, C_green = create_signal(signal_frame, "Lane C")

# ---------------- INFO LABELS ----------------
laneA_label = tk.Label(root, font=("Arial", 12), bg="#f4f6f7")
laneA_label.pack()
laneB_label = tk.Label(root, font=("Arial", 12), bg="#f4f6f7")
laneB_label.pack()
laneC_label = tk.Label(root, font=("Arial", 12), bg="#f4f6f7")
laneC_label.pack()

phase_label = tk.Label(root, font=("Arial", 13, "bold"), bg="#f4f6f7")
phase_label.pack(pady=5)

# ---------------- GRAPH ----------------
fig = Figure(figsize=(7, 4), dpi=100)
ax = fig.add_subplot(111)
canvas_graph = FigureCanvasTkAgg(fig, master=root)
canvas_graph.get_tk_widget().pack(pady=10)

time_steps = []
laneA_data = []
laneB_data = []
laneC_data = []
step = 0

# ---------------- INITIAL STATE ----------------
laneA, laneB, laneC = 50, 40, 45
current_green = "Lane A"
next_green = "Lane A"

phase = "GREEN"
timer = 0

MIN_GREEN = 4
YELLOW_TIME = 2
SWITCH_MARGIN = 5

MAX_CAPACITY = 150
MIN_CAPACITY = 10

mapping = {
    "Lane A": (laneA_canvas, A_red, A_yellow, A_green),
    "Lane B": (laneB_canvas, B_red, B_yellow, B_green),
    "Lane C": (laneC_canvas, C_red, C_yellow, C_green)
}

# ---------------- SIGNAL UPDATE ----------------
def update_signals():
    for canvas, r, y, g in mapping.values():
        canvas.itemconfig(r, fill="red")
        canvas.itemconfig(y, fill="grey")
        canvas.itemconfig(g, fill="grey")

    if phase == "GREEN":
        canvas, r, y, g = mapping[current_green]
        canvas.itemconfig(r, fill="grey")
        canvas.itemconfig(g, fill="green")

    elif phase == "SWITCHING":
        # Simultaneous switching phase
        # Current lane → Yellow
        canvas, r, y, g = mapping[current_green]
        canvas.itemconfig(r, fill="grey")
        canvas.itemconfig(y, fill="yellow")

        # Next lane → Red + Yellow
        canvas2, r2, y2, g2 = mapping[next_green]
        canvas2.itemconfig(y2, fill="yellow")

# ---------------- MAIN UPDATE ----------------
def update():
    global laneA, laneB, laneC
    global current_green, next_green
    global phase, timer, step

    densities = {"Lane A": laneA, "Lane B": laneB, "Lane C": laneC}

    pressures = {}
    for lane in densities:
        others = [densities[l] for l in densities if l != lane]
        pressures[lane] = densities[lane] - (sum(others)/2)

    best_lane = max(pressures, key=pressures.get)

    timer += 1

    if phase == "GREEN":
        if timer >= MIN_GREEN and \
           pressures[best_lane] > pressures[current_green] + SWITCH_MARGIN:
            phase = "SWITCHING"
            next_green = best_lane
            timer = 0

    elif phase == "SWITCHING":
        if timer >= YELLOW_TIME:
            current_green = next_green
            phase = "GREEN"
            timer = 0

    # -------- VEHICLE LOGIC --------
    total_density = laneA + laneB + laneC
    congestion_factor = max(0.4, 1 - total_density/500)

    arrivalA = int(random.randint(2, 4) * congestion_factor)
    arrivalB = int(random.randint(2, 4) * congestion_factor)
    arrivalC = int(random.randint(2, 4) * congestion_factor)

    green_flow = 12
    red_flow = 3

    if phase == "GREEN":
        if current_green == "Lane A":
            laneA += arrivalA - green_flow
            laneB += arrivalB + red_flow
            laneC += arrivalC + red_flow
        elif current_green == "Lane B":
            laneB += arrivalB - green_flow
            laneA += arrivalA + red_flow
            laneC += arrivalC + red_flow
        elif current_green == "Lane C":
            laneC += arrivalC - green_flow
            laneA += arrivalA + red_flow
            laneB += arrivalB + red_flow
    else:
        laneA += arrivalA
        laneB += arrivalB
        laneC += arrivalC

    laneA = max(MIN_CAPACITY, min(MAX_CAPACITY, laneA))
    laneB = max(MIN_CAPACITY, min(MAX_CAPACITY, laneB))
    laneC = max(MIN_CAPACITY, min(MAX_CAPACITY, laneC))

    update_signals()

    laneA_label.config(text=f"Lane A Density: {laneA}")
    laneB_label.config(text=f"Lane B Density: {laneB}")
    laneC_label.config(text=f"Lane C Density: {laneC}")
    phase_label.config(text=f"Phase: {phase} | Active Lane: {current_green}")

    time_steps.append(step)
    laneA_data.append(laneA)
    laneB_data.append(laneB)
    laneC_data.append(laneC)
    step += 1

    if len(time_steps) > 50:
        time_steps.pop(0)
        laneA_data.pop(0)
        laneB_data.pop(0)
        laneC_data.pop(0)

    ax.clear()
    ax.set_title("Traffic Density Evolution")
    ax.set_xlabel("Time")
    ax.set_ylabel("Vehicle Density")
    ax.plot(time_steps, laneA_data, label="Lane A")
    ax.plot(time_steps, laneB_data, label="Lane B")
    ax.plot(time_steps, laneC_data, label="Lane C")
    ax.legend()

    canvas_graph.draw()

    root.after(2000, update)

update()
root.mainloop()