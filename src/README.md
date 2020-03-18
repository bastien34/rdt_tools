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
 
## Ideas for future dev

- remove and install new extension in one command ```compile & install```

