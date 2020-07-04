class SearchInterface():

    def __init__(self, problem):
        pass

    def goal_p(self, state):
        raise NotImplementedError()

    def get_actions(self, state):
        raise NotImplementedError()

    def key(self, state):
        raise NotImplementedError()

    def cost_to_go(self, state):
        raise NotImplementedError()

    def distance_to_go(self, state):
        raise NotImplementedError()

    def expand(self,state):
        raise NotImplementedError()

    def initial_state(self):
        raise NotImplementedError()

    def apply_action(self, state, action):
        raise NotImplementedError()

    def undo_action(self, state, action):
        raise NotImplementedError()

    def vailadte_solution(self, action_list):
        raise NotImplementedError()


if __name__ == "__main__":
    si = SearchInterface()
    print("Hello World!")
