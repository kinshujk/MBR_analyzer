<h1>Master Boot Record analyzer</h1>

This program takes the MBR of a disk as input in the form of a raw file. It analyzes this file to produce the partition table entries on the record.

Make the mbr_info command using `$make` <br>
Run the program by passing the filename of the MBR to analyze `$./mbr_info FILENAME.raw`

Clean using `$make clean`