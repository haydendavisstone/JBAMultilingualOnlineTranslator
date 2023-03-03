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
    soup = BeautifulSoup(page_html, 'html.parser')

    output_translations(soup)
    output_examples(soup)


def output_translations(soup):

    translated_words = soup.find_all("span", {"class": "display-term"})

    print("\nFrench Translations:")

    translated_words = [translated_words[i].get_text() for i in range(len(translated_words))]

    for n in translated_words:
        print(f'{n}')


def output_examples(soup):
    translated_examples = soup.find_all("span", {"class": "text"})

    translated_examples = [element.text.strip() for element in
                           soup.find('section', id="examples-content").find_all('span', class_="text")]

    print("\nFrench Examples:")

    for i, n in enumerate(translated_examples):
        if i % 2 == 0 and i != 0:
            print('')
        print(f'{n}')


def main():
    target_lang = input('Type "en" if you want to translate from French into English, '
                        'or "fr" if you want to translate from English into French:')
    word = input('Type the word you want to translate:')
    print(f"You chose {target_lang} as a language to translate {word}.")

    page_html = get_response(target_lang, word)

    translate(page_html)


if __name__ == "__main__":
    main()
