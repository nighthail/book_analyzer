import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
import difflib

nlp = spacy.load("en_core_web_lg")

book = open('books/text.txt', encoding='utf-8')
text = book.read()

# book.close()

doc = nlp(text)


# #Tar fram alla unika karaktärer i boken:
#
# # Analyze syntax
# # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
#
# # Find named entities, phrases and concepts
# for entity in doc.ents:
#     # print(entity.text, entity.label_)
#
#     people = []
#     for ent in doc.ents:
#         if ent.label_ == "PERSON" and ent.text[0].isupper() and ent.text[0].isalpha() and not ent.text.isupper():
#             if ent.text not in people and """\n""" not in ent.text and "'s" not in ent.text:
#                 people.append(ent.text.strip())
#             elif ent.text not in people and """\n""" in ent.text and "'s" not in ent.text:
#                 n_word = ent.text.split("""\n""")
#                 people.append(''.join(n_word).strip())
#             elif ent.text not in people and """\n""" not in ent.text and "'s" in ent.text:
#                 s_word = ent.text.split("'s")
#                 people.append(s_word[0].strip())
#
#     compound_people = []
#     for person in people:
#         if person.count(" ") >= 1:
#             compound_people.append(person)
#
#
#     unique_names = []
#     new_list = []
#     final_list = []
#     n = 30
#     cutoff = 0.9
#     for to_compare in compound_people:
#         close_match = difflib.get_close_matches(to_compare, compound_people, n, cutoff)
#         unique_names.append(close_match)
#
#     # # Permutationer tas bort här:
#     # output = set(map(lambda x: tuple(sorted(x)),unique_names))
#
#     # Denna tar också bort permutationer!
#     result = []
#     for i in unique_names:
#         i.sort()
#         result.append(i)
#     output = []
#     for i in result:
#         if i not in output:
#             output.append(i)
#     output = list(map(tuple, output))
#
# #Denna skriver ut alla unika karaktärer:
#     # print(tuple(output))
#


# Denna gör summaries
# Filtering tokens
def make_summary():
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

    # print(freq_word.most_common(20))

    # Weighing sentences
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if word in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]
    # print(sent_strength)

    # Summarization
    summarized_sentences = nlargest(5, sent_strength, key=sent_strength.get)

    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)
    return summary


## Städa upp Karaktärer

# Tar fram alla unika karaktärer i boken:
# Find named entities, phrases and concepts
