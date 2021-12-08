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
    def __init__(self,parent,column,line,rotation,positions,depth,heuristic):
        #the init gamefiled doesnt include the piece
        self.parent = parent
        self.column = column
        self.line = line
        self.rotation = rotation
        self.positions = positions
        #self.gamefield = gamefield + self.positions #with piece
        self.depth = depth
        self.heuristic = heuristic
    
    def __str__(self):
        return str("Node:\nParent: "+str(self.parent)+"\nColumn: "+str(self.column)+"\nLine: "+str(self.line)+"\nRotation: "+str(self.rotation)+"\nPositions: "+str(self.positions)+"\nGamefield: "+str(self.gamefield)+"\nDepth: "+str(self.depth)+"\nHeuristic: "+str(self.heuristic)+"\n")

class SearchTree():
    def __init__(self,maxDepth,dimensions,message,piece):
        self.dimensions = dimensions
        self.message = message
        self.maxDepth = maxDepth
        self.piece = piece
        root = SearchNode(None,0,0,0,self.piece.positions,0,-90000)
        self.open_nodes=[root]
        self.best_heuristic = 0
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
        while self.open_nodes!=[]:
            node = self.open_nodes.pop(0)
            newnodes = []
            #criar nos para uma rotacao, para todas as posicoes, para a outra rotacao para todas as posicoes...
            for r in range(rotacoes[self.piece.name]):
                for i in range(-self.dimensions[0],self.dimensions[0],1): #iterate over the field
                    if not self.intersect(i,0):
                        #heuristic = simulate(piece.positions,i,0,game,width,height) 

# heuristic = simulate(piece.positions,i,0,game,width,height) 
# 				if heuristic > best_heuristic:
# 					best_heuristic=heuristic
# 					best_position=i
# 					best_rotation=r
# 		piece.rotate()			
# 	return best_position,best_rotation
                

        