import difflib
import os
from flask import Flask, render_template, request, redirect
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

app = Flask(__name__)
nlp = spacy.load("en_core_web_lg")

# Global variables
book_summary = None
unique_characters = None


def get_chosen_book(book_from_menu):
    if book_from_menu is None:
        book = open('books/Alice-In-Wonderland.txt', encoding='utf-8')
    else:
        book = open(f'books/{book_from_menu}', encoding='utf-8')
    text = book.read()
    book.close()

    doc = nlp(text)
    return doc


def make_summary(doc):
    keyword = []
    stopword = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if token.text in stopword or token.text in punctuation:
            continue
        if token.pos_ in pos_tag:
            keyword.append(token.text)

    freq_word = Counter(keyword)

    # Normalization
    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = int(freq_word[word] / max_freq)
    freq_word.most_common(20)

    # Weighing sentences
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if word in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]

    # Summarization
    summarized_sentences = nlargest(5, sent_strength, key=sent_strength.get)

    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)
    return summary


def get_all_characters(doc):
    global unique_characters
    for entity in doc.ents:
        people = []
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.text[0].isupper() and ent.text[0].isalpha() and not ent.text.isupper():
                if ent.text not in people and """\n""" not in ent.text and "'s" not in ent.text:
                    people.append(ent.text.strip())
                elif ent.text not in people and """\n""" in ent.text and "'s" not in ent.text:
                    n_word = ent.text.split("""\n""")
                    people.append(''.join(n_word).strip())
                elif ent.text not in people and """\n""" not in ent.text and "'s" in ent.text:
                    s_word = ent.text.split("'s")
                    people.append(s_word[0].strip())

    # compound_people = []
    # for person in people:
    #     if person.count(" ") >= 1:
    #         compound_people.append(person)

    unique_names = []
    n = 30
    cutoff = 0.9
    for to_compare in people:
        close_match = difflib.get_close_matches(to_compare, people, n, cutoff)
        unique_names.append(close_match)

    # Permutationer tas bort här:
    result = []
    for i in unique_names:
        i.sort()
        result.append(i)
        output = []
        for j in result:
            if j not in output:
                output.append(j)
    output = list(map(tuple, output))
    return output


def get_books():
    book_list = []
    for book in os.listdir("books"):
        if book.endswith(".txt"):
            book_list.append(book)
    return book_list

@app.route('/')
def index():
    doc = get_chosen_book(None)
    # Läser in book_summary funktionen
    global book_summary
    book_summary = make_summary(doc)

    global unique_characters
    unique_characters = get_all_characters(doc)

    global book_list
    book_list = get_books()

    return render_template('index.html', book_summary=book_summary, unique_characters=unique_characters,
                           book_list=book_list)


@app.route('/process', methods=['POST'])
def process():
    global book_summary
    global unique_characters
    if request.method == 'POST':
        chosen_book = request.form['chosen_book']
        doc = get_chosen_book(chosen_book)
        book_summary = make_summary(doc)
        unique_characters = get_all_characters(doc)
        book_title = chosen_book.replace('.txt', '')
        book_title = book_title.replace('-', ' ')
    else:
        chosen_book = 'text.txt'


    return render_template('index.html', book_summary=book_summary, unique_characters=unique_characters,
                           book_list=book_list, book_title=book_title)


if __name__ == '__main__':
    app.run(debug=True)
