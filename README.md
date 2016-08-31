# CBIR

**Alunos**                      **NUSP**
- Giovani Ortolani Barbosa    8936648
- Henrique Anacretto Pereira  8485799

**LEIA-ME**

O programa foi compilado utilizando python 2.7.6 em ambiente Ubuntu 14.04 com a biblioteca OpenCV 2.4.8.

1.  Geração do índice (arquivo principal 'indexGenerator.py')
    1.  Criar um diretório para conter os códigos-fonte do projeto, esse diretório deve conter os arquivos 'corel10k.py', 'indexGenerator.py' e 'searcher.py'.
    2.  Colocar o diretório 'descriptors' dentro do novo diretório.
    3.  Criar um diretório chamado 'indexes' dentro do novo diretório.
    4.  Utilizar o seguinte comando para gerar o índice:
        'python indexGenerator.py --images <diretório com as imagens> --method <fourier, gch ou lch> [--mask <3, 5 ou 7>]'
        Obs.: o parâmetro '--mask' é opcional e utilizado apenas para o método fourier, seu valor default é 7.
    O índice para o método escolhido será gerado dentro do diretório 'indexes' e ele terá extensão '.csv'.

2) Execução da busca (arquivo principal 'corel10k.py'
    a)  Utilizar o seguinte comando para realizar a busca:
        'python corel10k.py --images <diretório com as imagens> -q <caminho para a query> -n <numero de imagens similares> -m <fourier, gch ou lch> [--mask <3, 5 ou 7>] -d <chi2, manhattan ou euclidean>''
        Obs.: o parâmetro '--mask' é opcional e utilizado apenas para o método fourier, seu valor default é 7.
    b)  O número das imagens mais similares, em ordem descrescente de similaridade, à imagem de entrada (query) de acordo com o limite 
    passado pelo usuário serão exibidas na saída-padrão em modo de texto.
            
*Em caso de dúvida, utilizar o comando:
'python <corel10k.py ou indexGenerator.py> -h'