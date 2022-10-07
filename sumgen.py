import numpy as np
import tkinter as tk
import random as rand
import re

population = []
WIDTH = 1024
HEIGHT = 512
GENE_SIZE = 4
num_genes = 0
num_generations = 0
is_generated = False

# '#%02x%02x%02x' % (0, 128, 64)

def validate_number(number):
    return re.match("^[0-9]+$", number)


def generate_population(canvas: tk.Canvas, dim, chromosome_length):
    global population, is_generated, btn_start_simulation
    if validate_number(dim) and validate_number(chromosome_length):
        population = np.random.uniform(size=(int(dim), int(chromosome_length)), low=0, high=99).astype("int32")
        canvas.delete("all")
        for i, chromozome in enumerate(population):
            for j, gene in enumerate(chromozome):
                canvas.create_rectangle(j * GENE_SIZE, i * GENE_SIZE, j * GENE_SIZE + GENE_SIZE,
                                        i * GENE_SIZE + GENE_SIZE,
                                        fill='#%02x%02x%02x' % (0, 0, int((255 * population[i, j]) / 99)))
        is_generated = True
        btn_start_simulation.invoke()



# init window
window = tk.Tk()
window.geometry(str(WIDTH) + "x" + str(HEIGHT))

# init canvas
win_percentage = .75
canvas = tk.Canvas(window, width=WIDTH * win_percentage, height=HEIGHT)
canvas.config(bg="black")
canvas.pack(side=tk.LEFT)

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
    canvas,
    entry_dim_population.get(),
    entry_len_chromosome.get()
))
btn_generate_population.pack(pady=32)

btn_start_simulation = tk.Button(frame, text="Start simulatie", state=tk.DISABLED)
btn_start_simulation.pack(pady=8)

# frame.pack()
window.mainloop()
