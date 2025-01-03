import argparse
import os
from PIL import Image
from sys import argv
import numpy as np

parser = argparse.ArgumentParser(description='Конвертация изображения в текст')
parser.add_argument("filename", type=str, help="Путь к файлу с картинкой")
parser.add_argument("-d", "--debug", help="Показывать процесс обработки", action="store_true")
parser.add_argument("-o", "--output", type=str, default="", help="Сохранение в файл")
parser.add_argument("-s", "--size", type=int, default=-1, help="Размер изобрадения по горизонтали")
args = parser.parse_args()

cr = 13/24

def resize(img, size):
	width, height = img.size
	if width > height:
		ratio = width / size
		new_height = int(height / ratio)
		new_height = int(height)
		new_size = (size, int(new_height*cr))
	else:
		ratio = height / size
		new_width = int(width / ratio)
		new_size = (new_width, int(size*cr))
	img = img.resize(new_size, Image.LANCZOS)
	return img


img = Image.open(args.filename)

if args.size == -1: size = os.get_terminal_size()[0]
else: size = args.size
nimg = resize(img, size)

i = np.array(nimg)
print("\033[H\033[2J")

text = ""
step = 0
max = len(i)*len(i[0])
for line in i:
	for pix in line:
		step += 1
		r, g, b = pix[0], pix[1], pix[2]
		r, g, b = int(r), int(g), int(b)
		text += f"\033[48;2;{r};{g};{b}m "
		if args.debug: print(f"\033[H{step}/{max} ({round(step/max*100, 2)}%)")
	text += "\033[0;0m\n"

print("\033[H\033[2J")
print(text)

if args.output != "":
	with open(args.output, "w") as f:
		f.write(text)
