Here are the data files needed to run YoFrankie (Blender Game Engine Version)

To play this game you will need to have already installed Blender 2.49a or newer.

Without any modifications you can play the game by loading "levels/start_menu.blend" in blender, Game Menu, Start Game.
Or execute...
 "blenderplayer yo_frankie_stub.blend"

Problems with blender can be reported to the blender bug tracker.
http://projects.blender.org/tracker/?group_id=9&atid=125

Problems with datafiles and game logic can be reported to the yo-frankie tracker.
http://projects.blender.org/tracker/?atid=445&group_id=151&func=browse


The Makefile in this directory can be used to compress the datafiles for distribution,
Dependencies for make are...
* blender 2.49a+
* imagemagick
* python

Running make will do the following
* Images without alpha are converted to jpeg
* blendfiles are compressed

Resulting files are copied to ./package

Again, this is only needed for distribution, uncompressed files are about 300mb, and around 130mb when compressed.

Any further issues you can contact ideasman42@gmail.com