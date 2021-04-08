# RDT Utils

Provides tools to clean up a mission document.

- install a ```zip``` instead of a ```oxt```, it eases manipulation.

- Discover of the **Addon.xcu** pitfall. In image section, write ```<prop oor:name="URL">``` 
instead of ```<prop oor:name="URL" oor:type="xs:string">```. It will spare you time!

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

- button 'start CQ' create a directory and load medias in it, open track
- logs should automatically updated during new version extension generation

- open media in VLC using dbus loading track

- tool to compile menu from simplier format to xml


## logs

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

