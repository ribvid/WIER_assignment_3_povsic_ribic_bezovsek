# IEPS-tretji-seminar

### Dodajanje seznama slovenskih stop-wordov

Če namestimo paket nltk.stopwords, datoteka s stopwordi za slovenski jezik ne obstaja. Zato tudi dobimo error pri dodajanju
stopwordov v datoteki [stopwords.py](stopwords.py). Zato se v datoteki [slovenian](data/slovenian) nahaja vsebina z osnovnimi
stopwordi, ki jo moramo prilepiti v ustrezno mapo na računalniku - kjer se nahajajo podatki nltk knjižnice. V mojem primeru
sem moral datoteko dodati v mapo `C:\Users\Luka\AppData\Roaming\nltk_data\corpora\stopwords`. Nato vsebino lahko ustrezno
uvozimo, razširimo in uporabljamo v našem programu.

### Ustvarjanje invertnega indexa

V datoteki [start.py](start.py), se nahaja parameter **rebuild_index**. Ta nam pove, ali želimo ob zagonu ponovno ustvariti index
ali ne. Če je njegova vrednost nastavljena na False, se vsi dokumenti zgolj preberejo, ustrezno preobdelajo, tokenizirana
vsebina vseh dokumentov, pa se hrani v RAM-u (ta proces traja pribl. 45 sekund). V nasprotnem primeru moramo vrednost parametra
nastaviti na True, stara vsebina v podatkovni bazi se pobriše in zgradi se nov index (traja lahko nekaj ur). Celoten index
vseh dokumentov se nahaja v datoteki [inverted-index.db](inverted-index.db). 

### Iskanje

Iskanje zaženemo s skripto [search.py](search.py). Ta požene iskanje z uporabo inverznega
indeksa in klasično iskanje brez indeksa. Tako lahko že takoj vidimo razlike
v hitrosti med obema pristopoma.