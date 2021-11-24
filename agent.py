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
			#print("Sou o "+ piece_name)
	if piece_name!="":
		#print("piece received:"+str(piece))
		position,rotation =best(game,piece_name,x,y) 
		#TO DO:mudar medidas para deixar de estarem hardcoded
		#print("res:::")
		#print(position,rotation)
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
		return [""]
	#return []
	
# def identify_piece(piece):
# 		min_x=100
# 		min_y=100
# 		for t in piece:
# 			x,y=t[0],t[1]
# 			if(x<min_x):
# 				min_x=x
# 			if(y<min_y):
# 				min_y=y
# 		temp_piece=[]
# 		print(min_x,min_y)
# 		for t in piece:
# 			temp_piece.append([(t[0]-min_x)+1,(t[1]-min_y)+1])
# 		for p in original_pieces:
# 			if(temp_piece==original_pieces[p]):
# 				return p
			
def intersect(piece,i,j,game,width,height):
	#i=-1 0 1
	#j=-1 0 1
	res=False
	if piece:
		for x,y in piece:
			#print(game)
			if(x+i<1 or x+i>=width-1 or y+j>=height or [x+i,y+j] in game):
				res=True
	return res

def simulate(piece,i,j,game,width,height): #i=col j=linha
		while not intersect(piece,i,j,game,width,height):
			j+=1
		j-=1

		filled=[]
		
		for a,b in game: #a=col b=linha
			filled.append((a,b))
		for (x,y) in piece: #x=col y=linha
			filled.append([x+i,y+j])
		ag_height = aggregate_height(filled,height) #MINIMIZE
		comp_lines = check_complete_lines(filled,height) #MAXIMIZE
		num_holes = count_holes(filled,width,height) #MINIMIZE
		bumpiness = calc_bumpiness(filled,width,height) #MINIMIZE

		num1=-0.510066 #original
		#num1=-0.310066
		num2=0.760666 #original
		num3=-0.35663 #original
		num4=-0.184483 #original
		#num4=-0.284483

		#Acording to paper
			
		heuristic = num1*ag_height + num2*comp_lines + num3*num_holes + num4*bumpiness

		return heuristic


		# for x in range(height-1,-1,-1): #linhas
		# 	for y in range(1,width,1): #colunas
		# 		occupied=False
		# 		if([y,x] in game):
		# 			occupied=True
		# 		#funçao estranha
				
		# 		for a,b in piece:
					
		# 			if a+i==y and b+j==x:
		# 				occupied=True
				
		# 		if occupied and x<newheight:
		# 			newheight=x
		# 		if occupied:
		# 			if (y,x) not in filled:
		# 				filled.append((y,x))
		# 			#print("filled pos peça:",filled)
		# 			for k in range(x,height): #linhas
		# 			#for k in range(0,x):
		# 				if(y,k) not in filled:
		# 					holes+=1
		# 					filled.append((y,k))
		# 			#print("filled final:",list(set(filled)-set(f)))
		# 	#time.sleep(5)

def best(game,piece_name,width,height):
	best_heuristic = -900
	num_rotacoes=0
	best_position = None
	best_rotation=0
	
	for r in rotacoes[piece_name]:
		for i in range(-width,width,1): #percorrer o campo todo mas nao sei como
			if not intersect(r,i,0,game,width,height):#intersect(r,game): #r é a peça rodada
				heuristic = simulate(r,i,0,game,width,height) #NOVA HEURISTICA TRIALS
				if heuristic > best_heuristic:
					best_heuristic=heuristic
					best_position=i
					best_rotation=num_rotacoes			
		num_rotacoes+=1
	return best_position,best_rotation
counter=0
def aggregate_height(filled,height):
	global counter
	piece_by_column = {}
	for c,l in filled:
		if c not in piece_by_column:
			piece_by_column[c]=[height-l]
		else:
			piece_by_column[c].append(height-l)
	sum = 0
	
	for elem in piece_by_column:
		sum+=max(piece_by_column[elem])
	return sum

def check_complete_lines(filled,height):
	complete_lines=0
	pieces_by_line={}
	for c,l in filled:
		if height-l not in pieces_by_line:
			pieces_by_line[height-l]=[c]
		else:
			pieces_by_line[height-l].append(c)
	for elem in pieces_by_line:
		if len(pieces_by_line[elem])==8: #há linha completa
			complete_lines+=1
	return complete_lines

def count_holes(filled,width,height):
	holes=0
	for y in range(1,width):
		for x in range(1,height):
			for k in range(x,0,-1):
				if (y,k) not in filled:
					holes+=1
			break
	return holes

def calc_bumpiness(filled,width,height):
	piece_by_column = {}
	for wid in range(1,width-1):
		piece_by_column[wid]=[0]
	for c,l in filled:
		piece_by_column[c].append(height-l)
	
	for elem in piece_by_column:
		piece_by_column[elem]=max(piece_by_column[elem])

	bump = 0
	
	for hei in range(1,len(piece_by_column)-1):
		bump+=abs(piece_by_column[hei]-piece_by_column[hei+1])
	return bump

