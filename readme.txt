FileName: site_string_count

Author: Steven Lechner

External Libraries: requests

What it does:

This program will visit every accessible site in a domain and search for a
given string. It will do this by counting the string's occurrence on the
domain's home page, then collecting all the urls available in that page, and
then recursively repeating this activity on each yet unvisited url that it
finds. The program will output the search links and counts in a csv file.
It will print how much time it took to run.

How to run:

Make sure you're connected to the internet. Upon running, the user is asked to
input the domain they would like to search (starting with "www." and ending
with ".com", ".org", or ".net" ***NB: the program is restricted to those 3***).
They are then asked to input a string to be searched. Then wait patiently--it
can take a while, depending on how many pages are on the website you're
searching.

Before running, be sure to change the directory for both the final results csv
and for the draft csv to what you want them to be. You can update these on
line 28.

TODO:

Add a check of the domain's "robots.txt" file and limit the program's crawling
appropriately. This will involve adding a fourth parameter to the function,
probably a dictionary of the do's and don'ts and any time delays.
