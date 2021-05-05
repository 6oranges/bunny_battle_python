import pygame, os, math, random,sys
from pygame.locals import *
#import ctypes
walls = []
#user32 = ctypes.windll.user32
#user32.SetProcessDPIAware()
def font(size, text,color):
  return pygame.font.Font(None, size).render(text, True, color)
def load_image(name, colorkey=None): # Load Image
  fullname = os.path.join(name)
  try:
    image = pygame.image.load(fullname)
  except:
    raise SystemExit
  image = image.convert()
  if colorkey is not None:
    if colorkey is -1:
      colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
  return image, image.get_rect()
class picture: # Creates a new object with basic propertys
  def __init__(self,x,y,image):
    self.image = image
    self.x = x
    self.y = y
  def draw(self, screen):
    screen.blit(self.image, (self.x, self.y))
  def inwall(self):
    s = self.image.get_size()
    for w in walls:
      if self.y+s[1] > w.y and self.y < w.dy:
        if self.x+s[0] > w.x and self.x < w.dx:
          return True
def ForceField(x,y,image):
  r = picture(x,y,pygame.transform.scale(image,(32,32)))
  return r
def Grow(x,y,image):
  r = picture(x,y,image)
  return r
def Small(x,y,image):
  r = picture(x,y,image)
  return r
def Speed(x,y,image):
  r = picture(x,y,image)
  return r
def Knight(x,y,image):
  r = picture(x,y,image)
  return r
def HealthPack(x,y,image):
  r = picture(x,y,image)
  return r
def Grenade(x,y,direction,thrown,image,time,owner):
  r           = picture(x,y,image)
  r.owner     = owner
  r.thrown    = thrown
  r.xv        = direction * 20
  r.yv        = -10
  r.timeleft  = time+26
  r.direction = direction
  return r
class wall: # Creates a platform to jump on
  def __init__(self,x,y,dx,dy):
    self.x=x
    self.y=y
    self.dx=dx
    self.dy=dy
    walls.append(self)
class Bunny(): # Creates a bunny
  def __init__(self, x, y, image,bunnytype,player,platformer):
    self.sprite_sheet = pygame.transform.scale(image,(768,512))
    self.sprite_x = 0
    self.sprite_y = 2
    self.player=player
    self.s=64
    self.width = 64
    self.height = 64
    self.type=bunnytype
    self.typex=(self.type%4)*3
    self.typey=(round((float(self.type)/4.)-.499999)%2)*4
    self.x = x
    self.y = y
    self.inventory = []
    self.points = 0
    self.inventoryi=0
    self.limbs=4
    self.throwtime=0
    self.throwing=False
    self.hurtime = 0
    self.speed = 10
    self.growtime=-1
    self.stime = -1
    self.smalltime=-1
    self.bkills=0
    self.sheildt = -1
    self.selected = False
    self.b = False
    self.grail = False
    if platformer:
      self.xv = 0
      self.yv = 0
      self.direction=1
      self.jumping=-1
      self.jump= 0
      self.run = 0
    else:
      self.direction="DOWN"
    return
  def inwall(self):
    for w in walls:
      if self.y+self.s > w.y and self.y < w.dy:
        if self.x+self.s > w.x and self.x < w.dx:
          return True
    return False
  def loselimbs(self,limbs):
    if self.hurtime == 0 and self.sheildt == -1:
      if self.grail:
        self.limbs -= 1
        self.hurtime=60
      else:
        self.limbs-=limbs
        self.hurtime=20
  def move(self, num):
    if self.direction == "UP":
      if self.grail:
        self.y -= num
      else:
        self.y -= num-(4-self.limbs)*2
      self.sprite_y = 3+self.typey
    if self.direction == "DOWN":
      if self.grail:
        self.y += num
      else:
        self.y += num-(4-self.limbs)*2
      self.sprite_y = 0+self.typey
    if self.direction == "LEFT":
      if self.grail:
        self.x -= num
      else:
        self.x -= num-(4-self.limbs)*2
      self.sprite_y = 1+self.typey
    if self.direction == "RIGHT":
      if self.grail:
        self.x += num
      else:
        self.x += num-(4-self.limbs)*2
      self.sprite_y = 2+self.typey
    self.sprite_x += 1
    if self.sprite_x >= 3+self.typex:
      self.sprite_x = 0+self.typex
  def use_inventory(self):
    self.inventoryi -= 1
    if self.inventoryi < 0:
      self.inventoryi = 0
      return self.inventory.pop(self.inventoryi)
    else:
      return self.inventory.pop(self.inventoryi+1)
  def get_inventory(self):
    if len(self.inventory) > 0:
      return self.inventory[self.inventoryi]
    else:
      return ""
  def draw(self, screen):
    screen.blit(pygame.transform.scale(self.sprite_sheet,(self.s*12,self.s*8)), (self.x, self.y), (self.sprite_x * self.s, self.sprite_y * self.s, self.s, self.s))
