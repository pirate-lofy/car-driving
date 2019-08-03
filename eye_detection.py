import cv2 as cv

x0,y0,w0,h0=0,0,0,0
cap=None
arrow_len=50
dist=40
face_detector=cv.CascadeClassifier('haarcascade_frontalface_default.xml')

def detect(gray,frame):
    global face_detector
    faces=face_detector.detectMultiScale(gray,1.3,5)
    
    x,y,w,h=None,None,None,None
    if len(faces)!=0:
        (x,y,w,h)=faces[0]
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    
    if x and y and w and h:
        return frame,(x,y,w,h)
    return frame,(0,0,0,0)

def check_direction(x,x0):
    if x==0 or x0==0:
        return 'error'
    eps=15
    if(x-x0>eps):
        return 1
    elif(x-x0<-1*eps):
        return -1
    else:return 0

def check_distance(w,w0):
    if w==0 or w0==0:
        return 'error'
    eps=15
    if(w-w0>eps):
        return 1
    elif(w-w0<-1*eps):
        return -1
    else:return 0

def init():    
    global cap,w0,x0
    cap=cv.VideoCapture(0)
    _,frame=cap.read()
    gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    canvas,cord=detect(gray,frame)
    x0,y0,w0,h0=cord

def run():
    _,frame=cap.read()
    gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    canvas,cord=detect(gray,frame)
    x,y,w,h=cord
    distance=check_distance(w,w0)
    direction=check_direction(x,x0)
    return canvas,cord,distance,direction
    
def terminate():
    cap.release()
    cv.destroyAllWindows()
    
def setup():
    cv.namedWindow('player face')

def draw(canvas):
    cv.imshow('player face',canvas)
    if cv.waitKey(1)==27:
        terminate()


def draw_arrow(canvas,cord1,cord2):
    cv.arrowedLine(canvas,cord1,cord2,(0,255,0),10)
    
def upArrow(canvas,cord):
    x0,y0,w0,h0=cord
    x1=x0+w0/2
    y1=y0-dist
    x2=x1
    y2=y1-arrow_len
    draw_arrow(canvas,(int(x1),int(y1)),(int(x2),int(y2)))

def downArrow(canvas,cord):
    x0,y0,w0,h0=cord
    x1=x0+w0/2
    y1=y0+h0+dist
    x2=x1
    y2=y1+arrow_len
    draw_arrow(canvas,(int(x1),int(y1)),(int(x2),int(y2)))

def leftArrow(canvas,cord):
    x0,y0,w0,h0=cord
    x1=x0-dist
    y1=y0+h0/2
    x2=x1-arrow_len
    y2=y1
    draw_arrow(canvas,(int(x1),int(y1)),(int(x2),int(y2)))

def rightArrow(canvas,cord):
    x0,y0,w0,h0=cord
    x1=x0+w0+dist
    y1=y0+h0/2
    x2=x1+arrow_len
    y2=y1
    draw_arrow(canvas,(int(x1),int(y1)),(int(x2),int(y2)))