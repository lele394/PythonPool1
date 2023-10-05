echo "Please run this script in the provided conda environment if you do not wish to install libraries on your system."
echo "Conda does not have the right libstdc++.so files and thus create an error in LibGL."
echo "additional informations should be available in the report"
echo "If you have any doubts about how to run this project or fix any issues, please contact me using the university mail"
echo "I'm pretty proud of the graphical representation I did as it pushed me out of my comfort zone and would love to at least show it"
echo "leo.bechet@edu.univ-fcomte.fr"

#cd /home/$USER/miniconda/lib # $USER is the name of the session. Basically you need to cd in the conda lib directory
#mkdir backup  # Create a new folder to keep the original libstdc++
#mv libstd* backup  # Put all libstdc++ files into the folder, including soft links
#cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6  ./ # Copy the c++ dynamic link library of the system here
#ln -s libstdc++.so.6 libstdc++.so
#ln -s libstdc++.so.6 libstdc++.so.6.0.19