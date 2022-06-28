# RDT Utils

Provides tools to clean up a mission document.

- install a ```zip``` instead of a ```oxt```, it eases manipulation.

- Discover of the **Addon.xcu** pitfall. In image section, write ```<prop oor:name="URL">``` 
instead of ```<prop oor:name="URL" oor:type="xs:string">```. It will spare you time!

### Requires Java

https://www.java.com/en/download/manual.jsp

### Requires a VLC compat with vlc.__version__ surely x32

https://www.videolan.org/vlc/#download

### Python packages

- wxasync

- python-vlc


## On Ubuntu

Pb installing wxpython: try installing from a wheel, see:

https://stackoverflow.com/questions/41432665/error-failed-building-wheel-for-wxpython-phoenix-while-installing-wx#41432965



## On Windows

Installation on Windows requires VLC in `C:\Program Files\VideoLAN`

Python packages & pip are automatically checked & download at first start.
LibreOffice can be incompatible with `get-pip.py`. Check updates for both LO
and `get-pip.py`

https://pip.pypa.io/en/stable/installation/

Anyway the process of installing `pip` & python packages is simple. Use the
pyhon embedded with LibreOffice. 

    C:\Program Files\LibreOffice\program\python.exe get-pip.py

It will install pip. Then install packages manually (if the extension failed).

    python.exe -m pip install my_package


### Compile Player.exe using PyInstaller

PyInstaller provides an easy way to create an exe for windows. We don't need it 
anymore since the extension launch the player automatically.

   C:\Users\Bastien\Documents>python3 -m PyInstaller --onefile -i=logo.ico RDT.py --windowed

The logo is located in assets/

## Tools

A special class **Mission** has cleanup function in its ```__init__()``` which does:

- Apply special style for question (Inter Q)
- Remove blank char at the end of the line

Tools available in submenu **RDT/Toolbox**

- Timecode cleanup
- Upperise / lowerise questions 
- Remove blank lines
- Order questions
 

## todos

- logs should automatically updated during new version extension generation

- tool to compile menu from simplier format to xml


## logs

- 3.3.7 Use naïve singleton to avoid multiple keyhandler attachment
- 3.3.6 Compatible with Totem player
- 3.3.5 VLC Load track from file picker
- 3.3.4 Bind get_thinks_up to gui event 'load doc'
- 3.3.3 prefix even when string starts with TC
- 3.3.2 VLC launcher in toolbar

- 3.3.1 Get rid of playctl - use full python dbus - implement -+ playing ratio
  
- hit F2 from position starts playing even if paused
  
- automatic inaudible / incompris sequences
  
- implement audio controls + current styles
  
- wrap last word into brackets



## Ideas for future dev

- tool to create a new version (ex. using a flag -N to increment number of version)
- remove and install new extension in one command ```compile & install```

