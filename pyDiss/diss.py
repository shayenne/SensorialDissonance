from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from pylab import *


# Função copiada de adessowiki, iaptrans
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

# for com passo flexivel
def frange(x, y, jump):
  while x < y:
    yield x
    x = round(x+jump, 3)

# encontra todos os mínimos
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

    
# Função que calcula dissonância 3D
def dissmeasure(numpartials, frequ=[], ampl=[]):

  surf = []
  dstar= (float) (0.24);
  
  s1 = (float) (0.0207) ;
  s2 = (float) (18.96);  
  
  c1 = 5.0;      
  c2 = -5.0;
  a1 = (float) (-3.51); 
  a2 = (float) (-5.75); 
  
  ind = 0;
  
  lowint = 1 ;
  highint = 2.31 ; 
  inc = 0.01;
  
  size=(float)((highint-lowint)/inc);
  
  diss = [0]*131; 
  intervals = [0]*400;
  allpartialsatinterval = frequ.copy();#[0]*1024;
  
  # Calcula as bordas
  for interval in frange(lowint, highint, inc):
    d=0;

    for k in range(numpartials):
      allpartialsatinterval[k] = round(interval*(frequ[k]), 5);
  
    for i in range(numpartials):
      for j in range(numpartials):
        if (allpartialsatinterval[j]<frequ[i]):
          fmin = allpartialsatinterval[j] ;
        else: 
          fmin = frequ[i] ;
	  
        s=dstar*1.0/(s1*fmin+s2); 
	
        fdif=(float) (np.abs(allpartialsatinterval[j]-frequ[i])) ;
	
        arg1=1.0*a1*s*fdif; arg2=1.0*a2*s*fdif ;
	
        exp1=(float) (np.exp(arg1)); 
	
        exp2=(float) (np.exp(arg2));
	
        if (ampl[i]<ampl[j]):
          dnew=ampl[i]*(c1*exp1+c2*exp2);
        else:
          dnew=ampl[j]*(c1*exp1+c2*exp2); 
	  
        d = d+dnew;  
          
          
        #print(ind)
      
    diss[ind] = d;#//fill  diss array with dissonances
    intervals[ind] = interval;# // fill  intervals array with intervals 
    ind+=1;

  borda = diss
  X, Y = np.meshgrid(borda, np.transpose(borda))

  # Calcula as iterações

  for inter in frange(lowint, highint, inc):
    #print(inter)
    fr = np.dot(frequ, inter)
    #print (fr)
    ind = 0
    l = 0
    for interval in frange(lowint, highint, inc):
      d=0;
      for k in range(numpartials):
        allpartialsatinterval[k] = interval*(frequ[k]);

      #print ("Calculando a diss entre ", fr, allpartialsatinterval)
      #a = input()
      for i in range(numpartials):
        
        for j in range(numpartials):

          if (allpartialsatinterval[j]<fr[i]):
            fmin = allpartialsatinterval[j] ;

          else: 
            fmin = fr[i] ;
                
          s=dstar*1.0/(s1*fmin+s2); 
	  
          fdif=(float) (np.abs(allpartialsatinterval[j]-fr[i])) ;
	  
          arg1=1.0*a1*s*fdif; arg2=1.0*a2*s*fdif ;
	  
          exp1=(float) (np.exp(arg1)); 
	
          exp2=(float) (np.exp(arg2));
	  
          if (ampl[i]<ampl[j]):
            dnew=ampl[i]*(c1*exp1+c2*exp2);

          else:
            dnew=ampl[j]*(c1*exp1+c2*exp2); 
	  
          d = d+dnew;  
          
          
          #print(ind)

      diss[ind] = d;#//fill  diss array with dissonances
      intervals[ind] = interval;# // fill  intervals array with intervals 
      ###printf("%f %f\n", intervals[ind], diss[ind]);	
      ind+=1;

    
    #plt.plot(diss)
    #plt.show()
    surf.append(diss.copy())
    
    #print (surf[int(inter*100 - 100)])
  surf = surf + X + Y

  
  return surf

## MAIN ##

if __name__ == "__main__":
    
    ampl = []#[0]*1024;
    frequ = []#[0]*1024;

    numpartials = int(input())
	
    for i in range(numpartials):
        frequ.append(float(input()))#frequ[i] = float(input())
        ampl.append(float(input()))#ampl[i] = float(input())

    diss3D = dissmeasure(numpartials, frequ, ampl)

    X = np.arange(0, 131)
    Y = np.arange(0, 131)
    X, Y = np.meshgrid(X, Y)

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
    minimum = all_surface_minimum(diss3D)
    plt.imshow(minimum, cmap='hot')
    plt.show()

    # Encontra os indices dos minimos
    r, c = np.where (minimum > 0)
    
    plt.imshow(minimum, cmap='hot')

    ax = plt.gca()
    ax.cla() # clear things for fresh plot
    # change default range so that new circles will work
    ax.set_xlim((0,131))
    ax.set_ylim((0,131))

    order = []  # Vetor que mantera os pares de acordes em ordem de dissonancia
    for i in range(len(r)):

      if r[i] != c[i] and r[i] < 90 and c[i] < r[i]+15:
        order.append([r[i], c[i], diss3D[r[i]][c[i]]])
        circle = plt.Circle((r[i], c[i]), .5, color='b', fill=False)
        
        # key data point that we are encircling
        ax.plot((r[i]),(c[i]),'o',color='y')
        
        fig.gca().add_artist(circle)
    
    plt.show()

    order.sort(key=lambda tup: tup[2])
    ind = 0
    for chord in order:
      print ('Par',ind, ':', chord[0], chord[1], 'Dissonancia:', chord[2])
      print ('Semitons:', round(np.log(1+(chord[0]/100))/np.log(np.power(2, 1/12)), 3), round(np.log(1+(chord[1]/100))/np.log(np.power(2, 1/12)), 3))
      ind += 1
    #r, c = np.where( minimum < 1 )
    #plt.imshow(minimum[r, c])
    #plt.show()
    #print (minimum)
