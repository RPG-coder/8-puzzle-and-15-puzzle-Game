"""
    8-puzzle and 15-puzzle game is a puzzle game played by moving of tiles
    Copyright (C) 2018  Rahul Gautham Putcha

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    For more details on contact please do visit, https://rahulgputcha.com or email to rahulgautham95@gmail.com
	
"""

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
			self.oldMoves	= []
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
		self.score = 0
		self.reset_game()

	# Reset Game - Starting of Game or When 'R' button is Pressed
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
		self.oldMoves = [[self.blocks[(i,j)].number for i in range(int((self.numBlocks)**0.5)) for j in range(int((self.numBlocks)**0.5))]]
		self.score = self.calculateScore()

	# Exchange Blocks - Used for Swaping '0'_Block and clicked_Block
	def swapBlocks(self,block1,block2) :
			if not self.win :
				block1.number,block2.number = block2.number,block1.number
				block1.calculateOffset()
				block2.calculateOffset()
			if len(self.oldMoves)<=32 :
				self.oldMoves.append([self.blocks[(i,j)].number for i in range(int((self.numBlocks)**0.5)) for j in range(int((self.numBlocks)**0.5))])
			else :
				del self.oldMoves[0]
				self.oldMoves.append([self.blocks[(i,j)].number for i in range(int((self.numBlocks)**0.5)) for j in range(int((self.numBlocks)**0.5))])
			self.declareWin()

	# Assign Adjacent Blocks (up,down,left,right block) of Block[(i,j)]- For Movement Restriction
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

	#Declare Win - Check if user won the Game
	def declareWin(self) :
		self.score = self.calculateScore()
		if not self.score :
			self.win=True

	# Calculate Score -  lesser the score more chance to win the game
	# score = sigma(Block[(i,j)].dx + Block[(i,j)].dy) = Sum of position of all blocks relative to their original position
	def calculateScore(self) :
		sumd = 0
		for i in range(int((self.numBlocks)**0.5)) :
			for j in range(int((self.numBlocks)**0.5)) :
				if(self.blocks[(i,j)].number!=0) :
					sumd += self.blocks[(i,j)].dx+self.blocks[(i,j)].dy;
		return sumd;

	# Get Solvable - Using Inversion Algorithm
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

	# Next Hint - Computer Play or Choice using optimized Branch Bound Algorithm  -> returns BestRank obtained
	def nextHint(self,lastMove) :
		rank = {}
		oldScore  = self.calculateScore()
		bestScore = 999
		number	  = -1
		if not self.win :
				zeroBlock = None
				#Getting ZeroBlock
				for i in range(int((self.numBlocks)**0.5)) :
					for j in range(int((self.numBlocks)**0.5)) :
						if self.blocks[(i,j)].number == 0 : 
							zeroBlock = self.blocks[(i,j)]
				#Getting the Score for winning of each adjacent Block : Less Score More Chances
				if zeroBlock is not None :
					up,down,left,right = zeroBlock.up,zeroBlock.down,zeroBlock.left,zeroBlock.right
					for i in  up,down,left,right :
						if i is not None and (lastMove is None or lastMove.number!=i.number):
							self.swapBlocks(i,zeroBlock)
							nextMove = self.oldMoves[len(self.oldMoves)-1]
							del self.oldMoves[len(self.oldMoves)-1]
							score = self.calculateScore()
							if nextMove not in self.oldMoves :
								rank[i] = score
							self.swapBlocks(i,zeroBlock)
							del self.oldMoves[len(self.oldMoves)-1]

					#Getting the Best Score and removing all unnecessary ones
					if len(rank)>0 :
						bestScore = min(rank.values())
						rank = {i:value for i,value in list(rank.items()) if value==bestScore}
						if len(rank)>1 and bestScore<oldScore: 	#if there are more than one block, 
							#only one can fill the empty space,hences choosing most probable one
							for i in rank :
								self.swapBlocks(i,zeroBlock)
								nextMove = self.oldMoves[len(self.oldMoves)-1]
								del self.oldMoves[len(self.oldMoves)-1]
								if nextMove not in self.oldMoves :
									_,rank[i] = self.nextHint(zeroBlock)
								else : del self.oldMoves[len(self.oldMoves)-1]
								self.swapBlocks(i,zeroBlock)
								del self.oldMoves[len(self.oldMoves)-1]

							bestScore = min(rank.values())
							for i in rank : number,bestScore = i.number,rank[i]

						else :	#Otherwise, there is only one Block to Move then or most possibly can also be the next best way
							for i in rank : number,bestScore = i.number,rank[i]
					else :	#Otherwise, there is only one Block other than previously moved
						try:
							number,bestScore = i.number,bestScore
						except:
							return -1, -1
		return number,bestScore

'''
	# Rough display of the Block[(i,j)] for Debug purpose
	def display(self) :
		print("Index\t:\tActual_Pos\t:\tBlock_No\t:\tOffset")
		for i in range(int((self.numBlocks)**0.5)) :
			for j in range(int((self.numBlocks)**0.5)) :
				print(f"{(int((self.numBlocks)**0.5)*i+j)}\t:\t{(i,j)}\t\t:\t{self.blocks[(i,j)].number}\t\t:\t{(self.blocks[(i,j)].dx,self.blocks[(i,j)].dy)}")
'''
