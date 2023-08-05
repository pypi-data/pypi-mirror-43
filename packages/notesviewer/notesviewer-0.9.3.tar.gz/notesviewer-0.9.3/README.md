# notesviewer

A notes viewer written in python

## installation

pip install notesviewer

## usage

```
notesviewer --help
notesviewer version 
notesviewer list
notesviewer display <note> 
notesviewer insert <note> <title>
nosteviewer edit   <index> <note>
notesviewer delete <note>
notesviewer remove <index> <note>
notesviewer move <index> <fromnote> <tonote>
notesviewer addtags <note> <tag>
notesviewer tags <note>
notesviewer removetags <note> <tag(s)>
notesviewer showconfig
notesviewer setdefaultconfig
notesviewer search <regex> note(s)
notesviewer check
notesviewer interactive    #Not implemented yet

```

## changlog
```
0.9.3
- Changed parser argument for add,insert,delete,remove from name to note to be consistant
- Added help contenxt to commands when using notesviewer --help
```

## Contributing 
Pull requests are welcome. 

## Licsense 
GPL2
