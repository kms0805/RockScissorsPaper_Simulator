from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os


width = 800
height = 400
leftButton=False
mousePosX,mousePosY = 0,0
timeStep = 30
eye = [ 0, 15, 100];
ori = [ 0.0, 0.0, 0.0 ];
rot = [ 0.0, 0.0, 0.0 ];

def loadGlobalCoord():
	glLoadIdentity()
	gluLookAt(eye[0], eye[1], eye[2], ori[0], ori[1], ori[2], 0, 1, 0)

def glutMotion(x,y):
	global leftButton,mousePosX,mousePosY

	if(leftButton):
		dx = x - mousePosX;
		dy = y - mousePosY;

		mousePosX = x;
		mousePosY = y;

		ori[0] -= dx*0.04;
		ori[1] += dy*0.04;

	loadGlobalCoord();

def glutMouse(button, state, x, y):
	global leftButton,mousePosX,mousePosY

	if button == GLUT_LEFT_BUTTON:
		if state == GLUT_DOWN:
			leftButton = True
			mousePosX,mousePosY = x,y
		if state == GLUT_UP:
			leftButton = False

	if button == GLUT_RIGHT_BUTTON:
		return

def resize(w, h):

	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, w / h, 0.1, 500.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

ESCAPE = b'\x1b'
def glutKeyboard(key, x, y):
	global menu

	if key == b'g' and menu == 3:
		menu = 4
	if key == b'g' and menu == 6:
		menu = 2
	if key == ESCAPE:
		os._exit(0)



class Hand:
	def __init__(self, LR):
		# L이면 1, R이면 -1
		self.rsp = 'paper'
		self.state = np.array([0,0,0,0,0])
		self.LR = LR
		self.rotate_num = 0

	def r_to_rsp(self,rsp,speed):
		rock = np.array([0, 0, 0, 0, 0])
		scissors = np.array([0, 1, 1, 0, 0])
		paper = np.array([1, 1, 1, 1, 1])
		self.rsp = rsp
		if self.rotate_num > 0:
			if rsp == 'rock':
				self.state += rock * self.LR * -1 * speed
			if rsp == 'scissors':
				self.state += scissors * self.LR * -1 * speed
			if rsp == 'paper':
				self.state += paper * self.LR * -1 * speed
			self.rotate_num -= 1 * speed

	def rsp_to_r(self,speed):
		rock = np.array([0, 0, 0, 0, 0])
		scissors = np.array([0, 1, 1, 0, 0])
		paper = np.array([1, 1, 1, 1, 1])
		if self.rotate_num < 90:
			if self.rsp == 'rock':
				self.state += rock * self.LR * speed
			if self.rsp == 'scissors':
				self.state += scissors * self.LR * speed
			if self.rsp == 'paper':
				self.state += paper * self.LR * speed
			self.rotate_num += 1 * speed
		if self.rotate_num == 90:
			self.rsp = 'rock'

L = 1
R = -1
hand1 = Hand(R)
hand2 = Hand(L)
menu = 1
shake_dir = 1
shake_time = 0
shake_angle = 0
random1 = 0
random2 = 0

def init_shake():
	global shake_time
	global shake_angle
	global shake_dir
	global menu
	if shake_time > 5:
		shake_angle += 5
		if shake_angle == 90:
			menu = 2
			shake_time = 0
			shake_dir = 1
	else:
		shake_angle += 5 * shake_dir
		if shake_angle > 60 or shake_angle < -30:
			shake_dir = -1 * shake_dir
			shake_time += 1

def rsp_shake():
	global shake_time
	global shake_angle
	global shake_dir
	global menu
	global random1
	global random2

	if shake_time > 3:
		shake_angle += 5
		if shake_angle == 90:
			menu = 5
			shake_time = 0
			shake_dir = 1
			random1 = np.random.randint(3)
			random2 = np.random.randint(3)
	else:
		shake_angle += 5 * shake_dir
		if shake_angle > 100 or shake_angle < 40:
			shake_dir = -1 * shake_dir
			shake_time += 1

def Timer(unused):
	global hand1
	global hand2
	global menu
	global shake_time
	global shake_angle
	global random1
	global random2
	'''
	menu 1 -> 초기에 인사 하는 부분
	menu 2 -> 주먹을 쥐는 부분
	menu 3 -> 주먹 쥔 상태로 기다리는 부분
	menu 4 -> 가위바위보 하려고 손 흔드는 부분
	menu 5 -> 가위바위보 중 하나를 내는 부분
	menu 6 -> 가위바위보를 낸 상태에서 기다리는 부분
	'''
	if menu == 1:
		init_shake()
	if menu == 2:
		hand1.rsp_to_r(9)
		hand2.rsp_to_r(9)
		if hand1.rotate_num == 90:
			menu = 3
	if menu == 4:
		rsp_shake()
	if menu == 5:
		rsp_list = ['rock','scissors','paper']
		hand1.r_to_rsp(rsp_list[random1],9)
		hand2.r_to_rsp(rsp_list[random2],9)
		if hand1.rotate_num == 0:
			menu = 6
	glutPostRedisplay()
	glutTimerFunc(timeStep, Timer, 1)


