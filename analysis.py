import os
from enum import Enum
from typing import Any, Callable, Dict, List

# File parsing
from pyaon.hashing import (load)

# Algorithms
from pydaa.hashing import (open_addressing_hash_table,
                           separate_chaining_hash_table)

# Hash functions
from hash_functions import (identity_hash, modulo_hash, multiplication_hash,
                            left_shift_hash, right_shift_hash, add_hash,
                            xor_hash, minus_hash, multiplicative_method_hash,
                            knuth_multiplicative_method_hash,
                            murmur_hash3_x86_32_hash, farm_hash_hash,
                            city_hash_hash)

# Visualizations
from picods import (picoplot, picotable)

import matplotlib.pyplot as plt

import json

# Read data
data_build = list(
    sorted(
        map(
            lambda x: {
                "size": int("".join(filter(str.isdigit, x))),
                "data": load(f"./data/build/{x}"),
            },
            os.listdir("data/build"),
        ),
        key=lambda x: x["size"],
    ))

data_search = list(
    sorted(
        map(
            lambda x: {
                "size": int("".join(filter(str.isdigit, x))),
                "data": load(f"./data/search/{x}"),
            },
            os.listdir("data/search"),
        ),
        key=lambda x: x["size"],
    ))

# Hash functions factory
# For each hash function, we want to generate a hash function for each table size
# e.g. hash_functions["multiplicative_method"](table_size)(key) will return the hash value for the key
hash_functions = {
    "identity": identity_hash,
    "modulo": modulo_hash,
    "multiplication": multiplication_hash,
    "left_shift": left_shift_hash,
    # "right_shift": right_shift_hash,
    # "add": add_hash,
    # "xor": xor_hash,
    # "minus": minus_hash,
    "multiplicative_method": multiplicative_method_hash,
    "knuth_multiplicative_method": knuth_multiplicative_method_hash,
    "murmur_hash3_x86_32": murmur_hash3_x86_32_hash,
    "farm_hash": farm_hash_hash,
    "city_hash": city_hash_hash,
}

# Results construction
## I have 2 types of hash maps: open addressing and separate chaining, which I construct with: *_hash_table(table_size: int, hash_function: Callable[[int], int])
## I have multiple hash functions. I construct them with: hash_functions["hash_function_name"](table_size: int) -> Callable[[int], int]
## I have 2 types of data: data_build and data_search. Each entry in this list is a dictionary with 2 keys: "size" and "data". "size" is the size of the hash table, and "data" is the data to be inserted/searched.
## I have 2 types of operations: insert and search. both methods return (inserion: bool, time: int, comparisons: int)

# I want a output like this:
# output = {
#     "build": {
#         "open_addressing": {
#             "identity": [{"size": 100, "time": 0.001, "comparisons": 40}, ..., {"size": 1000, "time": 0.001, "comparisons": 40}],
#             ...,
#             "city_hash": {"""}
#         },
#         "separate_chaining": {"""},
#     },
#     "search": {"""},
# }

# some info:
# data_build and data_search have the same size and looks like [{"size": 50, "data": [1, 2, 3, 4, 5]}, ...]
# the output should be a dictionary with 2 keys: "build" and "search"
# output["build"] and output["search"] should be a dictionary with 2 keys: "open_addressing" and "separate_chaining"
# output["build"]["open_addressing"] and output["build"]["separate_chaining"] should be a dictionary with 12 various keys (hash function names)
# output["build"]["open_addressing"]["identity"] should be a list of dictionaries with 3 keys: "size", "time", "comparisons"
# The key "size" should be the same as the key "size" in data_build and data_search
# The key "time" should be the time it took to insert/search all the data in data_build and data_search
# The key "comparisons" should be the number of comparisons it took to insert/search all the data in data_build and data_search
# "time" and "comparisons" are obtained by calling the insert/search methods on the hash table constructed with the hash function and the data

# now, implements the code to generate the output. show me only new code, not the code I gave you.


class Operation(Enum):
    INSERT = "insert"
    SEARCH = "search"


