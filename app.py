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
        #samma kod som körs under '/' med undantag att en bok nu valts
        chosen_book = request.form['chosen_book']
        doc = nlp_code.get_chosen_book(chosen_book)
        book_summary = nlp_code.make_summary(doc)
        unique_characters = nlp_code.get_all_characters(doc)
        book_title = chosen_book.replace('.txt', '')
        book_title = book_title.replace('-', ' ')
    else:
        #Failsafe ifall ingen bok valts (på något sätt)
        chosen_book = 'Alice-in-Wonderland.txt'
        book_title = 'Alice in Wonderland'

    return render_template('index.html', book_summary=book_summary, unique_characters=unique_characters,
                           book_list=book_list, book_title=book_title)

if __name__ == '__main__':
    app.run(debug=True)
