
import pygame
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import queue

# Program

screen = pygame.display.set_mode((800,600))
screen.fill((255,255,255))

# Each Coordinate Definition
 
class spot:
    def __init__(self,x,y):
        self.i=x
        self.j=y
        self.visited=0
        self.neighbors=[]
        self.obs= False
        self.value=1

    def show(self,color,st):
        val = self.i==0 or self.i==row-1 or self.j==0 or self.j==cols-1
        if val:
            self.obs = True
            self.path(Img)
        else:
            pygame.draw.rect(screen,color,(round(self.j*w),round(self.i*h),round(w),round(h)),st)
        
        pygame.display.update()

    def path(self,image):
        screen.blit(image,(round(self.j*w),round(self.i*h),round(w),round(h)))
        pygame.display.update()
     
    def addNeighbors(self,grid):
        i = self.i
        j = self.j
        if i<row-1 and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i>1 and grid[self.i-1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j>1 and grid[i][self.j -1].obs == False:
            self.neighbors.append(grid[i][self.j - 1])
        if j<cols-1 and grid[i][self.j + 1].obs == False:
            self.neighbors.append(grid[i][self.j + 1])
            


    
# dimensions of grid
cols = 40
row = 30

# dimensions of each box
w = 20
h = 20

# Loading images

Img = pygame.image.load('cross.png').convert_alpha()
Img = pygame.transform.scale(Img, (20, 20))
startIcon = pygame.image.load('start.jpg')
startIcon = pygame.transform.scale(startIcon,(20,20))
endIcon = pygame.image.load('end.png')
endIcon = pygame.transform.scale(endIcon,(20,20))

# Create 2d array
grid= [0 for i in range(cols)]
for i in range(row):
    grid[i]=[0 for j in range(cols)]

# Create Spots
for j in range(cols):
    for i in range(row):
        grid[i][j]= spot(i,j)


#Show rect
for i in range(row):
    for j in range(cols):
        grid[i][j].show((127,255,230),1)

# On submit
def submit():
    global start
    global end
    st=startbox.get().split(',')
    ed=endbox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()


# Input Box
window= Tk()
window.title('Input Values')
heading1=Label(window,text="Enter Values",bd=1)
heading2=Label(window,text="range: 0<row<29,0<column<39")
label1=Label(window,text="Start(row,col)")
startbox=Entry(window)
label2=Label(window,text='End(row,col)')
endbox=Entry(window)
var=IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)
submit = Button(window,text='submit',command=submit)

# Griding
heading1.grid(columnspan=2,row=0)
heading2.grid(columnspan=2,row=1)
label1.grid(row=2,column=0)
startbox.grid(row=2,column=1,pady=3)
label2.grid(row=3,column=0)
endbox.grid(row=3,column=1,pady=3)
showPath.grid(columnspan=2,row=4)
submit.grid(columnspan =2,row =5)

window.update()
mainloop()


pygame.init()

def mousePress(x):
    t=x[0]
    w=x[1]
    g2 = t // (20)
    g1 = w // (20)
    access = grid[g1][g2]
    if access != start and access != end:
        if access.obs == False:
            access.show((0,0,0),0)
            access.obs = True


end.path(endIcon)
start.path(startIcon)

loop =True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

for i in range(row):
    for j in range(cols):
        grid[i][j].addNeighbors(grid)



def BFS():
    Q = queue.Queue()
    Q.put(start)
    start.visited = True
    pathMap = {start : 'Null' }
    while(not Q.empty()):
        pt = Q.get()
        if pt == end:
            break
        if( pt != start and var):
            pt.show((0,255,255),0)
        for nodes in pt.neighbors:
            if nodes.visited == False:
                nodes.visited = True
                pathMap[nodes] = pt
                if nodes !=end  and var:
                    nodes.show((0,0,139),0)
                Q.put(nodes)
    
    count = 0
    if end in pathMap.keys():
        child = end
        while pathMap[child] != start and pathMap[child] != 'Null':
            count+=1
            parent = pathMap[child]
            parent.show((34,139,34),0)
            child = parent
    
    else: count = -1

    printmessage(count)

# Message print
def printmessage(count):
    if count== -1:
        mssg='Path Not Found '
    else:
        mssg = 'The distance \n to the location is ' + str(count) + ' blocks away'
    Tk().wm_withdraw()
    messagebox.showinfo('message',mssg)


    while True:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.KEYDOWN or event.type==pygame.QUIT:
                pygame.quit()
                sys.exit('Thankyou for using the application :)')


BFS()






