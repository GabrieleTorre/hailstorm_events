from glob import glob
import numpy as np
import rasterio
import os


def normalize(band):
    band_min, band_max = (band.min(), band.max())
    return (band - band_min) / (band_max - band_min)


def brighten(band):
    alpha = 0.13
    beta = 0
    return np.clip(alpha*band+beta, 0, 255)


def rgb_from_jp2(path):
    '''
    :param path: where is stored IMG_DATA (from Sentinel)
    '''

    red = rasterio.open(glob(os.path.join(path, 'R20m', "*_" + 'B04' + "_*.jp2"))[0]).read(1)
    green = rasterio.open(glob(os.path.join(path, 'R20m', "*_" + 'B03' + "_*.jp2"))[0]).read(1)
    blue = rasterio.open(glob(os.path.join(path, 'R20m', "*_" + 'B02' + "_*.jp2"))[0]).read(1)

    red_bn = normalize(brighten(red))
    green_bn = normalize(brighten(green))
    blue_bn = normalize(brighten(blue))

    return np.dstack((red_bn, green_bn, blue_bn))

