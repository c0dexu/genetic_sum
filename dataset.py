import json
import random as rand
from enum import Enum


class Size(Enum):
    SMALL = 10
    MEDIUM = 20
    LARGE = 50


def generate_dataset(factor: int, type: Size, index: int):
    max_weights = [45, 200, 1000]
    dir = ""
    datasets = []
    name_type = ""
    if type == Size.SMALL:
        name_type = "small"
        dir = "knapsack_instances/instances_small"
    elif type == Size.MEDIUM:
        name_type = "medium"
        dir = "knapsack_instances/instances_medium"
    elif type == Size.LARGE:
        name_type = "large"
        dir = "knapsack_instances/instances_large"

    for i, max_weight in enumerate(max_weights):
        print(i)
        f = open(dir + "/instance_" + name_type + "_" + str(i + index) + ".txt", "w+")
        no_objects = type.value
        ratio = max_weight / no_objects
        ratio *= factor
        objects = [int(rand.uniform(0, 1) * ratio) for _ in range(no_objects)]
        weights = [int(rand.uniform(0, 1) * ratio) for _ in range(no_objects)]
        stringified_objs = "[ "
        stringified_weights = "[ "

        for object in objects:
            stringified_objs += str(object) + " "
        stringified_objs += "]"

        for weight in weights:
            stringified_weights += str(weight) + " "
        stringified_weights += "]"

        f.write("no_objects = " + str(no_objects) + "\n")
        f.write("max_weight = " + str(max_weight) + "\n")
        f.write("weights = " + str(stringified_weights) + "\n")
        f.write("objects = " + str(stringified_objs))
        f.close()


    


