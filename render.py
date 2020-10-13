"""
Sebastian G0nzalez
A simple screen viewer for starting in grafics class
BMP image renderer and you make lines

"""
#librarys:
import struct
import random
from encoder import *
from obj import Obj
#object render

def color(r, g, b):
	return bytes([b, g, r])

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

class Render(object):
	def __init__(self):																
		self.width = 500	#default						
		self.height = 500	#default				
		self.x = 0
		self.x_width = self.width
		self.y = 0
		self.y_height = self.height
		self.colorClear = self.rgbToColor(1,1,1)
		self.colorVertex = self.rgbToColor(0,0,0)
		self.framebuffer = []
		self.clear()

    #convert to color RGB
	def rgbToColor(self,r,g,b):
		return bytes([b*255,g*255,r*255])

    #relative means from the point where the point is
	def getRelativeCoordinate(self, point, horizontal=True):
		if(horizontal):
			return ((point)/(self.x_width/2))-1
		return ((point)/(self.y_height/2))-1
    

	def getRealCoordinate(self, point, horizontal=True):
		if(horizontal):												#If its an horizontal coordinate
			if(point>=1):												#To avoid index out of range
				return self.x + self.x_width - 1			
			return int((point+1)*(self.x_width/	2))+self.x
		elif(point>=1):													#To avoid index out of range
			return self.y + self.y_height - 1
		return int((point+1)*(self.y_height/2))+self.y

	def clear(self):
		self.framebuffer = [
			[self.colorClear for x in range(self.width)] 
			for y in range(self.height)
		]


	def clearColor(self, r, g, b):
		self.colorClear = self.rgbToColor(r,g,b)

	def CreateWindow(self,width,height):
		self.width = width
		self.height = height
		self.x = 0
		self.x_width = self.width
		self.y = 0
		self.y_height = self.height
		self.clear()								#This function will initialite the framebuffer with the specified width and height

	def viewPort(self, x, y, width, height):
		self.x = x
		self.x_width = width
		self.y = y
		self.y_height = height

	def vertex(self,x,y):
		realX = self.getRealCoordinate(x)
		realY = self.getRealCoordinate(y,False)
		self.framebuffer[realY][realX] = self.colorVertex

	def color(self,r,g,b):
		self.colorVertex = self.rgbToColor(r,g,b)

	#we need (x1,y1 --> x2,y2)	to make a line
	def line(self,relative_x1, relative_y1, relative_x2, relative_y2):
		x1 = self.getRealCoordinate(relative_x1)
		x2 = self.getRealCoordinate(relative_x2)
		y1 = self.getRealCoordinate(relative_y1,False)
		y2 = self.getRealCoordinate(relative_y2,False)
		steep=abs(y2 - y1)>abs(x2 - x1)
		if steep:
			x1, y1 = y1, x1
			x2, y2 = y2, x2
		if x1>x2:
			x1,x2 = x2,x1
			y1,y2 = y2,y1

		dy = abs(y2 - y1)
		dx = abs(x2 - x1)
		y = y1
		offset = 0
		threshold = dx

		for x in range(x1, x2):
			if offset>=threshold:
				y += 1 if y1 < y2 else -1
				threshold += 2*dx
			if steep:
				self.framebuffer[x][y] = self.colorVertex
			else:
				self.framebuffer[y][x] = self.colorVertex
			offset += 2*dy

	def point(self,x,y):
		self.framebuffer[y][x] = self.colorVertex

	def ray(self, x1, y1, x2, y2):
		toReturn=[]
		#steep => pendiente
		steep= abs(y2 - y1) > abs(x2 - x1)
		if steep:
			x1, y1 = y1, x1
			x2, y2 = y2, x2
		if x1 > x2:
			x1, x2 = x2, x1
			y1, y2 = y2, y1
		
		dy = abs(y2 - y1)
		dx = abs(x2 - x1)
		y = y1
		offset = 0
		threshold = dx

		for x in range(x1, x2):

			if offset >= threshold:
				y += 1 if y1 < y2 else -1
				threshold += 2*dx

			if steep:
				self.framebuffer[x][y] = self.colorVertex
				toReturn.append([y,x])
			else:
				self.framebuffer[y][x] = self.colorVertex
				toReturn.append([x,y])
			
			offset += 2*dy

		return toReturn








	#function that will paint in certain area,
	#of certain color specified
	#color -- rgb
	def paint(self, points, color):
		self.colorVertex=color

		if(len(points)>3):
			#initial statements
			centers_x = [0,0]
			centers_y = [0,0]
			points_count = 0
			#loop in points to find the centers of points of the figure
			for point in points:
				if (points_count%2 == 1) :
					centers_x[0] += point[0]
					centers_y[0] += point[1]
				else:
					centers_x[1] += point[0]
					centers_y[1] += point[1]

				points_count += 1
			
			#redondea los valores del centro pero toma en cuenta el points count
			centers_x[0] = round(centers_x[0] / points_count)*2 
			centers_y[0] = round(centers_y[0] / points_count)*2
			centers_x[1] = round(centers_x[1] / points_count)*2 
			centers_y[1] = round(centers_y[1] / points_count)*2

			#loop that woudlnt get of while 
			for center_x in centers_x:
				for center_y in centers_y:
					for index in range(len(points)):
						for pixel in self.ray(points[index][0],points[index][1], points[index-1][0], points[index-1][1]):
							self.ray(center_x, center_y, pixel[0], pixel[1])
					
					for pixel in self.ray(points[-1][0],points[-1][1],points[0][0],points[0][1]):
						self.ray(center_x,center_y,pixel[0],pixel[1])

		else:
			center_x = 0
			center_y = 0
			points_count = 0

			for point in points:
				center_x += point[0]
				center_y += point[1]
				points_count += 1
			
			center_x = round(center_x/points_count)
			center_y = round(center_y/points_count)

			for index in range(len(points)):
				for pixel in self.ray(points[index][0],points[index][1],points[index-1][0],points[index-1][1]):
					self.ray(center_x,center_y,pixel[0],pixel[1])

			for pixel in self.ray(points[-1][0],points[-1][1],points[0][0],points[0][1]):
				self.ray(center_x,center_y,pixel[0],pixel[1])



	def load(self, filename, translate, scale):
		model = Obj(filename)

		for face in model.faces:
			vcount = len(face)

			for dot in range(vcount):
				f1 = face[dot][0]
				f2 = face[(dot + 1) % vcount][0]

				v1 = model.vertices[f1 -1]
				v2 = model.vertices[f2 - 1]

				x1 = round((v1[0] + translate[0]) * scale[0])
				y1 = round((v1[1] + translate[1]) * scale[1])
				x2 = round((v2[0] + translate[0]) * scale[0])
				y2 = round((v2[1] + translate[1]) * scale[1])
				print(x1, y1, x2, y2)
				self.ray(x1, y1, x2, y2)



	def finish(self,filename):
		f = open(filename, 'bw')   #bw bytes writing

		#File header
		f.write(char('B'))
		f.write(char('M'))
		f.write(dword(14 + 40 + self.width*self.height*3))
		f.write(dword(0))
		f.write(dword(14 + 40 ))

		# Image Header
		f.write(dword(40))
		f.write(dword(self.width))
		f.write(dword(self.height))
		f.write(word(1))
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(self.width*self.height*3))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))

		# pixel data
		for x in range(self.height):
			for y in range(self.width):
				f.write(self.framebuffer[x][y])

		f.close()