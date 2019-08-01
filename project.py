import sys

open_goals = []
achievable = []
operators = []
sequence = []
initial = []


class Operator:
    def __init__(self, name, pre, delete, add, bindings):
        self.name = name
        self.pre = pre
        self.delete = delete
        self.add = add
        self.bindings = bindings


def parse_file(filename):
    global initial
    global x, planet
    with open(filename, 'r') as file:
        line = file.readline()  # This line should say GOAL:
        line = file.readline()
        while "  " in line.rstrip():
            # Add the goals to the appropriate list
            open_goals.append(line.replace('(', ' ').replace(',', ' ').replace(')', "").split())
            line = file.readline()

        line = file.readline()  # This line should say INITIAL:
        line = file.readline()
        while "  " in line.rstrip():
            # Add the initial conditions to the appropriate list
            achievable.append(line.replace('(', ' ').replace(',', ' ').replace(')', "").split())
            line = file.readline()

        bindings = []
        while line:
            if line.strip() == "NAME:":
                line = file.readline()
                # name stored as a list, first item being the name, and the rest are parameters
                name = line.replace('(', " ").replace(')', "").replace(',', " ").split()
                if len(name) > 1:
                    bindings.extend(name[1:])
                line = file.readline()  # This line should say PRE:
                line = file.readline()
                pre = []
                while "  " in line.rstrip():
                    # store preconditions for an operator
                    pre.append(line.replace('(', ' ').replace(',', ' ').replace(')', "").split())
                    line = file.readline()
                line = file.readline()
                delete = []
                while "  " in line.rstrip():
                    # store deletes for an operator
                    delete.append(line.replace('(', ' ').replace(',', ' ').replace(')', "").split())
                    line = file.readline()
                line = file.readline()
                add = []
                while "  " in line.rstrip():
                    # store adds for an operator
                    add.append(line.replace('(', ' ').replace(',', ' ').replace(')', "").split())
                    line = file.readline()
                # Add operator object to appropriate list
                operators.append(Operator(name, pre, delete, add, list(bindings)))
                bindings.clear()
            line = file.readline()

    # print(open_goals)
    # print(achievable)
    # for op in operators:
    #     print(op.add)
    initial = list(achievable)


def check_goals(a):
    for goal in open_goals:
        if a[0] == goal[0] and len(a) == len(goal):
            for i, arg in enumerate(a):
                if goal[i] == "WARM" or goal[i] == "LOW" or goal[i] == "DEEPSPACE":
                    if not arg.isupper():
                        return ""
                    if arg != goal[i]:
                        return ""
            return goal

    return ""


def plan():
    global open_goals
    global achievable
    global operators
    global sequence

    sorted_goals = list(open_goals)
    sorted_goals.sort()
    initial.sort()
    if len(open_goals) == 0 or sorted_goals == initial:
        print("SUCCESS")
        print()
        return 1
    else:
        matches = []
        for op in operators:
            matches.clear()
            for a in op.add:
                # see if the add condition matches a goal
                matching_goal = check_goals(a)
                if not matching_goal:
                    matches.clear()
                    break
                else:
                    matches.append(matching_goal)
            if matches:
                sequence.append(op)
                break

        if matches:  # all of the ADDS match a goal
            binds = list(op.bindings)
            # update Achievable with the correct bindings
            for i, a in enumerate(op.add):
                for j, bind in enumerate(a[1:]):
                    # print(op.bindings)
                    if bind in op.bindings:
                        pos = op.bindings.index(bind)
                    else:
                        pos = -1

                    # store the binding for later use
                    if pos != -1:
                        binds[pos] = matches[i][j + 1]

            # add to achievable
            new_achieve = [x for x in matches if x not in achievable]
            achievable.extend(new_achieve)
            new_goals = [x for x in open_goals if x not in matches]
            open_goals.clear()
            open_goals.extend(new_goals)

            # append PRE to open_goals
            to_append = []
            for p in op.pre:
                to_append.append(p[0])
                for arg in p[1:]:
                    if arg in op.bindings:
                        to_append.append(binds[op.bindings.index(arg)])
                    else:
                        if arg == "planet":
                            to_append.append(achievable[len(achievable) - 2][2])
                        else:
                            to_append.append(arg)
                if to_append in open_goals:
                    to_append.clear()
                    continue

                open_goals.append(list(to_append))
                to_append.clear()

            print("goals", open_goals)
            print("operation", sequence[len(sequence) - 1].name)
            print("achievable", achievable)
            print()
            return 0

        else:
            print("FAILURE")
            exit(0)


def write_story(x, planet):
    print(x + "'s Journey:")

    for op in sequence:
        if "TakeOff" in op.name:
            print(x + " needed to take off from EARTH.")
            print("Because " + x + " was on EARTH, he/she was able to takeoff,\nand he/she was not on EARTH anymore.")
            print()
            continue
        if "GoFaster" in op.name:
            print(x + " needed to go faster.")
            print("Because " + x + " was in orbit and " + x + " was at LOW speed, " +
                  "he/she was able to go faster,\nand he/she was not at LOW speed anymore.")
            print()
            continue
        if "FireRockets" in op.name:
            print(x + " needed to fire the rockets towards " + planet + ".")
            print("Because " + x + " was in space and " + x + " was at HIGH speed and " + x +
                  " was moving towards DEEPSPACE, he/she was able to fire the rockets,\n" +
                  "and he/she was not moving towards DEEPSPACE anymore.")
            print()
            continue
        if "AdjustToLand" in op.name:
            print(x + " needed to adjust to land on " + planet + ".")
            print("Because " + x + " was in space and " + x + " was moving towards " + planet + " and " +
                  x + " was at HIGH speed, he/she was able to adjust to land,\nand he/she was not at HIGH speed anymore "
                  "and he/she was not moving towards " + planet + " anymore.")
            print()
            continue
        if "LandOn" in op.name:
            print(x + " needed to land on " + planet + ".")
            print("Because " + x + " was near " + planet + " and " + x + " was at LOW speed, he/she was able to land," +
                  "\nand he/she was not near " + planet + " anymore and he/she was not at LOW speed anymore.")
            print()
            continue
        if "WarmTheFluid" in op.name:
            print(x + " needed to warm the fluid.")
            print("Because " + x + " landed on " + planet + " and the fluid was COLD, he/she was able to warm the fluid"
                  + ",\nand the fluid was not COLD anymore.")
            print()
            continue
        else:
            print("Step skipped")
            print()


if __name__ == '__main__':
    parse_file("operators.txt")
    x = open_goals[0][1]
    planet = open_goals[0][2]
    done = 0
    while not done:
        done = plan()

    # plan()
    # plan()
    # plan()
    # plan()
    # plan()
    # plan()
    # plan()

    sequence.reverse()
    print("Correct sequence of operations:")
    for op in sequence:
        print(op.name)

    print("")

    write_story(x, planet)
