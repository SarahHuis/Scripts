import os
os.system('cls')
path = r'C:\Users\Sarah\Documents\Blender\Scripts\Tutorials\Donut\Donut.py'
path = os.path.realpath(path)
exec(compile(open(path).read(), path, 'exec'))