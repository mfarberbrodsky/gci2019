import argparse
from collections import deque

arg_parser = argparse.ArgumentParser(
    description="A simple unit converter created in Python for CCExtractor, Google Code-In 2019.",
    epilog="Example: \"UnitConverter.py 350 cm m\" will convert 3 centimeters to meters, which is 3.5.")
arg_parser.add_argument("value", type=float, help="Value to convert")
arg_parser.add_argument("src_unit", help="Source unit (to convert from)")
arg_parser.add_argument("dst_unit", help="Destination unit (to convert to)")
arg_parser.add_argument("--table", help="Conversion table to use (defaults to conversion_table.txt)",
                        default="conversion_table.txt")
args = arg_parser.parse_args()


def table_to_graph(table_path):
    """Parse the conversion table file provided by the user, and return it as a graph used later for pathfinding."""

    graph = {}  # Adjacency list
    with open(table_path) as f:
        for line in f:
            src_unit, dst_unit, ratio = line.strip().split(" ")

            if src_unit not in graph:
                graph[src_unit] = set()
            graph[src_unit].add((dst_unit, float(ratio)))

            if dst_unit not in graph:
                graph[dst_unit] = set()
            graph[dst_unit].add((src_unit, 1 / float(ratio)))

    return graph


def find_path(graph, src_unit, dst_unit):
    """Find a path between two units in the graph (using BFS), and return the total ratio"""
    if src_unit == dst_unit:
        return [src_unit]

    if src_unit not in graph:
        return None

    visited = {src_unit}
    queue = deque([(src_unit, [], 1)])  # Each item is in the format (current_unit, current_path, current_ratio)

    while queue:
        current, path, ratio = queue.popleft()
        visited.add(current)
        for neighbor in graph[current]:
            neighbor_unit, neighbor_ratio = neighbor
            if neighbor_unit == dst_unit:
                return ratio * neighbor_ratio
            if neighbor_unit in visited:
                continue
            queue.append((neighbor_unit, path + [current], ratio * neighbor_ratio))
            visited.add(neighbor_unit)

    return None  # In case no path was found


graph = table_to_graph(args.table)
path_ratio = find_path(graph, args.src_unit, args.dst_unit)
if path_ratio:
    print("{} {} is {} {}".format(args.value, args.src_unit, args.value * path_ratio, args.dst_unit))
else:
    print("Impossible to convert between {} and {} using the given conversion table.".format(args.src_unit,
                                                                                             args.dst_unit))
