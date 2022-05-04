description of features you failed to implement, as well as any extra features you implemented
description of how you tested your program, and ALL of your system tests
Examples of system tests include testing various queries and pasting the results.

Group members: 
Midian Yoseph and Razan Karar

Known Bugs:
-We experienced issues with our output for a search, have tested pagerank and relevance 
seperately but we ran into an issue where the once you search a word "ball" for example 10 results
about ball will appear but if you search a word after that "cookie" for example all the results for
ball will appear, esentially whatever is searched first is what appears for every other search


Instructions for Use:
Begin by copying this line into your terminal, you can replace MedWiki.xml with any xml file of your choice
python3 index.py MedWiki.xml title.txt doc.txt word.txt 

Next, follow with either this line if you do not want to include pagerank in your calculations
python3 query.py title.txt doc.txt word.txt

or this line if you would like to include pagerank
python3 query.py --pagerank title.txt doc.txt word.txt

You will then be prompted to search something in the terminal. You are free to search any word.
If there are no results a message will appear, and if not you can continue to make queries. 

How We Tested our Program:
- We tested our parsing by making sure that all of our dictionaries were being populated properly 
and checked those values within our test_file.py. We checked our tf and idf calculations by making
that the tf and idf dictionaries were being populated correctly. Again most, of our logic for populating
these dictionaries is within this method so we just checked the value of each individual dictionary

-We tested our check links method by testing on random sets of things that might appear as a link,
checked for edge cases involving less.more of the brackets along with and without the presence of 
a pipe

- We tested our split link method by checking if we properly split a word with the presence of pipe,
our split_link method is called after we call check_link so we did not need to test for that in this 
test

- We tested our pagerank by checking the values for the pagerank given by the TA's in google drive
we also tested our pagerank function on an empty dictionary and made sure that nothing was being 
populated then either. We did not test our euclidian distance because we thought that by testing 
pagerank we are testing our distance method.
-We tested that the sum of the page ranks was equal to one as well 


System Tests:
- We ran our program through the small, medeium and big wikis and timed how long it took our index.py
to write these files. The small wiki took a 10 seconds, the medium wiki took 1 minute, 

How the Pieces of the Program Fit together:
-

Features we failed to Implement:
- we still don't seem to pass all of the gradescope methods 





