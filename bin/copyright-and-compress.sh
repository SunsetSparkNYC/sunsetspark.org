/usr/local/opt/mozjpeg/bin/cjpeg -quality 75 -targa -outfile $OF.jpg $IF.tga
exiv2 -M"set Exif.Image.Copyright © 2020 Sunset Spark, Inc." *.jpg
