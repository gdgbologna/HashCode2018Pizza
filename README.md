# Hash Code 2018 Pizza problem
:pizza: test round solution by GDG Bologna

## Problem explanation

*the following text is in Italian because is targeted to an italian community, if you're an english reader and needs a translation please create an issue*

Abbiamo da dividere una pizza rettangolare in diversi pezzi.
La pizza  è divisa in celle, ogni cella può contenere un pomodorino un fungo.
Bisogno massimizzare il numero di pezzi tenendo conto di vincoli sul numero di pomodorini e funghi minimimo per ogni pezzo ma anche su una dimensione massima del pezzo.

Il file di input del problema ha la seguente sintassi:
```
3 5 1 6 
TTTTT 
TMMMT 
TTTTT
```
Cioè una pizza di 3 righe x 5 colonne.
Bisogna che in ogni pezzo di sia almeno 1 pomodorino e un fungo.
E l'area massima del pezzo è di 6 celle.

Il file di output deve avere la seguente sintassi:
```
3
0 0 2 1
0 2 2 2
0 3 2 4
```
Che in pratica dice:
- sono riuscito a creare 3 pezzi
il primo pezzo è un rettangolo dalla cella (0,0) alla cella (2,1) oppure in altre parole è un rettangolo che comprende le righe dalla 0 alla 2 (3 righe) e le colonne dalla 0 alla 1 (2 colonne)
le altre righe sono gli altri pezzi e 

Visualizzata la soluzione è la seguente:

![soluzione](https://bytefreaks.net/wp-content/uploads/2017/01/google-hash-code-2017-Practice-Problem-Example-Submission.png)

Il problema può essere visto anche come la minimizzazione del numero di celle che non vanno a finire in pezzi tagliati e scritti nel file di output.
