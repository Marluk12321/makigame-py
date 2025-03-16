import os
import time
import random
import contextlib


try:
    import msvcrt

    def getch():
        return msvcrt.getch()

    def getchmaybe():
        if msvcrt.kbhit():
            return msvcrt.getch()
        return b''

    def cls():
        os.system("cls")

    @contextlib.contextmanager
    def realtime():
        yield
except ImportError:
    import fcntl, select, sys, tty, termios

    def getch():
        fd = sys.stdin.fileno()  # Get the file descriptor for standard input
        old_settings = termios.tcgetattr(fd)  # Save current terminal settings
        try:
            tty.setraw(fd)  # Switch to raw mode (disable buffering)
            return sys.stdin.read(1).encode()  # Read a single character
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restore settings

    def getchmaybe():
        dr, _, _ = select.select([sys.stdin], [], [], 0)  # Check input
        if dr != []:
            read_descriptor = dr[0]
            c = read_descriptor.read(1)  # Read a single character
            termios.tcflush(sys.stdin, termios.TCIFLUSH)  # Discard other characters
            return c.encode()
        return b''

    def cls():
        os.system("clear")

    @contextlib.contextmanager
    def realtime():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)  # Save old settings
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)  # Save old flags
        tty.setraw(fd)  # Set raw mode (for instant input)
        fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)  # Make stdin non-blocking
        try:
            yield
        finally:
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)  # Reset stdin flags
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restore settings


