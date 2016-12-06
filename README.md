# Whitewolf Character Generator
------------------------

Basic generation of NPCs for White Wolf chronicles.

Progress
------------------------

Systems Supported: 
 * Vampire: The Masquerade (Clan, Generation, Derangements)

Command Line Parameters
------------------------

Sheets are generated using the script Generator.py

Command line options:
 * -c <class weight filename>
   * CSV, where the first column is clan/class file and the second is percent of total.
   * See demo directory for an example.
   * If none is given, default Vampire Camarilla clans are used with equal probability.
 * -o <output filename>
   * File to print output to. If none is given, sheet is printed to screen.
 * -t <game type>
   * Game type to generate for. Default is Vampire: The Masquerade
 * -m <minimum "level">
   * Minimum power level for a character (i.e., generation in Vampire).
   * Default is 8th generation for Vampire.
 * -x <maximum level>
   * Maximum power level for a character.
   * Default is 13th generation for Vampire.

Example:
python Generation.py -d ../demo/sabbat.csv -o sheet.txt -t vampire -m 8 -x 13

Reporting Faults
------------------------

This tool is currently in the proof-of-concept stage, and has not been extensively tested. If you encounter any issues, please file a report, and I'll try to track it down.
