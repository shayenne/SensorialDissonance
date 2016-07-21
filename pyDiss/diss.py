from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import sys



# Função copiada de adessowiki: translada imagem
def iaptrans(f,t):
  import numpy as np
  g = np.empty_like(f) 
  if f.ndim == 1:
    W = f.shape[0]
    col = arange(W)
    g[:] = f[(col-t)%W]
  elif f.ndim == 2:
    H,W = f.shape
    rr,cc = t
    row,col = np.indices(f.shape)
    g[:] = f[(row-rr)%H, (col-cc)%W]
  elif f.ndim == 3:
    Z,H,W = f.shape
    zz,rr,cc = t
    z,row,col = np.indices(f.shape)
    g[:] = f[(z-zz)%Z, (row-rr)%H, (col-cc)%W]
  return g



# Função for com passo flexivel
def frange(x, y, jump):
  while x < y:
    yield x
    x = round(x*jump, 3)

    

# Função que encontra todos os mínimos
def all_surface_minimum(f):
  h = []
  vizinhos = [(1, 0), (1, -1), (0, 1), (0,-1), (-1, 1), (-1, 0), (-1, -1)]

  f2 = iaptrans(f, (1, 1))
  g = (f <= f2).astype(int)

  # Para cada vizinho, verifica se o elemento eh maior
  # Soh os minimos locais ficam com 1
  for (dh,dw) in vizinhos:
    f2 = iaptrans(f, (dh, dw))
    h.append((f <= f2).astype(int))
    p = (g & h[-1]).astype(int)
    g = p.copy()

  # Retorna apenas os minimos locais
  return np.multiply(f,g)[1:-1,1:-1]



# Função que recebe duas listas de frequencia e as amplitudes correspondentes
# e calcula a dissonancia para o par
def dissPair(freq1, freq2, ampl):
  
  # Constantes definidas em Sethares  
  dstar= (float) (0.24);
  s1 = (float) (0.0207) ;
  s2 = (float) (18.96);  
  c1 = 5.0;      
  c2 = -5.0;
  a1 = (float) (-3.51); 
  a2 = (float) (-5.75);  

  d = 0;
  numpartials = len(freq1);
  # Cálculo da dissonancia entre os dois sons
  for i in range(numpartials):
    for j in range(numpartials):
      if (freq2[j]<freq1[i]):
        fmin = freq2[j] ;
      else: 
        fmin = freq1[i] ;
      
      s=dstar*1.0/(s1*fmin+s2); 
      
      fdif=(float) (np.abs(freq2[j]-freq1[i])) ;
	
      arg1=1.0*a1*s*fdif; arg2=1.0*a2*s*fdif ;
      
      exp1=(float) (np.exp(arg1)); 
      
      exp2=(float) (np.exp(arg2));
      
      if (ampl[i]<ampl[j]):
        dnew=ampl[i]*(c1*exp1+c2*exp2);
      else:
        dnew=ampl[j]*(c1*exp1+c2*exp2); 
	  
      d = d+dnew;    

  # Dissonancia calculada
  return d



# Função que calcula dissonância 3D
def dissSurface(numpartials, frequ=[], ampl=[]):
  lowint = 1 ;
  highint = 2.47;
  cent = np.power(2, 1/100);
  inc = np.power(2, 1/100);
  
  size = (float)((highint-lowint)/inc);
  
  diss = [0]*131; 
  allpartialsatinterval = frequ.copy();

  # Dissonancia vertical e horizontal
  # Calcula as bordas # Calculate de margins
  ind = 0;
  for interval in frange(lowint, highint, inc):
    # Each step increments one cent
    allpartialsatinterval = np.dot(frequ, interval);
    #fill diss array with dissonances
    diss[ind] = dissPair(allpartialsatinterval, frequ, ampl);
    ind+=1;

  margin = diss;
  horz, vert = np.meshgrid(margin, np.transpose(margin));


  # Calcula os mínimos locais desta curva de dissonancia, inter menores que 2
  mins = []
  vals = []
  for i in range(1, 100):
    if diss[i-1] >= diss[i] and diss[i] <= diss[i+1]: 
      mins.append(i)
      vals.append(diss[i])

  # Ordena os mínimos do menor para o maior
  mins = [x for (y,x) in sorted(zip(vals,mins))]
  
  
  # Dissonancia diagonal
  # Calcula as iterações # Calculate de diagonals
  diag = []
  for inter in frange(lowint, highint, inc):
    fr = np.dot(frequ, inter)
    ind = 0
    for interval in frange(lowint, highint, inc):
      allpartialsatinterval = np.dot(frequ, interval);
      #fill diss array with dissonances
      diss[ind] = dissPair(allpartialsatinterval, fr, ampl);
      ind+=1;

    # Cópia do array: passagem de valor
    diag.append(diss.copy())

  # Matriz de dissonancia 3D
  surf = diag + horz + vert
  return surf, mins


