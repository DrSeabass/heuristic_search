class SearchInterface():

    def __init__(self, problem):
        pass

    def goal_p(self, state):
        """
        Does the supplied state represent a goal for the given search problem
        """
        raise NotImplementedError()

    def get_actions(self, state):
        """
        Per the domain, what actions can be taken from the supplied state.
        Returns the actions as a list
        """
        raise NotImplementedError()

    def key(self, state):
        """
        Returns a unique representation of the given state, suitable for use in hashtables
        """
        raise NotImplementedError()

    def cost_to_go(self, state):
        """
        Estimate of the cost of reaching a solution from the supplied state.
        Unless otherwise stated, assume an admissible (strictly underestimating) heuristic
        """
        raise NotImplementedError()

    def distance_to_go(self, state):
        """
        Estimate of the number of steps to reaching a solution from the supplied state.
        Unless otherwise stated, assume an admissible (strictly underestimating) heuristic
        """
        raise NotImplementedError()

    def expand(self,state):
        """
        Returns all states reachable by a single action from the given state
        """
        raise NotImplementedError()

    def initial_state(self):
        """
        Returns the starting state of the problem wrapped by the interface
        """
        raise NotImplementedError()

    def apply_action(self, state, action):
        """
        Applies an action to a state, mutating it into the state arrived at by that action
        From the graph perspective, this looks like:
        state -> action -> state'

        the cost of the action is returned
        """
        raise NotImplementedError()

    def undo_action(self, state, action):
        """
        Undoes an action in the same way as apply_action.
        The cost of taking the action is returned (the actual cost. not the negated cost)
        """
        raise NotImplementedError()

    def vailadte_solution(self, action_list, display=False):
        """
        Validates a solution against the problem
        Optionally, display the executed solution step by step

        Returns true when the solution is valid.  False otherwise
        """
        raise NotImplementedError()


if __name__ == "__main__":
    si = SearchInterface()
    print("Hello World!")