def draw_hand(hand):
	a1 = hand.state[0]
	a2 = hand.state[1]
	a3 = hand.state[2]
	a4 = hand.state[3]
	a5 = hand.state[4]

	# 손바닥
	glColor3f(1, 1, 0)
	glPushMatrix()
	glScalef(20,20, 4)
	glutSolidCube(1)
	glPopMatrix()

	#엄지
	glPushMatrix()
	glTranslatef(-11, 0, 0)
	glRotatef(60, 0, 0, 1)
	glRotate(a1, 1, 0, 0)
	draw_knuckle(4, 7, 4, 1, 0, 0)
	glPushMatrix()
	glTranslatef(0, 9, 0)
	glRotate(a1, 1, 0, 0)
	draw_knuckle(4, 6, 4, 0.9, 0.1, 0)
	glPopMatrix()
	glPopMatrix()

	#검지
	glPushMatrix()
	glTranslatef(-8, 11, 0)
	glRotate(a2, 1, 0, 0)
	glRotate(10,0,0,1)
	draw_knuckle(4, 7, 4,  1, 0.5, 0)
	glPushMatrix()
	glTranslatef(0, 9, 0)
	glRotate(a2, 1, 0, 0)
	draw_knuckle(4, 6, 4, 0.9, 0.6, 0)
	glPushMatrix()
	glTranslatef(0, 8, 0)
	glRotate(a2, 1, 0, 0)
	draw_knuckle(4, 5, 4, 0.8, 0.7, 0)
	glPopMatrix()
	glPopMatrix()
	glPopMatrix()

	#중지
	glPushMatrix()
	glTranslatef(-2.7, 11, 0)
	glRotate(a3, 1, 0, 0)
	glRotate(3, 0, 0, 1)
	draw_knuckle(4, 8, 4, 0.1, 0.9, 0)
	glPushMatrix()
	glTranslatef(0, 10, 0)
	glRotate(a3, 1, 0, 0)
	draw_knuckle(4, 6, 4, 0.2, 0.8, 0)
	glPushMatrix()
	glTranslatef(0, 8, 0)
	glRotate(a3, 1, 0, 0)
	draw_knuckle(4, 5, 4, 0.3, 0.7, 0)
	glPopMatrix()
	glPopMatrix()
	glPopMatrix()

	#약지
	glPushMatrix()
	glTranslatef(2.7, 11, 0)
	glRotate(a4, 1, 0, 0)
	glRotate(-3, 0, 0, 1)
	draw_knuckle(4, 7, 4, 0,  0.5, 0.5)
	glPushMatrix()
	glTranslatef(0, 9, 0)
	glRotate(a4, 1, 0, 0)
	draw_knuckle(4, 6, 4, 0, 0.4, 0.6)
	glPushMatrix()
	glTranslatef(0, 8, 0)
	glRotate(a4, 1, 0, 0)
	draw_knuckle(4, 5, 4, 0, 0.3, 0.7)
	glPopMatrix()
	glPopMatrix()
	glPopMatrix()

	#새끼
	glColor3f(0.2, 0.8, 0)
	glPushMatrix()
	glTranslatef(8, 11, 0)
	glRotate(a5, 1, 0, 0)
	glRotate(-10, 0, 0, 1)
	draw_knuckle(4, 6, 4, 0.5,  0, 0.5)
	glPushMatrix()
	glTranslatef(0, 8, 0)
	glRotate(a5, 1, 0, 0)
	draw_knuckle(4, 4, 4, 0.4 ,0 ,0.6)
	glPushMatrix()
	glTranslatef(0, 6, 0)
	glRotate(a5, 1, 0, 0)
	draw_knuckle(4, 4, 4, 0.3, 0, 0.7)
	glPopMatrix()
	glPopMatrix()
	glPopMatrix()

def draw_knuckle(x,y,z,r,g,b):
	draw_joint()
	glPushMatrix()
	glTranslatef(0, y/2+1, 0)
	glScalef(x,y,z)
	glColor3f(r,g,b)
	glutSolidCube(1)
	glPopMatrix()



def draw_joint():
	glPushMatrix()
	glColor3f(0.5,0.5,0.7)
	glutSolidSphere(2, 50, 50)
	glPopMatrix()



def display():
	global menu
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glEnable(GL_DEPTH_TEST)
	glClearColor(0.1, 0.1, 0.1, 1.0)
	if menu == 6:
		i = 0
		s = ["Left win!","Right win!", "DRAW"]
		if random1 == random2:
			i = 2
		elif random1 + 1 == random2 or random1 - 2 == random2:
			i = 1
		else:
			i = 0
		glColor3f(1.0, 1.0, 1.0)
		glPushMatrix()
		glRasterPos(-10, 20)
		for ch in s[i]:
			glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(ch)))
		glPopMatrix()
	if menu == 1:
		s = "!!Rock-Scissors-Paper Simulator!!"
		glColor3f(1.0, 1.0, 1.0)
		glPushMatrix()
		glRasterPos(-30, -20)
		for ch in s:
			glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(ch)))
		glPopMatrix()
	loadGlobalCoord()

	glPushMatrix()
	glTranslatef(-50, 0, 0)
	glRotate(-shake_angle, 0, 0, 1)
	draw_hand(hand2)
	glPopMatrix()

	glPushMatrix()
	glTranslatef(50,0,0)
	glRotate(shake_angle, 0, 0, 1)
	glRotatef(180, 0, 1, 0)
	draw_hand(hand1)
	glPopMatrix()



	glutSwapBuffers()


if __name__ == "__main__":
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(width, height)
	glutInitWindowPosition( 100, 0 )
	glutCreateWindow("ROCK-SCISSORS-PAPER_Simulator")
	glutReshapeFunc(resize)
	glutDisplayFunc(display)
	glutTimerFunc(timeStep, Timer, 1)
	glutKeyboardFunc(glutKeyboard)
	glutMouseFunc(glutMouse)
	glutMotionFunc(glutMotion)
	glutMainLoop()

