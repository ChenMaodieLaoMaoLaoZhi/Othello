'''
同学们可以在get_AI_move函数上测试自己的程序，这只需要返回最佳的落子位置即可
部分大家可能用到的变量和函数汇总：
self.sleep_time = 0 机器对战的时候的停顿时间，在调试阶段，同学们可以设置为0
其他见作业说明文档：

如果同学们在做作业过程中发现有bug，可以联系代码提供者(助教：xhp@163.sufe.edu.cn/18317026869)
'''
import time
from tkinter import *
from tkinter.messagebox import *
from Othello import Othello
import random


class OthelloGUI:
    def __init__(self):
        self.root = Tk('黑白棋')
        self.root.title(" 黑白棋")
        self.black_tile = PhotoImage(file='black.png')
        self.white_tile = PhotoImage(file='white.png')
        self.board_bg = PhotoImage(file='board.png')
        self.info = PhotoImage(file='info2.png')
        self.imgs = [self.black_tile, self.white_tile, self.board_bg, self.info]
        self.cv = Canvas(self.root, bg='green', width=720, height=720)
        self.gameOver = False
        self.gameoverStr = 'Game Over!  Score:'
        self.mainBoard = self.getNewBoard()
        self.playerTile = 'black'
        self.computerTile = 'white'
        self.turn = 'player'
        self.othello = Othello()
        self.white_no_choose=False
        self.black_no_choose=False
        self.AI_player='2018110110-张三'
        self.sleep_time = 0  # 每次停留时间，在调试阶段可以设为0

    # 重置棋盘
    def resetBoard(self):
        '''
        初始化棋盘，黑白棋的最初棋盘上是有两个白棋和黑棋
        :return:
        '''
        for x in range(8):
            for y in range(8):
                self.mainBoard[x][y] = 'none'
        # Starting pieces:
        self.mainBoard[3][3] = 'black'
        self.mainBoard[3][4] = 'white'
        self.mainBoard[4][3] = 'white'
        self.mainBoard[4][4] = 'black'

    def getNewBoard(self):
        '''
        开局建立新棋盘，所有棋子的位置都置为None
        :return:
        '''
        board = []
        for i in range(8):
            board.append(['none'] * 8)
        return board

    # 复制棋盘
    def getBoardCopy(self, board):
        '''
        将传入棋盘的布局复制并返回
        :param board:传入的棋盘布局，是一个8*8的字符串数组
        :return:复制好的棋盘布局数组
        '''
        dupeBoard = self.getNewBoard()
        for x in range(8):
            for y in range(8):
                dupeBoard[x][y] = board[x][y]
        return dupeBoard

    def getScoreOfBoard(self, board):
        '''
        获取给定棋盘上黑白双方的棋子数，可以为真实的棋盘mainBoard或者虚拟的棋盘布局
        :param board:传入的棋盘布局
        :return:统计此棋盘布局中黑白棋子的个数dict
        '''
        b_score = 0
        w_score = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'black':
                    b_score += 1
                if board[x][y] == 'white':
                    w_score += 1
        return {'black': b_score, 'white': w_score}

    def makeMove(self, board, tile, x_start, y_start):
        '''
        将一个tile棋子放到(xstart, ystart),之后的棋盘局面，如果有翻转的棋子，将会翻转，
        传入的board是数组，是实参，所以board的值会改变
        :param board:传入棋盘的布局，由于是数组结构，是实参，会被改变，
        :param tile:棋子颜色的字符串，值为“white”或者“black”
        :param x_start:目标位置的x，取值为（0-7）
        :param y_start:目标位置的y，取值为（0-7）
        :return:落子成功则返回True、否则返回False
        '''
        tilesToFlip = self.othello.isValidMove(board, tile, x_start, y_start)
        if tilesToFlip == False:
            return False
        board[x_start][y_start] = tile
        for x, y in tilesToFlip:  # tilesToFlip是需要翻转的棋子列表
            board[x][y] = tile  # 翻转棋子
        return True

    def getValidMoves(self, board, tile):
        '''
        获取棋盘布局board下的可以落子的位置
        :param board: 当前棋盘的布局
        :param tile: 棋子颜色的字符串，值为“white”或者“black”
        :return:返回可以落子位置的list,如[[1,2],[2,3]]
        '''
        validMoves = []
        for x in range(8):
            for y in range(8):
                if self.othello.isValidMove(board, tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves

    # 电脑走法（随机走法，大家也可以写一些稍微复杂的算法自行测试）
    def getComputerMove(self, board, computerTile):
        '''
        将可能的走法打乱，选取第一个可走的位置
        :param board: 传入的棋盘
        :param computerTile: 电脑的棋子颜色的字符串，值为“white”或者“black”
        :return: 走法的数组[x,y],如[2,1] etc.
        '''
        # 获取所以合法走法
        possibleMoves = self.getValidMoves(board, computerTile)
        if not possibleMoves:  # 如果没有合法走法
            print("电脑没有合法走法")
            return None
        # 打乱所有合法走法
        random.shuffle(possibleMoves)
        return possibleMoves[0]


    def isGameOver(self, board):
        '''
        判断游戏是否结束，结束条件为：传入board全部不为空（"none"）
        或者全部为白色棋子、或者全部为黑色棋子，
        或者黑棋和白棋都没地方落子
        :param board:棋盘布局
        :return:游戏是否结束
        '''
        not_have_none = True
        # 棋盘上只剩一种棋子，游戏也结束
        only_white = True
        only_black = True
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'none':
                    not_have_none = False
                if board[x][y] == 'white':
                    only_black = False
                if board[x][y] == 'black':
                    only_white = False
        return not_have_none or only_white or only_black or (self.white_no_choose and self.black_no_choose)

    # 画棋盘背景
    def drawQiPan(self):
        img1 = self.imgs[2]
        self.cv.create_image((360, 360), image=img1)
        self.cv.pack()

    def drawAll(self):
        '''
        画出棋盘和当前布局self.mainBoard的棋子
        :return:
        '''
        self.drawQiPan()
        for x in range(8):
            for y in range(8):
                if self.mainBoard[x][y] == 'black':
                    self.cv.create_image((x * 80 + 80, y * 80 + 80), image=self.imgs[0])
                    self.cv.pack()
                elif self.mainBoard[x][y] == 'white':
                    self.cv.create_image((x * 80 + 80, y * 80 + 80), image=self.imgs[1])
                    self.cv.pack()

    def drawCanGo(self):
        '''
        获取当前可以落子的位置的提示信息
        :return:
        '''
        list1 = self.getValidMoves(self.mainBoard, self.playerTile)
        for m in list1:
            x = m[0]
            y = m[1]
            self.cv.create_image((x * 80 + 80, y * 80 + 80), image=self.imgs[3])
            self.cv.pack()

    def callback(self, event):
        '''
        用户走棋
        :param event:用户点击事件，用于获取用户点击位置的坐标。
        :return:
        '''
        # global turn
        # print ("clicked at", event.x, event.y,turn)
        # x=(event.x)//40  #换算棋盘坐标
        # y=(event.y)//40
        if self.gameOver is False and self.turn == 'computer':  # 没轮到玩家走棋
            return
        col = int((event.x - 40) / 80)  # 换算棋盘坐标
        row = int((event.y - 40) / 80)
        if self.mainBoard[col][row] != "none":
            showinfo(title="提示", message="已有棋子")
        if self.makeMove(self.mainBoard, self.playerTile, col, row):  # 将一个玩家棋子放到(col, row)
            if self.getValidMoves(self.mainBoard, self.computerTile) != []:
                self.turn = 'computer'
        # 电脑走棋
        if self.getComputerMove(self.mainBoard, self.computerTile) is None:
            self.turn = 'player'
            showinfo(title="玩家继续", message="玩家继续")
        else:
            self.computerGo()
        # 重画所有的棋子和棋盘
        self.drawAll()
        self.drawCanGo()
        if self.isGameOver(self.mainBoard):  # 游戏结束，显示双方棋子数量
            scorePlayer = self.getScoreOfBoard(self.mainBoard)[self.playerTile]
            scoreComputer = self.getScoreOfBoard(self.mainBoard)[self.computerTile]
            outputStr = self.gameoverStr + "玩家:" + str(scorePlayer) + ":" + "电脑:" + str(scoreComputer)
            if scorePlayer==scoreComputer:
                outputStr+=", 【平 局】"
            elif scorePlayer>scoreComputer:
                outputStr += ", 【玩家胜】"
            else:
                outputStr += ", 【电脑胜】"
            showinfo(title="游戏结束", message=outputStr)
            print(outputStr)

    def computerGo(self):
        '''
        电脑走棋
        :return:
        '''
        if self.gameOver is False and self.turn == 'computer':
            # print("move:",self.getComputerMove(self.mainBoard, self.computerTile) )
            x, y = self.getComputerMove(self.mainBoard, self.computerTile)  # 电脑AI走法
            # x,y =self.get_AI_move(self.computerTile)
            self.makeMove(self.mainBoard, self.computerTile, x, y)
            savex, savey = x, y
            # 玩家没有可行的走法了，则电脑继续，否则切换到玩家走
            if self.getValidMoves(self.mainBoard, self.playerTile) != []:
                self.turn = 'player'
            else:
                if self.getValidMoves(self.mainBoard, self.computerTile) != []:
                    showinfo(title="电脑继续", message="电脑继续")
                    self.computerGo()

    def random_move(self,tile):
        '''
        随机算法
        :param tile: 棋子的颜色
        :return: 落子位置[x,y]，如果没有合法的落子位置，返回false
        '''
        possibleMoves = self.getValidMoves(self.mainBoard, tile)
        if not possibleMoves:  # 如果没有合法走法
            print("{}棋没有合法走法".format(tile))
            return None
        # 打乱所有合法走法
        random.shuffle(possibleMoves)
        return possibleMoves[0]

    def get_baseline_1_move(self,tile):
        '''
        同学们可以换上自己写的其他的baseline的测试函数，与自己写的AI算法对弈
        :param tile:
        :return:
        '''
        weight=[
        [999,-20,20,20,20,20,-20,999], 
	    [-20,-30,5,5,5,5,-30,-20], 
	    [20,5,1,1,1,1,5,20],
	    [20,5,1,1,1,1,5,20],
	    [20,5,1,1,1,1,5,20],
        [20,5,1,1,1,1,5,20],
	    [-20,-30,5,5,5,5,-30,-20],
	    [999,-20,20,20,20,20,-20,999]
                ]
        
        def cal(board):
            cal = 0
            if tile == 'white':
                a12 = [1,-1] 
            else:
                a12 = [1,1]
            for i in range(0,8):
                for j in range(0,8):
                    if board[i][j] == tile:
                        cal+= -dispresion(board, i, j)*a12[1]
                    if board[i][j] == change_turn(tile):
                        cal-= -dispresion(board, i, j)*a12[1]
            return cal
        
        def change_turn(turn):
            #也能用于换tile
            if turn == 'player':
                return 'computer'
            elif turn == 'computer':
                return 'player'
            elif turn == 'white':
                return 'black'
            elif turn == 'black':
                return 'white'    
                       
        def dispresion(board,x0,y0):
            disprenum = 0
            if self.othello.isOnBoard(x0, y0 + 1) and board[x0][y0 + 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0, y0 - 1) and board[x0][y0 - 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 + 1, y0) and board[x0 + 1][y0] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 - 1, y0) and board[x0 - 1][y0] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 + 1, y0 + 1) and board[x0 + 1][y0 + 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 - 1, y0 - 1) and board[x0 - 1][y0 - 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 - 1, y0 + 1) and board[x0 - 1][y0 + 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 + 1, y0 - 1) and board[x0 + 1][y0 - 1] == 'none':
                disprenum += 1
            return disprenum
        
        def alphaBeta(currentboard,alpha, beta,destepth,cutile):
            #推断和预见接下来的几步
            #返回 alpha 和 beta 的值,分别对应 computer_min和 player_max的上界和下界
            if destepth == 0:
                return cal(currentboard)
            elif cutile == tile:
                for x,y in self.getValidMoves(currentboard, tile):
                    timeboard = self.getBoardCopy(currentboard)
                    self.makeMove(timeboard, cutile, x, y)
                    value = alphaBeta(timeboard, alpha, beta, destepth - 1, change_turn(cutile))
                    if value > alpha :
                        alpha = value
                    if not alpha < beta:
                        break
                return alpha
            else:
                for x,y in self.getValidMoves(currentboard, tile):
                    timeboard = self.getBoardCopy(currentboard)
                    self.makeMove(timeboard, cutile, x, y)
                    value = alphaBeta(timeboard, alpha, beta, destepth - 1, change_turn(cutile))
                    if value < beta:
                        beta = value
                    if not alpha < beta:
                        break
                return beta  
            
        self.AI_player = 'test'
        currentboard = self.getBoardCopy(self.mainBoard)
        cutile = str(tile)
        possibleMoves = self.getValidMoves(self.mainBoard, tile) 
        
        actions = []
        alpha1 = float("-inf")
        beta1 = float("inf")
        alpha1 = alphaBeta(currentboard, alpha1, beta1, 5, cutile)
        for x, y in possibleMoves:
            if Othello().isOnCorner(x, y):
                return x, y
            dubeboard = self.getBoardCopy(self.mainBoard)
            self.makeMove(dubeboard,tile,x,y)
            alpha2 = float("-inf")
            beta2 = float("inf")
            beta2 = alphaBeta(dubeboard, alpha2, beta2, 4, change_turn(tile))
            if alpha1 == beta2:
                # 按照α，β分数的匹配选择出走法
                print('the choice is:[{0},{1}]'.format(x,y))
                actions.append((x,y)) 
            
        if len(actions) == 1:
            return actions[0]
        else:
            mindispresion = float('inf')
            for x, y in actions:
                eatdispersion = 0
                tilesToFlip = self.othello.isValidMove(currentboard, tile, x,y)
                for xi,yi in tilesToFlip:
                    eatdispersion += dispresion(currentboard,xi,yi)
                if (eatdispersion + dispresion(currentboard, x, y)) < mindispresion:
                    global minxy
                    minxy = [x,y]
                    mindispresion = (eatdispersion + dispresion(currentboard, x, y))
        
        return minxy
        
    def get_baseline_2_move(self,tile):
        weight=[
        [999,-20,20,20,20,20,-20,999], 
	    [-20,-30,5,5,5,5,-30,-20], 
	    [20,5,1,1,1,1,5,20],
	    [20,5,1,1,1,1,5,20],
	    [20,5,1,1,1,1,5,20],
        [20,5,1,1,1,1,5,20],
	    [-20,-30,5,5,5,5,-30,-20],
	    [999,-20,20,20,20,20,-20,999]
                ]
        
        def cal(board):
            cal = 0
            if tile == 'white':
                a12 = [2,-1] 
            else:
                a12 = [1, 1]
            for i in range(0,8):
                for j in range(0,8):
                    if board[i][j] == tile:
                        cal+= (weight[i][j]*a12[0] - dispresion(board, i, j)*a12[1])
                    if board[i][j] == change_turn(tile):
                        cal-= (weight[i][j]*a12[0] - dispresion(board, i, j)*a12[1])
            return cal
        
        def change_turn(turn):
            #也能用于换tile
            if turn == 'player':
                return 'computer'
            elif turn == 'computer':
                return 'player'
            elif turn == 'white':
                return 'black'
            elif turn == 'black':
                return 'white'    
                       
        def dispresion(board,x0,y0):
            disprenum = 0
            if self.othello.isOnBoard(x0, y0 + 1) and board[x0][y0 + 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0, y0 - 1) and board[x0][y0 - 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 + 1, y0) and board[x0 + 1][y0] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 - 1, y0) and board[x0 - 1][y0] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 + 1, y0 + 1) and board[x0 + 1][y0 + 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 - 1, y0 - 1) and board[x0 - 1][y0 - 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 - 1, y0 + 1) and board[x0 - 1][y0 + 1] == 'none':
                disprenum += 1
            if self.othello.isOnBoard(x0 + 1, y0 - 1) and board[x0 + 1][y0 - 1] == 'none':
                disprenum += 1
            return disprenum
        
        def alphaBeta(currentboard,alpha, beta,destepth,cutile):
            #推断和预见接下来的几步
            #返回 alpha 和 beta 的值,分别对应 computer_min和 player_max的上界和下界
            if destepth == 0:
                return cal(currentboard)
            elif cutile == tile:
                for x,y in self.getValidMoves(currentboard, tile):
                    timeboard = self.getBoardCopy(currentboard)
                    self.makeMove(timeboard, cutile, x, y)
                    value = alphaBeta(timeboard, alpha, beta, destepth - 1, change_turn(cutile))
                    if value > alpha :
                        alpha = value
                    if not alpha < beta:
                        break
                return alpha
            else:
                for x,y in self.getValidMoves(currentboard, tile):
                    timeboard = self.getBoardCopy(currentboard)
                    self.makeMove(timeboard, cutile, x, y)
                    value = alphaBeta(timeboard, alpha, beta, destepth - 1, change_turn(cutile))
                    if value < beta:
                        beta = value
                    if not alpha < beta:
                        break
                return beta  
            
        self.AI_player = 'test'
        currentboard = self.getBoardCopy(self.mainBoard)
        cutile = str(tile)
        possibleMoves = self.getValidMoves(self.mainBoard, tile) 
        
        actions = []
        alpha1 = float("-inf")
        beta1 = float("inf")
        alpha1 = alphaBeta(currentboard, alpha1, beta1, 4, cutile)
        for x, y in possibleMoves:
            if Othello().isOnCorner(x, y):
                return x, y
            dubeboard = self.getBoardCopy(self.mainBoard)
            self.makeMove(dubeboard,tile,x,y)
            alpha2 = float("-inf")
            beta2 = float("inf")
            beta2 = alphaBeta(dubeboard, alpha2, beta2, 3, change_turn(tile))
            if alpha1 == beta2:
                # 按照α，β分数的匹配选择出走法
                print('the choice is:[{0},{1}]'.format(x,y))
                actions.append((x,y)) 
            
        if len(actions) == 1:
            return actions[0]
        else:
            mindispresion = float('inf')
            for x, y in actions:
                eatdispersion = 0
                tilesToFlip = self.othello.isValidMove(currentboard, tile, x,y)
                for xi,yi in tilesToFlip:
                    eatdispersion += dispresion(currentboard,xi,yi)
                if (eatdispersion + dispresion(currentboard, x, y)) < mindispresion:
                    global minxy
                    minxy = [x,y]
                    mindispresion = (eatdispersion + dispresion(currentboard, x, y))
        
        return minxy
        return None

    def get_baseline_move(self,tile,baseline_num=0):
        '''
        获取baseline的落子位置
        :param tile: 棋子的颜色的字符串，值为“white”或者“black”
        :param baseline_num: baseline的编号
        :return: 返回一个最佳的落子位置[x,y]，如果没有落子位置或baseline编号不合规范，返回None
        '''
        if baseline_num==0:
            return self.random_move(tile)
        elif baseline_num==1:
            return self.get_baseline_1_move(tile)
        elif baseline_num==2:
            return self.get_baseline_2_move(tile)
        else:
            return None

    def get_AI_move(self,tile):
        '''
        这里是同学们需要实现的策略，默认是随机算法，主要是为了让程序跑起来
        同学们需要删掉return这一行，换上自己的算法
        程序的第一行为:self.AI_player='2018110110-张三'，替换成自己的学号-姓名，方便后续程序自动批阅
        :param tile:  棋子颜色的字符串，值为“white”或者“black”
        :return:  返回一个最佳的落子位置[x,y]，如果当前棋子没有可走位置，返回None
        '''
        '''
        同学们可以换上自己写的其他的baseline的测试函数，与自己写的AI算法对弈
        :param tile:
        :return:
        '''
        weight=[
        [70,-20,20,20,20,20,-20,70], 
	    [-20,-30,5,5,5,5,-30,-20], 
	    [20,5,1,1,1,1,5,20],
	    [20,5,1,1,1,1,5,20],
	    [20,5,1,1,1,1,5,20],
        [20,5,1,1,1,1,5,20],
	    [-20,-30,5,5,5,5,-30,-20],
	    [70,-20,20,20,20,20,-20,70]
                ]
        maxdep=5
        def cal(board,cutile):
            res=0
            for i in range(0,8):
                another=''
                if cutile=='white':
                    another='black'
                else:
                    another='white'
                for j in range(0,8):
                    if board[i][j]==cutile:
                        res+=weight[i][j]
                    if board[i][j]==another:
                        res-=weight[i][j]
            return res
        
        def  iscorner(x,y):
            return (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7)
        
        def change_turn(turn):
            #也能用于换tile
            if turn == 'player':
                return 'computer'
            elif turn == 'computer':
                return 'player'
            elif turn == 'white':
                return 'black'
            elif turn == 'black':
                return 'white'    
            
        def alphabeta(dep,board,cutile,a,b):
            if dep>maxdep:
                return None,cal(board,cutile)
            
            moves=self.getValidMoves(board,cutile)
            if not moves:
                return None,cal(board,cutile)
            
            MAX=-1e9
            MIN=1e9 
            action=[]
            if cutile==tile:
                nxt=change_turn(cutile)
                for move in moves:
                    if iscorner(move[0], move[1]):
                        return move,cal(board,cutile)
                    copybo=self.getBoardCopy(board)
                    self.makeMove(copybo,cutile,move[0],move[1])
                    pos,now=alphabeta(dep+1,copybo,nxt,a,b)
                    if a<now:
                        if b<now and move is not None:
                            return move,now
                        a=now
                    if now>MAX:
                        MAX=now
                        action=move
            else:
                nxt=change_turn(cutile)
                for move in moves:
                    if iscorner(move[0], move[1]):
                        return move,cal(board,cutile)
                    copybo=self.getBoardCopy(board)
                    self.makeMove(copybo,cutile,move[0],move[1])
                    pos,now=alphabeta(dep+1,copybo,nxt,a,b)
                    if b>now:
                        if a>now and move is not None:
                            return move,now
                        b=now
                    if now<MIN:
                        MIN=now
                        action=move

            if cutile == tile:
                return action,MAX
            else:
                return action,MIN
        
        board = self.getBoardCopy(self.mainBoard)
        self.AI_player = 'best-曹'
        action,res=alphabeta(0,board,tile,-1e9,1e9)            
        print(action)
        return action

        return None

    def white_move(self, tile='white'):
        '''
        此处为执白棋的程序需要实现的策略，此处为AI执白
        :param tile: 棋子颜色的字符串，值为“white”或者“black”,在此函数中，默认为白色！
        :return: 返回一个最佳的落子位置[x,y]
        '''
        return self.get_baseline_move(tile,2)
        #return self.get_AI_move(tile)

    def black_move(self, tile='black'):
        '''
        此处为执黑棋的程序需要实现的策略，此处为随机策略执黑
        :param tile: 棋子颜色的字符串，值为“white”或者“black”,在此函数中，默认为黑色！
        :return: 返回一个最佳的落子位置[x,y]
        '''
        # baseline的策略也可自定义，通过设置get_baseline_move函数的baseline_num进行调用
        #return self.get_baseline_move(tile,2)
        return self.get_AI_move(tile)

    def program_go(self, playerTile):
        '''
        程序走棋，交叉传入“white”、“black”字符串，交替执行走棋操作
        :param playerTile:当前玩家的棋子颜色
        :return:
        '''
        self.playerTile = playerTile
        self.drawAll()
        self.drawCanGo()
        self.root.update()
        time.sleep(self.sleep_time)
        if playerTile == 'white':
            can_move = self.white_move()
            if can_move is None:
                self.white_no_choose=True
                self.turn = 'black'
                print("program 2 【白棋】 没有走法")
                return
            else:
                self.white_no_choose=False
        elif playerTile == 'black':
            can_move = self.black_move()
            if can_move is None:
                self.black_no_choose=True
                print("program 1 【黑棋】 没有走法")
                self.turn = 'white'
                return
            else:
                self.black_no_choose=False
        x, y = can_move
        self.makeMove(self.mainBoard, playerTile, x, y)
        if self.isGameOver(self.mainBoard):  # 游戏结束，显示双方棋子数量
            self.gameOver=True
            # self.afterGameOver()

    def afterGameOver(self):
        self.drawAll()
        self.root.update()
        self.gameOver = True
        black_score = self.getScoreOfBoard(self.mainBoard)["black"]
        white_score = self.getScoreOfBoard(self.mainBoard)["white"]
        outputStr = self.gameoverStr + "白棋:" + str(white_score) + ":" + "黑棋:" + str(black_score)
        if black_score == white_score:
            outputStr += ", 【平 局】"
        elif black_score > white_score:
            outputStr += ", 【黑棋胜】"
        else:
            outputStr += ", 【白棋胜】"
        print(outputStr)
        showinfo(title="游戏结束", message=outputStr)

    def whoGoesFirst(self, mode=0):
        '''
        决定谁先走的函数，在人机对战模式下，mode==0，不建议修改！！
        因为机器对战不涉及谁先手的问题
        :param mode:0是人机对战，1是机器对战
        :return:先手的角色
        '''
        if mode == 0:
            if random.randint(0, 1) == 0:
                return 'computer'
            else:
                return 'player'
        else:
            return 'black'

    # GUI 界面启动
    def start(self, mode=0):
        '''
        GUI 界面启动函数
        黑白棋的规则是执黑先行！
        :param mode: 对战模式，默认为人机对战模式0，如果需要程序对战，请设置mode=1
        :return:
        '''
        self.resetBoard()
        if mode == 0:
            self.turn = self.whoGoesFirst()
            showinfo(title="游戏开始提示", message=self.turn + "先走!")
            print(self.turn, "先走!")

            if self.turn == 'player':
                self.playerTile = 'black'
                self.computerTile = 'white'
            else:
                self.playerTile = 'white'
                self.computerTile = 'black'
                self.computerGo()
            # 设置窗口
            self.cv = Canvas(self.root, bg='green', width=720, height=720)
            # 重画所有的棋子和棋盘
            self.drawAll()
            self.drawCanGo()
            self.cv.bind("<Button-1>", self.callback)
            self.root.update()
        elif mode == 1:
            for i in range(40):
                if not self.isGameOver(self.mainBoard):
                    self.program_go("black")
                    self.program_go("white")
                else:
                    self.afterGameOver()
                    break
        else:
            print("mode 参数有误！")
            return
        self.cv.pack()
        self.root.mainloop()


if __name__ == '__main__':
    # mode=0 是人机对战模式、mode=1是机器对战模式
    OthelloGUI().start(mode=1)
