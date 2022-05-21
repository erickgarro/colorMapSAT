import json
import os
import random
import datetime
import platform
import sys

from flask import Flask, render_template, send_from_directory, json
from subprocess import Popen
from subprocess import PIPE

gbi = 0
varToStr = ["invalid"]

def generate_random_unique_colors(n_colors):
    """
    Generate random hex colors for each node
    :param n_colors:  the number of colors to generate
    :return:        a array of hex colors
    """
    colors = []
    for c1 in range(n_colors):
        color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        for c2 in range(n_colors):
            if c1 == c2:
                color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        colors.append(color)
    return colors


def printClause(cl):
    print(map(lambda x: "%s%s" % (x < 0 and eval("'-'") or eval("''"), varToStr[abs(x)]), cl))


def varName(node, color):
    return "incolor({},{})".format(node, color)


def gvi(name):
    global gbi
    global varToStr
    gbi += 1
    varToStr.append(name)
    return gbi


def gen_vars(nodes, colors):
    varMap = {}

    # Insert here the code to add mapping from variable numbers to readable variable names.
    # For example, varMap[0] = "incolor(0,0)"
    for n in range(len(nodes)):
        for c in range(colors):
            name = varName(n, c)
            varMap[name] = gvi(name)
    return varMap


def genColConstr(nodes, colors, vars):
    clauses = []

    # Each node gets assigned one color
    for n in range(len(nodes)):
        clauses.append([vars[varName(n, c)] for c in range(colors)])

    # Neighbor nodes have different colors
    for n in range(len(nodes)):
        for c in range(colors):
            for n2 in nodes[n]:
                clauses.append([-vars[varName(n, c)], -vars[varName(n2, c)]])

    return clauses


# A helper function to print the cnf header
def printHeader(n):
    global gbi
    return "p cnf {} {}".format(gbi, n)


# A helper function to print a set of clauses cls
def printCnf(cls):
    return "\n".join(map(lambda x: "%s 0" % " ".join(map(str, x)), cls))


def to_int(string_array):
    """
    This methdod tries to convert a list of strings to a list of integers
    :param string_array:    a list of strings
    :return:                a list of integers, or a list of strings if the conversion fails
    """
    for i in range(len(string_array)):
        string_array[i] = int(string_array[i])
    return string_array


def write_dict_to_csv(_filename, _dict):
    """
    Write a dictionary to a CSV file
    :param _filename:  the filename without extension
    :param _dict:      the nodes dictionary
    """
    global f
    with open(_filename.lower() + ".csv", "w") as f:
        for key in _dict.keys():
            f.write(str(key) + "," + str(_dict[key])[1:-1].replace(" ", "").replace("'", "") + "\n")
    f.close()


def read_dict_from_csv(_filename):
    """
    Read a dictionary from a CSV file
    :param _filename:   the filename without extension
    :return:            the nodes' dictionary, either ints or strings
    """
    global f
    nodes = {}
    with open(_filename + ".csv", "r") as f:
        for line in f:
            line = line.replace("\n", "").split(",")

            try:
                line = to_int(line)
                nodes[line[0]] = line[1:]
            except:
                nodes[line[0]] = line[1]

    f.close()
    return nodes


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/<filename>')
def data(filename):
    return send_from_directory('static', filename)


