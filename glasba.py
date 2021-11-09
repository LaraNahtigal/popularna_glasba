import csv
import os
import orodja


import requests
import re

STEVILO_STRANI = 20
STEVILO_PESMI_NA_STRANI = 50

music_side_url = 'https://www.last.fm/tag/rock/tracks'
zacetek_url = 'https://www.last.fm'
music_directory = 'podatki_pesmi'
music_side_filename = 'glasba.html'
csv_filename = 'popularna_rock_glasba'

def preberi(mapa):
    for stran in range(1, STEVILO_STRANI + 1):
        url = music_side_url + f'?page={stran}'
        datoteka = os.path.join(mapa, f'prebrane_strani{stran}.html')
        orodja.shrani_spletno_stran(url, datoteka)

def poberi_povezave(strani):
    povezave = []
    for i in range(1, STEVILO_STRANI + 1):
        datoteka = os.path.join(strani, f"prebrane_strani{i}.html")
        with open(datoteka, "r",  encoding="utf-8") as music_side:
            pattern = r'<td.*?class="chartlist-name".*?<a.*?href="(/music/.*?)".*?</a>' 
            regexp = re.compile(pattern, re.DOTALL)
            page_content = music_side.read() 
            povezava = re.findall(regexp, page_content)
            povezave.extend(povezava)
    return povezave
    

def html_glasb(povezave, music_file): 
    stevilo_mape = 1      
    for povezava in povezave:
        song_url = zacetek_url + f'{povezava}'
        datoteka = os.path.join(music_file, f'glasbe{stevilo_mape}.html')
        orodja.shrani_spletno_stran(song_url, datoteka)
        stevilo_mape += 1

vzorec = (
    r'Scrobbles<.*?<abbr .*? title=".*?">(?P<scrobbles>.*?)</abbr>.*?>Listeners<.*?<abbr .*? title=".*?">(?P<st_poslusalcev>.*?)</abbr>'
    r'.*?<dd class="catalogue-metadata-description">.*?' 
    r'(?P<dolzina>\d..*?\d\d).*?'
    r'</p>.*?class="catalogue-tags ".*?'
    r'Related Tags.*?href="/tag/(?P<prvi_zanr>.*?)".*?'
    r'class="tag".*?href="/tag/(?P<drugi_zanr>.*?)".*?'
    r'class="tag".*?href="/tag/(?P<tretji_zanr>.*?)".*?'
    r'data-track-name="(?P<naslov>.*?)".*?'
    r'.*?data-artist-name="(?P<izvajalec>.*?)"'
)

def podatki_iz_html(music_file):
    iskani_podatki = []
    for i in range(STEVILO_PESMI_NA_STRANI * STEVILO_STRANI):
        mapa = f'glasbe{i+1}.html'
        zdruzi = os.path.join(music_file, mapa)
        vsebina = orodja.vsebina_datoteke(zdruzi)
        regexp = re.compile(vzorec, re.DOTALL)
        podatek = re.search(regexp, vsebina)
        if podatek:
            iskani_podatki.append(podatek.groupdict())
        print(iskani_podatki)
    return iskani_podatki


def main():
#    preberi(music_directory)    
#    poberi_povezave(music_directory)
#    povezave = poberi_povezave(music_directory)
#    html_glasb(povezave, music_side_filename)
    podatki_iz_html(music_side_filename)




if __name__ == '__main__':
    main()