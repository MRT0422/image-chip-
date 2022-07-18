# -*- coding: utf-8 -*-
#python2.7
import arcpy
import os

arcpy.CheckOutExtension("spatial")
arcpy.env.workspace = r'E:\Deep Learning\Deep Learnimg data'
shp = r'E:\Deep Learning\Deep Learnimg data\shape\mosaic.shp'  #shp文件
shp_outpath = r'E:\Deep Learning\Deep Learnimg data\shape label'    #导出的shp要素输出路径

img_list = 'E:\Deep Learning\Deep Learnimg data\image\mosaic.tif' #原始影像的保存轮径
img_out = "E:\Deep Learning\Deep Learnimg data\image label" #裁剪结果输出路径

# 导出shp中的每个要素
with arcpy.da.SearchCursor(shp, ["SHAPE@",'class']) as cursor:
    # SHAPE@指代单个要素，class是一个字段，query是条件
    for row in cursor:
        out_name = row[1] + '.shp'  # 输出文件名
        arcpy.FeatureClassToFeatureClass_conversion(row[0], shp_outpath, out_name)
print('shp 拆分完成')

clip_shp = []
file_path = "E:\Deep Learning\Deep Learnimg data\shape label"
shplist = os.listdir(file_path)
for i in shplist:
    if os.path.splitext(i)[1] == '.shp':
        print i
        clip_shp.append(i)

for i in range (len(clip_shp)):
    mask=os.path.join(shp_outpath+ '/'+ str(i)+ '.shp')
    outname = outname = os.path.join(img_out +'/' + str(i+1)+"_clp.tif")  # 指定输出文件的命名方式（以被裁剪文件名+_clip.tif命名）
    out_extract = arcpy.sa.ExtractByMask(img_list, mask)  # 执行按掩模提取操作
    out_extract.save(outname)  # 保存数据







