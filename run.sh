#!/bin/bash
cd ressources

# get player input start
echo "Do you wish to start the game in (r)ender mode or in (s)hell mode?"
echo "(One letter and case sensitive)"
read str1
echo $str1

if [ $str1 == "r" ]; then 
python3 render_mode.py
else
echo  "This is not the right way to play the game and does not support any"
echo "graphical display. All informations you will get are debug infos"
echo "from the objects in the simulation. It does show every variables"
echo "but are in no way meant to be used to play the game."
read
python3 shell-mode.py
fi