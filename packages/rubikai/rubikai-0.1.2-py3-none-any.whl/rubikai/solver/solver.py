from rubikai.solver import search
from rubikai.cube.cube import Cube, Face, Action
import numpy as np
import pandas as pd


class CubeProblem(search.SearchProblem):
    """ a Problem class to be used with the search module """

    def __init__(self, cube, quarter_metric=True):
        """
        :param cube: a rubikai.cube.cube.Cube instance
        :param quarter_metric: if True, use 90 degrees rotations only.
                               otherwise use also 180 degrees.
        """
        self.cube = cube
        self.expanded = 0
        self.actions = []
        if quarter_metric:
            k_values = (-1, 1)
        else:
            k_values = (-1, 1, 2)
        for layer in range(self.cube.layers // 2):
            for k in k_values:
                self.actions += [Action(face, k, layer) for face in Face]

    def get_start_state(self):
        return self.cube.copy()

    def is_goal_state(self, cube):
        return cube.is_solved()

    def get_successors(self, cube):
        self.expanded += 1
        successors = []
        for action in self.actions:
            successor = cube.copy().rotate(
                action.face, action.k, action.layer)
            successors.append((successor, action, 1))
        return successors

    def get_cost_of_actions(self, actions):
        return len(actions)


def solve(cube, heuristic=lambda *args: 0, verbose=False):
    """
    solves a given cube instance
    :param cube: rubikai.cube.cube.Cube instance
    :param heuristic: a heuristic function for A* search.
                      takes a cube and problem instances as input and returns
                      a number.
                      by default, uses the null heuristic (0 for every state)
    :param verbose: if True, prints some information about the search
    :return: a list of actions that solves the cube
    """
    cube_problem = CubeProblem(cube)
    solution = search.a_star(cube_problem, heuristic)
    if verbose:
        solution_str = ' '.join([str(s) for s in solution])
        print('Length %d solution found:\n%s' %
              (len(solution), solution_str))
        print('Expanded %d nodes.' % cube_problem.expanded)
    return solution, cube_problem.expanded


def random_actions(cube, num_actions, quarter_metric=True):
    """
    returns a sequence of random actions on the given cube
    (does not apply the actions to the cube)
    :param cube: Cube object
    :param num_actions: an integer >= 1
    :param quarter_metric: whether to use the quarter-turn metric or not
    :return: a sequence of `num_actions' actions
    """
    assert num_actions >= 1, "there's no sense in less than 1 steps"
    cube_problem = CubeProblem(cube, quarter_metric)
    last_cube = cube.copy()
    visited = {last_cube.copy()}
    possible_actions = cube_problem.actions
    actions = [None] * num_actions
    actions[0] = np.random.choice(possible_actions)
    for i in range(1, num_actions):
        rand_action = np.random.choice(possible_actions)
        while last_cube.copy().apply([rand_action]) in visited:
            rand_action = np.random.choice(possible_actions)
        actions[i] = rand_action
        last_cube.apply([rand_action])
        visited.add(last_cube.copy())
    return actions


def switchable(a_1, a_2):
    """
    decide if 2 actions can be swapped.
    two actions are independent if they are on opposite faces or on the same
    face but on different layers.
    :param a_1: first action
    :param a_2: second action
    :returns True if switchable, False otherwise
    """
    opposite_faces = a_1.face.value + a_2.face.value == 5
    same_face = a_1.face.value == a_2.face.value
    diff_layers = a_1.layer != a_2.layer
    if opposite_faces:
        return a_1.face.value > a_2.face.value
    elif same_face and diff_layers:
        return a_1.layer > a_2.layer
    else:
        return False


def bubble_sort(actions):
    """ bubble sort actions were switching is between independent actions """
    exchanges = True
    pass_num = len(actions) - 1
    while pass_num > 0 and exchanges:
        exchanges = False
        for i in range(pass_num):
            if switchable(actions[i], actions[i + 1]):
                exchanges = True
                temp = actions[i]
                actions[i] = actions[i + 1]
                actions[i + 1] = temp
        pass_num = pass_num - 1
    return actions


def reduce_same_actions(actions):
    """ reduce a sequence of the same actions """
    reduced_actions = []
    i = 0
    while i < len(actions):
        curr_action_k = actions[i].k
        j = i + 1
        while j < len(actions) and \
                actions[i].face.value == actions[j].face.value and \
                actions[i].layer == actions[j].layer:
            curr_action_k += actions[j].k
            j += 1
        # end while
        curr_action_k %= 4
        if curr_action_k == 2:
            a = Action(actions[i].face, -1, actions[i].layer)
            reduced_actions.append(a)
            reduced_actions.append(a)
        elif curr_action_k != 0:
            a = Action(actions[i].face, curr_action_k, actions[i].layer)
            reduced_actions.append(a)
        # end if
        i = j
    # end while
    return reduced_actions


def reduce_sequence(actions):
    """
    two actions on the cube are independent if they don't affect the same faces,
    in this case we can change the order of the actions.
    we then can go over sequences of dependent action and change a series
    of action to shorter ones.
    """
    return reduce_same_actions(bubble_sort(actions))


def generate_random_sequence(cube_size, d):
    if d == 0:
        return []
    rand_actions = []
    happy = False
    while not happy:
        cube = Cube(cube_size)
        rand_actions = random_actions(cube, 2*d)
        rand_actions = reduce_sequence(rand_actions)
        happy = len(rand_actions) >= d
    return rand_actions[:d]


def compare_heuristics(heuristics, cube_layers, d_values,
                       iterations, verbose=False):
    """
    uses the given heuristics to solve multiple instances of scrambled cubes
    and gathers information on the solutions.

    :param heuristics: a dictionary where the key is the heuristic name and the
                       value is the heuristic function handle
    :param cube_layers: number of cube layers the heuristic operates on
    :param d_values: an array-like of integers specifying the number of
                     scramble moves to check
    :param iterations: number of iterations for each num. of scramble moves
    :param verbose: if True, prints information as the test goes
    :returns: pandas DataFrame with all the data gathered
    """

    # print only if verbose is True
    def vprint(*a, **kw):
        if verbose:
            print(*a, **kw)
    # end vprint
    # create a dataframe
    name_col = 'heuristic_name'
    d_col = 'num_scrambles'
    opt_col = 'is_optimal'
    exp_col = 'expansions'
    df = pd.DataFrame(columns=[name_col, d_col, opt_col, exp_col])

    for i in range(iterations):
        vprint('Iteration:', i, '\n')
        for d in d_values:
            # generate a random sequence of length d and scramble the cube
            rand_seq = generate_random_sequence(cube_layers, d)
            vprint('Generated sequence:', rand_seq, '(length %d)' % d)
            c = Cube(cube_layers)
            c.apply(rand_seq)
            # test each heuristic on the scrambled cube
            for h_name in heuristics:
                h = heuristics[h_name]
                solution, expansions = solve(c, h, verbose)
                df = df.append({
                    name_col: h_name,
                    d_col: d,
                    opt_col: len(solution) == d,
                    exp_col: expansions
                }, ignore_index=True)
                vprint()
            # end for
            vprint()
        # end for
        vprint()
    # end for
    return df
