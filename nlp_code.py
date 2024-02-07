import difflib
import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

nlp = spacy.load("en_core_web_lg")


def get_chosen_book(book_from_menu):
    # Här hämtas texten som ska bearbetas.
    if book_from_menu is None:
        # Default-boken är Alice i Underlandet
        book = open('books/Alice-In-Wonderland.txt', encoding='utf-8')
    else:
        # Här hämtas boken från en lista
        book = open(f'books/{book_from_menu}', encoding='utf-8')
    # här läses texten
    text = book.read()
    # Här stängs boken så den tar upp mindre minne i datorn
    book.close()

    # bok-texten bearbetas med NLP och sparas som variabeln doc
    doc = nlp(text)
    # doc skickas iväg
    return doc


def prepare_own_text(own_text):
    #Här omvandlas den inmatade texten till ett NLP-dokument
    doc = nlp(own_text)
    return doc


def get_books():
    # Detta är en funktion som läser in alla texter med .txt som filändelse, och appendar dem i en lista
    book_list = []
    for book in os.listdir("books"):
        if book.endswith(".txt"):
            book_list.append(book)
    # Listan skickas vidare för att kunna skrivas ut i en meny på hemsidan
    return book_list


def make_summary(doc):
    # Doc har skickats in i funktionen från get chosen book.
    # Lista skapad
    keyword = []
    # Importerad lista av engelska stopp ord (pronomen, prepositioner etc)
    stopword = list(STOP_WORDS)
    # alla tokens med taggarna nedan sparas som lista
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if token.text in stopword or token.text in punctuation:
            # Hoppar över ord som är stoppord och punctuations
            continue
        if token.pos_ in pos_tag:
            # sparar enbart tokens som inte ingår i stopword eller punctuations
            keyword.append(token.text)

    # Räknar de vanligaste orden
    freq_word = Counter(keyword)

    # Normalization-processen
    # Letar upp den frekvensen av vardera keyword, med hjälp a Counter()funktionen
    # (1) frågar efter det absolut vanligaste elementet. [0] indikerar det första ordet i tuple, [1] är frekvensen
    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        # "Normaliserar" fekvensen genom att dela varje ords frekvens med det maximala antalet frekvenser,
        # konverterar sedan till int
        freq_word[word] = int(freq_word[word] / max_freq)
    # Använder most_common() funktionen från collections så värdet går att ordna
    freq_word.most_common(5)

    # "Vägning av meningar"
    # Tom dictionary skapas
    sent_strength = {}
    #
    for sent in doc.sents:
        for word in sent:
            # Kontrollerar om ordet finns med i den normaliserade frekvens-dicitonaryn
            # läggs ordets styrka till vid ordet.
            if word.text in freq_word.keys():
                # Placeholder, här görs inget urskilljande
                if word in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]

    # Summarization-process
    # Använder sig av nlargest, som är en funktion hos heapq för att få fram de fem
    # starkaste meningarna
    summarized_sentences = nlargest(5, sent_strength, key=sent_strength.get)

    # De 5 starkaste meningarna sorteras ut
    final_sentences = [w.text for w in summarized_sentences]
    # Här skrivs de in i samma string
    summary = ' '.join(final_sentences)
    # skickar ut summary-strängen
    return summary


def get_all_characters(doc):
    # Denna funktion är menad att ta fram alla unika namn i texten
    # Skapar en set för att spara namnen i
    people = set()
    # För varje entitet i texten:
    for ent in doc.ents:
        # Om entiteten har labeln person, första bokstaven är stor, alla bokstäver INTE är stora, och namnet enbart innehåller
        # bokstäver:
        if ent.label_ == "PERSON" and ent.text[0].isupper() and ent.text[0].isalpha() and not ent.text.isupper():
            # Städar upp namn som innehåller 's, och även inskrivna radbrytningar (hade en text som hade det problemet)
            cleaned_name = ent.text.strip().replace("'s", "").replace("\n", "").replace("´s", "")
            # Adderar namnen till settet
            people.add(cleaned_name)

    # Skapar lista över unika namn
    unique_names = []
    # Max antal namn i varje item, drog till med ett högt nummer
    n = 30
    # Så nära matchade namnen får vara, max 1.
    cutoff = 0.9

    # Här jämförs namnen i settet för att se om samma eller liknande namn
    # dyker upp flera ggr, så som Antony Smith vs Anthony Smith.
    for to_compare in people:
        # Använder difflib bibliotekets get_close_matches för att jämföra ord.
        close_match = difflib.get_close_matches(to_compare, people, n, cutoff)
        # appendar varje unikt namn
        unique_names.append(close_match)

    # tar bort dubletter, så som (Smith, Smit) vs (Smit, Smith).
    # Detta görs genom att först sortera namnen, omvandla dem till en tuple så ordningen av namn inte påverkar
    # slutresultatet. Set-konverteringen gör så enbart unik data ska få skrivas in.
    # omvandlingen till list är för att datan lättare ska kunna skrivas ut på hemsidan
    unique_names = list(set(tuple(sorted(names)) for names in unique_names))

    return unique_names

