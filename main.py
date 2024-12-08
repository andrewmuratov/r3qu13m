import os
import time
import random

width, height = 20, 10
player_char = "i"
entity_char = "x"
item_char = "o"
collected_char = "x"
empty_space = "."
wall_char = "#"

player_pos = [random.randint(1, height - 2), random.randint(1, width - 2)]
entity_pos = [random.randint(1, height - 2), random.randint(1, width - 2)]
items_collected = []
item_parts = ["barrel", "trigger", "bullets"]
map_grid = []
entity_moves_per_turn = 1

color_reset = "\033[0m"
color_player = "\033[37m"
color_entity = "\033[31m"
color_item = "\033[33m"
color_wall = "\033[90m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_map():
    global map_grid
    map_grid = [[empty_space if random.random() > 0.2 else wall_char for _ in range(width)] for _ in range(height)]
    map_grid[player_pos[0]][player_pos[1]] = empty_space
    map_grid[entity_pos[0]][entity_pos[1]] = empty_space
    place_items()

def place_items():
    placed = 0
    while placed < len(item_parts):
        y, x = random.randint(1, height - 2), random.randint(1, width - 2)
        if map_grid[y][x] == empty_space:
            map_grid[y][x] = item_char
            placed += 1

def render_map():
    clear_screen()
    for y, row in enumerate(map_grid):
        row_str = ""
        for x, cell in enumerate(row):
            if [y, x] == player_pos:
                row_str += f"{color_player}{player_char}{color_reset}"
            elif [y, x] == entity_pos:
                row_str += f"{color_entity}{entity_char}{color_reset}"
            elif cell == item_char:
                row_str += f"{color_item}{item_char}{color_reset}"
            elif cell == wall_char:
                row_str += f"{color_wall}{wall_char}{color_reset}"
            else:
                row_str += cell
        print(row_str)
    print(f"\nItems collected: {', '.join(items_collected) if items_collected else 'None'}")
    print(f"\nControls: W = Up, A = Left, S = Down, D = Right, Q = Quit")

def move_entity():
    global entity_pos
    for _ in range(entity_moves_per_turn):
        y_diff = player_pos[0] - entity_pos[0]
        x_diff = player_pos[1] - entity_pos[1]
        move_y = 1 if y_diff > 0 else -1 if y_diff < 0 else 0
        move_x = 1 if x_diff > 0 else -1 if x_diff < 0 else 0

        if random.choice([True, False]):
            new_pos = [entity_pos[0] + move_y, entity_pos[1]]
        else:
            new_pos = [entity_pos[0], entity_pos[1] + move_x]

        if map_grid[new_pos[0]][new_pos[1]] != wall_char:
            entity_pos = new_pos
        if entity_pos == player_pos:
            break

def check_game_end():
    if player_pos == entity_pos:
        clear_screen()
        print(f"{color_entity}The entity has caught you. The void takes you.{color_reset}")
        time.sleep(3)
        return True
    if len(items_collected) == len(item_parts):
        clear_screen()
        print(f"{color_player}You assemble the weapon. A single shot ends your torment. You shot yourself{color_reset}")
        time.sleep(3)
        return True
    return False

generate_map()

while True:
    render_map()

    if check_game_end():
        break

    move = input("\nYour move: ").lower()
    if move == "q":
        print(f"{color_player}You gave up. The entity claims you.{color_reset}")
        break

    new_pos = player_pos[:]
    if move == "w":
        new_pos[0] -= 1
    elif move == "s":
        new_pos[0] += 1
    elif move == "a":
        new_pos[1] -= 1
    elif move == "d":
        new_pos[1] += 1
    else:
        print("Invalid input. Use W/A/S/D to move.")
        time.sleep(1)
        continue

    if 0 <= new_pos[0] < height and 0 <= new_pos[1] < width and map_grid[new_pos[0]][new_pos[1]] != wall_char:
        player_pos = new_pos

    if map_grid[player_pos[0]][player_pos[1]] == item_char:
        part = random.choice([p for p in item_parts if p not in items_collected])
        items_collected.append(part)
        map_grid[player_pos[0]][player_pos[1]] = empty_space
        print(f"{color_item}You found a {part}!{color_reset}")
        time.sleep(1)

    move_entity()
