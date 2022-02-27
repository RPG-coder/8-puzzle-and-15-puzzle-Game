from puzzle import *
import numpy as np
import cv2

#Game GUI Classes
class GamePlay() :
	def __init__(self,puzzleCode,windowName,width,height) :
		self.width,self.height	= width,height-50
		self.puzzle_Code	= puzzleCode
		self.change		= True
		self.windowClose 	= False
		self.blockInfo	= []
		self.zeroBlock	= None
		self.row_size	= int((self.puzzle_Code+1)**0.5)
		self.image = np.zeros((self.width,self.height+50,3),np.uint8)
		self.game = Game(self.puzzle_Code)
		self.windowName = windowName
		self.lastMove   = None
		self.hint = -1

	def mainLoop(self) :
		cv2.setMouseCallback(self.windowName,self.mouseCall)
		while not self.windowClose :
			cv2.imshow(self.windowName,self.image)
			if self.change : 
				self.image = np.zeros((self.width,self.height+50,3),np.uint8)
				self.blockInfo = []
				self.draw()
				self.change = False
			key_pressed=cv2.waitKey(1)
			if key_pressed==27 : self.windowClose = True
			elif key_pressed==ord('r') or key_pressed==ord('R') : 
				self.game.reset_game()
				self.hint=-1
				self.change = True
			elif key_pressed==ord('h') or key_pressed==ord('H') : 
				#print(self.game.nextHint())
				self.hint,score = self.game.nextHint(self.lastMove)
				if self.hint != -1:
					self.change = True
				else:
					cv2.putText(self.image,"No moves available!!!",(int(width/2)-50,height-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)

	def draw(self) :
		for i in range(self.row_size) :
			for j in range(self.row_size) :
				start_point = (i*(self.width//self.row_size)+5,j*(self.height//self.row_size)+5)
				end_point   = ((i+1)*(self.width//self.row_size)-5,(j+1)*(self.height//self.row_size)-5)
				if self.game.blocks[(j,i)].number!=0 :
					color = (255,0,255)
					if self.game.blocks[(j,i)].number==self.hint : color = (0,255,0)
					cv2.rectangle(self.image,start_point,end_point,color,-1)
					text_pos = (start_point[0]+self.width//9,start_point[1]+self.height//7)
					cv2.putText(self.image,str(self.game.blocks[(j,i)].number),text_pos,cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
					cv2.putText(self.image,"Esc - Main Menu ",(width-150,height-30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
					cv2.putText(self.image,"R - Reset",(20,height-30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
					cv2.putText(self.image,"H - Hint",(20,height-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
					if self.game.win :
						cv2.putText(self.image,"You Win!!!",(int(width/2)-50,height-30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
					self.blockInfo.append((self.game.blocks[(j,i)],self.game.blocks[(j,i)].number,start_point,end_point))
				else :
					self.zeroBlock = self.game.blocks[(j,i)]


	def mouseCall(self,event,posx,posy,flag,param) :
		if event == cv2.EVENT_LBUTTONDOWN :
			block,number = self.getBlock(posx,posy)
			if block is not None or number!=-1 :
				if block in (self.zeroBlock.up,self.zeroBlock.down,self.zeroBlock.left,self.zeroBlock.right) :
					self.game.swapBlocks(self.zeroBlock,block)
					self.lastMove = self.zeroBlock
					self.change = True

	def getBlock(self,posx,posy) :
		for i in self.blockInfo :
			if i[2][0]<=posx<=i[3][0] and i[2][1]<=posy<=i[3][1] :
				return (i[0],i[1])
		return None,-1


#Main Program + Main Menu Creation
#Function Definition
def buttonPress(event,posx,posy,flag,param) :
	global difficulty
	if event == cv2.EVENT_LBUTTONDOWN :
		if width/2-50<=posx<=width/2+50 and height/2-100<=posy<=height/2-50 :
			difficulty=0
		elif (width/2)-50<=posx<=(width/2)+50 and (height/2)+50<=posy<=(height/2)+100 :
			difficulty=1 


#Main Program 
cv2.namedWindow("Puzzle-Game")
width,height = 450,450
mainMenuButton = []
difficulty = -1
cv2.setMouseCallback("Puzzle-Game",buttonPress)
while True :
	if cv2.waitKey(1) == 27 : break
	image = np.zeros((width,height,3),np.uint8)
	cv2.rectangle(image,(int(width/2)-50,int(height/2)-100),(int(width/2)+50,int(height/2)-50),(255,0,255),-1)
	cv2.rectangle(image,(int(width/2)-50,int(height/2)+50),(int(width/2)+50,int(height/2)+100),(255,0,255),-1)
	cv2.putText(image,"8-Puzzle",(int(width/2)-40,int(height/2)-70),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
	cv2.putText(image,"15-Puzzle",(int(width/2)-40,int(height/2)+75),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
	cv2.putText(image,"Esc - Exit ",(int(width/2)-40,int(height)-30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
	cv2.imshow("Puzzle-Game",image)
	if   difficulty == 0 :
		game8 = GamePlay(8,"Puzzle-Game",width,height)
		game8.mainLoop()
		difficulty = -1
		cv2.setMouseCallback("Puzzle-Game",buttonPress)
	elif difficulty == 1 :
		game8 = GamePlay(15,"Puzzle-Game",width,height)
		game8.mainLoop()
		difficulty = -1
		cv2.setMouseCallback("Puzzle-Game",buttonPress)
cv2.destroyAllWindows()