def process_data(
        data: List[Dict[str, Any]], hash_tables: Dict[str, Callable[..., Any]],
        hash_functions: Dict[str, Callable[[int], Callable[[int], int]]],
        operation: Operation) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    results: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}

    for table_type, table_constructor in hash_tables.items():
        results[table_type] = {}

        for hash_func_name, hash_func_constructor in hash_functions.items():
            results[table_type][hash_func_name] = []

            for data_entry in data:
                table_size = data_entry["size"]
                hash_func = hash_func_constructor(table_size)
                table = table_constructor(table_size, hash_func)

                total_time = 0
                comparisons = 0

                for key in data_entry["data"]:
                    if operation == Operation.INSERT:
                        _, (time, comp) = table.insert(key)
                    else:
                        _, (time, comp) = table.search(key)

                    comparisons += comp
                    total_time += time

                results[table_type][hash_func_name].append({
                    "size":
                    table_size,
                    "time":
                    total_time,
                    "comparisons":
                    comparisons
                })

    return results


hash_tables = {
    "open_addressing": open_addressing_hash_table,
    "separate_chaining": separate_chaining_hash_table,
}

output = {
    "build":
    process_data(data_build,
                 hash_tables,
                 hash_functions,
                 operation=Operation.INSERT),
    "search":
    process_data(data_search,
                 hash_tables,
                 hash_functions,
                 operation=Operation.SEARCH),
}


def save_results(output: Dict[str, Dict[str, Dict[str, List[Dict[str,
                                                                 Any]]]]]):
    with open("results.json", "w") as f:
        json.dump(output, f)


def load_results() -> Dict[str, Dict[str, Dict[str, List[Dict[str, Any]]]]]:
    with open("results.json", "r") as f:
        return json.load(f)


print("saving results")
# save_results(output)
print("results saved")
output = load_results()


def plot_results(output: Dict[str, Dict[str, Dict[str, List[Dict[str,
                                                                 Any]]]]]):
    for operation in output:
        for table_type in output[operation]:
            # Collect data for all hash functions to plot them in a single chart
            x_values_list = []
            y_time_values_list = []
            y_comparisons_values_list = []

            for hash_func_name in output[operation][table_type]:
                x_values = [
                    entry["size"]
                    for entry in output[operation][table_type][hash_func_name]
                ]
                time_values = [
                    entry["time"]
                    for entry in output[operation][table_type][hash_func_name]
                ]
                comparisons_values = [
                    entry["comparisons"]
                    for entry in output[operation][table_type][hash_func_name]
                ]

                x_values_list.append(x_values)
                y_time_values_list.append(time_values)
                y_comparisons_values_list.append(comparisons_values)

            hash_func_names = list(hash_functions.keys())

            # Plot time vs size
            picoplot(
                f"{operation.capitalize()} Time vs Size ({table_type.replace('_', ' ').capitalize()})",
                x_values_list,
                y_time_values_list,
                hash_func_names,
                plt.cm.tab10.colors,  # Default matplotlib color cycle
                "Size",
                "Tim")

            # Plot comparisons vs size
            picoplot(
                f"{operation.capitalize()} Comparisons vs Size ({table_type.replace('_', ' ').capitalize()})",
                x_values_list,
                y_comparisons_values_list,
                hash_func_names,
                plt.cm.tab10.colors,  # Default matplotlib color cycle
                "Size",
                "Comparisons")

            # Create table for each hash function
            for i, hash_func_name in enumerate(hash_func_names):
                table_data = [
                    x_values_list[i], y_time_values_list[i],
                    y_comparisons_values_list[i]
                ]

                # Transpose the table_data
                table_data_transposed = list(map(list, zip(*table_data)))

                picotable(
                    f"{operation.capitalize()} - {table_type.replace('_', ' ').capitalize()} - {hash_func_name}",
                    table_data_transposed, ["Size", "Time", "Comparisons"],
                    [f"Data {j+1}" for j in range(len(x_values_list[i]))],
                    round_digits=2,
                    color="#1ea5c1")


# Call the plot_results function with the output dictionary
plot_results(output)
