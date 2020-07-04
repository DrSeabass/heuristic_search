
class Node():
    """
    Node representation in a search tree / graph
    We rely on parent pointers and actions to reconstruct solutions once the problem is solved
    """
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.cost = 0
        self.action = action
        self.parent = parent
        if action:
            self.cost += action.cost
        if parent:
            self.cost += parent.cost

    def get_solution(self):
        path = []
        node = self
        while (node.parent != None):
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path

class BreadthFirstSearch():
    """
    Breadth first search
    """
    def __init__(self, problem_interface):
        self.problem_interface = problem_interface
        self.steps = 0
        self.solutions = {}


    def solve(self):
        queue = [Node(self.problem_interface.initial_state())]
        seen = {}
        duplicates = 0
        while(queue != []):
            self.steps += 1
            node = queue[0]
            queue = queue[1:]
            key_val = self.problem_interface.key(node.state)
            if (self.steps % 1000) == 0:
                print("Step {} Duplicates {} In Queue : {}".format(self.steps, duplicates, len(queue)))
            if key_val in seen:
                duplicates += 1
                continue
            seen[key_val] = node.cost
            if self.problem_interface.goal_p(node.state):
                self.solutions[0] = node.get_solution()
                self.costs = [node.cost]
                return
            for action in self.problem_interface.get_actions(node.state):
                child_state = node.state.copy()
                cost = self.problem_interface.apply_action(child_state, action)
                child = Node(child_state, action, node)
                queue.append(child)
        print("Exhausted queue without finding solution.  Problem unsolvable.")    
