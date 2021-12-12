import time 
import copy
rotacoes = {
    "S": 2,
    "Z": 2,
    "I": 2,
    "O": 1,
    "J": 4,
    "L": 4,
    "T": 4
}

num1=-0.510066 #original
num2=0.760666 #original
#num2=0.95
num3=-0.35663 #original
num4=-0.184483 #original
#num4=-0.3

class SearchNode():
    def __init__(self,parent,column,rotation,depth,heuristic,ag_height,num_holes,bumpiness,comp_lines,filled):
        self.parent = parent
        self.column = column
        self.rotation = rotation
        self.depth = depth
        self.heuristic = heuristic
        self.ag_height=ag_height
        self.num_holes=num_holes
        self.bumpiness=bumpiness
        self.comp_lines=comp_lines
        self.filled=filled
        
    
    def __str__(self):
        return str("Node:\nParent: "+str(self.parent)+"\nColumn: "+str(self.column)+"\nRotation: "+str(self.rotation)+"\nDepth: "+str(self.depth)+"\nHeuristic: "+str(self.heuristic)+"\n")

class SearchTree():
    def __init__(self,maxDepth,dimensions,game,piece,next_p):
        self.height=dimensions[1]
        self.width=dimensions[0]
        self.maxDepth = maxDepth
        self.piece = piece
        self.best_heuristic = -900000
        self.best_nodes=[]
        self.best_depth1=[] #Isto guarda os nodes com os 3 melhores valores no depth 1
        self.best_node=None
        self.pieces=[piece]+next_p
        self.filled=[[False]*(self.width-2) for _ in range(self.height-1) ]
        for (a,b) in game:
            self.filled[b-1][a-1]=True
        root = SearchNode(None,0,0,0,0,0,0,0,0,self.filled)
        self.open_nodes=[root]
    
    def __str__(self):
        return str("Tree:\nDimensions: "+str(self.height)+"-"+str(self.width)+"\nGame: "+str(game)+"\nMaxDepth: "+str(self.maxDepth)+"\nPiece: "+str(self.piece)+"\nROOT: "+str(self.open_nodes[0])+"\n")

    def get_path(self,node): #Devolve os nós que fazem a melhor heuristica
        if node.parent == None:
            return [] #nao preciso que retorne a raiz no path(?)
        path = self.get_path(node.parent)
        path += [node]
        return(path)

    def intersect(self,node,i,j):
        for x,y in self.piece.positions:
            if(x+i<1 or x+i>=self.width-1 or y+j>=self.height or node.filled[y+j-1][x+i-1]):
                return True
        return False

    #def simulate_heuristic(self,filled,lista): #i=col j=linha
    def simulate_heuristic(self,filled): #i=col j=linha
        sumheight=0
        holes=0
        bumpiness=0
        piece_by_column = [0]*(self.width-2)
        for y in range(1,self.width-1):
            for x in range(1,self.height):
                if filled[x-1][y-1]:
                    sumheight+=(self.height-x)
                    piece_by_column[y-1]=self.height-x
                    for k in range(x,self.height):
                        if not filled[k-1][y-1]:
                            holes+=1
                    break
        for hei in range(len(piece_by_column)-1):
            bumpiness+=abs(piece_by_column[hei]-piece_by_column[hei+1])
        #lines=sum(lista)
        lines=sum(sum(i) == 8 for i in filled)
        return num1*sumheight + num2*lines + num3*holes + num4*bumpiness,sumheight,holes,bumpiness,lines
        
    def calc_lines(self,filled):
        lista=[sum(i) == self.width-2 for i in filled]
        res = [i for i, val in enumerate(lista) if val]
        return res
        
    def search(self):

        while self.open_nodes!=[]:
            node = self.open_nodes.pop(0)
            newnodes = []
            if node.depth+1<=self.maxDepth:
                self.piece=self.pieces[node.depth] #ir buscar peça certa
                for r in range(rotacoes[self.piece.name]):
                    for i in range(-4,6,1): #iterate over the field
                        if not self.intersect(node,i,0):
                            j=0
                            while not self.intersect(node,i,j):
                                j+=1
                            j-=1
                            for (x,y) in self.piece.positions: #x=col y=linha
                                node.filled[y+j-1][x+i-1]=True

                            lines=[]
                            if self.maxDepth!=1: 
                                lines=self.calc_lines(node.filled)
                                
                                if lines!=[]:
                                    temp={}
                                    for l in lines:
                                        temp[l]=node.filled.pop(l)
                                        node.filled.insert(0,[False]*self.width)
                                    
                            #heuristic,a,b,c,d= self.simulate_heuristic(node.filled,lines)
                            heuristic,a,b,c,d= self.simulate_heuristic(node.filled)
                            n = SearchNode(node,i,r,node.depth+1,node.heuristic+heuristic,a,b,c,d,copy.deepcopy(node.filled))
                            if n.depth!=self.maxDepth:
                                newnodes.append(n)
                            if n.depth==self.maxDepth and n.heuristic>self.best_heuristic:
                                self.best_heuristic=n.heuristic
                                self.best_node = n

                            if self.maxDepth!=1:   
                                if lines!=[]:
                                    for l in temp:
                                        node.filled.pop(0)
                                        node.filled.insert(l,temp[l])
                            for (x,y) in self.piece.positions: #x=col y=linha
                                node.filled[y+j-1][x+i-1]=False
                    self.piece.rotate()
                self.open_nodes.extend(newnodes)
                #self.open_nodes.sort(key = lambda y : abs(y.column)+y.rotation)
                self.open_nodes.sort(key= lambda x : x.heuristic,reverse=True)
                self.open_nodes=self.open_nodes[:5]
        #print("ENDDDDD")
                

