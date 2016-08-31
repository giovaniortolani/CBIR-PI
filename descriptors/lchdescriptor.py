#-*- coding:utf-8 -*-

import cv2
import numpy as np

class LCHDescriptor:
	def __init__(self, bins):
		# armazena o numero de celulas que sera divido o histograma de cada canal
		self.bins = bins

	def describe(self, image):
		# converte a imagem para HSV
		# inicializa o vetor das caracterisicas extraidas da imagem
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []

		# computa o centro da imagem
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))

		# divide a imagem em quatro regioes (4 retangulos iguais)
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]

		# gera uma mascara em forma de elipse no centro da imagem
		(axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

		# itera sobre os retangulos
		for (startX, endX, startY, endY) in segments:
			# gera uma mascara em cada retangulo atraves da subtracao da elipse (retangulo - elipse)
			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)

			# extrai o histograma da mascara gerada e armazena no vetor das caracteristicas
			hist = self.histogram(image, cornerMask)
			features.extend(hist)

		# extrai o histograma da elipse e armazena no vetor de caracteristicas
		hist = self.histogram(image, ellipMask)
		features.extend(hist)

		return features

	def histogram(self, image, mask):
		# extrai o histograma da imagem atraves da mascara dada e normaliza
		# OpenCV usa Hue como um valor entre 0 e 180, Saturation e Value entre 0 e 255
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
		hist = cv2.normalize(hist).flatten()

		return hist