@app.route('/<country>/<colors>')
def run_sat(country, colors):  # put application's code here
    # if not (os.path.isfile(SATsolver) and os.access(SATsolver, os.X_OK)):
    # if Z3 is installed with homebrew in the PATH env no need to explicitly specify the solver

    # --> Uncomment these two lines just once to convert a graphs to CSV files <-- #
    # write_dict_to_csv('us' + '_nodes', nodes_graph)
    # write_dict_to_csv('us' + '_nodes_ids', us)

    nodes_graph = read_dict_from_csv(country + '_nodes')
    nodes_ids = read_dict_from_csv(country + '_nodes_ids')
    colors = int(colors)

    varMap = gen_vars(nodes_graph, colors)
    rules = genColConstr(nodes_graph, colors, varMap)

    head = printHeader(len(rules))
    rls = printCnf(rules)

    timestamp = str(datetime.datetime.now().timestamp()).replace(".", "")

    # here we create the cnf file for SATsolver
    fl = open(country + "_" + str(colors) + "_colors" + "_" + timestamp + ".cnf", "w")
    fl.write("\n".join([head, rls]))
    fl.close()

    z3_build = sys.path[0] + '/' + './z3_linux ' + sys.path[0] + '/'
    if platform.system() == 'Darwin':
        z3_build = sys.path[0] + '/' + './z3_mac ' + sys.path[0] + '/'


    # this is for running SATsolver
    cmd = z3_build + country + "_" + str(colors) + "_colors" + "_" + timestamp + ".cnf"
    ms_out = Popen([cmd], stdout=PIPE, shell=True).communicate()[0]

    # SATsolver with these arguments writes the solution to a file called "solution".  Let's check it
    res = ms_out.decode('utf-8')

    # Print output
    print(res)
    res = res.strip().split('\n')
    solutions = {}
    facts_solutions = []

    nodes_colors = []
    # if it was satisfiable, we want to have the assignment printed out
    if res[0] == "s SATISFIABLE":
        # First get the assignment, which is on the second line of the file, and split it on spaces
        # Read the solution
        asgn = map(int, res[1].split()[1:])
        # Then get the variables that are positive, and get their names.
        # This way we know that everything not printed is false.
        # The last element in asgn is the trailing zero and we can ignore it

        # Convert the solution to our names
        facts = map(lambda x: varToStr[abs(x)], filter(lambda x: x > 0, asgn))
        # facts_solutions = []

        nodes_colors = [0] * colors
        for c in range(colors):
            nodes_colors[c] = []

        for f in facts:
            print(f)
            facts_solutions.append(f)
            f = f.replace('incolor(', '')
            f = f.replace(')', '').split(',')
            node_name = nodes_ids[int(f[0])]
            nodes_colors[int(f[1])].append(node_name)

        # remove empty indexes in nodes_colors
        nodes_colors = [x for x in nodes_colors if x]
        solutions['facts'] = facts_solutions
        solutions['nodesColor'] = nodes_colors
        solutions['hexColors'] = generate_random_unique_colors(len(nodes_colors))

    # elif res[0] == "s UNSATISFIABLE":
    else:
        nodes_names = []
        solutions['facts'] = []
        for val in nodes_ids.values():
            nodes_names.append(val)
        nodes_colors = [nodes_names]
        solutions['hexColors'] = []
        solutions['hexColors'].append('#a8a8a8')
    # else:
    #     solutions['facts'] = facts_solutions
    #     solutions['nodesColor'] = nodes_colors
    #     solutions['hexColors'] = generate_random_unique_colors(len(nodes_colors))

    # read cnf file
    with open(country + "_" + str(colors) + "_colors" + "_" + timestamp + ".cnf", "r") as f:
        lines = f.readlines()
    f.close()

    #read topology json file
    sys.path.insert(1, "../static/")
    with open(country + "-all.geo.json", "r") as f:
        topology = json.load(f)
    f.close()

    solutions['data'] = nodes_colors
    solutions['country'] = country
    solutions['colors'] = colors
    solutions['sat'] = res
    solutions['cnf'] = lines
    solutions['topology'] = topology

    # save solutions to disk in static folder
    filename = "sol_" + country + "_" + str(colors) + "_" + timestamp + ".json"
    with open(filename, "w") as f:
        json.dump(solutions, f)
    f.close()

    # cleanup CNF
    os.remove(country + "_" + str(colors) + "_colors" + "_" + timestamp + ".cnf")

    return render_template('map-viewer.html', country=country, colors=colors, timestamp=timestamp)


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)

# add event listener in html
