import requests
from bs4 import BeautifulSoup


def get_response(lang_base, lang_translate, word):
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = "https://context.reverso.net/translation/"
    url = base_url + f"{lang_base.lower()}-{lang_translate.lower()}/{word}"
    r = requests.get(url, headers=headers)
    return r.content


def translate(page_html, lang_translate):
    soup = BeautifulSoup(page_html, 'html.parser')

    output_translations(soup, lang_translate)
    output_examples(soup, lang_translate)


def output_translations(soup, lang_translate):
    translated_words = soup.find_all("span", {"class": "display-term"})

    print(f"\n{lang_translate} Translations:")

    translated_words = [translated_words[i].get_text() for i in range(len(translated_words))]

    for n in translated_words:
        print(f'{n}')


def output_examples(soup, lang_translate):

    translated_examples = [element.text.strip() for element in
                           soup.find('section', id='examples-content').find_all('span', class_='text')]

    print(f"\n{lang_translate} Examples:")

    for i, n in enumerate(translated_examples):
        if i % 2 == 0 and i != 0:
            print('')
        print(f'{n}')


def get_langs():
    print("Hello, welcome to the translator. Translator supports:")
    language_list = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish',
                     'Portuguese', 'Romanian', 'Russian', 'Turkish']

    for i, n in enumerate(language_list):
        print(f"{i+1}. {n}")

    lang_base = language_list[int(input("Type the number of your language:"))-1]
    lang_translate = language_list[int(input("Type the number of language you want to translate to:"))-1]
    word = input("Type the word you want to translate:")

    return lang_base, lang_translate, word


def main():
    lang_base, lang_translate, word = get_langs()

    page_html = get_response(lang_base, lang_translate, word)

    translate(page_html, lang_translate)


if __name__ == "__main__":
    main()
