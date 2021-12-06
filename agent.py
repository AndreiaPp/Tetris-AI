import time
from shape import SHAPES 
# original_pieces={
# 	"S":[[4,2],[4,3],[5,3],[5,4]], 
# 	"Z":[[4,2],[3,3],[4,3],[3,4]], 
# 	"I":[[2,2],[3,2],[4,2],[5,2]], 
# 	"O":[[3,3],[4,3],[3,4],[4,4]], 
#  	"J":[[4,2],[5,2],[4,3],[4,4]], 
#  	"L":[[4,2],[4,3],[4,4],[5,4]], 
#  	"T":[[4,2],[4,3],[5,3],[4,4]] 
# }
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
num1=-0.510066 #original
#num1=-0.610066 
num2=0.760666 #original
#num2=0.90
num3=-0.35663 #original
num4=-0.184483 #original
# num1=-0.510066 #original
		# #num1=-0.610066 
		# num2=0.760666 #original
		# #num2=1
		# num3=-0.35663 #original
		# num4=-0.184483 #original
def run_ai(game,piece,x,y):
	piece_name=""
	# for p in original_pieces:
	# 	if(original_pieces[p]==piece):
	# 		piece_name=p	
	for p in normalized_pieces:
		if normalized_pieces[p]==normalize_piece(piece):
			piece_name=p
	#ir ao shape
	#print(piece_name)
	
	#buscar shape com este nome
	#set shape com pos inicial
	#piece=esta shape
	if piece_name!="":
		#print(piece)
		for s in SHAPES:
			if s.name==piece_name:
				s.set_pos((x - s.dimensions.x) / 2, 1)
				piece=s
	
		#print(piece.positions)
		#piece.rotate()
		#print(piece.positions)
		#print("......")
		position,rotation =best(game,piece.name,piece,x,y) 
		#TO DO:change rotations to not hardcoded
		ret=[] #return all actions
		for i in range(rotation):
			ret.append("w")
		while position<0: 
			ret.append("a") 
			position+=1
		while position>0:
			ret.append("d") 
			position-=1
		ret.append("s")
		return ret
	else:
		return []

def normalize_piece(piece):
	temp=[]
	w=min(a for a,b in piece)
	h=min(b for a,b in piece)
	for a,b in piece:
		temp.append([a-w,b-h])
	return temp

def intersect(piece_pos,i,j,game,width,height):
	res=False
	for x,y in piece_pos:
		if(x+i<1 or x+i>=width-1 or y+j>=height or [x+i,y+j] in game):
			res=True
	return res

def simulate(piece_pos,i,j,game,width,height): #i=col j=linha
		while not intersect(piece_pos,i,j,game,width,height):
			j+=1
		j-=1
		filled=[(a,b) for a,b in game]
		for (x,y) in piece_pos: #x=col y=linha
			filled.append((x+i,y+j))
			
		
		comp_lines = check_complete_lines(filled,height,width) #MAXIMIZE
		ag_height,num_holes,bumpiness= height_holes(filled,width,height) #MINIMIZE BOTH
		#Acording to paper
		return num1*ag_height + num2*comp_lines + num3*num_holes + num4*bumpiness
		
def best(game,piece_name,piece,width,height):
	best_heuristic = -90000
	best_position = None
	best_rotation=0
	#print(piece_name)
	for r in range(rotacoes[piece_name]):
		#print(piece.positions)
		for i in range(-width,width,1): #iterate over the field
			if not intersect(piece.positions,i,0,game,width,height): #r is the rotated piece
				heuristic = simulate(piece.positions,i,0,game,width,height) 
				if heuristic > best_heuristic:
					best_heuristic=heuristic
					best_position=i
					best_rotation=r
		piece.rotate()			
	return best_position,best_rotation
counter=0


def height_holes(filled,width,height):
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
	#print(abs(piece_by_column[hei]-piece_by_column[hei+1]) for hei in range(1,len(piece_by_column)-1))
	for hei in range(1,len(piece_by_column)-1):
		bumpiness+=abs(piece_by_column[hei]-piece_by_column[hei+1])
	return sum,holes,bumpiness

def check_complete_lines(filled,height,width):
	pieces_by_line={}
	for c,l in filled:
		if height-l not in pieces_by_line:
			pieces_by_line[height-l]=1
		else:
			pieces_by_line[height-l]+=1
	#return sum(value == 8 for value in pieces_by_line.values())
	return sum(value == width-2 for value in pieces_by_line.values())
