import os
import re
import nltk

stopwords = set()
cleaned_words = None

def load_stopwords():
    # stopwords = set()
    folder = "StopWords"
    for file in os.listdir(folder):
        # print(file)
        with open(os.path.join(folder, file), 'r') as f:
            text = f.read().split()
            words = [word.lower() for word in text]
            stopwords.update(words)
    # print(stopwords)
    return stopwords

def remove_stopwords(text):
    # words = text.split()
    # for word in words:
    #     result = re.split(',|:|\.', word)
    #     if len(result) > 1:
    #         words.remove(word)
    #         for word in result:
    #             if word != "":
    #                 words.append(word)
    ## 75 23 0.5306122394835486 0.11722488024255397
    words = nltk.word_tokenize(text)
    ## 75 23 0.5306122394835486 0.09712586709898328
    cleaned_words = [word for word in words if word.lower() not in stopwords]
    # cleaned_text = ' '.join(cleaned_words)
    return cleaned_words

def positive_words(text):
    positive_dictionary = {}
    
    with open('MasterDictionary/positive-words.txt', 'r') as file:
        words = file.readlines()

    for word in words:
        word = word.strip()
        positive_dictionary[word] = 0

    for word in text:
        if word in positive_dictionary.keys():
            positive_dictionary[word] += 1
    positive_score = sum(positive_dictionary.values())
    # print(positive_score)
    return positive_score


def negative_words(text):
    negative_dictionary = {}

    with open('MasterDictionary/negative-words.txt', 'r') as file:
        words = file.readlines()

    for word in words:
        word = word.strip()
        negative_dictionary[word] = 0

    for word in text:
        if word in negative_dictionary.keys():
            negative_dictionary[word] -= 1
    negative_score = sum(negative_dictionary.values())
    # print(negative_score)
    return negative_score

def syllable_count(word):
    vowels_pattern = r'[aeiouAEIOU]+'
    vowels_sequences = re.findall(vowels_pattern, word)
    syllable_count = len(vowels_sequences)

    if word.endswith('es') or word.endswith('ed'):
        syllable_count -= 1
    return syllable_count

def derive_variables(cleaned_words):
    positiveScore = positive_words(cleaned_words)
    negativeScore = negative_words(cleaned_words) * -1
    # Polarity Score: Range is from -1 to +1
    polarityScore = (positiveScore - negativeScore) / ((positiveScore + negativeScore) + 0.000001)

    # Subjectivity Score: Range is from 0 to +1
    subjectivityScore = (positiveScore + negativeScore) / ((len(cleaned_words)) + 0.000001)

    return (positiveScore, negativeScore, polarityScore, subjectivityScore)


def words_analysis(text):
    # Readability analysis
    tokens = nltk.word_tokenize(text)
    words = [word for word in tokens if word.isalnum()]
    sentences = nltk.sent_tokenize(text)

    # 5. avg sentence length
    avg_sentence_len = len(words) / len(sentences)

    # 6. percentage of complex words
    complexwords = [word for word in words if syllable_count(word) > 2]
    percentage_complexwords = len(complexwords) / len(words)

    # 7. Fog Index: Range 6-17
    fog_index = 0.4 * (avg_sentence_len + percentage_complexwords)

    # 8. Average Number of Words Per Sentence
    avg_words_per_sentence = len(words) / len(sentences)

    # 9. Complex Word Count
    complex_words_count = len(complexwords)

    # 10. Word Count
    word_count = len(words)

    # 11. Syllable Count Per Word
    syllables_count = [syllable_count(word) for word in words]
    avg_syllable_per_word = len(syllables_count) / len(words)

    # 12. Personal Pronouns
    pronoun_pattern = r'\b(I|we|my|ours|us)\b'
    pronoun_matches = re.findall(pronoun_pattern, text, flags=re.IGNORECASE)
    pronoun_matches = [pronoun for pronoun in pronoun_matches if pronoun.lower() != 'us']
    pronoun_count = len(pronoun_matches)

    # 13. Average Word Length
    word_sum = 0
    for word in words:
        word_sum += len(word)
    avg_word_length = word_sum / len(words)

    return avg_sentence_len, percentage_complexwords, fog_index, avg_words_per_sentence, complex_words_count, word_count, avg_syllable_per_word, pronoun_count, avg_word_length