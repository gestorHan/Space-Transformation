import pygame

def init(H, W, Title):
    pygame.init()
    win = pygame.display.set_mode((800, 500))
    pygame.display.set_caption(Title)
    pygame.font.init()
    return win

class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, point):
        return (self.x + point.x, self.y + point.y)

    def adx(self, x0):
        self.x += x0

    def ady(self, y0):
        self.y += y0


class Axis:

    vel = 2
    pxWidth = 1
    refRad = 3
    refZoom = 2
    refSpace = 50

    def __init__(self, center: XY):
        self.center = XY(int(center.x), int(center.y))

    def ref2T(self, tuple2):
        return (self.refX(tuple2[0]), self.refY(tuple2[1]))

    def refX(self, n: float):
        return int(n*self.refSpace + self.center.x)

    def refY(self, n: float):
        return int(-n * self.refSpace + self.center.y)

    def draw(self, win: pygame.Surface):
        pygame.draw.line(win, (255, 255, 0), (self.center.x, 0),
                         (self.center.x, h), self.pxWidth)
        pygame.draw.line(win, (255, 255, 0), (0, self.center.y),
                         (w, self.center.y), self.pxWidth)
        self.drawReferences(win)

    def drawReferences(self, win: pygame.Surface):
        for i in range(win.get_width()//(self.refSpace) + 1):
            pygame.draw.circle(win, (255, 255, 0), (i*self.refSpace +
                               (self.center.x % self.refSpace),  self.center.y), self.refRad)
        for i in range(win.get_height()//(self.refSpace) + 1):
            pygame.draw.circle(win, (255, 255, 0), (self.center.x,
                               (self.center.y % self.refSpace) + i*self.refSpace), self.refRad)


class Line:
    width = 2

    def __init__(self, startX, startY, endX, endY):
        self.start = XY(startX, startY)
        self.end = XY(endX, endY)

    def drawInAxis(self, axis, win):
        pygame.draw.line(win, (255, 255, 0), (axis.refX(self.start.x), axis.refY(
            self.start.y)), (axis.refX(self.end.x), axis.refY(self.end.y)), self.width)

class LineSet:
    width = 2
    def __init__(self, startX, startY, endX, endY):
        self.start = XY(startX, startY)
        self.end = XY(endX, endY)

    def drawInAxis(self, axis, win):
        pygame.draw.line(win, (255, 255, 0), (axis.refX(self.start.x), axis.refY(
            self.start.y)), (axis.refX(self.end.x), axis.refY(self.end.y)), self.width)


class Polygon:
    width = 2

    def __init__(self, points):
        self.points = points

    def drawInAxis(self, axis: Axis, win):
        truePoints = map(axis.ref2T, self.points)
        pygame.draw.polygon(win, (255, 0, 50), list(truePoints), self.width)

def checkActions(keys, axis, win):
    if keys[pygame.K_LEFT]:
            axis.center.adx(-axis.vel)
    if keys[pygame.K_RIGHT]:
            axis.center.adx(axis.vel)
    if keys[pygame.K_UP]:
            axis.center.ady(-axis.vel)
    if keys[pygame.K_DOWN]:
            axis.center.ady(axis.vel)
    if keys[pygame.K_u] and axis.refSpace <= win.get_width()/2:
            axis.refSpace += axis.refZoom
    if keys[pygame.K_y] and axis.refSpace > axis.refZoom:
            axis.refSpace -= axis.refZoom

def drawMouseCursor(win):
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        pygame.draw.circle(win , (0,0,255) , pygame.mouse.get_pos(),5)

def printMousePosWin(win,font, axis):
    x, y = pygame.mouse.get_pos()
    x = round((x-axis.center.x)/axis.refSpace,2)
    y = -round((y-axis.center.y)/axis.refSpace,2)
    textsurface = font.render(str(x)+" "+str(y), False, (255, 0, 0))        
    win.blit(textsurface, dest=(0,0))

def renderInAxis(axis: Axis ,win, list):
    axis.draw(win)
    for drawable in list:
        drawable.drawInAxis(axis,win)

def keepOpen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


if __name__ == "__main__":

    win = init(500, 600, "2D graphs and transformations")
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    w, h = pygame.display.get_surface().get_size()
    axis = Axis(XY(w/2, h/2))

    triangle = Polygon([(-0.5,0.5),
                        (4.5,1.5),
                        (1.5,3.5)])
    
    quadrilateral = Polygon([
        (0,1),
        (0,-1),
        (1,0),
        (-1,0)
    ])
    run = True

    while keepOpen():
        pygame.time.delay(1000//60)

        checkActions(pygame.key.get_pressed(),axis,win)

        win.fill((0, 0, 0))
        renderInAxis(axis, win, [triangle,quadrilateral])

        drawMouseCursor(win)
        printMousePosWin(win , font, axis)
        pygame.display.update()
