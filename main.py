import analysis
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

stopwords = None

df = pd.read_excel('Input.xlsx', sheet_name='Sheet1')
urls = list(df['URL'])

op_dataframe = pd.DataFrame()
num_of_articles = 0

for url in urls:
    response = requests.get(url)

    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')

        headline = soup.find('title')
        headline_text = headline.get_text()

        body_paragraphs = soup.find_all("p")
        body_text = '\n'.join([p.text for p in body_paragraphs])
        
        article_text = headline_text + "\n" + body_text

        # Saving article text in file
        file_name = re.sub(r'[/\\]', '_', url)
        with open(file_name+".txt", "w") as file:
            file.write(article_text)

    else:
        print("Failed to retrieve the webpage. Status code: ", response.status_code)
    
    if stopwords == None:
        stopwords = analysis.load_stopwords()
        # print(stopwords)

    cleaned_words = analysis.remove_stopwords(article_text)
    
    positivescore, negativescore, polarscore, subjectivityscore = analysis.derive_variables(cleaned_words)
    # print(positivescore, negativescore, polarscore, subjectivityscore)

    var5, var6, var7, var8, var9, var10, var11, var12, var13 = analysis.words_analysis(article_text)
    data = {
        'URL': [url],
        'Positive Score': [positivescore],
        'Negative Score': [negativescore],
        'Polarity Score': [polarscore],
        'Subjectivity Score': [subjectivityscore],
        'Avg sentence length': [var5], 
        'Percentage of complex words': [var6],
        'Fog Index': [var7],
        'Avg Number of words per sentence': [var8],
        'Complex word count': [var9],
        'Word count': [var10],
        'Syllable per word': [var11],
        'Personal pronoun': [var12],
        'Avg word length': [var13]
    }
    op_dataframe = op_dataframe._append(pd.DataFrame(data), ignore_index=True)

    num_of_articles += 1
    print(num_of_articles)

excel_file = 'output.xlsx'
op_dataframe.to_excel(excel_file, index=False)