#-*- coding:utf-8 -*-

import numpy as np 
import csv
import math
import sys

class Searcher:
	def __init__(self, indexPath):
		# armazena o caminho para o indice 
		self.indexPath = indexPath

	def search(self, queryFeatures, limit, distance):
		# inicializa o dicionario que contera os resultados
		# e' do tipo {imageID, score}
		# imageID (chave) = numero da imagem
		# score = quao similar a imageID e' em relacao 'a query
		results = {}

		# abre o arquivo com o indice
		with open(self.indexPath) as f:
			# inicializa o leitor de arquivos csv
			reader = csv.reader(f)

			# percorre por todas as linhas do arquivo de indice (cada linha e' um vetor de caracteristicas de uma imagem do banco)
			for row in reader:
				# recupera o vetor de caracteristicas e armazena em features
				features = [float(x) for x in row[1:]]
				# calcula a similaridade entre uma imagem e a query
				if distance.upper() == "CHI2":
					score = self.chi2_distance(features, queryFeatures)
				elif distance.upper() == "MANHATTAN": 
					score = self.manhattan_distance(features, queryFeatures)
				elif distance.upper() == "EUCLIDEAN":
					score = self.euclidean_distance(features, queryFeatures)
				else:
					sys.exit("Metrica de distancia invalida!")

				# adiciona o resultado ao dicionario
				results[row[0]] = score

			f.close()

		# ordena em ordem decrescente (imagem mais similares primeiro)
		results = sorted([(v, k) for (k, v) in results.items()])

		return results[:limit]

	def chi2_distance(self, histA, histB, eps = 1e-10):
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

		return d

	def manhattan_distance(self, histA, histB):
		d = np.sum([abs((a - b)) for (a, b) in zip(histA, histB)])

		return d

	def euclidean_distance(self, histA, histB):
		d = math.sqrt(np.sum([(a - b) ** 2 for (a, b) in zip(histA, histB)]))

		return d


