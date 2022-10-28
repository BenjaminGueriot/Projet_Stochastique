# from osgeo import gdal
# import numpy
# import matplotlib.pyplot as plt

# ds = gdal.Open(r'D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_1987_10m.tif')
# # gt = ds.GetGeoTransform()
# # proj = ds.GetProjection()

# band = ds.GetRasterBand(3)
# array=band.ReadAsArray()
# print(ds.RasterCount)
# plt.figure()
# plt.imshow(array)
# plt.show()

import imageio
from hashlib import new
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import numpy as np
 
 
paris1987 = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_1987_10m.tif")
paris2007 = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_2007_10m.tif")
paris2011 = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_2011_10m.tif")
paris2022 = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_2022_10m.tif")
parisBase = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_2011_10m_base.tif")


vert=paris1987[:,:,1]
plt.figure(figsize=(4,4))
plt.imshow(vert)
plt.show()
print(vert)


def mu(tab):
    res=[0,0,0]
    for i in tab:
        for color in range(3):
            res[color]+=i[color]
    
    for color in range(len(res)):
        res[color]=res[color]/len(tab)
    return res

def sigma(tab):
    res=[0,0,0]
    r=[]
    g=[]
    b=[]
    for pix in tab:
        r.append(pix[0])
        g.append(pix[1])
        b.append(pix[2])
    res[0]=np.std(r)
    res[1]=np.std(g)
    res[2]=np.std(b)
    return res

def imageAnalyse(image):
    finaltab=[]
    for line in range(0,len(image),3):
        newline=[]
        for column in range(0,len(image[0]),3):
            tab=[]
            for i in range(3):
                for j in range(3):
                    if line+i<len(image) and column+j<len(image[0]):
                        tab.append(image[line+i][column+j])
            data=(mu(tab),sigma(tab))
            newline.append(data)
        finaltab.append(newline) 

    return finaltab
    #print("y=" + str(len(finaltab)) + " x=" + str(len(finaltab[0])))


def entropieRelative(mu1,sigma1,mu2,sigma2):
    return ((1/2)*(mu1-mu2)**2*((1/sigma1**2)+(1/sigma2**2)))+((1/2)*(sigma1**2/sigma2**2)+(sigma2**2/sigma1**2))

def entropieRelativeImage(image1,image2):
    resfinal=[]
    for color in range(3):
        res=[]
        for line in range(len(image1)):
            newline=[]
            for column in range(len(image1[0])):
                mu1=image1[line][column][0][color]
                sigma1=image1[line][column][1][color]+1
                mu2=image2[line][column][0][color]
                sigma2=image2[line][column][1][color]+1
                newline.append(entropieRelative(mu1,sigma1,mu2,sigma2))
            res.append(newline)
        resfinal.append(res)
    return resfinal

#print(entropieRelativeImage(imageAnalyse(paris1987),imageAnalyse(paris2022)))
# for i in range(3):
#     plt.figure()
#     plt.imshow(entropieRelativeImage(imageAnalyse(paris1987),imageAnalyse(paris2022))[i])
#     plt.show()