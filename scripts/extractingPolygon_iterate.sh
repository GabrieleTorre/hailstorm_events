#!/bin/bash

out_dir='./tiff-files/'

for f in /Volumes/SSD1/Sentinel-2/2022/*.SAFE;do
    python extractingPolygon_fromSentinel2.py $f --directory_out $out_dir;
done
