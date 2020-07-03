from algorithms import RandomWalk
from domains import PegSolitaireBoard, PegSolitaireInterface

if __name__ == "__main__":
    problem = PegSolitaireBoard()
    interface = PegSolitaireInterface(problem)
    solver = RandomWalk(interface)
    solver.solve()
    
    print("Found a solution after {} tries.\n".format(len(solver.costs)))
    for index, solution in solver.solutions.items():
        for move in solution:
            print(problem)
            print(move)
            interface.apply_action(problem, move)
    print(problem)
