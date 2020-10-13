from render import Render

gl = Render()										
gl.CreateWindow(9000,9000)
gl.clearColor(0,0,0)
gl.clear()
gl.color(1,1,1)
gl.load('./tarea1/Bowl.obj', (40, 40), (40, 40))
gl.finish('Bigmax.bmp')
