import time
from shape import SHAPES 
from tree_search import SearchTree,SearchNode

normalized_pieces={
	"I":[[0, 0], [1, 0], [2, 0], [3, 0]],
	"S":[[0, 0], [0, 1], [1, 1], [1, 2]],
	"J":[[0, 0], [1, 0], [0, 1], [0, 2]],
	"T":[[0, 0], [0, 1], [1, 1], [0, 2]],
	"O":[[0, 0], [1, 0], [0, 1], [1, 1]],
	"L":[[0, 0], [0, 1], [0, 2], [1, 2]],
	"Z":[[1, 0], [0, 1], [1, 1], [0, 2]]

}
v=list(normalized_pieces.values())
k=list(normalized_pieces.keys())
init_pieces={}

def run_ai(game,piece,next_pieces,x,y,lookahead):
	piece_name=""
	pi=normalize_piece(piece)  #removes the offset of a piece	
	if pi in v:
		piece_name=k[v.index(pi)] #identify piece name
	if piece_name not in init_pieces: #save piece original position
		init_pieces[piece_name]=piece
	if init_pieces[piece_name] != piece: #piece is no longer on its original position
		return []
		
	if piece_name!="": #we have an original piece
	
		for s in SHAPES: #save the shape corresponding to the piece (that way we can use all shape.py methods) 
			if s.name==piece_name:
				s.set_pos((x - s.dimensions.x) / 2, 1)
				piece=s
		next_p=[]
		for i in range(lookahead): #identify and save the shapes of next_pieces according to the lookahead
			pi=normalize_piece(next_pieces[i])	
			if pi in v:
				temp=k[v.index(pi)] 
				for s in SHAPES:
					if s.name==temp:
						s.set_pos((x - s.dimensions.x) / 2, 1)
						next_p.append(s)
						
		t=SearchTree(lookahead+1,(x,y),game,piece,next_p) #create tree
		t.search() #search best node
		nos=t.get_path(t.best_node) #get path of best node
		no=nos[0] #get best node corresponding to current piece
		pos = no.column #get number of shifts to be executed
		rot = no.rotation #get number of rotations to be executed
		ret=[] #array containing all actions to be executed
		for i in range(rot): #add rotations to the array
			ret.append("w")
		while pos<0: #add left shifts to the array
			ret.append("a") 
			pos+=1
		while pos>0: #add right shifts to the array
			ret.append("d") 
			pos-=1
		ret.append("s") #add hard drop to the array
		return ret 
	else: #we don't have an original piece
		return [""]

#this method puts the piece in the left upper hand corner 
def normalize_piece(piece):
	temp=[]
	w=min(a for a,b in piece)
	h=min(b for a,b in piece)
	for a,b in piece:
		temp.append([a-w,b-h])
	return temp

