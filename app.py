from flask import Flask, render_template, request
import nlp_code

app = Flask(__name__)

# Global variables
book_summary = None
unique_characters = None


@app.route('/')
def index():
    #när sidan öppnas körs denna kod:
    #Ingen bok har ännu valts, så None används som placeholder
    doc = nlp_code.get_chosen_book(None)
    global book_summary
    #när doc återfåtts körs make_summary från nlp_code:
    book_summary = nlp_code.make_summary(doc)
    global unique_characters
    #när doc återfåtts körs get_all_characters från nlp_code:
    unique_characters = nlp_code.get_all_characters(doc)
    global book_list
    #När återfås texterna som finns i /books.
    #Placeholder är Alice i Underlandet tills en bok valts
    book_list = nlp_code.get_books()
    book_title = 'Alice in Wonderland'

    return render_template('index.html', book_summary=book_summary, unique_characters=unique_characters,
                           book_list=book_list, book_title=book_title)


#Denna kod körs när en bok har valts:
#Det går säkert att kombinera '/' med denna, men då jag är ny till flask
#har jag inte hittat ett fungerande sätt ännu.
@app.route('/process', methods=['POST'])
def process():
    global book_summary
    global unique_characters
    #Om en bok valts i listan och användaren klickat på submit:
    if request.method == 'POST':
        own_text = request.form['own_text']
        if own_text == '':
            # samma kod som körs under '/' med undantag att en bok nu valts
            chosen_book = request.form['chosen_book']
            doc = nlp_code.get_chosen_book(chosen_book)
            book_summary = nlp_code.make_summary(doc)
            unique_characters = nlp_code.get_all_characters(doc)
            book_title = chosen_book.replace('.txt', '')
            book_title = book_title.replace('-', ' ')
        else:
            doc = nlp_code.prepare_own_text(own_text)
            book_summary = nlp_code.make_summary(doc)
            unique_characters = nlp_code.get_all_characters(doc)
            book_title = "Your text"
    else:
        # Failsafe ifall ingen bok valts (på något sätt)
        chosen_book = 'Alice-in-Wonderland.txt'
        book_title = 'Alice in Wonderland'

    return render_template('index.html', book_summary=book_summary, unique_characters=unique_characters,
                           book_list=book_list, book_title=book_title)

@app.route('/compare_page')
def compare_page():
    text_1 = 'Enter your text below to analyze it'
    text_2 = 'Enter your text below to analyze it'
    similarity_string = 'Similarity between the two texts displayed here'

    return render_template('compare.html', text_1=text_1, text_2=text_2, similarity_string=similarity_string)
@app.route('/compare_func', methods=['POST'])
def compare():
    global text_1, text_2, similarity, similarity_string
    #tar in två texter från två text areas
    compare_text_1 = request.form['compare_text_1']
    compare_text_2 = request.form['compare_text_2']
    #kontrollerar att texterna går att analysera
    if compare_text_1 == compare_text_2 or compare_text_1 == '' or compare_text_2 == '':
        text_1 = 'Faulty data input'
        text_2 = 'Faulty data input'
        similarity_string = ''
    else:
        #Om texterna fungerar skickas de vidare var för sig till funktionerna som
        #förberered dem för att kunna summeras
        doc_1 = nlp_code.prepare_own_text(compare_text_1)
        doc_2 = nlp_code.prepare_own_text(compare_text_2)
        text_1 = nlp_code.make_summary(doc_1)
        text_2 = nlp_code.make_summary(doc_2)
        #Med hjälp av spacys similarity kan vi få ut likheter mellan två texter
        similarity = doc_1.similarity(doc_2)
        similarity = round(similarity, 2)
        similarity = similarity * 100
        similarity_string = 'The texts are ' + str(similarity) + '% similar using spaCY similarity'

    return render_template('compare.html', text_1=text_1, text_2=text_2, similarity_string=similarity_string)


if __name__ == '__main__':
    app.run(debug=True)
