# -*- coding: utf-8 -*-
'''
运行环境需要在python2.7中进行,
代码实现的功能为批量拼接影像
运行可能需要删除注释
'''

import arcpy
import os
import sys
# print (sys.getdefaultencoding())
# os.chdir(r'E:\Deep Learning\image')
arcpy.CheckExtension('Spatial') #查看GIS权限
base = r'E:\Deep Learning\Deep Learnimg image\20200716_015628_1039_3B_AnalyticMS_SR_harmonized_clip.tif'
out_coor_system = arcpy.Describe(base).spatialReference #获取图像的坐标系统(空间参考)
bandcount = arcpy.Describe(base).bandCount #获取影像波段

file_name_list = 'E:\Deep Learning\Deep Learnimg image' #原始影像的保存路径
input_file_list = os.listdir(file_name_list) #获取影像列表数据集
out_file_path = 'E:\Deep Learning\Deep Learnimg image' #输出拼接影像的保存路径，最好为新的文件夹
out_file_name="mosaic.tif" #拼接完成影像的名称

#arcpy.GetRasterProperties_management()函数获取第一栅格的像素x边边长,
cell_size_x=arcpy.GetRasterProperties_management(base,"CELLSIZEX")
cell_size=cell_size_x.getOutput(0)
#arcpy.GetRasterProperties_management 获取图像的数据类型
value_type=arcpy.GetRasterProperties_management(base,"VALUETYPE")

describe=arcpy.Describe(base)
spatial_reference=describe.spatialReference #获取图像的空间参考
#创建一个tiff数据集
arcpy.CreateRasterDataset_management(out_file_path,out_file_name,cell_size,"16_BIT_SIGNED",
                                    spatial_reference,bandcount)

out_file=out_file_path+'\\'+out_file_name #输出的拼接图像+名称

for file in input_file_list:
    file_path_name=file_name_list+'\\'+file #遍历每一景需要拼接的图像
    print(file_path_name)
    arcpy.Mosaic_management([file_path_name],out_file) #进行每一景图像的拼接

