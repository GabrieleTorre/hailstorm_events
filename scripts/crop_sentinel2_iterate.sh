#!/bin/bash

# out_dir='./tiff-files/'
out_dir='/Users/beppe/Projects/AgriTech/sentinel_cropped/'

# for f in /Volumes/SSD1/Sentinel-2/2022/*.SAFE;do
for f in /Users/beppe/Projects/AgriTech/Sentinel-2/2021/*.SAFE;do
    python crop_sentinel2.py $f --directory_out $out_dir;
done
