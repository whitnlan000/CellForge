import sys, pygame, lark
import random
import os, re
import cellular_automata as ca
import startup
import numpy as np

width, height = startup.run()
grid_list = [height, width]

print("YAHAH1A")
#os.chdir("Main")
# Get a cell's neighbors
def get_neighbors(arr, x, y, radius):
    h, w = arr.shape

    y_indices, x_indices = np.ogrid[:h, :w]

    dy = np.abs(y_indices - y)
    dx = np.abs(x_indices - x)

    mask = (dy <= radius) & (dx <= radius) & ~((dy == 0) & (dx == 0))

    values = arr[mask]
    coords = np.column_stack(np.where(mask))

    return values, coords




os.environ['SDL_AUDIODRIVER'] = 'dsp'


# Parse a non-header line
def parse_line(rule_text, replacements):
    if "if" not in rule_text:
        return False

    cond = rule_text.split("if", 1)[1].split("end", 1)[0].strip()

    print(replacements)
    for k, v in replacements.items():
        cond = cond.replace(k, v)

    print("Evaluating:", cond)

    try:
        result = eval(cond)
    except Exception as e:
        print("Eval error:", cond, e)
        return False

    return bool(result)




# Tree_To_Dict
def tree_to_dict(node):
    if isinstance(node, lark.Tree):
        return {
            node.data: [tree_to_dict(child) for child in node.children]
        }

    elif isinstance(node, lark.Token):
        return node.value

    else:
        return str(node)


original_grammar = lark.Lark("""
    start:header*

    header:label "{" content* "}" 
    label: IDENTIFIER
    IDENTIFIER: /[A-Za-z_][A-Za-z0-9_]*/

    content: /[^;{}]+/ ";"

    %import common.WS
    %ignore WS
""")

line_grammar = lark.Lark("""
    start: line+

    line: assignment if_clause

    assignment: target "=" value

    target: current
        | form

    value: form
        | neighbors
        | coords
        | MATH

    current: "$"
    form: "!" IDENTIFIER

    neighbors: "`" IDENTIFIER radius?
    radius: "@" MATH

    coords: "[" MATH "," MATH "]"

    if_clause: "if" LOGIC "end"
    LOGIC: /[^;]+(?=end)/


    condition: (neighbors | MATH) comp (neighbors | MATH)
    comp: "==" | "!=" | "<" | "<=" | ">" | ">="

    MATH: /[^);]+/

    IDENTIFIER: /[A-Za-z_][A-Za-z0-9_]*/

    %import common.WS
    %ignore WS
""")

search_dir = '.'
target_file_name = 'script.txt'
matching_files = []

for root, dirs, files in os.walk(search_dir):
    if target_file_name in files:
        full_path = os.path.join(root, target_file_name)
        matching_files.append(full_path)

for file_path in matching_files:
    print(file_path)


headers = original_grammar.parse(open(file_path).read())


varis = {"`form2": "3"}

#Rule headers
parsed_rules = []

for header in headers.find_data("header"):
    label = header.children[0].children[0]  # header name

    if label.lower() == "rules":
        for content in header.find_data("content"):
            rule_text = content.children[0]
            parsed_rules.append((rule_text, line_grammar.parse(rule_text)))


compiled_rules = []
for rule_text, rule in parsed_rules:
    assignments = list(rule.find_data("assignment"))

    compiled_rules.append((rule_text, assignments))


print("rules",compiled_rules)
#State Header
state_list = []

for header in headers.find_data("header"):
    label = header.children[0].children[0]

    if label.lower() == "states":
        for content in header.find_data("content"):
            state_name = content.children[0].strip()
            state_list.append(state_name)


#Grid Header


print("states",state_list)
ca.array = np.full((int(grid_list[0]),int(grid_list[1])), state_list[0], dtype=object)
pygame.init()

width = int(grid_list[0]) * 10
height = int(grid_list[1]) * 10

print("Creating window:", width, height)

ca.SCREEN = pygame.display.set_mode((width, height), pygame.RESIZABLE)
x0, y0 = 4, 4  # y=row, x=col


"""
ca.array[11][10] = "wire_off"
ca.array[11][14] = "wire_off"

ca.array[10][10] = "wire_delay"  # .
ca.array[10][11] = "wire_delay"  # .
ca.array[10][12] = "wire_on"  # .
ca.array[10][13] = "wire_off"  # .
ca.array[10][14] = "wire_off"  # .

ca.array[12][10] = "wire_off"  # .
ca.array[12][11] = "wire_off"  # .
ca.array[12][12] = "wire_off"  # .
ca.array[12][13] = "wire_off"  # .
ca.array[12][14] = "wire_off"  # .

ca.array[13][12] = "or"  # .
ca.array[14][12] = "wire_off"  # .


#ca.array[9][12] = "or"  # .
ca.array[8][12] = "wire_off"  # .
"""


tick_number = 0
def ticker():
    global tick_number

    pygame.time.Clock().tick(60)
    ca.tick()

    temp_array = ca.array.copy()

    rows, cols = ca.array.shape

    tick_number += 1

    if tick_number % 10 == 0:
        for row in range(rows):
            for col in range(cols):

                vals, coords = get_neighbors(
                    ca.array,
                    col,   # x
                    row,   # y
                    1
                )

                varis = {}

                

                for rule_text, assignments in compiled_rules:
                    #print(row,col)

                    fixed_text = rule_text
                    #fixed_text = fixed_text.replace("y",str(col))


                    coord_matches = re.findall(r"\[([^,]+),([^,]+)\]", fixed_text)


                    for x_str, y_str in coord_matches:

                        x_val, y_val = eval(x_str.replace("x",str(row)).replace("y",str(col))), eval(y_str.replace("y",str(col)).replace("x",str(row)))
                        x_str, y_str = x_str.replace("x",str(row)).replace("y",str(col)), y_str.replace("y",str(col)).replace("x",str(row))

                        if 0 <= y_val < ca.array.shape[0] and 0 <= x_val < ca.array.shape[1]:
                            cell_value = ca.array[y_val][x_val]

                            for state in state_list:
                                varis[f"[{x_str},{y_str}]"] = f"'{cell_value}'"

                    #print("JJSJS:" ,eval(y_str))

                    varis["x"] = str(row)
                    varis["y"] = str(col)
                    varis["$"] = "'"+str(temp_array[row][col])+"'"


                    radius_matches = re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)@(\d+)", rule_text)

                    for state, rad_str in radius_matches:
                        rad = int(rad_str)

                        vals_r, _ = get_neighbors(ca.array, col, row, rad)
                        count_r = np.sum(vals_r==state)
                        varis[f"`{state}@{rad}"] = str(count_r)
                        #print(f"`{state}@{rad}",str(count_r))



                    for assignment in assignments:

                        target_node = assignment.children[0]
                        value_node = assignment.children[1]

                        target_form = None
                        for f in target_node.find_data("form"):
                            target_form = str(f.children[0])

                        value_form = None
                        for f in value_node.find_data("form"):
                            value_form = str(f.children[0])

                        if (
                            ca.array[row][col] == target_form
                            and parse_line(rule_text, varis)
                        ):
                            temp_array[row][col] = value_form

        ca.array = temp_array
        print("done")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ticker()