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
num3=-0.35663 #original
num4=-0.184483 #original

#create the nodes
class SearchNode():
    def __init__(self,parent,column,rotation,depth,heuristic,filled):
        self.parent = parent
        self.column = column
        self.rotation = rotation
        self.depth = depth
        self.heuristic = heuristic
        self.filled=filled
    def __str__(self):
        return str("Node:\nParent: "+str(self.parent)+"\nColumn: "+str(self.column)+"\nRotation: "+str(self.rotation)+"\nDepth: "+str(self.depth)+"\nHeuristic: "+str(self.heuristic)+"\nFilled: "+str(self.filled)+"\n")

#create the tree
class SearchTree():
    def __init__(self,maxDepth,dimensions,game,piece,next_p):
        self.height=dimensions[1]
        self.width=dimensions[0]
        self.maxDepth = maxDepth
        self.piece = piece
        self.best_heuristic = -900000 
        self.best_node=None
        self.pieces=[piece]+next_p #put all pieces in the same array
        self.filled=[[False]*(self.width-2) for _ in range(self.height-1) ] #create binary matrix representing empty game field
        for (a,b) in game: #fill said matrix with occupied positions in game field
            self.filled[b-1][a-1]=True
        root = SearchNode(None,0,0,0,0,self.filled) 
        self.open_nodes=[root] 
        
    def __str__(self):
        return str("Tree:\nDimensions: "+str(self.height)+"-"+str(self.width)+"\nMaxDepth: "+str(self.maxDepth)+"\nPiece: "+str(self.piece)+"\nROOT: "+str(self.open_nodes[0])+"\n")

    #search for best leaf node    
    def search(self):
        while self.open_nodes!=[]:
            node = self.open_nodes.pop(0)
            newnodes = []
            self.piece=self.pieces[node.depth] #fetch correct piece
            for r in range(rotacoes[self.piece.name]):
                for i in range(-4,6,1): #iterate over the field
                    if not self.intersect(node,i,0):
                        j=0
                        while not self.intersect(node,i,j): #descend piece
                            j+=1
                        j-=1
                        for (x,y) in self.piece.positions: #x=col y=linha
                            node.filled[y+j-1][x+i-1]=True #simulate piece in game field
                        lines=[]
                        if self.maxDepth!=1: 
                            lines=self.simulate_lines(node.filled)
                            if lines!=[]: #simulate the removal of lines from game field
                                temp={}
                                for l in lines:
                                    temp[l]=node.filled.pop(l)
                                    node.filled.insert(0,[False]*(self.width-2)) #add empty line for good dimensions purpose
                                
                        heuristic= self.calculate_heuristic(node.filled,lines)
                        n = SearchNode(node,i,r,node.depth+1,node.heuristic+heuristic,copy.deepcopy(node.filled)) #create node
                        if n.depth!=self.maxDepth: #if it's not a leaf node, we add it to newnodes
                            newnodes.append(n)
                            
                        if n.depth==self.maxDepth and n.heuristic>self.best_heuristic: #if it's a leaf node, we compare the heuristic to save the best one
                            self.best_heuristic=n.heuristic
                            self.best_node = n
                        #next lines are for backtracking the game field	
                        if self.maxDepth!=1:   
                            if lines!=[]: 
                                for l in temp:
                                    node.filled.pop(0)
                                    node.filled.insert(l,temp[l])
                        for (x,y) in self.piece.positions: #x=col y=linha
                            node.filled[y+j-1][x+i-1]=False
                            
                self.piece.rotate() #rotate the piece 
            self.open_nodes.extend(newnodes)
            self.open_nodes.sort(key= lambda x : x.heuristic,reverse=True) #sort
            self.open_nodes=self.open_nodes[:3] #we only open the 3 best nodes of each depth
    
    #check if piece colides with the field limits or other pieces
    def intersect(self,node,i,j):
        for x,y in self.piece.positions:
            if(x+i<1 or x+i>=self.width-1 or y+j>=self.height or node.filled[y+j-1][x+i-1]):
                return True
        return False 
   
    #simulate the number of complete lines
    def simulate_lines(self,filled):
        lista=[sum(i) == self.width-2 for i in filled] #check if line is full of "true" meaning line is complete
        res = [i for i, val in enumerate(lista) if val] #return indexes of complete lines
        return res   
        
    #each parameter is explained on the presentation
    def calculate_heuristic(self,filled,lista): #i=col j=linha
        sumheight=0
        holes=0
        bumpiness=0
        piece_by_column = [0]*(self.width-2)
        for y in range(1,self.width-1): #for each column
            for x in range(1,self.height):
                if filled[x-1][y-1]: #go down until we find a filled position
                    sumheight+=(self.height-x)
                    piece_by_column[y-1]=self.height-x
                    for k in range(x,self.height): #count holes
                        if not filled[k-1][y-1]:
                            holes+=1
                    break
             
        for hei in range(len(piece_by_column)-1): #calculate bumpiness
            bumpiness+=abs(piece_by_column[hei]-piece_by_column[hei+1])
            
        lines=len(lista) #calculate number of complete lines
        return num1*sumheight + num2*lines + num3*holes + num4*bumpiness
        
    #returns the best path from leaf node until node whose parent is the root
    def get_path(self,node): 
        if node.parent == None:
            return [] 
        path = self.get_path(node.parent)
        path += [node]
        return(path)


