description of features you failed to implement, as well as any extra features you implemented
description of how you tested your program, and ALL of your system tests
Examples of system tests include testing various queries and pasting the results.

Group members: 
Midian Yoseph and Razan Karar

Known Bugs:
Experienced issues when it came to using the calculated relevance scores and pagerank 
when printing out the top 10 pages. 10 pages do print when you search for a word, but 
currently, the printed pages are not the ones with the highest relevancy scores

Instructions for Use:
Begin by copying this line into your terminal, you can replace MedWiki.xml with any xml file of your choice
python3 index.py MedWiki.xml title.txt doc.txt word.txt 

Next, follow with either this line if you do not want to include pagerank in your calculations
python3 query.py title.txt doc.txt word.txt

or this line if you would like to include pagerank
python3 query.py --pagerank title.txt doc.txt word.txt

You will then be prompted to search something in the terminal. You are free to search any word.
If there are no results a message will appear, and if not you can continue to make queries. 


How the Pieces of the Program Fit together:


Features we failed to Implement:


How We Tested our Program:


