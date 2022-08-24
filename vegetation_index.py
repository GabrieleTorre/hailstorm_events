import numpy as np

'''
Sentinel-2 band legend (-> our mapping)

#B01  - Coastal aerosol
#B02  - Blue                            -> #1 (R10m)
#B03  - Green                           -> #2 (R10m)
#B04  - Red                             -> #3 (R10m)
#B05  - Vegetation Red Edge (µm 0.705)  -> #4 (R20m)
#B06  - Vegetation Red Edge (µm 0.740)
#B07  - Vegetation Red Edge (µm 0.783)
#B08  - NIR                             -> #5 (R10m)
#B08A - Vegetation Red Edge (µm 0.865)  -> #6 (R20m)
#B09  - Water vapour
#B10 - SWIR - Cirrus
#B11 - SWIR (µm 1.610)                  -> #7 (R20m)
#B12 - SWIR (µm 2.190)                  -> #8 (R20m)

'''


def NDVI(mem_file):
    # NDVI = (NIR – RED)/(NIR + RED)
    return np.array([(mem_file.read(5) - mem_file.read(3)) / (mem_file.read(5) + mem_file.read(3))])