class drawing:

    def newln(self,brredova):
        for self.i in range(brredova): print(end="\r\n")

    def space(self,brrazmaka):
        self.razmaci=""
        for self.i in range(brrazmaka): self.razmaci+=" "
        return self.razmaci

    def line(self):
        self.ispis=""
        for self.i in range(79): self.ispis+="-"
        print(self.ispis,end="\r\n")

    def drawlives(self):
        self.ispis="  Lives:"
        for self.i in range(3-self.lives): self.ispis+=" X"
        for self.i in range(self.lives): self.ispis+=" O"
        return self.ispis

    def time(self):
        self.ispis="Time elapsed: "
        self.ispis+=str(self.tt//60//10)+str(self.tt//60%10)+":"+str(self.tt%60//10)+str(self.tt%60%10)
        return self.ispis

class components(drawing):

    def top(self,ver):
        cls()
        if ver=="ws": print(self.space(24)+"W/S - menu navigation, E - select",end="\r\n")
        elif ver=="ad": print(self.space(24)+"A/D - menu navigation, E - select",end="\r\n")
        elif ver=="q": print(self.space(36)+"Q - back",end="\r\n")
        elif ver=="g": print(self.drawlives()+self.space(45)+self.time(),end="\r\n")
        self.line()

    def menustart(self):
        self.newln(8)
        for self.j in range(len(self.startwrt)):
            if self.startpos==self.j:
                print(self.space(35)+"> "+self.startwrt[self.j].upper()+" <",end="\r\n")
            else: print(self.space(37)+self.startwrt[self.j],end="\r\n")
            self.newln(1)
        self.newln(7)
        self.line()

    def info(self):
        self.newln(6)
        print(self.space(25)+"Use W,A,S,D to move,",end="\r\n")
        print(self.space(25)+"P to pause or Q to exit",end="\r\n")
        self.newln(1)
        print(self.space(25)+"Hitting an asteroid makes you",end="\r\n")
        print(self.space(25)+"lose one of your 3 lives.",end="\r\n")
        print(self.space(25)+"Try dodging the incoming asteroids.",end="\r\n")
        print(self.space(25)+"When the asteroids stop coming",end="\r\n")
        print(self.space(25)+"prepare yourself!",end="\r\n")
        self.newln(7)
        self.line()

    def endscrn(self,ver):
        if ver=="q":
            self.newln(9)
            print(self.space(25)+"Are you sure you want to quit?",end="\r\n")
        elif ver=="go":
            self.newln(7)
            print(self.space(35)+"GAME OVER!",end="\r\n")
            self.newln(3)
            print(self.space(37)+"Retry:",end="\r\n")
        self.newln(1)
        if self.quitpos: print(self.space(34)+" yes  / >NO<",end="\r\n")
        else: print(self.space(34)+">YES< /  no",end="\r\n")
        if ver=="q": self.newln(9)
        elif ver=="go": self.newln(7)
        self.line()

    def pausescrn(self):
        self.newln(7)
        print(self.space(35)+"Game paused",end="\r\n")
        self.newln(2)
        for self.j in range(len(self.pausewrt)):
            if self.pausepos==self.j:
                print(self.space(35)+"> "+self.pausewrt[self.j].upper()+" <",end="\r\n")
            else: print(self.space(37)+self.pausewrt[self.j],end="\r\n")
            self.newln(1)
        self.newln(7)
        self.line()

    def main(self):
        self.instructions=self.ai.drawcalc(self.char,self.enemy)
        for self.i in range(len(self.instructions)):
            if type(self.instructions[self.i])==type(1): continue
            elif self.instructions[self.i]=="nl": self.newln(self.instructions[self.i+1])
            elif self.instructions[self.i]=="ch":
                print(self.char.draw(self.instructions[self.i+1]),end="\r\n")
            elif self.instructions[self.i]=="en":
                print(self.enemy.draw(self.instructions[self.i+1],self.instructions[self.i+2]),end="\r\n")
            elif self.instructions[self.i]=="ench":
                self.ispis=self.enemy.draw(self.instructions[self.i+1],self.instructions[self.i+2])
                self.ispis+=self.char.draw(self.instructions[self.i+3])
                print(self.ispis,end="\r\n")
            elif self.instructions[self.i]=="chen":
                self.ispis=self.char.draw(self.instructions[self.i+1])
                self.ispis+=self.enemy.draw(self.instructions[self.i+2],self.instructions[self.i+3])
                print(self.ispis,end="\r\n")
        self.line()

class menu(components):

    startwrt=["Start","Instructions","Quit"]
    pausewrt=["Resume","Quit"]
    menumoves=[b'w',b's',b'q',b'e',b'a',b'd']

    def __init__(self):
        self.startpos=0

    def start(self):
        self.c=''
        while 1:
            self.top("ws")
            self.menustart()
            self.c=getch()
            if self.c==self.menumoves[0]:
                self.startpos-=1
                self.startpos%=3
            elif self.c==self.menumoves[1]:
                self.startpos+=1
                self.startpos%=3
            elif self.c==self.menumoves[3]:
                if self.startpos==0: return 0
                if self.startpos==1: self.instructions()
                if self.startpos==2:
                    if self.end("q"):
                        cls()
                        break

    def instructions(self):
        while self.c!=self.menumoves[2]:
            self.top("q")
            self.info()
            self.c=getch()

    def end(self,ver):
        self.quitpos=0
        while 1:
            self.top("ad")
            self.endscrn(ver)
            self.c=getch()
            if self.c==self.menumoves[4] and self.quitpos: self.quitpos=0
            elif self.c==self.menumoves[5] and not self.quitpos: self.quitpos=1
            elif self.c==self.menumoves[3]:
                return not self.quitpos

    def pause(self):
        self.pausepos=0
        while 1:
            self.top("ws")
            self.pausescrn()
            self.c=getch()
            if self.c==self.menumoves[0]:
                self.pausepos-=1
                self.pausepos%=2
            if self.c==self.menumoves[1]:
                self.pausepos+=1
                self.pausepos%=2
            if self.c==self.menumoves[3]:
                if self.pausepos==0: return 0
                elif self.pausepos==1:
                    if self.end("q"): return 1

class ai:

    def __init__(self):
        self.spawnlocs=[[0,4,8,12,16],[1,5,9,13,17]]
        self.setup()

    def setup(self):
        self.mode=[10,1]

    def drawcalc(self,char,enemy):
        self.instructions=[]
        self.encount=0
        self.chardone=0
        for self.i in range(21):
            if self.encount<len(enemy.exists) and enemy.exists[self.encount] and self.i in range(enemy.y[self.encount],enemy.y[self.encount]+4):
                if not self.chardone and self.i==char.y:
                    if char.x<enemy.x[self.encount]:
                        self.instructions+=["chen",char.x]
                        self.instructions+=[enemy.x[self.encount]-char.x-len(char.draw(0)),self.i-enemy.y[self.encount]]
                    else:
                        self.instructions+=["ench",enemy.x[self.encount],self.i-enemy.y[self.encount]]
                        self.instructions+=[char.x-enemy.x[self.encount]-len(enemy.draw(0,0))]
                    self.chardone=1
                else: self.instructions+=["en",enemy.x[self.encount],self.i-enemy.y[self.encount]]
                if self.i-enemy.y[self.encount]==len(enemy.rows)-1: self.encount+=1
            elif not self.chardone and self.i==char.y:
                self.instructions+=["ch",char.x]
                self.chardone=1
            elif len(self.instructions)>=2 and self.instructions[len(self.instructions)-2]=="nl":
                self.instructions[len(self.instructions)-1]+=1
            else: self.instructions+=["nl",1]
        return self.instructions

    def spawncalc(self,char,enemy,t):
        if 0 not in enemy.exists or not t: return
        if not self.mode[0]:
            self.mode[0]=10
            self.mode[1]=int(random.random()*3)
        if self.mode[1]:
            self.counter=0
            while self.counter<100:
                self.loc=int(random.random()*17)
                self.test=1
                for self.i in range(len(enemy.exists)):
                    if not enemy.exists[self.i]: break
                    if self.loc in range(enemy.y[self.i]-3,enemy.y[self.i]+4):
                        self.test=0
                        break
                if self.test: break
                self.counter+=1
            if self.counter<100:
                self.spd=int(random.random()*4+3)
                if self.spd==5: self.spd=6
                enemy.spawn(self.loc,self.spd)
            self.mode[0]-=1
        else:
            if 1 in enemy.exists: return
            while 1:
                self.emptyrow=int(random.random()*6)
                if abs(char.y-self.emptyrow*4): break
            if abs(char.y-self.emptyrow*4) in range(1,6): self.spd=6
            elif abs(char.y-self.emptyrow*4) in range(6,11): self.spd=4
            elif abs(char.y-self.emptyrow*4) in range(11,16): self.spd=3
            else: self.spd=2
            for self.i in range(len(self.spawnlocs[0])):
                if self.i>=self.emptyrow: enemy.spawn(self.spawnlocs[1][self.i],self.spd)
                else: enemy.spawn(self.spawnlocs[0][self.i],self.spd)
            self.mode=[10,1]

    def collisioncalc(self,char,enemy):
        for self.i in range(len(enemy.exists)):
            if not enemy.exists[self.i]: break
            self.yrange=range(enemy.y[self.i],enemy.y[self.i]+len(enemy.rows))
            self.xrange=range(enemy.x[self.i]-len(char.draw(0))+1,enemy.x[self.i]+len(enemy.draw(0,0)))
            if char.y in self.yrange and char.x in self.xrange:
                enemy.despawn(self.i)
                enemy.sort()
                return 1
        return 0

class char(components):

    def __init__(self):
        self.setup()

    def setup(self):
        self.x=2
        self.y=10

    def move(self,c):
        if c==b'a' and self.x>1: self.x-=2
        elif c==b'd' and self.x<71: self.x+=2
        elif c==b'w' and self.y>0: self.y-=1
        elif c==b's' and self.y<20: self.y+=1

    def draw(self,relpos):
        return self.space(relpos)+"=)#II#>"

class enemy(components):

    def __init__(self):
        self.rows=["/#####\\"]
        self.rows+=["#[   ]#"]
        self.rows+=["#[   ]#"]
        self.rows+=["\\#####/"]
        self.setup()

    def setup(self):
        self.exists=[0,0,0,0,0]
        self.x=[0,0,0,0,0]
        self.y=[0,0,0,0,0]
        self.speed=[0,0,0,0,0]

    def spawn(self,y,spd):
        if 0 not in self.exists: return
        for self.i in range(len(self.exists)):
            if self.exists[self.i]:
                if self.y[self.i]==y: return
                else: continue
            self.exists[self.i]=1
            self.x[self.i]=72
            self.y[self.i]=y
            self.speed[self.i]=spd
            break
        self.sort()

    def despawn(self,num):
        self.exists[num]=0
        self.x[num]=0
        self.y[num]=0
        self.speed[num]=0

    def sort(self):
        for self.i in range(len(self.exists)-1):
            if self.exists[self.i]: continue
            if 1 in self.exists[self.i:]:
                for self.j in range(self.i,len(self.exists)):
                    if self.exists[self.j]:
                        self.exists[self.i]=1
                        self.x[self.i]=self.x[self.j]
                        self.y[self.i]=self.y[self.j]
                        self.speed[self.i]=self.speed[self.j]
                        self.despawn(self.j)
                        break
        for self.i in range(len(self.exists)-1,0,-1):
            if not self.exists[self.i]: continue
            if self.y[self.i]<self.y[self.i-1]:
                self.temp=[self.x[self.i],self.y[self.i],self.speed[self.i]]
                self.x[self.i]=self.x[self.i-1]
                self.y[self.i]=self.y[self.i-1]
                self.speed[self.i]=self.speed[self.i-1]
                self.x[self.i-1]=self.temp[0]
                self.y[self.i-1]=self.temp[1]
                self.speed[self.i-1]=self.temp[2]

    def move(self):
        self.despawned=0
        for self.i in range(len(self.exists)):
            if self.exists[self.i]:
                if self.x[self.i]>self.speed[self.i]-1: self.x[self.i]-=self.speed[self.i]
                else:
                    self.despawn(self.i)
                    self.despawned=1
        if self.despawned: self.sort()

    def draw(self,relpos,row):
        return self.space(relpos)+self.rows[row]

class game(components):

    tact=10
    movespeed=10
    spawnspeed=2

    charmoves=[b'w',b'a',b's',b'd']
    choices=[b'y',b'n']
    stoppers=[b'q',b'p']

    menu=menu()
    char=char()
    enemy=enemy()
    ai=ai()

    def __init__(self):
        random.seed(time.time())
        self.setup()
        self.menuch=self.menu.start()
        if self.menuch==0: self.run()

    def setup(self):
        self.c=''
        self.t=0
        self.tt=0
        self.lives=3

    def end(self):
        if not self.menu.end("go"): cls()
        else:
            self.char.setup()
            self.enemy.setup()
            self.ai.setup()
            self.setup()
            self.run()

    def stop(self):
        if self.c==b'q': self.quit=self.menu.end("q")
        elif self.c==b'p': self.quit=self.menu.pause()
        if not self.quit:
            self.c=''
            self.run()
        else: cls()

    def run(self):
        with realtime():
            while self.c not in self.stoppers and self.lives:
                if self.c in self.charmoves or self.t%(self.tact/self.movespeed)==0:
                    if self.c in self.charmoves:
                        self.char.move(self.c)
                        self.c=''
                    if self.t%(self.tact/self.movespeed)==0:
                        self.enemy.move()
                    if self.t%(self.tact/self.spawnspeed)==0:
                        self.ai.spawncalc(self.char,self.enemy,self.t//(self.tact/self.spawnspeed))
                    self.lives-=self.ai.collisioncalc(self.char,self.enemy)
                    self.top("g")
                    self.main()
                self.t+=1
                if not self.t%self.tact: self.tt=self.t//self.tact
                self.c = getchmaybe()
                time.sleep(1/self.tact)
        if self.lives: self.stop()
        else: self.end()


game=game()
