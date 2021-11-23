import pygame
import shape
import time
class Event():
	type=None
	key=None
	def __init__(self,type,key):
		self.type=type
		self.key=key
		
# original_pieces2={
# 	"S":[[1,1],[1,2],[2,2],[2,3]],
#  	"Z":[[2,1],[1,2],[2,2],[1,3]],
# 	"I":[[1,1],[2,1],[3,1],[4,1]],
# 	"O":[[1,2],[2,2],[1,3],[2,3]], #fixed
# 	"J":[[1,1],[2,1],[1,2],[1,3]],
# 	"L":[[2,1],[2,2],[2,3],[3,3]], #fixed
# 	"T":[[1,1],[1,2],[2,2],[1,3]]
#	}	
original_pieces={
	"S":[[4,2],[4,3],[5,3],[5,4]], #ta
	"Z":[[4,2],[3,3],[4,3],[3,4]], #ta
	"I":[[2,2],[3,2],[4,2],[5,2]], #ta
	"O":[[3,3],[4,3],[3,4],[4,4]], #ta
 	"J":[[4,2],[5,2],[4,3],[4,4]], #ta
 	"L":[[4,2],[4,3],[4,4],[5,4]], #ta
 	"T":[[4,2],[4,3],[5,3],[4,4]] #ta
}
rotacoes = {
    "S": [[[4,2],[4,3],[5,3],[5,4]], [[4,3],[5,3],[3,4],[4,4]]],
    "Z": [[[4,2],[3,3],[4,3],[3,4]], [[3,3],[4,3],[4,4],[5,4]]],
    "I": [[[2,2],[3,2],[4,2],[5,2]], [[4,1],[4,2],[4,3],[4,4]]],
    "O": [[[3,3],[4,3],[3,4],[4,4]]],
    "J": [[[4,2],[5,2],[4,3],[4,4]], [[3,3],[4,3],[5,3],[5,4]], [[4,2],[4,3],[3,4],[4,4]], [[3,2],[3,3],[4,3],[5,3]]],
	"L": [[[4,2],[4,3],[4,4],[5,4]], [[3,3],[4,3],[5,3],[3,4]], [[3,2],[4,2],[4,3],[4,4]], [[5,2],[3,3],[4,3],[5,3]]],
    "T": [[[4,2],[4,3],[5,3],[4,4]], [[3,3],[4,3],[5,3],[4,4]], [[4,2],[3,3],[4,3],[4,4]], [[4,2],[3,3],[4,3],[5,3]]]
}
counter=0

piece_name=""
def run_ai(game,piece,x,y):
	#if piece:
	#global counter
	piece_name=""
	#global piece_name
	#counter +=1
	# if counter<3:
	# 	return []
	#counter = 0
	#print(piece)
	for p in original_pieces:
		if(original_pieces[p]==piece):
			piece_name=p
			print("Sou o "+ piece_name)
	if piece_name!="":
		print("piece received:"+str(piece))
		position,rotation =best(game,piece_name,10,30) 
		#TO DO:mudar medidas para deixar de estarem hardcoded
		print("res:::")
		print(position,rotation)
		ret=[] #retornar logo os comandos todos
		for i in range(rotation):
			ret.append("w")
		while position<0: #nao sei como traduzir o game_figure.x
			ret.append("a") 
			position+=1
		while position>0:
			ret.append("d") 
			position-=1
		#min_y=min(min(rotacoes[piece_name][rotation], key=lambda x: x[1]))
		#print(min_y)
		#for i in range(30-min_y):
		ret.append("s")
		#print(ret)
		return ret
	else:
		return ["s"]
	#return []
	
def identify_piece(piece):
		min_x=100
		min_y=100
		for t in piece:
			x,y=t[0],t[1]
			if(x<min_x):
				min_x=x
			if(y<min_y):
				min_y=y
		temp_piece=[]
		print(min_x,min_y)
		for t in piece:
			temp_piece.append([(t[0]-min_x)+1,(t[1]-min_y)+1])
		for p in original_pieces:
			if(temp_piece==original_pieces[p]):
				return p
			
def intersect(piece,i,j,game,width,height):
	#i=-1 0 1
	#j=-1 0 1
	res=False
	if piece:
		for x,y in piece:
			#print(game)
			if(x+i<1 or x+i>=width-1 or y+j>=height-1 or [x+i,y+j] in game):
				res=True
	return res

# def intersect(piece,game):
# 	for block in piece:
# 		if block in game:
# 			return True
# 	return False

def simulate(piece,i,j,game,width,height):
		while not intersect(piece,i,j,game,width,height):
			j+=1
		j-=1
		newheight=height
		holes=0
		filled=[]
		
		for x in range(height-1,-1,-1):
			for y in range(width):
				occupied=False
				if([x,y] in game):
					occupied=True
				#funçao estranha
				for a,b in piece:
					if a+j==x and b+i==y:
						occupied=True
				if occupied and x<newheight:
					newheight=x
				if occupied:
					filled.append((x,y))
					for k in range(x,height):
						if(k,y) not in filled:
							holes+=1
							filled.append((k,y))
		#print("---"+str(holes)+"--"+str(height-newheight))
		return holes,height-newheight

# def best(game,piece,width,height):
# 	best_height=height
# 	best_holes=width*height
# 	best_position=None
# 	best_rot=None
	
# 	for rot in range(4): #rodamos 4 vezes
# 		#como rodar??
# 		pass


def best(game,piece_name,width,height):
	best_height=height
	best_holes=width*height
	best_position=None
	best_rotation=None
	
	num_rotacoes = 0
	for r in rotacoes[piece_name]:
		print("rotacao"+str(r))
		for i in range(-width,width): #percorrer o campo todo mas nao sei como
		#for i in range(width):
			if not intersect(r,i,0,game,width,height):#intersect(r,game): #r é a peça rodada
				simholes,simheight = simulate(r,i,0,game,width,height)
				if best_position is None or best_holes>simholes or (best_holes==simholes and best_height>simheight):
					best_height=simheight
					best_holes=simholes
					best_position=i
					best_rotation=num_rotacoes
		print(best_position,best_rotation)			
		num_rotacoes+=1
	print(num_rotacoes)
	print(best_rotation)
	return best_position,best_rotation

# def best(game,piece_name,width,height):
# 	best_holes=width*height
# 	best_position = None
# 	best_rotation = None

# 	num_rotacoes = 0

# 	for r in rotacoes[piece_name]:
# 		#percorrer da esquerda pra direita
# 		#se intercetar todos, subimos uma altura

# 		if not intersect(r,game):
