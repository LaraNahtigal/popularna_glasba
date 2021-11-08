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
            #print(len(povezave))
            #print(povezave)
    return povezave
    

def html_glasb(povezave, music_file): 
    stevilo_mape = 1      
    for povezava in povezave:
        url = zacetek_url + f'{povezava}'
        datoteka = os.path.join(music_file, f'glasbe{stevilo_mape}.html')
        orodja.shrani_spletno_stran(url, datoteka)
        stevilo_mape += 1

def main():
#    preberi(music_directory)    
#    poberi_povezave(music_directory)
#    povezave = poberi_povezave(music_directory)
#    html_glasb(povezave, music_side_filename)






#def save_frontpage(page, directory, filename):
#    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
#    "directory"/"filename"."""
#    raise NotImplementedError()
#
#
################################################################################
## Po pridobitvi podatkov jih želimo obdelati.
################################################################################
#
#
#def read_file_to_string(directory, filename):
#    with open(os.path.join(directory, filename), encoding="utf-8") as input_file:
#        return input_file.read()
#
#
## Definirajte funkcijo, ki sprejme niz, ki predstavlja vsebino spletne strani,
## in ga razdeli na dele, kjer vsak del predstavlja en oglas. To storite s
## pomočjo regularnih izrazov, ki označujejo začetek in konec posameznega
## oglasa. Funkcija naj vrne seznam nizov.
#
#
#def page_to_ads(page_content):
#    pattern = r'<tr(.*?)class="(.*?)chartlist-row(.*?)</tr>'
#    regexp = re.compile(pattern, re.DOTALL)
#
#    return re.findall(regexp, page_content)
#
#
## Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušči
## podatke o imenu, lokaciji, datumu objave in ceni v oglasu.
#
#
#def get_dict_from_ad_block(block):
#    pattern = r'<a(.*?)class="(.*?)chartlist-play-button(.*?)data-track-url="(?P<href>).*?".*?</a>'
#    regexp = re.compile(pattern, re.DOTALL)
#    najdeno = re.search(regexp, block)
#    if najdeno:
#        return najdeno.groupdict()
#    return None
#
#
## Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
## besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
## vseh oglasih strani.
#
#
#def ads_from_file(filename, directory):
#    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
#    pretvori (razčleni) v pripadajoč seznam slovarjev za vsak oglas posebej."""
#    raise NotImplementedError()
#
#
################################################################################
## Obdelane podatke želimo sedaj shraniti.
################################################################################
#
#
#def write_csv(fieldnames, rows, directory, filename):
#    """
#    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
#    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
#    """
#    os.makedirs(directory, exist_ok=True)
#    path = os.path.join(directory, filename)
#    with open(path, 'w', encoding='utf-8') as csv_file:
#        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#        writer.writeheader()
#        for row in rows:
#            writer.writerow(row)
#    return
#
#
## Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
## podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
## stolpce [fieldnames] pridobite iz slovarjev.
#
#
#def write_cat_ads_to_csv(ads, directory, filename):
#    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
#    parametroma "directory"/"filename". Funkcija predpostavi, da so ključi vseh
#    slovarjev parametra ads enaki in je seznam ads neprazen."""
#    # Stavek assert preveri da zahteva velja
#    # Če drži se program normalno izvaja, drugače pa sproži napako
#    # Prednost je v tem, da ga lahko pod določenimi pogoji izklopimo v
#    # produkcijskem okolju
#    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
#    raise NotImplementedError()
#
#
## Celoten program poženemo v glavni funkciji
#
#def main(redownload=True, reparse=True):
#    """Funkcija izvede celoten del pridobivanja podatkov:
#    1. Oglase prenese iz bolhe
#    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
#    3. Podatke shrani v csv datoteko
#    """
#    # Najprej v lokalno datoteko shranimo glavno stran
#      
#    #spletna_stran = download_url_to_string(music_side_url)
#    #save_string_to_file(spletna_stran, music_directory, music_side_filename)
#
#    # Iz lokalne (html) datoteke preberemo podatke
#    vsebina = read_file_to_string(music_directory, music_side_filename)
#
#    # Podatke preberemo v lepšo obliko (seznam slovarjev)
#
#    seznam_reklam = page_to_ads(vsebina)
#    print(seznam_reklam)
#    seznam_podatkov = [
#        get_dict_from_ad_block(oglas) for oglas in seznam_reklam
#    ]
#
#    print(seznam_podatkov)
#
#    # Podatke shranimo v csv datoteko
#
#    # Dodatno: S pomočjo parametrov funkcije main omogoči nadzor, ali se
#    # celotna spletna stran ob vsakem zagon prenese (četudi že obstaja)
#    # in enako za pretvorbo
#
#    
#
#


if __name__ == '__main__':
    main()