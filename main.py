import matplotlib.pyplot as plt
import math
import numpy as np
points_counter= 0 
all_data_leter=""

#obliczenie momentow algorytmem macierzowym z cwiczen
#funkcja zwraca tez tablice wartosci h, poniewaz bedzie ona potrzebna do obliczenie wartosci w zadanym punkcie
def calculate_moments(x,y,n):
    h=[1 for i in range(n)]
    b=[1 for i in range(n)]
    for i in range(n):
        h[i]=x[i+1]-x[i]
        b[i]=6*(y[i+1]-y[i])/h[i]

    u=[1 for i in range(n)]
    v=[1 for i in range(n)]
    u[1]=2*(h[0]+h[1])
    v[1]=b[1]-b[0]

    for i in range(2,n,1):
        u[i]=2*(h[i-1]+h[i]) - h[i-1]*h[i-1]/u[i-1]
        v[i]=b[i]-b[i-1]-h[i-1]*v[i-1]/u[i-1]
    M=[1 for i in range(n+1)]
    M[n]=0
    for i in range(n-1,0,-1):  # n-1, n-2....1
        M[i]=(v[i]-h[i]*M[i+1])/u[i]

    M[0]=0
    return (M,h)


#wyszukiwanie do ktorego z przedzialow nalezy "arg"
def getIndex(arg,t):
    i=0
    if(arg<=t[0]):
        return 0
    if(arg>=t[len(t)-2]):
        return len(t)-2
    for el in t:
        if(arg<el):
            return i-1
        i=i+1

#obliczenie wartosci w punkcie korzystajac z wzorku z wykladu //Tego za uzycie ktorego na egzaminie jest -15pkt n_n 
def getval(arg,t,M,h,y):
    i=getIndex(arg,t)
    return M[i]/(6*h[i]) *pow((t[i+1]-arg),3) + M[i+1]/(6*h[i]) *pow((arg-t[i]),3) + (y[i+1]/h[i] - M[i+1]*h[i]/6)*(arg-t[i]) + (y[i]/h[i] - M[i]*h[i]/6)*(t[i+1]-arg)

#Korzystalem z geogebry do doboru punktow. Punkty na wyjsciu sa tam w postaci: P=(x,y). Funkcja ponizej przerabia zbior takich punktow na 2 tablice z wspolrzednymi x i y 
#Przyklad:
#input: "A(1,4) B(2,8) C(3,12)"
#output: [1,2,3],[4,8,12]
def geogebra_output_to_arrays(punkty_string): 
    xs = []
    ys = []
    for l in punkty_string.split('\n'):
        if l:
            x, y = l.split('=')[1].strip('()').split(',')
            xs.append(float(x))
            ys.append(float(y))
    return xs, ys

#funkcja ktora na podstawie danych z pliku "filename" tworzy punkty do narysowania litery  
#precision to odpowiednik M z L8.7
def create_points(filename,precision=150):
    data=open(filename)
    (values1,values2)=geogebra_output_to_arrays(data.read())
    #print(values1)
    #print(values2)

    n=len(values1)-1
    global points_counter
    global all_data_leter
    points_counter=points_counter+len(values1)
    t=[i/n for i in range(n+1)]
    (moments_X,h_X)=calculate_moments(t,values1,n)
    (moments_Y,h_Y)=calculate_moments(t,values2,n)

    OX=[getval(i/precision,t,moments_X,h_X,values1) for i in range (precision)]
    OY=[getval(i/precision,t,moments_Y,h_Y,values2) for i in range (precision)]

    #stworzenie stringa z informacjami odnosnie tego na podstawie jakich danych powstala dana litera
    all_data_leter="Liczba punktow: n = " + str(len(values1))+"\n"+"Wartosci [t0,..tn]: "+ str(t) +"\n"
    all_data_leter=all_data_leter+"Wartosci [x0,x1, ..., xn] = "+ str(values1) + "\n"
    all_data_leter=all_data_leter+"Wartosci [y0,y1, ..., yn] = "+ str(values2) + "\n"
    all_data_leter=all_data_leter+"Wartosci [u0,u1, ..., un] = "+ str([i/precision for i in range(precision)])

    return (OX,OY)
    

#Otwieranie kolejnych plikow z danymi i na ich podstawie rysowanie liter na wykresie

#Generowanie punktow u 
precision=40
(OX_P,OY_P)= create_points("Letters\\P.txt",precision)
#with open('Letters_info\\P.txt', 'a') as f:
#    f.write(all_data_leter)
#f.close()
(OX_a,OY_a)= create_points("Letters\\a.txt",precision)
(OX_w,OY_w)= create_points("Letters\\w.txt",precision)
(OX_el,OY_el)= create_points("Letters\\el.txt",100)
(OX_W,OY_W)= create_points("Letters\\W_surname.txt",50)
(OX_o,OY_o)= create_points("Letters\\o_surname.txt",60)
(OX_zz,OY_zz)= create_points("Letters\\z_surname.txt",precision)
(OX_k,OY_k)= create_points("Letters\\line_surname.txt",precision)
(OX_ny,OY_ny)= create_points("Letters\\ny_surname.txt",60)


#Dodatnie liter do wykresu
fig,ax=plt.subplots(nrows=1)
ax.plot(OX_P,OY_P,color='blue',linewidth='1.8')
ax.plot(OX_a,OY_a,color='blue',linewidth='1.8')
ax.plot(OX_w,OY_w,color='blue',linewidth='1.5')
ax.plot(OX_el,OY_el,color='blue',linewidth='1.5')

ax.plot(OX_W,OY_W,color='blue',linewidth='1.5')
ax.plot(OX_o,OY_o,color='blue',linewidth='1.5')
ax.plot(OX_zz,OY_zz,color='blue',linewidth='1.5')
ax.plot(OX_k,OY_k,color='blue',linewidth='1.5')
ax.plot(OX_ny,OY_ny,color='blue',linewidth='1.5')

print("Łączna liczba użytych punktów: ${points_counter}",points_counter)
plt.show()



