import numpy as np
import tkinter as tk
import random as rand
import re

population = np.zeros(shape=(3, 3))
WIDTH = 1024
HEIGHT = 512
GENE_SIZE = 8
num_genes = 0
num_generations = 0
isInitial = False
min_value = 16
win_percentage = .75


# '#%02x%02x%02x' % (0, 128, 64)

def validate_number(number):
    return re.match("^[0-9]+$", number)


def set_generated_flag():
    global is_generated
    is_generated = True


def generate_population(canvas_frame: tk.Frame, canvas: tk.Canvas, dim, chromosome_length):
    global population, is_generated, btn_start_simulation, GENE_SIZE, WIDTH, HEIGHT
    if validate_number(dim) and validate_number(chromosome_length) and not isInitial:
        population = np.random.uniform(size=(int(dim), int(chromosome_length)), low=0, high=99).astype("int32")
        old_width = canvas.winfo_width()
        old_height = canvas.winfo_height()
        new_width = GENE_SIZE * population.shape[1]
        new_height = GENE_SIZE * population.shape[0]
        dw = new_width - old_width
        dh = new_height - old_height
        width = old_width + dw
        height = old_height + dh

        if width >= WIDTH:
            canvas.config(width=old_width + dw, scrollregion=(0, 0, width, height))
        else:
            canvas.config(width=WIDTH * win_percentage, scrollregion=(0, 0, WIDTH * win_percentage, HEIGHT))

        if height >= HEIGHT:
            canvas.config(height=old_height + dh, scrollregion=(0, 0, width, height))
        else:
            canvas.config(height=HEIGHT, scrollregion=(0, 0, WIDTH * win_percentage, HEIGHT))

        draw_population(canvas, population, 0, 0)


def draw_population(canvas: tk.Canvas, pop: np.ndarray, x0, y0):
    global GENE_SIZE

    width = int(WIDTH * win_percentage)
    height = HEIGHT
    population_width = pop.shape[1]
    population_height = pop.shape[0]

    x1 = x0 + pop.shape[1]

    if population_height * GENE_SIZE > height:
        y1 = y0 + height // GENE_SIZE
    else:
        y1 = y0 + population_height

    canvas.delete("all")
    for i in range(y0, y1):
        for j in range(x0, x1):
            canvas.create_rectangle(j * GENE_SIZE, i * GENE_SIZE, j * GENE_SIZE + GENE_SIZE,
                                    i * GENE_SIZE + GENE_SIZE,
                                    fill='#%02x%02x%02x' % (0, 0, int((255 * pop[i - y0, j - x0]) / 99)))


def scroll_callback(event: tk.Event):
    print(event.delta)


def fitness(pop: np.ndarray):
    return np.sum(pop, axis=1)


def crossover(parent1, parent2):
    axis = rand.randint(1, len(parent1) - 2)
    return np.hstack((parent1[0:axis], parent2[axis:]))


def mutate(chromozome: np.ndarray):
    pass


def on_refresh():
    length = scroll_y.get()[1] - scroll_y.get()[0]
    y = scroll_y.get()[1] - length
    k = int(canvas.winfo_reqheight() * y)
    print(k)
    draw_population(canvas, population, 0, k // GENE_SIZE)


def on_mousemovement(event):
    global canvas, population, GENE_SIZE
    k = int(HEIGHT * scroll_y.get()[1]) * GENE_SIZE
    print(k)
    draw_population(canvas, population, 0, 64)


# init window
window = tk.Tk()
window.geometry(str(WIDTH) + "x" + str(HEIGHT))

# canvas frame
canvas_frame = tk.Frame(window, width=WIDTH * win_percentage, height=HEIGHT)
canvas_frame.pack(side=tk.LEFT)

# init canvas
canvas = tk.Canvas(canvas_frame, width=WIDTH * win_percentage, height=HEIGHT)

# scrolling
scroll_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
scroll_y.pack(fill="y", side=tk.RIGHT)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.config(bg="black", yscrollcommand=scroll_y.set, scrollregion=(0, 0, WIDTH, HEIGHT))

frame = tk.Frame(window, width=WIDTH * (1 - win_percentage), height=HEIGHT)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.pack()

# labels & text boxes
lb_no_generations = tk.Label(frame, text="Nr. generații:")
lb_no_generations.pack(pady=8)
entry_no_generations = tk.Entry(frame)
entry_no_generations.pack()

lb_no_generations = tk.Label(frame, text="Dimensiune populatie")
lb_no_generations.pack(pady=8)
entry_dim_population = tk.Entry(frame)
entry_dim_population.pack()

lb_no_generations = tk.Label(frame, text="Lungime cromozom")
lb_no_generations.pack(pady=8)
entry_len_chromosome = tk.Entry(frame)
entry_len_chromosome.pack()

lb_no_generations = tk.Label(frame, text="Probabilitate mutație(%)")
lb_no_generations.pack(pady=8)
entry_mutation_probability = tk.Entry(frame)
entry_mutation_probability.pack()

# buttons
btn_generate_population = tk.Button(frame, text="Genereaza populatie", command=lambda: generate_population(
    canvas_frame,
    canvas,
    entry_dim_population.get(),
    entry_len_chromosome.get()
))
btn_generate_population.pack(pady=32)

btn_start_simulation = tk.Button(frame, text="Start simulatie")
btn_start_simulation.pack(pady=8)

btn_refresh = tk.Button(frame, text="Refresh", command=on_refresh)
btn_refresh.pack(pady=8)

# frame.pack()
window.mainloop()
