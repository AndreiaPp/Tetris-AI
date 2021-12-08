from abc import ABC, abstractmethod

class SearchDomain(ABC): #Formata a estrutura de um domínio de aplicação

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

class SearchProblem: 
    def __init__(self, width, height,filled,initial_shape):
        self.width = width
        self.height = height
        self.filled = filled
        self.initial_shape = initial_shape

class Piece:
    def __init__(self,shape,heuristic,next_piece,depth=0):
        self.shape = shape
        self.heuristic = heuristic
        self.next_piece = next_piece
        self.depth = depth
    def __str__(self):
        return "piece(" + str(self.shape) + "," + str(self.heuristic)+ "," + str(self.next_piece) + ")"
    def __repr__(self):
        return str(self)

class TreeSearch:
    def __init__(self,problem):
        self.problem = problem
        root = Piece(problem.initial, None,0)
        self.open_nodes = [root]
        self.solution = None

    def get_path(self,node):
        # if node.parent == None:
        #     return [node.state]
        # path = self.get_path(node.parent)
        # path += [node.state]
        # return(path)
        pass
        

    #  def __init__(self,problem, strategy='breadth'): 
    #     self.problem = problem
    #     root = SearchNode(problem.initial, None,0)#,0,self.problem.domain.heuristic(self.problem.initial,self.problem.goal))
    #     self.open_nodes = [root]
    #     self.strategy = strategy
    #     self.solution = None
    #     self.length=1
    #     self.terminals=0
    #     self.non_terminals=0
    #     self.avg_branching=0
    #     self.average_depth = 0
    #     self.cum_depth = 0
    #     self.cost = 0 #Custo total da solução (soma dos custos das sucessivas transições)
    #     self.highest_cost_nodes = [root]
