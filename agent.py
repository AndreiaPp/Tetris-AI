import pygame
import shape
class Event():
	type=None
	key=None
	def __init__(self,type,key):
		self.type=type
		self.key=key
		
# original_pieces2={
# 	"S":[[1,1],[1,2],[2,2],[2,3]],
# 	"Z":[[2,1],[1,2],[2,2],[1,3]],
# 	"I":[[1,1],[2,1],[3,1],[4,1]],
# 	"O":[[1,1],[2,1],[1,2],[2,2]],
# 	"J":[[1,1],[2,1],[1,2],[1,3]],
# 	"L":[[1,1],[1,2],[1,3],[2,3]],
# 	"T":[[1,1],[1,2],[2,2],[1,3]]
# 	}	
original_pieces={
	# "S":[[4,2],[4,3],[5,3],[5,4]],
	"S":[[4,3],[4,4],[5,4],[5,5]],
	# "Z":[[4,2],[3,3],[4,3],[3,4]],
	"Z":[[4,3],[3,4],[4,4],[3,5]],
	# "I":[[2,2],[3,2],[4,2],[5,2]],
	"I":[[2,3],[3,3],[4,3],[5,3]],
	# "O":[[3,3],[4,3],[3,4],[4,4]],
	"O":[[3,4],[4,4],[3,5],[4,5]],
	#"J":[[4,2],[5,2],[4,3],[4,4]],
	"J":[[4,3],[5,3],[4,4],[4,5]],
	# "L":[[4,2],[4,3],[4,4],[5,4]],
	"L":[[4,3],[4,4],[4,5],[5,5]],
	# "T":[[4,2],[4,3],[5,3],[4,4]]
	"T":[[4,3],[4,4],[5,4],[4,5]]
}
rotacoes = {
    "S": [[[4,3],[4,4],[5,4],[5,5]], [[4,4],[5,4],[3,5],[4,5]]],
    "Z": [[[4,2],[3,3],[4,3],[3,4]], [[3,3],[4,3],[4,4],[5,4]]],
    "I": [[[2,2],[3,2],[4,2],[5,2]], [[4,1],[4,2],[4,3],[4,4]]],
    "O": [[[3,3],[4,3],[3,4],[4,4]]],
    "J": [[[4,2],[5,2],[4,3],[4,4]], [[3,3],[4,3],[5,3],[5,4]], [[4,2],[4,3],[3,4],[4,4]], [[3,2],[3,3],[4,3],[5,3]]],
	"L": [[[4,2],[4,3],[4,4],[5,4]], [[3,3],[4,3],[5,3],[3,4]], [[3,2],[4,2],[4,3],[4,4]], [[5,2],[3,3],[4,3],[5,3]]],
    "T": [[[4,2],[4,3],[5,3],[4,4]], [[3,3],[4,3],[5,3],[4,4]], [[4,2],[3,3],[4,3],[4,4]], [[4,2],[3,3],[4,3],[5,3]]]
}
counter=0
# def run_ai(game,piece,x,y):
# 	if piece:
# 		global counter
# 		#original_pieces[identify_piece(piece)]
# 		#c=shape(identify_piece(piece))
# 		#for i in c:
# 		#		print(i.plan)
# 		piece_name=""
# 		for p in original_pieces:
# 			if(original_pieces[p]==piece):
				
# 				piece_name=p
# 				print("Sou o "+ piece_name)
# 		num_rotacoes=0
# 		for i in rotacoes[piece_name]:
# 			#simular com esta rotação
# 			num_rotacoes+=1
# 		counter +=1
# 		if counter<3:
# 			return []
# 		counter = 0
		
# 		if not intersect(piece,-1,0,game,x,y):
# 			e= Event(pygame.KEYDOWN,pygame.K_LEFT)
# 		elif not intersect(piece,1,0,game,x,y):
# 			e= Event(pygame.KEYDOWN,pygame.K_RIGHT)
# 		else:
# 			e= Event(pygame.KEYDOWN,pygame.K_DOWN)

# 		return [e]
# 	return []

piece_name=""
def run_ai(game,piece,x,y):
	if piece:
		global counter
		global piece_name
		counter +=1
		if counter<3:
			return []
		counter = 0
		print(piece)
		for p in original_pieces:
			if(original_pieces[p]==piece):
				piece_name=p
				print("Sou o "+ piece_name)
		position,rotation =best(game,piece_name,10,30) 
		#TO DO:mudar medidas para deixar de estarem hardcoded
		print(position,rotation)
		ret=[] #retornar logo os comandos todos
		for i in range(rotation):
			ret.append(Event(pygame.KEYDOWN, pygame.K_UP))
		while position<0: #nao sei como traduzir o game_figure.x
			ret.append(Event(pygame.KEYDOWN, pygame.K_RIGHT)) 
			position+=1
		while position>0:
			ret.append(Event(pygame.KEYDOWN, pygame.K_RIGHT)) 
			position-=1
		ret.append(Event(pygame.KEYDOWN, pygame.K_SPACE))
		
		return ret
	return []
	
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
			if(x+i<1 or x+i>=width-1 or y+j>=height-1 or [x+i,y+j] in game):
				res=True
	return res

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
				if occupied and x<newheight:
					newheight=x
				if occupied:
					filled.append((x,y))
					for k in range(x,height):
						if(k,y) not in filled:
							holes+=1
							filled.append((k,y))
		print("---"+str(holes)+"--"+str(height-newheight))
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
		print(r)
		for i in range(-width,width): #percorrer o campo todo mas nao sei como
			
			if not intersect(r,i,0,game,width,height): #r é a peça rodada
				simholes,simheight = simulate(r,i,0,game,width,height)
				if best_position is None or best_holes>simholes or (best_holes==simholes and best_height>simheight):
					best_height=simheight
					best_holes=simholes
					best_position=i
					best_rotation=num_rotacoes
					
		num_rotacoes+=1
	print(num_rotacoes)
	print(best_rotation)
	return best_position,best_rotation