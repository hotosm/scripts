# Various scripts written for HOT

## Listing:

`preset2style.py` - handles converting and/or merging JOSM XML preset file into an osm2pgsql style file.

Instructions for usage on Windows:

* Download these two files to your desktop:
    
    https://github.com/hotosm/scripts/raw/master/preset2style.py
    https://github.com/hotosm/presets/raw/master/hdm_presets_3.xml
    http://svn.openstreetmap.org/applications/utils/export/osm2pgsql/default.style

* Make sure you have Python >= 2.5 installed and on your PATH

* Then open a command console by going to Start > Run > cmd.

* Then move into the directory on your desktop with the files you downloaded:

    $ cd Desktop

* And run this command which will create the 'hdm.style' file you can use with osm2pgsql

    $ c:\Python25\Python.exe preset2style.py --preset hdm_presets_3.xml --style default.style > hdm.style


Instructions for usage on Linux/Mac:

* Create a working directory

    $ mkdir hotosm
    $ cd hotosm

* Download preset2style.py

    $ wget --no-check-certificate https://github.com/hotosm/scripts/raw/master/preset2style.py

* Download a preset for JOSM:

    $ wget --no-check-certificate https://github.com/hotosm/presets/raw/master/hdm_presets_3.xml 

* Download the latest default osm2pgsql style file:

    $ wget --no-check-certificate http://svn.openstreetmap.org/applications/utils/export/osm2pgsql/default.style

* Then convert the preset, combine with the default.style and output a new, custom style file (hdm.style) for osm2pgsql:

    $ python preset2style.py --preset hdm_presets_3.xml --style default.style > hdm.style

* Then you can use this new style file (hdm.style) with osm2pgsql like:

    $ osm2pgsql -d <dbname> -S hdm.style haiti.osm

   