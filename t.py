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
num5=0
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
    def __init__(self,maxDepth,dimensions,message,piece,next_p):
        self.dimensions = dimensions
        self.message = message
        self.maxDepth = maxDepth
        self.piece = piece
        self.best_heuristic = -900000
        self.best_nodes=[]
        self.best_depth1=[] #Isto guarda os nodes com os 3 melhores valores no depth 1
        self.best_node=None
        self.pieces=[piece]+next_p
        self.filled=[[False]*self.dimensions[0] for _ in range(self.dimensions[1]) ]
        for (a,b) in self.message.get('game'):
            self.filled[b][a]=True
        root = SearchNode(None,0,0,0,0,0,0,0,0,self.filled)
        self.open_nodes=[root]
    
    def __str__(self):
        return str("Tree:\nDimensions: "+str(self.dimensions)+"\nMessage: "+str(self.message)+"\nMaxDepth: "+str(self.maxDepth)+"\nPiece: "+str(self.piece)+"\nROOT: "+str(self.open_nodes[0])+"\n")

    def get_path(self,node): #Devolve os nós que fazem a melhor heuristica
        if node.parent == None:
            return [] #nao preciso que retorne a raiz no path(?)
        path = self.get_path(node.parent)
        path += [node]
        return(path)

    def intersect(self,i,j):
        res=False
        width=self.dimensions[0]
        height=self.dimensions[1]
        for x,y in self.piece.positions:
            if(x+i<1 or x+i>=width-1 or y+j>=height or [x+i,y+j] in self.message.get('game')):
                res=True
        return res

    def simulate_heuristic(self,filled): #i=col j=linha
        comp_lines = self.check_complete_lines(filled)
        ag_height,num_holes,bumpiness,dif= self.height_holes(filled)
        #Acording to paper
        return num1*ag_height + num2*comp_lines + num3*num_holes + num4*bumpiness + num5*dif,ag_height,num_holes,bumpiness,comp_lines

    def check_complete_lines(self,filled):
        width=self.dimensions[0]
        height=self.dimensions[1]
        return sum(sum(i) == width-2 for i in filled)

    def height_holes(self,filled):
        width=self.dimensions[0]
        height=self.dimensions[1]
        sumheight=0
        holes=0
        bumpiness=0
        piece_by_column = [0]*(width-2)
        for y in range(1,width-1):
            for x in range(1,height):
                if filled[x][y]:
                    sumheight+=(height-x)
                    piece_by_column[y-1]=height-x
                    for k in range(x,height):
                        if not filled[k][y]:
                            holes+=1
                    break    
        minus=min(piece_by_column)
        maxus=max(piece_by_column)
        for hei in range(1,len(piece_by_column)-1):
            bumpiness+=abs(piece_by_column[hei]-piece_by_column[hei+1])
        return sumheight,holes,bumpiness,(maxus-minus)

    def search(self):
        while self.open_nodes!=[]:
            node = self.open_nodes.pop(0)
            newnodes = []
            if node.depth+1<=self.maxDepth:
                self.piece=self.pieces[node.depth] #ir buscar peça certa
                for r in range(rotacoes[self.piece.name]):
                    for i in range(-self.dimensions[0],self.dimensions[0],1): #iterate over the field
                        if not self.intersect(i,0):
                            j=0
                            while not self.intersect(i,j):
                                j+=1
                            j-=1
                            for (x,y) in self.piece.positions: #x=col y=linha
                                node.filled[y+j][x+i]=True
                            heuristic,a,b,c,d = self.simulate_heuristic(node.filled)
                            n = SearchNode(node,i,r,node.depth+1,node.heuristic+heuristic,a,b,c,d,node.filled)
                            for (x,y) in self.piece.positions: #x=col y=linha
                                node.filled[y+j][x+i]=False
                            if (n.depth<=self.maxDepth):
                                if len(self.best_depth1)<3:
                                    self.best_depth1.append(n)
                                else:
                                    heurs = [i.heuristic for i in self.best_depth1]
                                    minimo = min(heurs)
                                    if n.heuristic > minimo:
                                        self.best_depth1.remove(self.best_depth1[heurs.index(minimo)])
                                        print("REMOVED ",minimo)
                                        print("ADDED ",n.heuristic)
                                        self.best_depth1.append(n)
                                        heurs = [i.heuristic for i in self.best_depth1] #SO PRA DEBUG
                                        print("THIS IS BEST DEPTH ",heurs)
                                        print(n.depth)
                                newnodes.append(n)
                                if n.depth==self.maxDepth and n.heuristic>self.best_heuristic:
                                    if n.depth>1: #Novo nó so sera considerado se o seu parent estiver nos 3 melhores
                                        if n.parent not in self.best_depth1:
                                            continue
                                    #print(n.depth,n.column,n.rotation,n.heuristic, "pai:",n.parent.depth,n.parent.column,n.parent.rotation)
                                    #if n.parent in self.best_depth1:
                                    self.best_heuristic=n.heuristic
                                    print("THIS IS THE HEURISTIC",n.heuristic)
                                    self.best_node = n
                                elif n.depth==self.maxDepth and n.heuristic>self.best_heuristic: #Isto é para tentar ter o minimo de acoes pra msm heuristica
                                    if n.depth>1:
                                        if n.parent not in self.best_depth1:
                                            continue
                                    desvio = abs(n.column)+abs(n.rotation)
                                    if desvio < (abs(self.best_node.column)+abs(self.best_node.rotation)): #significa que tem menos acoes
                                        self.best_heuristic=n.heuristic
                                        print("THIS IS THE HEURISTIC",n.heuristic)
                                        self.best_node = n

                    self.piece.rotate()
                self.open_nodes.extend(newnodes)
                self.open_nodes.sort(key = lambda x : x.heuristic)
                self.open_nodes=self.open_nodes[:3]
                print(".....................:",len(self.open_nodes))
           
        #print("ENDDDDD")
                

        
