import difflib
import os
from flask import Flask, render_template, request, redirect
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
import nlp_code

app = Flask(__name__)

# Global variables
book_summary = None
unique_characters = None


@app.route('/')
def index():
    doc = nlp_code.get_chosen_book(None)
    global book_summary
    book_summary = nlp_code.make_summary(doc)
    global unique_characters
    unique_characters = nlp_code.get_all_characters(doc)
    global book_list
    book_list = nlp_code.get_books()
    book_title = 'Alice in Wonderland'

    return render_template('index.html', book_summary=book_summary, unique_characters=unique_characters,
                           book_list=book_list, book_title=book_title)


@app.route('/process', methods=['POST'])
def process():
    global book_summary
    global unique_characters
    if request.method == 'POST':
        chosen_book = request.form['chosen_book']
        doc = nlp_code.get_chosen_book(chosen_book)
        book_summary = nlp_code.make_summary(doc)
        unique_characters = nlp_code.get_all_characters(doc)
        book_title = chosen_book.replace('.txt', '')
        book_title = book_title.replace('-', ' ')
    else:
        chosen_book = 'text.txt'
        book_title = 'Alice in Wonderland'

    return render_template('index.html', book_summary=book_summary, unique_characters=unique_characters,
                           book_list=book_list, book_title=book_title)

if __name__ == '__main__':
    app.run(debug=True)
