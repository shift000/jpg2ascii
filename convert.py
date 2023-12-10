# CONVERT.PY
import sys, os

# Todo : add input filepath

from PIL import Image
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='convert .jpg to ascii image')
parser.add_argument('file', help='image file to process')
parser.add_argument('-s', '--space', help='use space to expand?', action='store_true')
parser.add_argument('-bs', '--blocksize', help='use space to expand?', required=False)
parser.add_argument('-i', '--inverted', help='invert ascii table', required=False, default="y", action='store_false')
parser.add_argument('-f', '--force', help='force more chars', required=False, nargs='?', const=1, type=int)
parser.add_argument('-e', '--extract', help='delete border chars', required=False, nargs='?', const=5, type=int)

args = parser.parse_args()

def expand_charmap(charmap, repetition):
	expanded_charmap = {}
	for key, value in charmap.items():
		for i in range(repetition):
			expanded_charmap[key * repetition + i] = value
	return expanded_charmap

charmap = {
	 0: ".", 1: ",", 2: "-", 3: "_", 4: "~", 5: "*", 6: "+", 7: ":", 8: ";", 9: "]",
    10: "}", 11: "{", 12: "[", 13: "(", 14: ")", 15: "=", 16: "/", 17: "\\", 18: "!",
    19: "?", 20: "§", 21: "%", 22: "@", 23: "&", 24: "$", 25: "#"
}

charmap = expand_charmap(charmap, args.force if args.force else 1)
charlen = len(charmap)-1

if args.extract:
	for e in range(args.extract):
		charmap[e] = " "

print(args.inverted)
if args.inverted:
	charmap_inv = {}
	chark = list(charmap.keys())

	pointer = 0
	for e in range(charlen, -1, -1):
		charmap_inv[chark[pointer]] = charmap[e]
		pointer += 1
	charmap = charmap_inv

spacer = ""
tuneR, tuneG, tuneB = 8, 1, 4

if args.file:		# SYS ARGUMENT
	file = args.file
else:
	print("No file given")
	exit()

try:
	im = np.array(Image.open(file))
except:
	print("error opening file {file}")
	exit()

img_height = im.shape[0]
img_width = im.shape[1]

term_size = os.get_terminal_size()[0]-2

if args.blocksize:
	if args.space:
		term_size /= 2
		spacer = " "
	block_size = float(args.blocksize)
else:
	if args.space:
		term_size /= 2
		spacer = " "
	block_size = float(img_width / term_size)

wBlocks = int(img_width/block_size)
wBlocks = wBlocks + 1 if img_width%block_size > 0 else wBlocks

hBlocks = int(img_height/block_size)
hBlocks = hBlocks + 1 if img_height%block_size > 0 else hBlocks


print(f'[+] Öffne image {file}')
print(f'[?] {img_width}x{img_height}, wBlocks : {wBlocks}, hBlocks : {hBlocks}, Blocksize : {block_size}')

mace = np.zeros([hBlocks, wBlocks], dtype=int)

for i, i_w in enumerate(im):
	for e, i_h in enumerate(i_w):
		y = int(i/block_size)
		x = int(e/block_size)
		
		try:
			val = int((tuneR*(i_h[0]/100) + tuneG*(i_h[1]/100) + tuneB*(i_h[2]/100)))
		except IndexError:
			#print(f"mumble mumble {y} {x}")
			continue
			
		if val > 20:
			continue
		
		mace[y][x] += val
			
mmax = max(mace[1])

for i, itemW in enumerate(mace):
	line = ""
	for itemH in itemW:
		try:
			divisor = int(mmax/charlen) if int(mmax/charlen) > 0 else 1
			case = charlen - ( int(itemH / divisor)-1 )
		except ValueError:
			continue
		
		if case < 0:
			case = 1
		elif case > charlen:
			case = charlen
		
		line += f'{spacer}{charmap[case]}'
	print(line)