#-*- coding:utf-8 -*-

import cv2
import argparse
import time
import sys
from descriptors.fourierdescriptor import FourierDescriptor
from descriptors.gchdescriptor import GCHDescriptor
from descriptors.lchdescriptor import LCHDescriptor
from searcher import Searcher

# realiza a checagem do numero de imagens semelhantes 'a query
def check_negative(value):
    ivalue = int(value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("Entre com um valor entre 1 e 10000.")
    return ivalue	

# realiza a checagem do tamanho da mascara de Fourier
def check_mask(value):
    ivalue = int(value)
    if ivalue != 3 and ivalue != 5 and ivalue != 7:
        raise argparse.ArgumentTypeError("Tamanho da mascara deve ser 3, 5 ou 7.")
    return ivalue

# verificacao dos argumentos da linha de comando
parser = argparse.ArgumentParser()
parser.add_argument("-images", required = True,
				help = "Caminho para o diretorio com as imagens de consulta.")
parser.add_argument("-q", "--query", required = True,
				help = "Caminho para a imagem de busca.")
parser.add_argument("-n", "--limit", required = True, type = check_negative,
				help = "Numero de imagens similares a serem buscadas.")
parser.add_argument("-m", "--method", required = True,
				help = "Nome do metodo descritor a ser utilizado.")
parser.add_argument("--mask", required = False, default = 7, type = check_mask,
                    help = "Tamanho da mascara (3x3, 5x5 ou 7x7) a ser utilizada no descritor de Fourier. Padrao = 7.")
parser.add_argument("-d", "--distance", required = True,
				help = "Nome do metrica de distancia para comparacao de histogramas.")
args = vars(parser.parse_args())

t1 = time.time()

# verifica o metodo a ser usado e inicializa um objeto para o respectivo metodo
if(args["method"].upper() == "FOURIER"):
	queryDesc = FourierDescriptor(args["mask"])
	indexFilepath = "indexes/" + str(args["mask"]) + "fourierindex.csv"
elif(args["method"].upper() == "GCH"):
	queryDesc = GCHDescriptor((9, 12, 4))
	indexFilepath = "indexes/gchindex.csv"
elif(args["method"].upper() == "LCH"):
	queryDesc = LCHDescriptor((9, 12, 3))
	indexFilepath = "indexes/lchindex.csv"
else:
	sys.exit("\nMetodo descritor invalido!\n")

# carrega a imagem de consulta em memoria e aplica o descritor
query = cv2.imread(args["query"])
queryFeatures = queryDesc.describe(query)

# inicializa um objeto que ira' fazer a comparacao da imagem de consulta com o banco de imagens
searcher = Searcher(indexFilepath)
# realiza a consulta das n-imagens mais semelhantes 
results = searcher.search(queryFeatures, int(args["limit"]), args["distance"])

############################## DESCOMENTAR AQUI PRA MANDAR #####################################################
# percorre o vetor com as imagens mais semelhantes e imprime na saida padrao em ordem decrescente de similaridade
#for (score, imageID) in results:
#	print imageID
################################################################################################################
t2 = time.time()
print "Tempo: %.2f s" % (t2 - t1)
############################## COMENTAR DAQUI PARA BAIXO SE DESCOMENTAR EM CIMA ######################################################

r = 800.0 / query.shape[1]
dim = (800, int(query.shape[0] * r))

resized = cv2.resize(query, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("Query", resized)

# loop over the results
for (score, resultID) in results:

	#load the result image and display it
	result = cv2.imread("images/"+resultID+".jpg")
	
	r = 800.0 / result.shape[1]
	dim = (800, int(result.shape[0] * r))

	resized = cv2.resize(result, dim, interpolation = cv2.INTER_AREA)
	cv2.imshow("Result", resized)
	cv2.waitKey(0)

