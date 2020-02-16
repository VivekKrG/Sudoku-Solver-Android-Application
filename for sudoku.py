# importing libraries
import numpy as np
import cv2

field_threshold = {'1': 0.6, '2': 0.6, '3': 0.5, '4': 0.68, '5': 0.55, '6': 0.63, '7': 0.6, '8': 0.55, '9': 0.55}


# Function to Generate bounding
# boxes around detected fields
def getBoxed(img, img_gray, template, field_name="policy_no"):
	w, h = template.shape[::-1]

	# Apply template matching
	res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

	hits = np.where(res >= field_threshold[field_name])

	# Draw a rectangle around the matched region.
	for pt in zip(*hits[::-1]):
		cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

		y = pt[1] - 10 if pt[1] - 10 > 10 else pt[1] + h + 20

		cv2.putText(img, field_name, (pt[0], y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)

	return img


# Driver Function
if __name__ == '__main__':
	# Read the original document image
	# img = cv2.imread('sudoku_temp/template.jpg')
	img = cv2.imread('im1.jpg')
	cv2.imshow('ss', img)
	cv2.waitKey(0)

	img = cv2.resize(img, (360, 360))
	# cv2.imshow('img', img)
	# cv2.waitKey(0)

	lower_white = np.array([160, 160, 160], dtype=np.uint8)
	upper_white = np.array([255, 255, 255], dtype=np.uint8)
	img_gray = cv2.inRange(img, lower_white, upper_white)  # could also use threshold

	# 3-d to 2-d conversion

	# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imshow('img gray', img_gray)
	cv2.waitKey(0)
	# cv2.destroyAllWindows()

	# ----------
	imgheight = img_gray.shape[0]
	imgwidth = img_gray.shape[1]

	M = imgheight // 9
	N = imgwidth // 9
	print('image height:', imgheight, 'width:', imgwidth, 'M:', M)

	sudoku = [[0 for i in range(9)] for j in range(9)]

	# for i in range(9):
	# 	print(sudoku[i])

	row = 0
	col = 0
	for y in range(0, imgheight, M):
		for x in range(0, imgwidth, N):
			y1 = y + M
			x1 = x + N
			tiles = img_gray[y:y + M, x:x + N]

			# im = img[y:y1, x:x1]
			# cv2.imshow('grid:', im)
			# cv2.waitKey(500)
	# ------------

			for i in range(9, 0, -1):
				directory = "sudoku_temp/{}.png".format(i)
				template = cv2.imread(directory, 0)
				# img[y:y1, x:x1] = getBoxed(im.copy(), tiles.copy(), template, str(i))
				res = cv2.matchTemplate(tiles, template, cv2.TM_CCOEFF_NORMED)

				# cv2.imshow('tiles :img gray', tiles)
				# cv2.waitKey(100)
				hits = np.where(res >= field_threshold[str(i)])

				# print(type(hits)) -> <class 'tuple'>
				# print(hits) -> (array([], dtype=int32), array([], dtype=int32))
				if hits[0].size > 0:
					sudoku[row][col] = i
					# print('found length:', hits[0].size, 'number found:', i)
					break
			# else:
			# 	print('found nothing, returning 0')

			# print(row, col, end=' | ')
			col += 1
		# print()
		row += 1
		col = 0

	cv2.imwrite("sudoku_output.png", img)
	# cv2.imwrite("Me_Rakesh_Output.jpg", img)
	# cv2.imshow('Detected', img)
	print()
	for i in range(9):
		print(sudoku[i])