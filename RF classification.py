from sklearn import datasets
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from osgeo import gdal
from osgeo import osr
from osgeo import ogr


def createClassifier(inraster, inshp, field: str = "Id", treenum: int = 100):
    rasterspatial = gdal.Open(inraster)
    spatial2 = osr.SpatialReference()
    spatial2.ImportFromWkt(rasterspatial.GetProjectionRef())  #获得空间参考信息
    shpspatial = ogr.Open(inshp)
    layer = shpspatial.GetLayer(0)
    spatial1 = layer.GetSpatialRef()

    ct = osr.CreateCoordinateTransformation(spatial1, spatial2)
    oFeature = layer.GetNextFeature()
    # 下面开始遍历图层中的要素
    geom = oFeature.GetGeometryRef()
    if geom.GetGeometryType() == ogr.wkbPoint:
        return createClassifierByPoint(inraster, inshp)
    k = geom.GetGeometryType()
    if geom.GetGeometryType() != ogr.wkbPolygon:
        print("样本必须为单部件多边形")
        return False
    trainX = list()
    trainY = list()
    print("读取样本")
    while oFeature is not None:
        geom = oFeature.GetGeometryRef()
        wkt = geom.ExportToWkt()
        points = WKTToPoints(wkt)
        polygonPoints = []
        value = oFeature.GetField(field)
        for point in points:
            pC = ct.TransformPoint(point.X, point.Y, 0)
            polygonPoints.append(Point(pC[0], pC[1]))

        arr, width, height, BandsCount, leftX, upY = GetSubRaster(inraster, polygonPoints)
        for i in range(height):
            for k in range(width):
                nodata = True
                tem = list()
                for bc in range(BandsCount):
                    v = int(arr[bc][i][k])
                    tem.append(v)
                    if v > 0: nodata = False
                if nodata:
                    continue
                trainX.append(tem)
                trainY.append(int(value))
        oFeature = layer.GetNextFeature()

    ct = None
    spatial1 = None
    spatial2 = None
    print("训练样本")
    clf = RandomForestClassifier(n_estimators=treenum)
    clf.fit(trainX, trainY)  # 训练样本
    print("训练完成")
    return clf

