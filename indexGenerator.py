#-*- coding:utf-8 -*-

import cv2
import argparse
import glob
import time
import sys
from descriptors.fourierdescriptor import FourierDescriptor
from descriptors.gchdescriptor import GCHDescriptor
from descriptors.lchdescriptor import LCHDescriptor

# realiza a checagem do tamanho da mascara de Fourier
def check_mask(value):
    ivalue = int(value)
    if ivalue != 3 and ivalue != 5 and ivalue != 7:
        raise argparse.ArgumentTypeError("Tamanho da mascara deve ser 3, 5 ou 7.")        
    return ivalue

# verificacao dos argumentos da linha de comando
parser = argparse.ArgumentParser()
parser.add_argument("--images", required = True,
                    help = "Caminho para o diretorio com as imagens de consulta.")
parser.add_argument("--method", required = True,
                    help = "Nome do metodo descritor a ser utilizado.")
parser.add_argument("--mask", required = False, default = 7, type = check_mask,
                    help = "Tamanho da mascara (3x3, 5x5 ou 7x7) a ser utilizada no descritor de Fourier. Padrao = 7.")
args = vars(parser.parse_args())

t1 = time.time()

# verifica o metodo a ser usado e inicializa um objeto para o respectivo metodo
if(args["method"].upper() == "FOURIER"):
    print "Gerando o indice do banco de imagens em \"%s\" para o metodo FOURIER com mascara %dx%d ..." % (args["images"], args["mask"], args["mask"])
    descriptor = FourierDescriptor(args["mask"])
    indexFilepath = "indexes/" + str(args["mask"]) + "fourierindex.csv"
elif(args["method"].upper() == "GCH"):
    print "Gerando o indice do banco de imagens em \"%s\" para o metodo GCH ..." % (args["images"])
    descriptor = GCHDescriptor((9, 12, 4))
    indexFilepath = "indexes/gchindex.csv"
elif(args["method"].upper() == "LCH"):
    print "Gerando o indice do banco de imagens em \"%s\" para o metodo LCH ..." % (args["images"])
    descriptor = LCHDescriptor((9, 12, 3))
    indexFilepath = "indexes/lchindex.csv"
else:
    sys.exit("Metodo descritor invalido!")

# abre o indice para escrita
indexFile = open(indexFilepath, "w")

# atraves da funcao glob do modulo glob busca os nomes da imagens
for imagePath in glob.glob(args["images"] + "/*.jpg"):
    # extrai o numero da imagem
    ini = imagePath.rfind("/") + 1
    end = imagePath.rfind(".")
    imageID = imagePath[ini:end]
    # carrega a imagem em memoria
    image = cv2.imread(imagePath)

    # caso a imagem nao esteja vazia
    if image is not None:
        # aplica o descritor na imagem
        features = descriptor.describe(image)

        # escreve o vetor de caracterisicas no arquivo de indice (cada linha e' uma imagem)
        features = [str(f) for f in features]
        indexFile.write("%s, %s\n" % (imageID, ",".join(features)))

indexFile.close()

print "Indice gerado com sucesso!"

t2 = time.time()
print "Tempo: %.2f s" % (t2 - t1)