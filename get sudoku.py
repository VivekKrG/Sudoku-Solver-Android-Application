import numpy as np
import cv2


class ImageToMat:
	field_threshold = {'1': 0.6, '2': 0.6, '3': 0.5, '4': 0.68, '5': 0.55, '6': 0.63, '7': 0.6, '8': 0.55, '9': 0.55}

	def __init__(self, directory):
		self.directory = directory  # directory should be path of image (in string)
		# Read the original document image
		self.img = cv2.imread(directory)
		# cv2.imshow('ss', self.img)
		# cv2.waitKey(0)
		self.img_gray = None
		# sudoku matrix will keep result
		self.sudoku = [[0 for i in range(9)] for j in range(9)]

	def scan_image(self):
		# Firstly resize image
		self.img = cv2.resize(self.img, (360, 360))
		# cv2.imshow('img', img)
		# cv2.waitKey(0)

		# Clean background as white and full darken the numbers and grids(3D=>2D).
		lower_white = np.array([160, 160, 160], dtype=np.uint8)
		upper_white = np.array([255, 255, 255], dtype=np.uint8)
		self.img_gray = cv2.inRange(self.img, lower_white, upper_white)  # could also use threshold
		# cv2.imshow('img gray', img_gray)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		imgheight = self.img_gray.shape[0]
		imgwidth = self.img_gray.shape[1]

		m = imgheight // 9
		n = imgwidth // 9

		row = 0
		col = 0
		for y in range(0, imgheight, m):
			for x in range(0, imgwidth, n):
				y1 = y + m
				x1 = x + n
				tiles = self.img_gray[y:y1, x:x1]

				for i in range(9, 0, -1):
					directory = "sudoku_temp/{}.png".format(i)
					template = cv2.imread(directory, 0)
					# img[y:y1, x:x1] = getBoxed(im.copy(), tiles.copy(), template, str(i))
					res = cv2.matchTemplate(tiles, template, cv2.TM_CCOEFF_NORMED)

					# cv2.imshow('tiles :img gray', tiles)
					# cv2.waitKey(100)
					hits = np.where(res >= ImageToMat.field_threshold[str(i)])

					# print(type(hits)) -> <class 'tuple'>
					# print(hits) -> (array([], dtype=int32), array([], dtype=int32))
					if hits[0].size > 0:
						self.sudoku[row][col] = i
						# print('found length:', hits[0].size, 'number found:', i)
						break
				col += 1
			row += 1
			col = 0


image_path = 'im4.jpg'
image_tomat = ImageToMat(image_path)
image_tomat.scan_image()
cv2.imshow('scanned', image_tomat.img_gray)

for row in image_tomat.sudoku:
	print(row)
cv2.waitKey(0)