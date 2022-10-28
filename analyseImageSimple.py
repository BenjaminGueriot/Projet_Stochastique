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
from matplotlib import image, pyplot as plt
from matplotlib import image as mpimg
import numpy as np
 
 
paris1987 = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_1987_10m.tif")[:,:,0]
paris2007 = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_2007_10m.tif")[:,:,0]
paris2011 = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_2011_10m.tif")[:,:,0]
paris2022 = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_2022_10m.tif")[:,:,0]
parisBase = mpimg.imread("D:\Documents\WORK\IDU4\STOCHASTIQUE\Projet_Stochastique\paris_2011_10m_base.tif")


# vert=paris1987
# plt.figure(figsize=(4,4))
# plt.imshow(vert)
# plt.show()



def mu(tab):
    return np.mean(tab)

def sigma(tab):
    return np.std(tab)

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


def entropieRelative(mu1,sigma1,mu2,sigma2):
    return ((1/2)*(mu1-mu2)**2*((1/sigma1**2)+(1/sigma2**2)))+((1/2)*(sigma1**2/sigma2**2)+(sigma2**2/sigma1**2))

def entropieRelativeImage(image1,image2):
    resfinal=[]
    for line in range(len(image1)):
        newline=[]
        for column in range(len(image1[0])):
            mu1=image1[line][column][0]
            sigma1=image1[line][column][1]+1
            mu2=image2[line][column][0]
            sigma2=image2[line][column][1]+1
            ER=entropieRelative(mu1,sigma1,mu2,sigma2)
            if ER<10000:
                newline.append(0)
            else:
                newline.append(ER)
        resfinal.append(newline)
    return resfinal

#print(entropieRelativeImage(imageAnalyse(paris1987),imageAnalyse(paris2022)))

def displayParis(imageEvol,imageParis):
    imageParisEvol=[]
    for line in range(len(imageParis)):
        newline=[]
        for column in range(len(imageParis[0])):
            if imageEvol[int(line/3)][int(column/3)]==0:
                newline.append([imageParis[line][column],imageParis[line][column],imageParis[line][column]])
            else:
                newline.append([0,256,0])
        imageParisEvol.append(newline)
    #print(imageParisEvol)
    plt.figure()
    # plt.imshow(entropieRelativeImage(imageAnalyse(paris2022),imageAnalyse(paris1987)))
    plt.imshow(imageParisEvol)
    plt.show()

displayParis(entropieRelativeImage(imageAnalyse(paris2022),imageAnalyse(paris1987)),parisBase)