#------------------------ MAIN --------------------------#
if __name__ == "__main__":

  # Variáveis de controle
  sendFile = True
  plotGraphs = False
  printMatrix = False
  fivemins = False
  
  # Opções da linha de comando
  if (len(sys.argv) > 1):
    if ('-m' in sys.argv):
      pointMins = True
    
    if ('-l' in sys.argv):
      sendFile = False

    if ('-g' in sys.argv):
      plotGraphs = True
      
    if ('-d' in sys.argv):
      printMatrix = True
      
    if ('-h' in sys.argv):
      print("Opções:")
      print(" -d - imprime a matriz de dissonância")
      print(" -l - lista os pares de acordes")
      print(" -g - plota os gráficos")
      print(" -m - guarda minimos da curva 2D em um arquivo")
      print(" sem parametros envia os pares para os arquivos rNotes e sNotes")
      sys.exit()
  # Fim das opções


  # Definição das listas a serem usadas
  ampl = []
  frequ = []
  numpartials = int(input())


  # Leitura dos dados de entrada (MODIFICAR)
  # Neste formato: frequencia e amplitude até o numero de parciais indicado
  for i in range(numpartials):
    frequ.append(float(input()))
    ampl.append(float(input()))

        
  # Cálculo da matriz de dissonancia
  diss3D, mins = dissSurface(numpartials, frequ, ampl)

    
  # Impressao da matriz: linha de comando
  if printMatrix:
    print(" ".join(map(str,diss3D)))

      
  # Cálculo dos mínimos de dissonância
  X = np.arange(0, 131)
  Y = np.arange(0, 131)
  X, Y = np.meshgrid(X, Y)
  minimum = all_surface_minimum(diss3D)
  # Encontra os indices dos minimos
  r, c = np.where (minimum > 0)
  
    
  # Impressao dos graficos: linha de comando
  if (plotGraphs):
    # Plota o grafico como surface
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_wireframe(X, Y, diss3D, rstride=1, cstride=1)
    ax.set_zlim(-1.01, 10.01)
    plt.show()
    
    # Plota o grafico como imagem 2D
    im = plt.imshow(diss3D, cmap='hot')
    plt.colorbar(im, orientation='horizontal')
    plt.show()
    
    # Plota somente os minimos locais
    plt.imshow(minimum, cmap='hot')
    plt.show()

    ax = plt.gca()
    ax.cla() # clear things for fresh plot
    # change default range so that new circles will work
    ax.set_xlim((0,131))
    ax.set_ylim((0,131))
  # Fim da impressao dos graficos

  
  # Escolhe as tríades que se afastam das margens e diagonal em pelo menos
  # 1 semitom
  stom = np.power(2, 2/12)
  # Vetor que manterá pares de acordes em ordem de dissonancia
  order = [] 
  for i in range(len(r)):    
    n1 = 1+r[i]/100
    n2 = 1+c[i]/100
    
    # A distância musical entre todas as notas devem ser maior que 1 semitom
    if n1 > stom and n2/n1 > stom and 2/n2 > stom:
      order.append([r[i], c[i], diss3D[r[i]][c[i]]])

      if plotGraphs:
        circle = plt.Circle((r[i], c[i]), .5, color='b', fill=False)  
        # key data point that we are encircling
        ax.plot((r[i]),(c[i]),'o',color='y')
        fig.gca().add_artist(circle)
      
  if plotGraphs:
    plt.show()
    

  # Ordena os pares de acordo com a dissonancia    
  order.sort(key=lambda tup: tup[2])

  # Guarda os minimos em um arquivo: linha de comando
  if pointMins:
    f = open("minimos.txt", "w")
    for i in range(len(mins)):
      f.write("%f %d ;" % (np.power(2, mins[i]/100.0), i))
    f.close()
    
  # Envia resultados para o arquivo de texto: linha de comando
  if sendFile:
    fr = open("rNotes.txt", "w")
    fs = open("sNotes.txt", "w")
    for i in range(len(order)):
      fr.write("%f %d ;" % (np.power(2, order[i][0]/100.0), i))
      fs.write("%f %d ;" % (np.power(2, order[i][1]/100.0), i))
    fr.close()
    fs.close()
  else:
    # Imprime resultados na tela
    r1200log2 = 39.86314 # Conversao de intervalo para semitons
    for i in range(len(order)):
      print ('Par', i, ':', (np.power(2, order[i][0]/100.0)),
             (np.power(2, order[i][1]/100.0)), 'Dissonancia:', order[i][2])
      print ('Semitons:',
             39.86314*(np.log(np.power(2, order[i][0]/100.0))/np.log(10)),
             39.86314*(np.log(np.power(2, order[i][1]/100.0)))/np.log(10))
      


        
