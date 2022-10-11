import numpy as np
import tkinter as tk
import random as rand
import re
import time
import threading

population = np.zeros(shape=(3, 3))
WIDTH = 1024
HEIGHT = 512
GENE_SIZE = 8
num_genes = 0
num_generations = 0
isInitial = False
min_value = 16
win_percentage = .75
spd_alg = 1


# '#%02x%02x%02x' % (0, 128, 64)

def validate_number(number):
    return re.match("^[0-9]+$", number)


def generate_population(canvas_frame: tk.Frame, canvas: tk.Canvas, dim, chromosome_length):
    global population, is_generated, btn_start_simulation, GENE_SIZE, WIDTH, HEIGHT
    if validate_number(dim) and validate_number(chromosome_length):
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

    sliced_population = pop[y0:y1 + 1]

    canvas.delete("all")
    for i in range(y0, y1):
        for j in range(x0, x1):
            color = '#%02x%02x%02x' % (0, int((255 * sliced_population[i - y0, j - x0]) / 99), 0)
            canvas.create_rectangle(j * GENE_SIZE, i * GENE_SIZE, j * GENE_SIZE + GENE_SIZE,
                                    i * GENE_SIZE + GENE_SIZE,
                                    fill=color)


def scroll_callback(event: tk.Event):
    print(event.delta)


def fitness(pop: np.ndarray):
    return np.sum(pop, axis=1)


def crossover(parent1, parent2):
    axis = rand.randint(1, len(parent1) - 2)
    return np.hstack((parent1[0:axis], parent2[axis:]))


def mutate(chromosome: np.ndarray):
    rand_pos1 = rand.randint(0, len(chromosome) - 1)
    rand_pos2 = rand.randint(0, len(chromosome) - 1)
    chromosome[rand_pos1], chromosome[rand_pos2] = chromosome[rand_pos2], chromosome[rand_pos1]


def select_elitism(pop: np.ndarray):
    sorted_fitness = np.sort(pop)[::-1]
    sorted_fitness = sorted_fitness.tolist()
    sorted_population = pop.tolist()
    sorted_population = [x for _, x in sorted(zip(sorted_fitness, sorted_population))]
    return np.asarray(sorted_population), 3


def init_algorithm():
    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()


def run():
    global num_generations, population, btn_start_simulation, canvas
    num_generations = int(entry_no_generations.get())
    mutation_probability = float(entry_mutation_probability.get()) / 100
    generation = 0
    max_secs = 2
    # execution_speed = max_secs * (1 - float(entry_spd_alg.get()) / 100)
    btn_start_simulation.config(state=tk.DISABLED)

    while generation < num_generations:
        print(f"{generation}")
        # selectie parinti
        sorted_population, num_elites = select_elitism(population)
        selected_parents = sorted_population[:num_elites]
        population = sorted_population[num_elites:]
        # incrucisare
        child1 = crossover(selected_parents[0], selected_parents[1])
        child2 = crossover(selected_parents[0], selected_parents[2])
        child3 = crossover(selected_parents[1], selected_parents[2])

        # mutatie
        children = np.asarray([child1, child2, child3])
        for child in children:
            r = rand.uniform(0, 1)
            if r <= mutation_probability:
                mutate(child)
        population = np.vstack((population, children))
        on_refresh()
        generation += 1

    btn_start_simulation.config(state=tk.ACTIVE)
    max_index = np.argmax(fitness(population))
    max_chromosome = population[max_index]
    print(fitness(population))
    print(max_index)
    text = str(fitness(population)[max_index])
    canvas.create_text((population.shape[1] + len(text)) * GENE_SIZE, max_index * GENE_SIZE, text=text, fill="white")

    for j in range(0, len(max_chromosome)):
        color = '#%02x%02x%02x' % (int((255 * max_chromosome[j]) / 99), 0, int((255 * max_chromosome[j]) / 99))
        canvas.create_rectangle(j * GENE_SIZE, max_index * GENE_SIZE, j * GENE_SIZE + GENE_SIZE,
                                max_index * GENE_SIZE + GENE_SIZE, fill=color)


def on_refresh():
    length = scroll_y.get()[1] - scroll_y.get()[0]
    y = scroll_y.get()[1] - length
    k = int(canvas.winfo_reqheight() * y)
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

lb_spd_alg = tk.Label(frame, text="Viteza algoritmului")
lb_spd_alg.pack(pady=8)
entry_spd_alg = tk.Entry(frame)
lb_spd_alg.pack()

# buttons
btn_generate_population = tk.Button(frame, text="Genereaza populatie", command=lambda: generate_population(
    canvas_frame,
    canvas,
    entry_dim_population.get(),
    entry_len_chromosome.get()
))
btn_generate_population.pack(pady=32)

btn_start_simulation = tk.Button(frame, text="Start simulatie", command=init_algorithm)
btn_start_simulation.pack(pady=8)

btn_refresh = tk.Button(frame, text="Refresh", command=on_refresh)
btn_refresh.pack(pady=8)

btn_download = tk.Button(frame, text="Descarca statistici", state=tk.DISABLED)
btn_download.pack(pady=16)


# frame.pack()
def init_program():
    global window
    window.mainloop()
