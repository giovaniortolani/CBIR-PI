#-*- coding:utf-8 -*-

import cv2
import numpy as np
import sys

class FourierDescriptor:

	def __init__(self, maskSize):
		# armazena o tamanho da mascara
		self.maskSize = maskSize

	def shift_dft(self, src, dst = None):
	    '''
	        Rearrange the quadrants of Fourier image so that the origin is at
	        the image center. Swaps quadrant 1 with 3, and 2 with 4.

	        src and dst arrays must be equal size & type
	    '''
	    if dst is None:
	    	dst = np.empty(src.shape, src.dtype)
	    elif src.shape != dst.shape:
	    	raise ValueError("src and dst must have equal sizes")
	    elif src.dtype != dst.dtype:
	    	raise TypeError("src and dst must have equal types")

		if src is dst:
			ret = np.empty(src.shape, src.dtype)
		else:
			ret = dst

		h, w = src.shape[:2]

		cx1 = cx2 = w/2
		cy1 = cy2 = h/2

	    # if the size is odd, then adjust the bottom/right quadrants
		if w % 2 != 0:
			cx2 += 1
		if h % 2 != 0:
			cy2 += 1

	    # swap quadrants

		# swap q1 and q3
		ret[h-cy1:, w-cx1:] = src[0:cy1 , 0:cx1 ]   # q1 -> q3
		ret[0:cy2 , 0:cx2 ] = src[h-cy2:, w-cx2:]   # q3 -> q1

		# swap q2 and q4
		ret[0:cy2 , w-cx2:] = src[h-cy2:, 0:cx2 ]   # q2 -> q4
		ret[h-cy1:, 0:cx1 ] = src[0:cy1 , w-cx1:]   # q4 -> q2

		if src is dst:
		    dst[:,:] = ret

		dst2 = cv2.normalize(dst).flatten()
		print (dst2)
		print (len(dst2))

		return dst

	def describe(self, image):
		#Convert to graysacale
		im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		features = []
		h, w = im.shape[:2]

		realInput = im.astype(np.float64)

		# perform an optimally sized dft
		dft_M = cv2.getOptimalDFTSize(w)
		dft_N = cv2.getOptimalDFTSize(h)

		# copy A to dft_A and pad dft_A with zeros
		dft_A = np.zeros((dft_N, dft_M, 2), dtype=np.float64)
		dft_A[:h, :w, 0] = realInput

		# no need to pad bottom part of dft_A with zeros because of
		# use of nonzeroRows parameter in cv2.dft()
		cv2.dft(dft_A, dst=dft_A, nonzeroRows=h)

		# Split fourier into real and imaginary parts
		image_Re, image_Im = cv2.split(dft_A)

		# Compute the magnitude of the spectrum Mag = sqrt(Re^2 + Im^2)
		magnitude = cv2.sqrt(image_Re**2.0 + image_Im**2.0)

		# Compute log(1 + Mag)
		log_spectrum = cv2.log(1.0 + magnitude)

		# Rearrange the quadrants of Fourier image so that the origin is at
		# the image center
		self.shift_dft(log_spectrum, log_spectrum)

		# normalize and display the results as rgb
		cv2.normalize(log_spectrum, log_spectrum, 0.0, 1.0, cv2.NORM_MINMAX)

		h, w = log_spectrum.shape[:2]
		
		#Calcula media com uma mascara de 3x3		
		if(self.maskSize == 3):
			i_h = 1
			while i_h < h:
				i_w = 1
				while i_w < w:
					s = log_spectrum[i_h-1, i_w-1] + log_spectrum[i_h-1, i_w] + log_spectrum[i_h-1, i_w+1] + log_spectrum[i_h, i_w-1] + log_spectrum[i_h, i_w] + log_spectrum[i_h, i_w+1] + log_spectrum[i_h+1, i_w-1] + log_spectrum[i_h+1, i_w] + log_spectrum[i_h+1, i_w+1]
					p = s/9
					features.append(p)
					i_w += 3
				i_h += 3
		
		#Calcula media com uma mascara de 5x5
		elif(self.maskSize == 5):
			i_h = 2
			while i_h < h:
				i_w = 2
				while i_w < w:
					s = log_spectrum[i_h-2, i_w-2] + log_spectrum[i_h-2, i_w-1] + log_spectrum[i_h-2, i_w+1] + log_spectrum[i_h-2, i_w] + log_spectrum[i_h-2, i_w+1] + log_spectrum[i_h-2, i_w+2]
					s += log_spectrum[i_h-1, i_w-2] + log_spectrum[i_h-1, i_w-1] + log_spectrum[i_h-1, i_w+1] + log_spectrum[i_h-1, i_w] + log_spectrum[i_h-1, i_w+1] + log_spectrum[i_h-1, i_w+2]
					s += log_spectrum[i_h, i_w-2] + log_spectrum[i_h, i_w-1] + log_spectrum[i_h, i_w+1] + log_spectrum[i_h, i_w] + log_spectrum[i_h, i_w+1] + log_spectrum[i_h, i_w+2]
					s += log_spectrum[i_h+1, i_w-2] + log_spectrum[i_h+1, i_w-1] + log_spectrum[i_h+1, i_w+1] + log_spectrum[i_h+1, i_w] + log_spectrum[i_h+1, i_w+1] + log_spectrum[i_h+1, i_w+2]
					s += log_spectrum[i_h+2, i_w-2] + log_spectrum[i_h+2, i_w-1] + log_spectrum[i_h+2, i_w+1] + log_spectrum[i_h+2, i_w] + log_spectrum[i_h+2, i_w+1] + log_spectrum[i_h+2, i_w+2]
					p = s/25
					features.append(p)
					i_w += 5
				i_h += 5
		#Calcula media com uma mascara de 7x7
		elif(self.maskSize == 7):
			i_h = 3
			while i_h < h-7:
				i_w = 3
				while i_w < w-7:
					s = log_spectrum[i_h-3, i_w-3] + log_spectrum[i_h-3, i_w-2] + log_spectrum[i_h-3, i_w-1] + log_spectrum[i_h-3, i_w] + log_spectrum[i_h-3, i_w+1] + log_spectrum[i_h-3, i_w+2] + log_spectrum[i_h-3, i_w+3]
					s += log_spectrum[i_h-2, i_w-3] + log_spectrum[i_h-2, i_w-2] + log_spectrum[i_h-2, i_w-1] + log_spectrum[i_h-2, i_w] + log_spectrum[i_h-2, i_w+1] + log_spectrum[i_h-2, i_w+2] + log_spectrum[i_h-2, i_w+3]
					s += log_spectrum[i_h-1, i_w-3] + log_spectrum[i_h-1, i_w-2] + log_spectrum[i_h-1, i_w-1] + log_spectrum[i_h-1, i_w] + log_spectrum[i_h-1, i_w+1] + log_spectrum[i_h-1, i_w+2] + log_spectrum[i_h-1, i_w+3]
					s += log_spectrum[i_h, i_w-3] + log_spectrum[i_h, i_w-2] + log_spectrum[i_h, i_w-1] + log_spectrum[i_h, i_w] + log_spectrum[i_h, i_w+1] + log_spectrum[i_h, i_w+2] + log_spectrum[i_h, i_w+3]
					s += log_spectrum[i_h+1, i_w-3] + log_spectrum[i_h+1, i_w-2] + log_spectrum[i_h+1, i_w-1] + log_spectrum[i_h+1, i_w] + log_spectrum[i_h+1, i_w+1] + log_spectrum[i_h+1, i_w+2] + log_spectrum[i_h+1, i_w+3]
					s += log_spectrum[i_h+2, i_w-3] + log_spectrum[i_h+2, i_w-2] + log_spectrum[i_h+2, i_w-1] + log_spectrum[i_h+2, i_w] + log_spectrum[i_h+2, i_w+1] + log_spectrum[i_h+2, i_w+2] + log_spectrum[i_h+2, i_w+3]
					s += log_spectrum[i_h+3, i_w-3] + log_spectrum[i_h+3, i_w-2] + log_spectrum[i_h+3, i_w-1] + log_spectrum[i_h+3, i_w] + log_spectrum[i_h+3, i_w+1] + log_spectrum[i_h+3, i_w+2] + log_spectrum[i_h+3, i_w+3]
					p = s/49
					features.append(p)
					i_w += 7
				i_h += 7

		return features