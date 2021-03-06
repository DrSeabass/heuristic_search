"""
Random walk on heuristic search problems
"""

import math
import random

class RandomWalk():
    
    def __init__(self, problem_interface, seed=None):
        self.problem_interface = problem_interface
        self.seed = seed
        self.iterations = 0
        self.steps = []
        self.costs = []
        self.solutions = {}
        
        if self.seed:
            self.random = random.Random(seed)
        else:
            self.random = random.Random()

    def get_step(self, state):
        actions = self.problem_interface.get_actions(state)
        if actions:
            return self.random.choice(actions)
        return False

    def walk(self, index):
        state = self.problem_interface.initial_state()
        current_trace = []
        control_var = True
        total_cost = 0
        while control_var:
            if self.problem_interface.goal_p(state):
                self.steps.append(len(current_trace))
                self.costs.append(total_cost)
                self.solutions[index] = current_trace
                return True
            else:
                next_step = self.get_step(state)
                if next_step:
                    cost = self.problem_interface.apply_action(state, next_step)
                    current_trace.append(next_step)
                    total_cost += cost
                else:
                    self.steps.append(len(current_trace))
                    self.costs.append(math.inf)
                    return False
        return False

    def solve(self):
        iteration = 0
        solved = False
        while not self.walk(iteration):
            iteration += 1

        
        
