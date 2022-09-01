from rasterio.plot import show
from tiff_utils import *
from glob import glob
import pandas as pd
import numpy as np
import rasterio
import argparse
import os
import gc


def tiff_creation(date, src_data_dir, my_points):
    tiff_file = os.path.join(tiff_root_data_dir, date + ".tiff")
    tiff_f = None

    for i, (band, resolution) in enumerate(bands_and_resolutions, start=1):
        band_file = glob(os.path.join(src_data_dir, resolution, "*_" + band + "_*.jp2"))[0]
        band_f = rasterio.open(band_file, driver="JP2OpenJPEG")
        band_data = band_f.read(1)

        if band_data.shape[0] < target_dim[0] and band_data.shape[1] < target_dim[1]:
            print("Extrapolating", band_data.shape, "to", target_dim)
            band_data = extrapolate(band_data, target_dim).astype(band_f.dtypes[0])

        if tiff_f is None:
            profile = band_f.profile
            profile.update(driver="Gtiff", count=len(bands_and_resolutions))
            tiff_f = MemoryFile().open(**profile)

        print("Writing band {} for date {}".format(band, date))
        tiff_f.write(band_data, i)
        band_f.close()

    my_poly = get_test_polygon(my_points)
    tiff_f_cropped = crop_memory_tiff_file(tiff_f, [my_poly], crop=True)

    tiff_f.close()
    tiff_f = None

    f = rasterio.open(tiff_file, "w", **tiff_f_cropped.profile)
    f.write(tiff_f_cropped.read())
    f.close()

    tiff_f_cropped.close()


def main(x, tiff_root_data_dir, my_points, bands_and_resolutions, target_dim):

    src_data_dirs = []
    # per ogni giorno a disposizione individua il path in cui recuperare i dati
    date = x.split('/')[-1].split(".")[0]
    curr_data_dir = glob(os.path.join(x, "GRANULE/*/IMG_DATA"))[0]
    tiff_creation(date, curr_data_dir, my_points)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="cuttingout .save data into tiff",
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("directory_in",  default="None", help="Data In location")
    parser.add_argument("--directory_out", default="None", help="Data Out location")
    args = parser.parse_args()

    # definire le bande che si vogliono utilizzare
    bands = ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B11", "B12"]
    # e la relativa risoluzione
    resolutions = ["R10m", "R10m", "R10m", "R20m", "R20m", "R20m", "R10m", "R20m",
                   "R20m", "R20m"]

    bands_and_resolutions = list(zip(bands, resolutions))

    target_dim = (10980, 10980)

    my_points = [
                    (45.10, 10.98), (45.10, 11.14),
                    (44.99, 11.14), (44.99, 10.98)
                ]

    main(args.directory_in, args.directory_out, my_points,
         bands_and_resolutions, target_dim)
