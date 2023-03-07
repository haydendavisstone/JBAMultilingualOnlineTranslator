import argparse
import requests
from bs4 import BeautifulSoup

def get_response(lang_base, lang_translate, word):
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = "https://context.reverso.net/translation/"
    url = base_url + f"{lang_base.lower()}-{lang_translate.lower()}/{word}"
    try:
        r = requests.get(url, headers=headers)
    except ConnectionError:
        print('Something wrong with your internet connection')
        exit()

    return r.content


def translate(page_html, lang_translate, file, word):
    soup = BeautifulSoup(page_html, 'html.parser')

    output_translations(soup, lang_translate, file, word)
    output_examples(soup, lang_translate, file)

def output_translations(soup, lang_translate, file, word):

    translated_words = soup.find_all("span", {"class": "display-term"})

    if not translated_words:
        print(f"Sorry, unable to find {word}")
        quit()

    print(f"{lang_translate} Translation:")
    file.write(f"{lang_translate} Translation:\n")

    print(f"{translated_words[0].get_text()}\n")
    file.write(f"{translated_words[0].get_text()}\n\n")


def output_examples(soup, lang_translate, file):

    translated_examples = [element.text.strip() for element in
                           soup.find('section', id='examples-content').find_all('span', class_='text')]

    print(f"{lang_translate} Examples:")
    file.write(f"{lang_translate} Examples:\n")

    print(f"{translated_examples[0]}")
    file.write(f"{translated_examples[0]}\n")

    print(f"{translated_examples[1]}\n\n")
    file.write(f"{translated_examples[1]}\n\n\n")


def get_langs(language_dict):
    parser = argparse.ArgumentParser()

    parser.add_argument('lang_base', type=str)
    parser.add_argument('lang_translate', type=str)
    parser.add_argument('word', type=str)

    args = parser.parse_args()

    lang_base = args.lang_base.capitalize()
    lang_translate = args.lang_translate.capitalize()

    if lang_base not in language_dict.values():
        print(f"Sorry, the program doesn't support {lang_base}")
        exit()

    if args.lang_translate == 'all':
        lang_translate = 0
    elif lang_translate not in language_dict.values():
        print(f"Sorry, the program doesn't support {lang_translate}")
        exit()

    return lang_base, lang_translate, args.word

def multi_translate(lang_base, word, language_dict, file):

    for i in language_dict:

        if language_dict[i] == lang_base:
            continue

        page_html = get_response(lang_base, language_dict[i], word)
        translate(page_html, language_dict[i], file, word)


def main():
    language_dict = {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew", 7: "Japanese",
                     8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}

    lang_base, lang_translate, word = get_langs(language_dict)

    file = open(f'{word}.txt', 'w', encoding='utf-8')

    if lang_translate != 0:
        page_html = get_response(lang_base, lang_translate, word)
        translate(page_html, lang_translate, file, word)
    else:
        multi_translate(lang_base, word, language_dict, file)


if __name__ == "__main__":
    main()
