import requests
from bs4 import BeautifulSoup


def get_response(lang_base, lang_translate, word):
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = "https://context.reverso.net/translation/"
    url = base_url + f"{lang_base.lower()}-{lang_translate.lower()}/{word}"
    r = requests.get(url, headers=headers)
    return r.content


def translate(page_html, lang_translate, file):
    soup = BeautifulSoup(page_html, 'html.parser')

    output_translations(soup, lang_translate, file)
    output_examples(soup, lang_translate, file)

def output_translations(soup, lang_translate, file):
    translated_words = soup.find_all("span", {"class": "display-term"})

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
    print("Hello, welcome to the translator. Translator supports:")

    for i in language_dict:
        print(f"{i}. {language_dict[i]}")

    lang_base = language_dict[int(input("Type the number of your language:"))]
    lang_translate = input("Type the number of a language you want to translate to or '0' to translate to all languages:")
    if int(lang_translate) in language_dict:
        lang_translate = language_dict[int(lang_translate)]
    elif lang_translate == '0':
        lang_translate = 0

    word = input("Type the word you want to translate:")

    return lang_base, lang_translate, word

def multi_translate(lang_base, word, language_dict, file):

    for i in language_dict:

        if language_dict[i] == lang_base:
            continue

        page_html = get_response(lang_base, language_dict[i], word)
        translate(page_html, language_dict[i], file)


def main():
    language_dict = {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew", 7: "Japanese",
                     8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}

    lang_base, lang_translate, word = get_langs(language_dict)

    file = open(f'{word}.txt', 'w', encoding='utf-8')

    if lang_translate != 0:
        page_html = get_response(lang_base, lang_translate, word)
        translate(page_html, lang_translate, file)
    else:
        multi_translate(lang_base, word, language_dict, file)


if __name__ == "__main__":
    main()
