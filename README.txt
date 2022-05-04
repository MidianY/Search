description of features you failed to implement, as well as any extra features you implemented
description of how you tested your program, and ALL of your system tests
Examples of system tests include testing various queries and pasting the results.

Group members: 
Midian Yoseph and Razan Karar

Known Bugs:
-We experienced issues with our pagerank. We seem to get correct results for the first pagerank example given in the handout but when we tested it on the other ones our numbers were quite small and they do not add up to 1
- We thought the source of this issue was that we were not properly checking all edgecases for our weight calculations but in the end we believe we thought of all the necessary edge cases associated with it. This led us to examine
if we were checking/identifying links properly and properly populating our dicrionary that maps from pageID's to a set of the pages it has linked. We ran unit tests and found we were checking for links properly and ran through our debugger to find our linked id dictionary was also populating properly, so ultimately we could not solve this bug. 

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
- We ran our program through the small, medium and big wikis and timed how long it took our index.py
to write these files. The small wiki took a 10 seconds, the medium wiki took 1 minute, and the big wiki took 4 minutes. 

In addition to the unit tests on our file, we also did system testing by using the terminal to run a variety of different queries on different xlm files. We ran each query both with and without pagerank.

First, we used the medium wiki to run three “standard” (non-edge cases) queries. Below are our expected and actual search results for each one.

Without Pagerank:
search: baseball 
Actual:
1 Oakland Athletics
2 Minor league baseball
3 Kenesaw Mountain Landis
4 Miami Marlins
5 Fantasy sport
6 Out
7 October 30
8 January 7
9 Hub
10 February 2

Expected:
1 Oakland Athletics
2 Minor league baseball
3 Miami Marlins
4 Fantasy sport
5 Kenesaw Mountain Landis
6 Out
7 October 30
8 January 7
9 Hub
10 February 2

search: United States
Actual
1 Federated States of Micronesia
2 Imperial units
3 Joule
4 Knowledge Aided Retrieval in Activity Context
5 Imperialism in Asia
6 Elbridge Gerry
7 Martin Van Buren
8 Pennsylvania
9 Finite-state machine
10 Metastability

Expected
1 Federated States of Micronesia
2 Imperial units
3 Joule
4 Knowledge Aided Retrieval in Activity Context
5 Imperialism in Asia
6 Elbridge Gerry
7 Martin Van Buren
8 Pennsylvania
9 Finite-state machine
10 Louisiana
 
search: FIRE
Actual
Firewall (construction)
Pale Fire
Ride the Lightning
G?tterd?mmerung
FSB
Keiretsu
Hephaestus
Izabella Scorupco
KAB-500KR
Justin Martyr

Expected
1 Firewall (construction)
2 Pale Fire
3 Ride the Lightning
4 G?tterd?mmerung
5 FSB
6 Keiretsu
7 Hephaestus
8 KAB-500KR
9 Izabella Scorupco
10 Justin Martyr


With Pagerank
search: baseball

Actual:
1 Ohio
2 Oakland Athletics
3 Kenesaw Mountain Landis
4 February 2
5 Miami Marlins
6 Netherlands
7 Minor league baseball
8 Kansas
9 Pennsylvania
10 Fantasy sport

Expected:
1 Ohio
2 February 2
3 Oakland Athletics
4 Kenesaw Mountain Landis
5 Miami Marlins
6 Netherlands
7 Minor league baseball
8 Kansas
9 Pennsylvania
10 Fantasy sport

search: United States
Actual: 
Netherlands
Ohio
Illinois
Michigan
Pakistan
Franklin D. Roosevelt
Pennsylvania
Norway
International Criminal Court
Louisiana

Expected:
1 Netherlands
2 Ohio
3 Illinois
4 Michigan
5 Pakistan
6 International Criminal Court
7 Franklin D. Roosevelt
8 Pennsylvania
9 Norway
10 Louisiana

search: FIRE
Actual
Falklands War
Justin Martyr
Empress Suiko
Firewall (construction)
New Amsterdam
Pale Fire
Montoneros
Hermann G?ring
Nazi Germany
Navy

Expected
1 Falklands War
2 Justin Martyr
3 Firewall (construction)
4 Empress Suiko
5 New Amsterdam
6 Pale Fire
7 Montoneros
8 Hermann G?ring
9 Nazi Germany
10 Navy

We then used the medium xml file to test edge cases:

We tested word parsing by searching “fired”, “FIRE, and “this fire””. As expected, for both with and without pagerank, the results for each of these queries was exactly the same as the results for “fire”
We tested the case in which there were less than 10 query results by searching specific word that only was present in one doc (“Tony’s”) and as expected, it returned a list consistign of only the doc in which that string appeared (“1 Freestyle”)
We tested that a number could be treated as a string by searching “1823”, and as expected, it treated it as a word and returned the respective results 
We searched “”, “ “, “the”, and “jdjfksk” and received the output “no results found”, which is exactly what we expected

We then tested on an empty xml and checked to make sure that our query generated no results for all of the searches we tried on medium wiki.


How the Pieces of the Program Fit together:
- Most of the logic of this program is contained within the Index class. This class goes through all the documents and populated important dictionaries which it uses to create three files: a titles, doc, and word file. The title txt holds all of the titles of the wiki pages along with their associated pageID's, the doc txt contains all of the words along with their pageID and their calculated relevance scores. The index creates and stores alll this information so that once the Query class is ran then it produces results based on a search within seconds. It can easily access the infromation it needs to because the Index class did all the work in properly storing it. 

Features we failed to Implement/Features we added:
- We failed to properly finish pagerank, although it works on some documents, we struggled to get it to work for all edge cases. As outlined in the 'Known Bugs' section we could not figure out where our issuefor pagerank was coming from 
- Our program was storing a lot of things so a design choice we had was to not store our max count, aj, in a dictionary. We felt that our space could be better used for something else. Instead we thought to pass in aj into one of our helper methods that was populating our word_id_to_freq dictionary methods. Because this method was being called for each new word we knew that the max value rather than being stored could be updated with each iteration and then that value at that instant can then be used to populate our tf and idf dictionaries. 





