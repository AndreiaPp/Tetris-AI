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


class SearchNode():
    def __init__(self,parent,column,rotation,depth,heuristic):
        #the init gamefiled doesnt include the piece
        self.parent = parent
        self.column = column
        #self.line = line this is not needed(?)
        self.rotation = rotation
        #self.positions = positions not needed(?)
        #self.gamefield = gamefield + self.positions #with piece
        self.depth = depth
        self.heuristic = heuristic
    
    def __str__(self):
        return str("Node:\nParent: "+str(self.parent)+"\nColumn: "+str(self.column)+"\nRotation: "+str(self.rotation)+"\nDepth: "+str(self.depth)+"\nHeuristic: "+str(self.heuristic)+"\n")

class SearchTree():
    def __init__(self,maxDepth,dimensions,message,piece):
        self.dimensions = dimensions
        self.message = message
        self.maxDepth = maxDepth
        self.piece = piece
        root = SearchNode(None,0,0,0,0)
        self.open_nodes=[root]
        self.best_heuristic = -900000
        self.best_nodes=[]
    
    def __str__(self):
        return str("Tree:\nDimensions: "+str(self.dimensions)+"\nMessage: "+str(self.message)+"\nMaxDepth: "+str(self.maxDepth)+"\nPiece: "+str(self.piece)+"\nROOT: "+str(self.open_nodes[0])+"\n")

    def get_path(self,node): #Devolve os nós que fazem a melhor heuristica
        if node.parent == None:
            #return [node]
            return [node] #nao preciso que retorne a raiz no path(?)
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

    def simulate_heuristic(self,i,j): #i=col j=linha
        while not self.intersect(i,j):
            j+=1
        j-=1
        filled=[(a,b) for a,b in self.message.get('game')]
        for (x,y) in self.piece.positions: #x=col y=linha
            filled.append((x+i,y+j))
		
        comp_lines = self.check_complete_lines(filled)
        ag_height,num_holes,bumpiness= self.height_holes(filled)

		#Acording to paper
        return num1*ag_height + num2*comp_lines + num3*num_holes + num4*bumpiness

    def check_complete_lines(self,filled):
        width=self.dimensions[0]
        height=self.dimensions[1]

        pieces_by_line={}
        for c,l in filled:
            if height-l not in pieces_by_line:
                pieces_by_line[height-l]=1
            else:
                pieces_by_line[height-l]+=1
        return sum(value == width-2 for value in pieces_by_line.values())

    def height_holes(self,filled):
        width=self.dimensions[0]
        height=self.dimensions[1]
        sum=0
        holes=0
        bumpiness=0
        piece_by_column = {}
        for y in range(1,width-1):
            piece_by_column[y]=0
            for x in range(1,height):
                if (y,x) in filled:
                    sum+=(height-x)
                    piece_by_column[y]=height-x
                    for k in range(x,height):
                        if (y,k) not in filled:
                            holes+=1
                    break        
        for hei in range(1,len(piece_by_column)-1):
            bumpiness+=abs(piece_by_column[hei]-piece_by_column[hei+1])
        return sum,holes,bumpiness

    def search(self):
        #print("BEGINNNNNNN")
        while self.open_nodes!=[]:
            node = self.open_nodes.pop(0)
            newnodes = []
            if node.depth+1>self.maxDepth:
                break
            #criar nos para uma rotacao, para todas as posicoes, para a outra rotacao para todas as posicoes...
            for r in range(rotacoes[self.piece.name]):
                for i in range(-self.dimensions[0],self.dimensions[0],1): #iterate over the field
                    if not self.intersect(i,0):
                        heuristic = self.simulate_heuristic(i,0)
                        n = SearchNode(node,i,r,node.depth+1,node.heuristic+heuristic)
                        #if (n not in self.get_path(node)) and (n.depth<=self.maxDepth):
                        if (n.depth<=self.maxDepth):
                            newnodes.append(n)
                            if n.heuristic>self.best_heuristic:
                                self.best_heuristic=n.heuristic
                                #print("Here")
                                self.best_nodes = self.get_path(n)
                                self.best_nodes = [self.best_nodes[i] for i in range(len(self.best_nodes)-1,-1,-1)]
                                #print(self.get_path(n))
                self.piece.rotate()
            #greedy
            self.open_nodes.extend(newnodes)
            self.open_nodes.sort(key = lambda x : x.heuristic)
        #print("ENDDDDD")
                

        