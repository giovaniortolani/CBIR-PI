#-*- coding:utf-8 -*-

import cv2

class GCHDescriptor:
	def __init__(self, bins):
		# armazena o numero de celulas que sera divido o histograma de cada canal
		self.bins = bins

	def describe(self, image):
		# converte a imagem para HSV
		# inicializa o vetor das caracterisicas extraidas da imagem
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []

		# extrai o histograma da imagem atraves da mascara dada e normaliza
		# OpenCV usa Hue como um valor entre 0 e 180, Saturation e Value entre 0 e 255
		features = cv2.calcHist([image], [0, 1, 2], None, self.bins, [0, 180, 0, 256, 0, 256])
		features = cv2.normalize(features).flatten()

		return features