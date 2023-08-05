========
wikiwall
========
*wikiwall* is a CLI that downloads a random image from Wikiart's Hi-Res page and sets it as your desktop background in MacOS.

.. image:: https://github.com/kylepw/wikiwall/blob/master/console.gif?raw=true
	:align: center

Features
--------
- Easily customize your desktop with new hi-res artwork from the command line.
- Update your wallpaper periodically with your favorite scheduler.

Requirements
------------
- Python 3.6 or higher
- macOS


Installation
------------ 
::

	$ git clone https://github.com/kylepw/wikiwall.git 
	$ cd wikiwall
	$ pip3 install -e .

If you want, automatically change your wallpaper each night with launchd: ::

	wikiwall$ sed -i.bak -e "s|WIKIWALL|$(which wikiwall)|g" wikiwall.plist
	wikiwall$ cp wikiwall.plist ~/Library/LaunchAgents
	wikiwall$ launchctl load ~/Library/LaunchAgents/wikiwall.plist


Usage
----- 
::

	$ wikiwall --help
	Usage: wikiwall [OPTIONS]

	  Set desktop background in MacOS to random WikiArt image.

	Options:
  	  --dest TEXT      Download images to specified destination.
  	  --limit INTEGER  Number of files to keep in download directory. Set to -1 for no limit. Default is 10.
  	  --debug          Show debugging messages.
  	  --help           Show this message and exit.
 
Todo
----
- Add to PyPI.
- Add documentation to Sphinx.
- Add support for other operating systems.

License
-------
`MIT License <https://github.com/kylepw/wikiwall/blob/master/LICENSE>`_
