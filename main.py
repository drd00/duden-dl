import requests
from bs4 import BeautifulSoup

while True:
    noun_verb = input("N or V? ").lower().strip()
    if noun_verb != 'n' and noun_verb != 'v':
        quit()

    query = input("Enter query: ").strip()
    query.replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe')

    try:
        response = None
        if noun_verb == 'v':
            request_url = 'http://www.duden.de/rechtschreibung/{}'.format(query)
            response = requests.get(request_url)
        elif noun_verb == 'n':
            search_url = 'https://www.duden.de/suchen/dudenonline/{}'.format(query)
            response = requests.get(search_url)
            bs = BeautifulSoup(response.text, 'html.parser')
            request_url = 'http://www.duden.de{}'.format(bs.find('a', class_='vignette__label')['href'])
            print(request_url)
            response = requests.get(request_url)

        bs = BeautifulSoup(response.text, 'html.parser')
        pronunciation_section = bs.find('dd', class_='pronunciation-guide__diction')
        audio_link = pronunciation_section.find('a', class_='pronunciation-guide__sound')['href']
        print(audio_link)

        response = requests.get(audio_link)

        if response.status_code == 200:
            filename = f"{query}.mp3"
            with open(filename, 'wb') as f:
                f.write(response.content)

    except Exception as e:
        print(f'Some error {e}')

