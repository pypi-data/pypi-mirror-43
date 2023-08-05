"""
Programmer: Blake Brown
Version 0.0.7
# FractalTools
a small bundle of tools to quickly generate julia and mandelbrot sets

MIT License

Copyright (c) 2019 Custards1

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import numpy
import matplotlib.pyplot as plt


name = "FractalTools"


##The following functions create a graph of a set, the julia set is highly tweakable by inputting diffrent c1,c2,and n values in the parameter
##use the plot functions and zoom functions to see a set

class Mandelbrot:
    def Mandelbrot(real,im):
        c = complex(real,im)
        z= 0.0j
        i=0
        while z.real*z.real+z.imag*z.imag < 4 and i < 100:
            z=z*z+c
            i=i+1
        if i == 100:
            return 100
        else:
            return i
    def Plot(rows,colums,colormap):
        result=numpy.zeros([rows,colums])
        for r_i,real in enumerate(numpy.linspace(-2,1,num = rows,)):
                for c_i,imag in enumerate(numpy.linspace(-1,1,num = colums)):
                        result[r_i,c_i] = Mandelbrot.Mandelbrot(real,imag)
        plt.figure(figsize = [15,15])
        plt.imshow(result.T,cmap=colormap,interpolation='sinc',extent=[-1.65,1.15,-1.2,1.0])
        print("sucsess")
        plt.show()
    def ZoomPlot(rows,colums,xn,x,yn,y,colormap):
        assert xn>=-2 and x<=1, 'Your x bounds are out of range'
        assert yn >= -1 and y <= 1, 'Your y bounds are out of range'
        result=numpy.zeros([rows,colums])
        for r_i,real in enumerate(numpy.linspace(xn,x,num = rows,)):
                for c_i,imag in enumerate(numpy.linspace(yn,y,num = colums)):
                        result[r_i,c_i] = Mandelbrot.Mandelbrot(real,imag)
        plt.figure(figsize = [15,15])
        plt.imshow(result.T,cmap=colormap,interpolation='sinc',extent=[xn,x,yn,y])
        print("sucsess")
        plt.show()
        
    
class Julia:
    def Julia(real,im,c1,c2,n):
        z = complex(real,im)
        c = complex(c1,c2)
        zr = z.real
        zi = z.imag
        i=0
        while zr*zr + zi*zi < 4 and i < 100:
                xtemp = (zr*zr+zi*zi)**(n/2) * numpy.cos(n*numpy.arctan2(zi,zr)) + c.real
                zi = (zr*zr+zi*zi)**(n/2)*numpy.sin(n*numpy.arctan2(zi,zr)) + c.imag
                zr = xtemp
                i=i+1
        if i == 100:
                return 100
                   
        else:
                return i
    def Plot(rows,colums,c1,c2,n,colormap):
        assert -1<= c1 <=1,"c1 needs to be between -1 and 1"
        assert -1<= c2 <=1, "c2 needs to be between -1 and 1"
        result=numpy.zeros([rows,colums])
        for r_i,real in enumerate(numpy.linspace(-1,1,num = rows,)):
                for c_i,imag in enumerate(numpy.linspace(-1,1,num = colums)):
                        result[r_i,c_i] = Julia.Julia(real,imag,c1,c2,n)

        plt.figure(figsize = [15,15])
        plt.imshow(result.T,cmap=colormap,interpolation='sinc',extent=[-1.65,1.15,-1.2,1.])
        print("sucsess")
        plt.show()
    
    def ZoomPlot(rows,colums,ext_xn,ext_x,ext_yn,ext_y,c1,c2,n,colormap):
        result=numpy.zeros([rows,colums])
        for r_i,real in enumerate(numpy.linspace(ext_xn,ext_x,num = rows,)):
                for c_i,imag in enumerate(numpy.linspace(ext_yn,ext_y,num = colums)):
                        result[r_i,c_i] = Julia.Julia(real,imag,c1,c2,n)
        plt.figure(figsize = [15,15])
        plt.imshow(result.T,cmap=colormap,interpolation='sinc',extent=[ext_xn,ext_x,ext_yn,ext_y])
        print("sucsess")
        plt.show()


   
