import csv
import os
from unittest import skip
import orodja

import re

STEVILO_STRANI = 20
STEVILO_PESMI_NA_STRANI = 50

url_osnovne_strani = 'https://www.last.fm/tag/rock/tracks'
zacetna_stran_url = 'https://www.last.fm'
mapa_osnovnih_strani = 'osnovne_strani'
mapa_glasbe = 'glasba.html'
csv_datoteka = 'popularna_rock_glasba.csv'
csv_album_datoteka = 'albumi_popularnih_glasb.csv'


def preberi(mapa):
    for i in range(STEVILO_STRANI):
        url = url_osnovne_strani + f'?page={i+1}'
        datoteka = os.path.join(mapa, f'prebrane_strani{i+1}.html')
        orodja.shrani_spletno_stran(url, datoteka)


def poberi_povezave(strani):
    povezave = []
    for i in range(STEVILO_STRANI):
        datoteka = os.path.join(strani, f"prebrane_strani{i+1}.html")
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
        song_url = zacetna_stran_url + f'{povezava}'
        datoteka = os.path.join(music_file, f'glasbe{stevilo_mape}.html')
        orodja.shrani_spletno_stran(song_url, datoteka)
        stevilo_mape += 1


vzorec = re.compile( 
    r'Scrobbles<.*?<abbr .*? title=".*?">(?P<scrobbles>.*?)</abbr>.*?>Listeners<.*?<abbr .*? title=".*?">(?P<st_poslusalcev>.*?)</abbr>'
    r'.*?<dd class="catalogue-metadata-description">.*?' 
    r'(?P<dolzina>\d..*?\d\d).*?'
    r'</p>.*?class="catalogue-tags ".*?'
    r'Related Tags.*?href="/tag/(?P<prvi_zanr>.*?)".*?'
    r'class="tag".*?href="/tag/(?P<drugi_zanr>.*?)".*?'
    r'class="tag".*?href="/tag/(?P<tretji_zanr>.*?)".*?'
    r'data-track-name="(?P<naslov>.*?)".*?'
    r'.*?data-artist-name="(?P<izvajalec>.*?)"',
    flags=re.DOTALL
)


vzorec_besedilo = re.compile(
    r'Lyrics.*?<a href=.*?>(?P<besedilo>.*?)</a>.*?',
    flags=re.DOTALL
)


vzorec_album = re.compile(
    r'>Featured On.*?itemprop="url".*?>(?P<ime>.*?)</a>',
    flags=re.DOTALL
)
     

def podatki_iz_html(glasbena_datoteka):
    iskani_podatki = []
    for i in range(STEVILO_PESMI_NA_STRANI * STEVILO_STRANI):
        mapa = f'glasbe{i+1}.html'
        zdruzi = os.path.join(glasbena_datoteka, mapa)
        if os.path.exists(zdruzi):
            vsebina = orodja.vsebina_datoteke(zdruzi)
            podatki = re.search(vzorec, vsebina)
            podatki_albuma = re.search(vzorec_album, vsebina)
            podatki_besedilo = re.search(vzorec_besedilo, vsebina)
            if podatki:
                ena_glasba = podatki.groupdict()
                ena_glasba["prvi_zanr"] = ena_glasba["prvi_zanr"].replace("+", " ")
                ena_glasba["drugi_zanr"] = ena_glasba["drugi_zanr"].replace("+", " ")
                ena_glasba["tretji_zanr"] = ena_glasba["tretji_zanr"].replace("+", " ")
                min, sek = ena_glasba["dolzina"].strip().split(":")
                ena_glasba["dolzina_v_sek"] = int(min)*60 + int(sek)
                if ena_glasba["st_poslusalcev"].count("M") == 1:
                    if ena_glasba["st_poslusalcev"].count(".") == 1:
                        milijon, tisoc = ena_glasba["st_poslusalcev"].replace("M", "").split(".")
                        ena_glasba["poslusalci_tisoc"] = int(milijon)*1000 + int(tisoc)*100
                    else:
                        ena_glasba["poslusalci_tisoc"] = int(ena_glasba["st_poslusalcev"].replace("M", ""))*1000
                else:
                    if ena_glasba["st_poslusalcev"].count(".") == 1:
                        tisoc, _ = ena_glasba["st_poslusalcev"].replace("K", "").split(".")
                        ena_glasba["poslusalci_tisoc"] = int(tisoc)
                    else:
                        ena_glasba["poslusalci_tisoc"] = int(ena_glasba["st_poslusalcev"].replace("K", ""))
                if ena_glasba["scrobbles"].count("M") == 1:
                    if ena_glasba["scrobbles"].count(".") == 1:
                        milijon, tisoc = ena_glasba["scrobbles"].replace("M", "").split(".")
                        ena_glasba["scrobbles_tisoc"] = int(milijon)*1000 + int(tisoc)*100
                    else:
                        ena_glasba["scrobbles_tisoc"] = int(ena_glasba["scrobbles"].replace("M", ""))*1000
                else:
                    if ena_glasba["scrobbles"].count(".") == 1:
                        tisoc, _ = ena_glasba["scrobbles"].replace("K", "").split(".")
                        ena_glasba["scrobbles_tisoc"] = int(tisoc)
                    else:
                        ena_glasba["scrobbles_tisoc"] = int(ena_glasba["scrobbles"].replace("K", ""))
                album = podatki_albuma.groupdict()
                besedilo = podatki_besedilo.groupdict()
                if podatki_albuma:
                    ena_glasba["album"] = album["ime"]
                else:
                    ena_glasba["album"] = None
                if podatki_besedilo:
                    ena_glasba["besedilo"] = besedilo["besedilo"]
                else:
                    ena_glasba["besedilo"] = None
                #print(ena_glasba)
                iskani_podatki.append(ena_glasba)
    return iskani_podatki


def main():
#    preberi(mapa_osnovnih_strani)    
#    poberi_povezave(mapa_osnovnih_strani)
#    povezave = poberi_povezave(mapa_osnovnih_strani)
#    html_glasb(povezave, mapa_glasbe)
    podatki_iz_html(mapa_glasbe)
    slovarji = podatki_iz_html(mapa_glasbe)
    orodja.zapisi_csv(slovarji, ['izvajalec', 'naslov', 'st_poslusalcev', 'poslusalci_tisoc', 'scrobbles','scrobbles_tisoc', 'dolzina', 'dolzina_v_sek', 'prvi_zanr', 'drugi_zanr', 'tretji_zanr', 'album', 'besedilo', ], csv_datoteka)





if __name__ == '__main__':
    main()