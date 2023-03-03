import requests
from bs4 import BeautifulSoup

def get_response(target_lang, word):
    headers = {'User-Agent': 'Mozilla/5.0'}
    query = {"en": "french-english", "fr": "english-french"}
    base_url = "https://context.reverso.net/translation/"
    url = base_url + f"{query[target_lang]}/{word}"
    r = requests.get(url, headers=headers)
    print(r.status_code, "OK" if r else "Fail")
    return r.content

def translate(page_html):
    print('Translations')

    soup = BeautifulSoup(page_html, 'html.parser')

    translated_words = soup.find_all("span", {"class": "display-term"})

    translated_words = [translated_words[i].get_text() for i in range(len(translated_words))]

    print(translated_words)

    translated_sentences = soup.find_all("span", {"class": "text"})

    translated_sentences = [element.text.strip() for element in
                            soup.find('section', id="examples-content").find_all('span', class_="text")]

    print(translated_sentences)


def main():
    target_lang = input('Type "en" if you want to translate from French into English, '
                            'or "fr" if you want to translate from English into French:')
    word = input('Type the word you want to translate:')
    print(f"You chose {target_lang} as a language to translate {word}.")

    page_html = get_response(target_lang, word)

    translate(page_html)

if __name__ == "__main__":
    main()




