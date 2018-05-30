from random import shuffle


#Basic Unit (Block)
class Block() :
	def __init__(self,number,i,j,maxBlocks) :
		if 0<=number<maxBlocks :
			self.number	= number
			self.pos	= (i,j)
			self.up		= None
			self.down	= None
			self.left	= None
			self.right	= None
			self.numBlocks	= maxBlocks
			self.calculateOffset()
		else :
			print("Puzzle Crashed!!")
			quit()

	def calculateOffset(self) :
		if self.number != 0 :
			self.dy	= abs(((self.number-1)%int((self.numBlocks)**0.5))-self.pos[1])
			self.dx	= abs(int((self.number-1)//int((self.numBlocks)**0.5))-self.pos[0])
		else : self.dx=self.dy=-1

#Puzzle Game Class
class Game() :
	def __init__(self,puzzleCode) :
		self.numBlocks	= puzzleCode+1
		self.final_set	= [i+1 for i in range(self.numBlocks-1)]
		self.final_set.append(0)
		self.getSolvable()
		self.win = False
		self.reset_game()

	def reset_game(self) :
		if self.win :
			self.getSolvable()

		self.win = False
		self.blocks = {}
		for i in range(int((self.numBlocks)**0.5)) :
			for j in range(int((self.numBlocks)**0.5)) :
				self.blocks[(i,j)] = Block(self.start_set[int(((self.numBlocks)**0.5)*i)+j],i,j,self.numBlocks)

		for i in range(int((self.numBlocks)**0.5)) :
			for j in range(int((self.numBlocks)**0.5)) :
				self.assignAdjacent(i,j)

	def swapBlocks(self,block1,block2) :
			if not self.win :
				block1.number,block2.number = block2.number,block1.number
				block1.calculateOffset()
				block2.calculateOffset()
			self.declareWin()
			#self.nextHint()

	def assignAdjacent(self,i,j) :
		if i==0 :
			self.blocks[(i,j)].up,self.blocks[(i,j)].down = None , self.blocks[(i+1,j)]
		elif i== int((self.numBlocks**0.5)-1) :
			self.blocks[(i,j)].up,self.blocks[(i,j)].down = self.blocks[(i-1,j)] , None 
		else :
			self.blocks[(i,j)].up,self.blocks[(i,j)].down = self.blocks[(i-1,j)] , self.blocks[(i+1,j)] 

		if j==0 :
			self.blocks[(i,j)].left,self.blocks[(i,j)].right = None , self.blocks[(i,j+1)]
		elif j== int((self.numBlocks**0.5)-1) :
			self.blocks[(i,j)].left,self.blocks[(i,j)].right = self.blocks[(i,j-1)] , None 
		else :
			self.blocks[(i,j)].left,self.blocks[(i,j)].right = self.blocks[(i,j-1)] , self.blocks[(i,j+1)] 

	def declareWin(self) :
		block_number = [self.blocks[(i,j)].number for i in range(int(self.numBlocks**0.5))for j in range(int(self.numBlocks**0.5))]
		if(block_number==self.final_set) :
			self.win = True

	def getSolvable(self) :
		self.start_set	= [i for i in range(self.numBlocks)]
		inversion=0 
		while True :
			inversion = 0
			shuffle(self.start_set)
			for i in range(0,self.numBlocks-1) :
				for j in  range(i+1,self.numBlocks) :
					if (self.start_set[j] and self.start_set[i] and self.start_set[i]>self.start_set[j]) :
                				inversion+=1;
			if self.numBlocks%2!=0 or self.find0()%2!=0:
        			if inversion%2==0 : break
 
	def find0(self) :
		for i in range(int(self.numBlocks**0.5)-1,-1,-1) :
			for j in range(int(self.numBlocks**0.5)-1,-1,-1) :
				if self.start_set[i*(int(self.numBlocks**0.5))+j] == 0 :
					return int(self.numBlocks**0.5)-i;

	def display(self) :
		print("Index\t:\tActual_Pos\t:\tBlock_No\t:\tOffset")
		for i in range(int((self.numBlocks)**0.5)) :
			for j in range(int((self.numBlocks)**0.5)) :
				print(f"{(int((self.numBlocks)**0.5)*i+j)}\t:\t{(i,j)}\t\t:\t{self.blocks[(i,j)].number}\t\t:\t 				{(self.blocks[(i,j)].dx,self.blocks[(i,j)].dy)}")

