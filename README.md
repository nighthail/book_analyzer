# NLP Text analyzer using spaCy

A NLP text analyzer and summarization web application. Uses flask for interface and spaCy for text processing.
Comments are in Swedish and describe each step of the application, as part of assignment.
All texts used are of Public Domain.

#how to use
Clone repository, download all requirements and run the flask application.
On index-page, scroll down to see the menu. From the drop down menu you can pick a text from the /books folder. 
If you add a txt file to this folder and restart the application, your text will pop up as a choice on said menu.
Click submit after picking a text. The resulting processed text will be a summary of your text, and a list of (cast) characters.

if you rather enter your own text you do that in the text area. After entering your text, click submit and the same process will happen
for your entered text.

If you rather compare two texts, click "Compare two texts" link at the bottom of the page. You are taken to the compare-page
where you can enter two texts in text areas at the bottom of the page. After entering two texts, click submit.
The result will be summaries of each text, along with a similarity score.


Known issues:
Non-character words pop up under characters. This is due to a nlp label problem where some words are mislabelled.
Similarities between texts only go after word-for-word similarities and not sentiment or an understanding of texts.
spaCy calculations are slow in flask unless the text is very short
