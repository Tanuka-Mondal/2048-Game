from tkinter import *
from tkinter import messagebox
import random

class Board:
    backgroundColor={

        '2': '#ffea00',
        '4': '#eb7610',
        '8': '#ff0000',
        '16': '#ff00b3',
        '32': '#2b00ff',
        '64': '#084f1b',
        '128': '#00ff44',
        '256': '#00fffb',
        '512': '#7300ff',
        '1024': '#017573',
        '2048': '#ff00e1',
    }
    color={
        '2': '#ff0000',
        '4': '#f7f2f2',
        '8': '#f7f2f2',
        '16': '#f7f2f2',
        '32': '#f7f2f2',
        '64': '#f7f2f2',
        '128': '#2b00ff',
        '256': '#2b00ff',
        '512': '#f7f2f2',
        '1024': '#f7f2f2',
    }

    def __init__(self):
        self.n=4
        self.window=Tk()
        self.window.title('2048 Game')
        self.gameArea=Frame(self.window,bg= 'black')
        self.board=[]
        self.gridCell=[[0]*4 for i in range(4)]
        self.compress=False
        self.merge=False
        self.moved=False
        self.score=0

        for i in range(4):
            rows=[]
            for j in range(4):
                l=Label(self.gameArea,text='',bg='black',
                font=('verdana',22,'bold'),width=4,height=2)
                l.grid(row=i,column=j,padx=7,pady=7)

                rows.append(l);
            self.board.append(rows)
        self.gameArea.grid()

    def Rev(self):
        for n in range(4):
            i=0
            j=3
            while(i<j):
                self.gridCell[n][i],self.gridCell[n][j]=self.gridCell[n][j],self.gridCell[n][i]
                i+=1
                j-=1

    def Trans(self):
        self.gridCell=[list(t)for t in zip(*self.gridCell)]

    def Compress_Box(self):
        self.compress=False
        var1=[[0] *4 for i in range(4)]
        for i in range(4):
            count=0
            for j in range(4):
                if self.gridCell[i][j]!=0:
                    var1[i][count]=self.gridCell[i][j]
                    if count!=j:
                        self.compress=True
                    count+=1
        self.gridCell=var1

    def Merge_Box(self):
        self.merge=False
        for i in range(4):
            for j in range(4 - 1):
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j + 1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True

    def Random_Cell(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    cells.append((i, j))
        var2=random.choice(cells)
        i=var2[0]
        j=var2[1]
        self.gridCell[i][j]=2
    
    def Merge_Check(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
        
        for i in range(3):
            for j in range(4):
                if self.gridCell[i+1][j] == self.gridCell[i][j]:
                    return True
        return False

    def Colour_Box(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j]==0:
                    self.board[i][j].config(text='',bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),
                    bg=self.backgroundColor.get(str(self.gridCell[i][j])),
                    fg=self.color.get(str(self.gridCell[i][j])))

class Game:
    def __init__(self,myGame):
        self.myGame=myGame
        self.end=False
        self.won=False

    def start(self):
        self.myGame.Random_Cell()
        self.myGame.Random_Cell()
        self.myGame.Colour_Box()
        self.myGame.window.bind('<Key>', self.link_keys)
        self.myGame.window.mainloop()
    
    def link_keys(self,event):
        if self.end or self.won:
            return

        self.myGame.compress = False
        self.myGame.merge = False
        self.myGame.moved = False

        My_Key=event.keysym

        if My_Key=='Up':
            self.myGame.Trans()
            self.myGame.Compress_Box()
            self.myGame.Merge_Box()
            self.myGame.moved = self.myGame.compress or self.myGame.merge
            self.myGame.Compress_Box()
            self.myGame.Trans()

        elif My_Key=='Down':
            self.myGame.Trans()
            self.myGame.Rev()
            self.myGame.Compress_Box()
            self.myGame.Merge_Box()
            self.myGame.moved = self.myGame.compress or self.myGame.merge
            self.myGame.Compress_Box()
            self.myGame.Rev()
            self.myGame.Trans()

        elif My_Key=='Left':
            self.myGame.Compress_Box()
            self.myGame.Merge_Box()
            self.myGame.moved = self.myGame.compress or self.myGame.merge
            self.myGame.Compress_Box()

        elif My_Key=='Right':
            self.myGame.Rev()
            self.myGame.Compress_Box()
            self.myGame.Merge_Box()
            self.myGame.moved = self.myGame.compress or self.myGame.merge
            self.myGame.Compress_Box()
            self.myGame.Rev()
        else:
            pass

        self.myGame.Colour_Box()
        print(self.myGame.score)

        var4=0
        for i in range(4):
            for j in range(4):
                if(self.myGame.gridCell[i][j]==2048):
                    var4=1
                    break

        if(var4==1): #found 2048
            self.won=True
            messagebox.showinfo('2048', message='Congratulations!!!')
            print("Winner")
            return

        for i in range(4):
            for j in range(4):
                if self.myGame.gridCell[i][j]==0:
                    var4=1
                    break

        if not (var4 or self.myGame.Merge_Check()):
            self.end=True
            messagebox.showinfo('2048','Alas! Game Over!!!')
            print("Over")

        if self.myGame.moved:
            self.myGame.Random_Cell()
        
        self.myGame.Colour_Box()
    

myGame =Board()
game2048 = Game( myGame)
game2048.start()