class start():
  def __init__(self):
    self.size = [1920, 1080]
    pygame.init()
    self.platformer=False
    self.debug = False
    self.loadbar = 500.0/196
    self.barpos = 0
    wall(0,self.size[1],self.size[0],self.size[1]-20)
    wall(0,self.size[1]-200,self.size[0]/2-100,self.size[1]-180)
    wall(self.size[0]/2+100,self.size[1]-200,self.size[0],self.size[1]-180)
    wall(0,self.size[1]-400,self.size[0]/2+300,self.size[1]-380)
    wall(self.size[0]/2+500,self.size[1]-400,self.size[0],self.size[1]-380)
    self.surface = pygame.display.set_mode(self.size,pygame.FULLSCREEN)
    #self.ProgressDisplay = pygame.font.Font(None, 50)
    #self.bunnybattle = pygame.font.Font(None, 100).render("Bunny Battle", True, (100,100,100))
    self.Loading("Setting Caption and Icon...")
    pygame.display.set_caption("Bunny Battle")
    pygame.display.set_icon(pygame.image.load("Icon.png"))
    self.Loading("Setting Bunny Names...")
    self.bunnynames = []
    for b in range(10):
      self.bunnynames.append("Bunny"+str(b+1))
    x=open("names.txt","r")
    y=x.read()
    x.close()
    if False and len(y) > 0:
      z=y.split("\n")
      for i in range(len(z)):
        self.bunnynames[i]=z[i]
    self.Loading("Loading Bunnys.png...")
    self.bunnypics=pygame.image.load('Bunnys.png')
    self.grass=pygame.image.load('grass.png')
    self.bunnypics.set_colorkey((255,255,255))
    self.Loading("Loading Knight.png...")
    self.knightpic=pygame.image.load('knight.png')
    self.knightpic.set_colorkey((0,0,0))
    self.Loading("Loading HHG.png...")
    self.Grenadepic=load_image("HHG.png",(255,255,255))[0]
    self.Loading("Loading HHGP.png...")
    self.Pulled=load_image("HHGP.png",(255,255,255))[0]
    self.explodepics=[]
    for i in range(26):
      self.Loading("Loading Explosion/E"+str(i+1)+".png...")
      self.explodepics.append(pygame.image.load("Explosion/E"+str(i+1)+".png"))
    self.Loading("Loading holygrail.png...")
    self.grail=pygame.image.load("holygrail.png")
    self.Loading("Loading HealthPack.png...")
    self.Pack=pygame.image.load("HealthPack.png")
    self.Loading("Loading Heart.png...")
    self.life=pygame.image.load("Heart.png")
    self.Loading("Loading Force Field.png...")
    self.Force=pygame.image.load("Force Field Old.png")
    self.Loading("Loading Grow.png...")
    self.Grow=pygame.image.load("Grow.png")
    self.Loading("Loading Glow.png...")
    self.Glow=pygame.image.load("Glow.png")
    self.Loading("Loading Small.png...")
    self.Small=pygame.image.load("Small.png")
    self.Grow=pygame.transform.scale(self.Grow,(34,32))
    self.Loading("Loading Speed Up.png...")
    self.Speed=pygame.image.load("Speed Up.png")
    self.Speed=pygame.transform.scale(self.Speed,(40,40))
    self.Speed.set_colorkey((255,255,255))
    self.Loading("Loading Sounds: Explode.wav...")
    self.explode=pygame.mixer.Sound("Explode.wav")
    self.Loading("Loading Sounds: Pull.wav...")
    self.Pull=pygame.mixer.Sound("Pull.wav")
    self.Loading("Loading Sounds: BunnyDeath.wav...")
    self.die=pygame.mixer.Sound("BunnyDeath.wav")
    self.Loading("Loading Sounds: KnightDie.wav...")
    self.Knightdie=pygame.mixer.Sound("KnightDie.wav")
    self.Knightdie.set_volume(0.2)
    self.Loading("Loading Sounds: Background.wav...")
    self.background=pygame.mixer.Sound("Background.wav")
    self.background.set_volume(0.01)
    self.backdrops=[]
    self.backdrop=0
    for i in range(143):
      self.Loading("Loading Backdrops/Frame "+str(i+1)+" (80ms) (combine).png...")
      self.backdrops.append(pygame.image.load("Backdrops/Frame "+str(i+1)+" (80ms) (combine).png"))
      self.backdrops[i]=pygame.transform.scale(self.backdrops[i],(self.size[0],self.size[1]))
    self.Loading("Loading Play.png...")
    self.Play=load_image("Play.png",(255,255,255))[0]
    self.Loading("Loading checked.png...")
    self.checked=load_image("checked.png",(255,255,255))[0]
    self.Loading("Loading unchecked.png...")
    self.unchecked=load_image("unchecked.png",(255,255,255))[0]
    self.Loading("Loading Selectingcheck.png...")
    self.checkselect=load_image("Selectingcheck.png",(255,255,255))[0]
    self.Loading("Loading Quit.png...")
    self.Quit=load_image("Quit.png",(255,255,255))[0]
    self.Loading("Loading Options.png...")
    self.Options=load_image("Options.png",(255,255,255))[0]
    self.Loading("Loading Select.png...")
    self.Select=load_image("Select.png",(255,255,255))[0]
    self.selecting = 0
    self.startpressed=False
    self.bt = 0 #Background Timer
    self.clock = pygame.time.Clock()
    self.Loading("Loading Variables...")
    self.variables("Menu")
    self.done = False
    self.messages=["WhoBunny:","SomeBunny:","EveryBunny:","AnyBunny:","OtherBunny:","Bunny:","NoBunny:","ThingBunny:"]
    self.background.play()
    self.keys=set()
    self.buttons=set()
    self.menuselect = [2,10]
    while not self.done:
      self.clock.tick(20)
      self.newkeys = set()
      self.newbuttons=set()
      self.keyboard=[]
      for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
          pass
        if event.type == pygame.QUIT:
          self.done=True
        if event.type == pygame.KEYDOWN:
          self.keys.add(event.key)
          self.newkeys.add(event.key)
          if len(event.unicode) > 0:
            self.keyboard.append(event.unicode)
        if event.type == pygame.KEYUP:
          self.keys.discard(event.key)
        if event.type == pygame.MOUSEMOTION:
          self.mouse_position = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
          self.buttons.add(event.button)
          self.newbuttons.add(event.button)
        if event.type == pygame.MOUSEBUTTONUP:
          self.buttons.discard(event.button)
      self.evolve()
      self.draw()
      pygame.display.flip()
    x=open("names.txt","w")
    x.write("\n".join(self.bunnynames))
    x.close()
  def get_keys(self,num): # Returns keys num is pressing
    events=[]
    if len(self.joysticks) > 0:
      if self.joysticks[num].get_button(0) == 1:
        events.append('A')
      if self.joysticks[num].get_button(1) == 1:
        events.append('B')
      if self.joysticks[num].get_button(9) == 1:
        events.append('start')
      if self.joysticks[num].get_button(8) == 1:
        events.append('select')
      if round(self.joysticks[num].get_axis(0)) == -1:
        events.append('left')
      if round(self.joysticks[num].get_axis(0)) == 1:
        events.append('right')
      if round(self.joysticks[num].get_axis(1)) == -1:
        events.append('up')
      if round(self.joysticks[num].get_axis(1)) == 1:
        events.append('down')
    elif num == 0:
      if pygame.K_RCTRL in self.keys:
        events.append("A")
      if pygame.K_RALT in self.keys:
        events.append("B")
      if pygame.K_RETURN in self.keys:
        events.append("start")
      if pygame.K_RSHIFT in self.keys:
        events.append("select")
      if pygame.K_LEFT in self.keys:
        events.append("left")
      if pygame.K_RIGHT in self.keys:
        events.append("right")
      if pygame.K_UP in self.keys:
        events.append("up")
      if pygame.K_DOWN in self.keys:
        events.append("down")
    elif num == 1:
      if pygame.K_LALT in self.keys:
        events.append("A")
      if pygame.K_LCTRL in self.keys:
        events.append("B")
      if pygame.K_LSHIFT in self.keys:
        events.append("start")
      if pygame.K_TAB in self.keys:
        events.append("select")
      if pygame.K_a in self.keys:
        events.append("left")
      if pygame.K_d in self.keys:
        events.append("right")
      if pygame.K_w in self.keys:
        events.append("up")
      if pygame.K_s in self.keys:
        events.append("down")
    return events
  def Loading(self,description): # Shows what the computer is loading at that time
    pygame.event.get()
    self.barpos += self.loadbar
    self.surface.fill((120,195,128))
    #self.surface.blit(self.ProgressDisplay.render(description, True, (100,100,100)),(0,self.size[1]-50))
    #self.surface.blit(self.bunnybattle,(self.size[0]/2-200,self.size[1]/2-50))
    pygame.draw.rect(self.surface,(0,200,255),(self.size[0]/2-200,self.size[1]/2-100,int(self.barpos),10),0)
    pygame.draw.rect(self.surface,(0,100,255),(self.size[0]/2-200,self.size[1]/2-90,int(self.barpos),5),0)
    pygame.draw.rect(self.surface,(0,0,0),(self.size[0]/2-200,self.size[1]/2-100,500,15),2)
    self.surface.blit(font(20,str(int(self.barpos/5))+"%",(0,0,0)),(self.size[0]/2-200,self.size[1]/2-120))
    pygame.display.flip()
  def findjoy(self): # Reloads all remotes
    pygame.joystick.quit()
    pygame.joystick.init()
    self.joysticks=[]
    for i in range(pygame.joystick.get_count()):
      self.joysticks.append(pygame.joystick.Joystick(i))
      self.joysticks[len(self.joysticks)-1].init()
  def variables(self,mode): # Changes the mode
    self.mode=mode
    self.findjoy()
    self.score=[]
    if mode == "Playing":
      self.grailx = random.randrange(0,self.size[0]-50)
      self.graily = random.randrange(0,self.size[1]-50)
      self.grailt = random.randrange(400,2000)
      self.players = pygame.joystick.get_count()
      if self.players > 0:
        self.bunnys = []
        for i in range(self.players):
          self.bunnys.append(Bunny(100+100*i, 100+100*i, self.bunnypics,i,i,self.platformer))
      else:
        self.players=2
        self.bunnys = [Bunny(100, 100, self.bunnypics,0,0,self.platformer),Bunny(200, 200, self.bunnypics,1,1,self.platformer)]
      self.players = len(self.bunnys)
    if mode == "Menu":
      self.selected = 0
      self.backdrop=0
      self.menui = 0
    self.grenadelist = []
    self.knights = []
    self.healthpacks = []
    self.ForceFields=[]
    self.GrowUps=[]
    self.SmallUps=[]
    self.SpeedUps=[]
    self.selecting == False
  def evolve(self): # Evolves the game
    events=self.get_keys(0)
    if self.startpressed == True:
      if not "start" in events:
        self.startpressed = False
    self.bt += 1
    if self.bt > 2740:
      self.background.play()
      self.bt = 0
    if self.mode=="Score" or self.mode=="Playing":
      if self.startpressed == False:
        if "start" in events:
          self.variables("Menu")
          self.startpressed = True
    elif self.mode=="Menu": # The Menu
      if "select" in events:
        if self.selecting == False:
          self.selected += 1
          self.selecting = True
          if self.selected > self.menuselect[self.menui]:
            self.selected = 0
      else:
        self.selecting = False
      if self.menui == 1:
        i = self.selected - 3
        for k in self.keyboard:
          self.bunnynames[i] += k
        if 8 in self.newkeys:
          self.bunnynames[i] = self.bunnynames[i][0:len(self.bunnynames[i])-2:1]
      if "start" in events:
        if self.startpressed == False:
          self.startpressed = True
          if self.menui == 0:
            if self.selected == 0:
              self.variables("Playing")
            elif self.selected == 1:
              self.menui = 1
              self.selected = 0
            elif self.selected == 2:
              self.done = True
          elif self.menui == 1:
            if self.selected == 0:
              self.menui = 0
              self.selected = 1
            elif self.selected == 1:
              if self.platformer:
                self.platformer = False
              else:
                self.platformer = True
            elif self.selected == 2:
              if self.debug:
                self.debug = False
              else:
                self.debug = True
    if self.mode=="Playing": # Everything that happens while playing
      if self.players > 0:
        if random.randrange(1, int(300/self.players)) == 1:
          for i in range(random.randrange(1, 2)):
            self.ForceFields.append(ForceField(random.randrange(0,self.size[0]), random.randrange(0,self.size[1]),self.Force))
        if random.randrange(1, int(300/self.players)) == 1:
          for i in range(random.randrange(1, 2)):
            self.GrowUps.append(Grow(random.randrange(0,self.size[0]), random.randrange(0,self.size[1]),self.Grow))
        #if random.randrange(1, 300/self.players) == 1:
         # for i in range(random.randrange(1, 2)):
          #  self.SmallUps.append(Small(random.randrange(0,self.size[0]), random.randrange(0,self.size[1]),self.Small))
        if random.randrange(1, int(50/self.players)) == 1:
          for i in range(random.randrange(1, 2)):
            self.SpeedUps.append(Speed(random.randrange(0,self.size[0]), random.randrange(0,self.size[1]),self.Speed))
        if random.randrange(1, int(300/self.players)) == 1:
          for i in range(random.randrange(1, 2)):
            self.healthpacks.append(HealthPack(random.randrange(0,self.size[0]), random.randrange(0,self.size[1]),self.Pack))
        if random.randrange(1, int(200/self.players)) == 1:
          for i in range(random.randrange(1, 2)):
            self.grenadelist.append(Grenade(random.randrange(0,self.size[0]), random.randrange(0,self.size[1]),"UP",False,self.Grenadepic,0,0))
        if random.randrange(1, int(50/self.players)) == 1:
          for i in range(random.randrange(1, 2)):
            self.knights.append(Knight(random.randrange(0,self.size[0]), random.randrange(0,self.size[1]), self.knightpic))
      if self.grailt > 0:
        self.grailt -= 1
      for i in range(len(self.bunnys)):
        if self.bunnys[i].growtime > 0:
          for x in range(len(self.bunnys)):
            if x != i:
              if self.bunnys[x].growtime == -1:
                if math.sqrt((((self.bunnys[i].x+self.bunnys[i].s/2)-(self.bunnys[x].x+self.bunnys[x].s/2))**2)+((self.bunnys[i].y+self.bunnys[i].s/2)-(self.bunnys[x].y+self.bunnys[x].s/2))**2)<=self.bunnys[i].s/2+self.bunnys[x].s/2:
                  self.bunnys[x].loselimbs(2)
                  if self.bunnys[x].limbs < 1:
                    self.bunnys[i].points+= 10
                    self.bunnys[i].bkills+= 1
        if self.bunnys[i].hurtime > 0:
          self.bunnys[i].hurtime -= 1
        if self.bunnys[i].growtime > -1:
          self.bunnys[i].growtime -= 1
        if self.bunnys[i].growtime == 0:
          self.bunnys[i].s = 64
          self.bunnys[i].x+=self.bunnys[i].s/2
          self.bunnys[i].y+=self.bunnys[i].s/2
        if self.bunnys[i].sheildt > -1:
          self.bunnys[i].sheildt -= 1
        #if self.bunnys[i].sheildt == 0:
        if self.bunnys[i].smalltime > -1:
          self.bunnys[i].smalltime -= 1
        if self.bunnys[i].smalltime == 0:
          self.bunnys[i].s = 64
          self.bunnys[i].x-=self.bunnys[i].s/4
          self.bunnys[i].y-=self.bunnys[i].s/4
        if self.bunnys[i].stime > -1:
          self.bunnys[i].stime -= 1
        if self.bunnys[i].stime == 0:
          self.bunnys[i].speed = 10
        if self.bunnys[i].limbs < 1:
          self.bunnys[i].points/=2
          self.bunnys[i].limbs=4
          self.bunnys[i].x=random.randrange(0,self.size[0])
          self.bunnys[i].y=random.randrange(0,self.size[1])
          self.bunnys[i].inventory=[]
          self.bunnys[i].throwing=False
          self.bunnys[i].throwtime=0
          self.bunnys[i].speed = 10
          self.bunnys[i].s = 64
          self.bunnys[i].stime = 0
          self.bunnys[i].growtime = 0
          if self.bunnys[i].grail == True:
            self.grailt = random.randrange(200,400)
            self.grailx = random.randrange(0,self.size[0]-50)
            self.graily = random.randrange(0,self.size[1]-50)
            self.bunnys[i].grail = False
          self.die.play()
        events=self.get_keys(i)
        if self.platformer == False:
          if 'left' in events:
            self.bunnys[i].direction = "LEFT"
          if 'right' in events:
            self.bunnys[i].direction = "RIGHT"
          if 'up' in events:
            self.bunnys[i].direction = "UP"
          if 'down' in events:
            self.bunnys[i].direction = "DOWN"
          if self.bunnys[i].y <= 0:
            self.bunnys[i].y=self.size[1]-1
          if self.bunnys[i].y >= self.size[1]:
            self.bunnys[i].y=1
        else:
          if self.bunnys[i].jumping == -1:
            self.bunnys[i].jump = 0
            self.bunnys[i].run = 0
            if 'left' in events:
              self.bunnys[i].direction = -1
              self.bunnys[i].y+=1
              if self.bunnys[i].inwall():
                self.bunnys[i].sprite_x = 2
                self.bunnys[i].jumping = 4
                self.bunnys[i].jump = 6
                self.bunnys[i].run = 6
            if 'right' in events:
              self.bunnys[i].direction = 1
              self.bunnys[i].y+=1
              if self.bunnys[i].inwall():
                self.bunnys[i].sprite_x = 2
                self.bunnys[i].jumping = 4
                self.bunnys[i].jump = 6
                self.bunnys[i].run = 6
            if 'up' in events:
              self.bunnys[i].y+=1
              if self.bunnys[i].inwall():
                self.bunnys[i].sprite_x = 2
                self.bunnys[i].jumping = 4
                self.bunnys[i].jump += 16
                self.bunnys[i].run += 10
          if self.bunnys[i].jumping > -1:
            self.bunnys[i].jumping -= 1
          if self.bunnys[i].jumping == 0:
            self.bunnys[i].xv += self.bunnys[i].run * self.bunnys[i].direction
            while self.bunnys[i].inwall():
              self.bunnys[i].y -= 1
            self.bunnys[i].yv -= self.bunnys[i].jump
            self.bunnys[i].sprite_x = 0
        if self.bunnys[i].x <= 0:
          self.bunnys[i].x=self.size[0]-1
        if self.bunnys[i].x >= self.size[0]:
          self.bunnys[i].x=1
        if "B" in events:
          if self.bunnys[i].throwing == True:
            if self.bunnys[i].throwtime==0:
              self.grenadelist.append(Grenade((self.bunnys[i].x+self.bunnys[i].s/2)-7, (self.bunnys[i].y+self.bunnys[i].s/2)-7, self.bunnys[i].direction, True,self.Pulled,0,i))
              self.bunnys[i].throwing=False
            else:
              self.bunnys[i].throwtime-=1
          if self.bunnys[i].b == False:
            self.bunnys[i].b = True
            a=self.bunnys[i].get_inventory()
            if a == "Grenade":
              if self.bunnys[i].throwing==False:
                self.bunnys[i].use_inventory()
                self.bunnys[i].throwtime=60
                self.bunnys[i].throwing=True
                self.Pull.play()
            elif a == "forcefield":
              self.bunnys[i].sheildt = 50
              self.bunnys[i].use_inventory()
        else:
          self.bunnys[i].b = False
          if self.bunnys[i].throwing==True:
            self.grenadelist.append(Grenade((self.bunnys[i].x+self.bunnys[i].s/2)-7, (self.bunnys[i].y+self.bunnys[i].s/2)-7, self.bunnys[i].direction, True,self.Pulled,self.bunnys[i].throwtime,i))
            self.bunnys[i].throwing=False
        if "select" in events:
          if self.bunnys[i].selected == False:
            self.bunnys[i].selected = True
            self.bunnys[i].inventoryi+=1
            if len(self.bunnys[i].inventory) <= self.bunnys[i].inventoryi:
              self.bunnys[i].inventoryi = 0
        else:
          self.bunnys[i].selected = False
        if "start" in events:
          pass
        if self.platformer:
          self.bunnys[i].x += self.bunnys[i].xv
          self.bunnys[i].y += self.bunnys[i].yv
          self.bunnys[i].xv *= 0.95
          if self.bunnys[i].inwall():
            self.bunnys[i].y -= self.bunnys[i].yv
            self.bunnys[i].yv = 0
            if self.bunnys[i].sprite_x == 0:
              self.bunnys[i].sprite_x = 1
          else:
            self.bunnys[i].yv += 1
          if self.bunnys[i].direction == 1:
            self.bunnys[i].sprite_y = 2
          else:
            self.bunnys[i].sprite_y = 1
        else:
          self.bunnys[i].move(self.bunnys[i].speed)
      for t in self.grenadelist:
        if t.thrown==True:
          if t.timeleft>26:
            if self.platformer:
              t.x += t.xv
              t.y += t.yv
              t.xv *= 0.95
              if t.inwall():
                t.y -= self.bunnys[i].yv
                t.yv = 0
              else:
                t.yv +=1
            else:
              if t.direction=="UP":
                t.y-=12
              if t.direction=="DOWN":
                t.y+=12
              if t.direction=="LEFT":
                t.x-=12
              if t.direction=="RIGHT":
                t.x+=12
              if t.y <= 0:
                t.y=self.size[1]-1
              if t.y >= self.size[1]:
                t.y=1
            if t.x <= 0:
              t.x=self.size[0]-1
            if t.x >= self.size[0]:
              t.x=1
          if t.timeleft == 26:
            t.image=self.explodepics[0]
            self.explode.play()
            t.x-=180
            t.y-=180
          if t.timeleft==0:
            self.grenadelist.remove(t)
            break
          if t.timeleft <= 26:
            t.image=self.explodepics[26-t.timeleft]
            for i in range(len(self.bunnys)):
              x1 = self.bunnys[i].x+16
              y1 = self.bunnys[i].y+16
              x2 = t.x+180
              y2 = t.y+180
              d = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
              if d <= 50:
                self.bunnys[i].loselimbs(4)
              if d <= 100:
                self.bunnys[i].loselimbs(3)
              if d <= 140:
                self.bunnys[i].loselimbs(2)
              if d <= 180:
                self.bunnys[i].loselimbs(1)
              if self.bunnys[i].limbs < 1:
                if i != t.owner:
                  self.bunnys[t.owner].points += 10
                  self.bunnys[t.owner].bkills += 1
          t.timeleft -= 1
        else:
          for i in range(len(self.bunnys)):
            if math.sqrt((((self.bunnys[i].x+self.bunnys[i].s/2)-(t.x+8))**2)+((self.bunnys[i].y+self.bunnys[i].s/2)-(t.y+8))**2)<=self.bunnys[i].s/2+8:
              if len(self.bunnys[i].inventory) < 3:
                self.bunnys[i].inventory.append("Grenade")
                self.grenadelist.remove(t)
                break
      for i in range(len(self.bunnys)):
        if self.grailt == 0:
          if math.sqrt((((self.bunnys[i].x+self.bunnys[i].s/2)-(self.grailx+25))**2)+((self.bunnys[i].y+self.bunnys[i].s/2)-(self.graily+25))**2)<=self.bunnys[i].s/2+25:
            self.grailt = -1
            self.bunnys[i].grail = True
        for k in self.knights:
          if math.sqrt((((self.bunnys[i].x+self.bunnys[i].s/2)-(k.x+18))**2)+((self.bunnys[i].y+self.bunnys[i].s/2)-(k.y+18))**2)<=self.bunnys[i].s/2+18:
            self.bunnys[i].points+=1
            self.knights.remove(k)
            self.Knightdie.play()
            break
        for g in self.GrowUps:
          if math.sqrt((((self.bunnys[i].x+self.bunnys[i].s/2)-(g.x+18))**2)+((self.bunnys[i].y+self.bunnys[i].s/2)-(g.y+18))**2)<=self.bunnys[i].s/2+18:
            if self.bunnys[i].growtime==-1:
              self.bunnys[i].x-=self.bunnys[i].s/2
              self.bunnys[i].y-=self.bunnys[i].s/2
            self.bunnys[i].growtime=100
            self.bunnys[i].s=128
            self.GrowUps.remove(g)
            break
        for s in self.SmallUps:
          if math.sqrt((((self.bunnys[i].x+self.bunnys[i].s/2)-(s.x+18))**2)+((self.bunnys[i].y+self.bunnys[i].s/2)-(s.y+18))**2)<=self.bunnys[i].s/2+18:
            if self.bunnys[i].smalltime==-1:
              if self.bunnys[i].growtime==-1:
                self.bunnys[i].x+=32
                self.bunnys[i].y+=32
              else:
                self.bunnys[i].x+=8
                self.bunnys[i].y+=8
            self.bunnys[i].smalltime=300
            self.bunnys[i].s=32
            self.SmallUps.remove(s)
            break
        for s in self.SpeedUps:
          if math.sqrt((((self.bunnys[i].x+self.bunnys[i].s/2)-(s.x+10))**2)+((self.bunnys[i].y+self.bunnys[i].s/2)-(s.y+10))**2)<=self.bunnys[i].s/2+10:
            self.bunnys[i].speed+=2
            self.bunnys[i].stime=50
            self.SpeedUps.remove(s)
            break
        for h in self.healthpacks:
          if math.sqrt((((self.bunnys[i].x+self.bunnys[i].s/2)-(h.x+19))**2)+((self.bunnys[i].y+self.bunnys[i].s/2)-(h.y+19))**2)<=self.bunnys[i].s/2+19:
            if self.bunnys[i].limbs < 4:
              self.bunnys[i].limbs+=1
            self.healthpacks.remove(h)
            break
        for f in self.ForceFields:
          if math.sqrt((((self.bunnys[i].x+self.bunnys[i].s/2)-(f.x+19))**2)+((self.bunnys[i].y+self.bunnys[i].s/2)-(f.y+19))**2)<=self.bunnys[i].s/2+19:
            if len(self.bunnys[i].inventory) < 3:
              self.bunnys[i].inventory.append("forcefield")
              self.ForceFields.remove(f)
              break
        if self.bunnys[i].points >= self.players*15:
          self.score=[]
          for b in range(len(self.bunnys)):
            self.bunnys[b].direction = "RIGHT"
            self.bunnys[b].s = 64
          check = sorted(self.bunnys, key=lambda bunny: bunny.points,reverse=True)
          for s in range(len(check)):
            self.score.append(check[s].player)
          self.mode = "Score"
    return
  def high(self): # The same as max() command
    h = 0
    w = 0
    for i in range(len(self.bunnys)):
      if self.bunnys[i].points > h:
        h = self.bunnys[i].points
        w = i
    return w
  def draw(self): # Draws everthing
    if self.mode == "Menu": # Menu
      self.surface.blit(self.backdrops[int(self.backdrop)],(0,0))
      self.backdrop+= 1
      if self.backdrop > 142:
        self.backdrop = 0
      if self.menui == 0:
        self.surface.blit(self.Play,(self.size[0]/2-270,(self.size[1]/2-250)+140*0))
        self.surface.blit(self.Options,(self.size[0]/2-270,(self.size[1]/2-250)+140*1))
        self.surface.blit(self.Quit,(self.size[0]/2-270,(self.size[1]/2-250)+140*2))
        self.surface.blit(self.Select,(self.size[0]/2-270,(self.size[1]/2-250)+140*self.selected))
      if self.menui == 1:
        self.surface.blit(font(40,"Return", (255, 255, 255)),(self.size[0]/2-230,(self.size[1]/2-240)+50*0))
        self.surface.blit(font(40,"Platformer mode", (255, 255, 255)),(self.size[0]/2-230,(self.size[1]/2-240)+50*1))
        if self.platformer:
          self.surface.blit(self.checked,(self.size[0]/2-270,(self.size[1]/2-250)+50*1))
        else:
          self.surface.blit(self.unchecked,(self.size[0]/2-270,(self.size[1]/2-250)+50*1))
        self.surface.blit(font(40,"Debug Mode", (255, 255, 255)),(self.size[0]/2-230,(self.size[1]/2-240)+50*2))
        if self.debug:
          self.surface.blit(self.checked,(self.size[0]/2-270,(self.size[1]/2-250)+50*2))
        else:
          self.surface.blit(self.unchecked,(self.size[0]/2-270,(self.size[1]/2-250)+50*2))
        self.surface.blit(self.checkselect,(self.size[0]/2-270,(self.size[1]/2-250)+50*self.selected))
        for bn in range(8):
          self.surface.blit(font(40,self.bunnynames[bn], (255, 255, 255)),(self.size[0]/2-230,(self.size[1]/2-240)+50*(3+bn)))
      self.surface.blit(font(120,"Bunny Battle", (255, 255, 255)),(self.size[0]/2-250,0))
      self.surface.blit(font(50,"Coded By: Jeanette, Tim, Sarah", (255, 255, 255)),(0,self.size[1]-30))
    if self.mode=="Playing": # Playing Drawing
      if self.platformer:
        self.surface.fill((0,255,255))
        for wall in walls:
          pygame.draw.rect(self.surface,(0,255,0),(wall.x,wall.y,wall.dx-wall.x,wall.dy-wall.y),0)
      else:
        self.surface.fill((120,195,128))
        #self.surface.blit(pygame.transform.scale(self.grass,(self.size[0],self.size[1])),(0,0))
      for g in self.grenadelist:
        g.draw(self.surface)
      for h in self.healthpacks:
        h.draw(self.surface)
      for k in self.knights:
        k.draw(self.surface)
      for g in self.GrowUps:
        g.draw(self.surface)
      for s in self.SmallUps:
        s.draw(self.surface)
      for f in self.ForceFields:
        f.draw(self.surface)
      for s in self.SpeedUps:
        s.draw(self.surface)
      for i in range(len(self.bunnys)):
        if self.bunnys[i].grail == True:
          self.surface.blit(pygame.transform.scale(self.grail,(25,25)),(self.bunnys[i].x+self.bunnys[i].s/2,self.bunnys[i].y-50))
        if self.bunnys[i].sheildt >= 0:
          self.surface.blit(pygame.transform.scale(self.Force,(self.bunnys[i].s,self.bunnys[i].s)),(self.bunnys[i].x,self.bunnys[i].y))
        self.bunnys[i].draw(self.surface)
        if len(self.bunnys[i].inventory) > 0:
          if len(self.bunnys[i].inventory) <= self.bunnys[i].inventoryi:
             self.bunnys[i].inventoryi = 0
          if self.bunnys[i].inventory[self.bunnys[i].inventoryi] == "forcefield":
            self.surface.blit(pygame.transform.scale(self.Force,(20,20)),(self.bunnys[i].x-22,self.bunnys[i].y-20))
          if self.bunnys[i].inventory[self.bunnys[i].inventoryi] == "Grenade":
            self.surface.blit(pygame.transform.scale(self.Grenadepic,(20,20)),(self.bunnys[i].x-22,self.bunnys[i].y-20))
        if self.bunnys[i].growtime >= 0:
          self.surface.blit(font(50,str(self.bunnys[i].points), (100, 100, 100)),(self.bunnys[i].x+60,self.bunnys[i].y-20))
        else:
          self.surface.blit(font(50,str(self.bunnys[i].points), (100, 100, 100)),(self.bunnys[i].x,self.bunnys[i].y-50))
        for h in range(self.bunnys[i].limbs):
          self.surface.blit(self.life,(self.bunnys[i].x+(h*14),self.bunnys[i].y-9))
        if self.high() == i:
          self.surface.blit(pygame.transform.scale(self.Glow,(self.bunnys[i].s+20,self.bunnys[i].s+20)),(self.bunnys[i].x-10,self.bunnys[i].y-10))
        self.surface.blit(font(50,str(self.bunnynames[i]), (100, 100, 100)),(self.bunnys[i].x-20,self.bunnys[i].y+(self.bunnys[i].s+10)))
      if self.grailt == 0:
        self.surface.blit(self.grail,(self.grailx,self.graily))
      if self.debug:
        self.surface.blit(font(20,"Debug Mode", (100, 100, 100)),(0,30*0))
        self.surface.blit(font(20,"Time until grail: " + str(self.grailt/20.0), (100, 100, 100)),(0,30*1))
        self.surface.blit(font(20,"Players: " + str(self.players), (100, 100, 100)),(0,30*2))
        self.surface.blit(font(20,"knights: " + str(len(self.knights)), (100, 100, 100)),(0,30*3))
        self.surface.blit(font(20,"grenades: " + str(len(self.grenadelist)), (100, 100, 100)),(0,30*4))
        self.surface.blit(font(20,"healthpacks: " + str(len(self.healthpacks)), (100, 100, 100)),(0,30*5))
        self.surface.blit(font(20,"ForceFields: " + str(len(self.ForceFields)), (100, 100, 100)),(0,30*6))
        self.surface.blit(font(20,"GrowUps: " + str(len(self.GrowUps)), (100, 100, 100)),(0,30*7))
        self.surface.blit(font(20,"SmallUps: " + str(len(self.SmallUps)), (100, 100, 100)),(0,30*8))
        self.surface.blit(font(20,"SpeedUps: " + str(len(self.SpeedUps)), (100, 100, 100)),(0,30*9))
    if self.mode=="Score": # Score Drawing
        self.surface.fill((120,195,128))
        for i in range(self.players):
          self.surface.blit(font(36,self.messages[i], (100, 100, 100)),(self.size[0]/2-200,(50*(i))+150))
        for i in range(len(self.score)):
          self.surface.blit(font(36,self.bunnynames[self.score[i]]+" | Points:"+str(self.bunnys[self.score[i]].points)+" | Bunny Kills:"+str(self.bunnys[self.score[i]].bkills), (100, 100, 100)),(self.size[0]/2+50,(50*(i))+150))
          self.bunnys[self.score[i]].x=self.size[0]/2-50
          self.bunnys[self.score[i]].y=(50*(i))+125
        self.surface.blit(self.grail,(self.size[0]/2-250,125))
        for i in range(len(self.bunnys)):
          self.bunnys[i].move(0)
          self.bunnys[i].draw(self.surface)
        self.surface.blit(font(36,"Press Start on main remote to go to menu", (100, 100, 100)),(self.size[0]/2-200,(50*(i+2))+150))
        self.surface.blit(font(40,"Jeanette won again!!", (100, 100, 100)),(self.size[0]/2-100,(50*(i+2))+200))
start()
pygame.quit()
