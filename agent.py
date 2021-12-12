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
rotacoes = {
    "S": 2,
    "Z": 2,
    "I": 2,
    "O": 1,
    "J": 4,
	"L": 4,
    "T": 4
}
init_pieces={}
v=list(normalized_pieces.values())
k=list(normalized_pieces.keys())
def run_ai(game,piece,next_pieces,x,y,state,lookahead):
	piece_name=""
	pi=normalize_piece(piece)	
	if pi in v:
		piece_name=k[v.index(pi)] #identificar peça
	
	if piece_name not in init_pieces:
		init_pieces[piece_name]=piece
	if init_pieces[piece_name] != piece: #a peça ja nao está na posiçao inicial
		return []

	if piece_name!="":
		#print(piece_name)
		for s in SHAPES:
			if s.name==piece_name:
				s.set_pos((x - s.dimensions.x) / 2, 1)
				piece=s
		next_p=[]
		for i in range(lookahead): #adicionar proximas peças a lista
			pi=normalize_piece(next_pieces[i])	
			if pi in v:
				temp=k[v.index(pi)] #identificar peça
				for s in SHAPES:
					if s.name==temp:
						s.set_pos((x - s.dimensions.x) / 2, 1)
						next_p.append(s)
		t=SearchTree(lookahead+1,(x,y),game,piece,next_p)
		t.search() #efetua a pesquisa
		#no=t.find_best()
		nos=t.get_path(t.best_node)
		#print("HELLOOO")
		#print(t.best_node)
		#print("______")
		#for i in nos:
	#		print(str(i))
		#print(nos)
		no=nos[0]
		pos = no.column
		rot = no.rotation
		#no=nos[1]
		#print(no.depth,no.column,no.rotation,no.heuristic, "pai:",no.parent.depth,no.parent.column,no.parent.rotation)
		#for u in range(len(nos)):
		#	print("final nos[",u,"]",nos[u].column,nos[u].rotation)
		#print("final:",pos,rot)
		#print("ag_height:",no.ag_height,"holes:",no.num_holes,"bump",no.bumpiness,"lines",no.comp_lines)
		#print("...................................................................")
		ret=[] #return all actions
		print("FIELD",no.filled)
		for i in range(rot):
			ret.append("w")
		while pos<0: 
			ret.append("a") 
			pos+=1
		while pos>0:
			ret.append("d") 
			pos-=1
		ret.append("s")
		return ret
	else:
		print(piece)
		return [""]

def normalize_piece(piece):
	temp=[]
	w=min(a for a,b in piece)
	h=min(b for a,b in piece)
	for a,b in piece:
		temp.append([a-w,b-h])
	return temp

