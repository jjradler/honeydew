# README.md
## Honeydew -- Version 0.3
### Your Source For Source Code To-Do and Fix-Me Lists!
Written By: Joseph J. Radler ([website][website] and [github][github])

---
### Description

Honeydew is a simple Python3 script in its current prototype form that will scan
the text files in the current directory for inline `To-Do` and `Fix-Me` comments.

---
### Deployment Notes:

This prototype (v0.3) is currently implemented to read code comments beginning
with the octothorpe (\#) character. It also does not currently discriminate
between standard text and source code files, however this functionality is
on my current To-Do list.

Another function I plan to add is the ability for the script to update/archive
items on the To-Do list automatically if they have been checked off.

I plan to extend it to include C/C++/Swift, Java, Javascript, Bash, Ruby,
Haskell, MATLAB, HTML, and Golang comments in the near future (but probably not
all at once!)

Also coming as soon as possible is an extension to allow this to be installed
automatically in the folder of your choosing and then called as a command.

Finally, the endgame here is to have the above functions, but also having
Honeydew scan subfolders of the working folder to create a "Master To-Do" list
as well as a "To-Do" list in each subdirectory of a project folder automatically.

The test file and test directories are there for development purposes and when I
have a more refined version of the program they will be moved to another
location.

---
### Invocation
To use this script, simply place it in the working directory containing your
source files.

**WARNING:** Before executing the script, if you have a `TODO.md` file already
existing in the directory containing `honeydew.py`, the script
*will erase the existing one and replace it with the automatically
generated file!*

Sufficed to say, use at your own risk!

Just run the script in the usual manner as any other Python script:

`python3 honeydew.py`

and let it do the work for you! If only it would do the actual list, too...

[website]: https://jjradler.github.io
[github]: https://github.com/jjradler
