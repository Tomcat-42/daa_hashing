import os
from enum import Enum
from typing import Any, Callable, Dict, List
from pprint import pprint as pp


# File parsing
from pyaon.hashing import (load)

# Algorithms
from pydaa.hashing import (open_addressing_hash_table,
                           separate_chaining_hash_table)

# Hash functions
from hash_functions import (modulo_hash, knuth_multiplicative_method_hash)

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
    # "identity": identity_hash,
    "modulo": modulo_hash,
    # "multiplication": multiplication_hash,
    # "left_shift": left_shift_hash,
    # "right_shift": right_shift_hash,
    # "add": add_hash,
    # "xor": xor_hash,
    # "minus": minus_hash,
    # "multiplicative_method": multiplicative_method_hash,
    "knuth_multiplicative_method": knuth_multiplicative_method_hash,
    # "murmur_hash3_x86_32": murmur_hash3_x86_32_hash,
    # "farm_hash": farm_hash_hash,
    # "city_hash": city_hash_hash,
}

hash_tables = {
    "open_addressing": open_addressing_hash_table,
    "separate_chaining": separate_chaining_hash_table,
}


class Operation(Enum):
    INSERT = "insert"
    SEARCH = "search"


def build_hash_tables(
    data_sizes: List[int], hash_tables: Dict[str, Callable[..., Any]],
    hash_functions: Dict[str, Callable[[int], Callable[[int], int]]]
) -> Dict[str, Dict[str, Dict[int, Any]]]:
    constructed_hash_tables = {}

    for table_type, table_constructor in hash_tables.items():
        constructed_hash_tables[table_type] = {}

        for hash_func_name, hash_func_constructor in hash_functions.items():
            constructed_hash_tables[table_type][hash_func_name] = {}

            for data_size in data_sizes:
                hash_func = hash_func_constructor(500)
                table = table_constructor(500, hash_func)
                constructed_hash_tables[table_type][hash_func_name][
                    data_size] = table

    return constructed_hash_tables


# process_data function
def process_data(
        data: List[Dict[str, Any]], hash_tables: Dict[str, Callable[..., Any]],
        hash_functions: Dict[str, Callable[[int], Callable[[int], int]]],
        constructed_hash_tables: Dict[str, Dict[str, Dict[int, Any]]],
        operation: Operation) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    results: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}

    for table_type, table_constructor in hash_tables.items():
        results[table_type] = {}

        for hash_func_name, hash_func_constructor in hash_functions.items():
            results[table_type][hash_func_name] = []

            for data_entry in data:
                print(
                    f"Processing {table_type} {hash_func_name} {data_entry['size']} on {operation.value}"
                )
                table_size = data_entry["size"]
                table = constructed_hash_tables[table_type][hash_func_name][
                    table_size]

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


# Build hash tables for all combinations of table type, hash function, and data size
constructed_hash_tables = build_hash_tables(
    [entry["size"] for entry in data_build], hash_tables, hash_functions)

# Generate output
# output = {
#     "build":
#     process_data(data_build,
#                  hash_tables,
#                  hash_functions,
#                  constructed_hash_tables,
#                  operation=Operation.INSERT),
#     "search":
#     process_data(data_search,
#                  hash_tables,
#                  hash_functions,
#                  constructed_hash_tables,
#                  operation=Operation.SEARCH),
# }

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
# pp(output)
plot_results(output)
