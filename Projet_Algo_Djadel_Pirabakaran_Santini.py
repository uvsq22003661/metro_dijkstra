import sys
import tkinter as tk
from tkinter import ttk

#variables
arretes = [] #dico contenant som1 et som2 des E
choix =[] #liste du menu déroulant pour l'affichage
bloque = [] #liste qui montre où ce n'est pas connexe
dicE = {} #dico contenant som1, sa station d'arrivée puis son temps entre les deux
dicgare = {} #dico contenant le numéro de la station, avec son nom, son métro et son terminus
dicoregroupe = {} #dico permettant de trier pour le menu déroulant les doublons
noeuds = [str(i) for i in range(0, 376)] #liste de toutes les stations
path = './metrobis.txt'
visites = [] #liste des visites du graphe pr verifier connexité
sys.setrecursionlimit(1000) #permet d'étendre le nombre de récursivité possible pour la connexité


#########RECUPERATION DES DONNEES#################
with open(path, encoding='utf8') as f:
    for i in range(379):
        line = f.readline()
        if i >= 3:
            line = line.split('/')
            characters = '\n'
            line[4] = ''.join( x for x in line[4] if x not in characters)
            dicgare[line[1]]= [line[2],line[3],line[4]]
    for i in range(472):
        line = f.readline()
        line = line.split(' ')
        characters = '\n'
        line[3] = ''.join(x for x in line[3] if x not in characters)
        if line[1] in dicE:
            stock = dicE[line[1]]
            stock.extend([line[2], int(line[3])])
            dicE[line[1]] = stock
        else:
            dicE[line[1]] = [line[2], int(line[3])]


with open(path,'r') as f:
        for i in range(379):
           line = f.readline()
        if i > 3:
            for i in range(472):
                line = f.readline()
                line = line.split(' ')
                characters = '\n'
                line[3] = ''.join( x for x in line[3] if x not in characters)
                arretes.append((line[1] , line[2]))


def dico_adj():
    """Renvoie la representation en liste d'adjacence du graphe,keys =
    les noeuds du graphe et values = listes de noeuds adjacents"""
    dic_adj = {}
    for E in arretes:
        noeud1, noeud2 = E[0], E[1]
        if not noeud1 in dic_adj.keys():
            dic_adj[noeud1] = []
        dic_adj[noeud1].append(noeud2)  #noeud2 est adjacent à noeud1
        if not noeud2 in dic_adj.keys():
            dic_adj[noeud2] = []
        dic_adj[noeud2].append(noeud1)  #noeud1 est adjacent à noeud2
    return dic_adj


def bidirectionnel():
    """rend dicE bidirectionnel"""
    global dicE
    for elt in noeuds:
        if elt not in dicE:
            tmp = []
            for e in dicE:
                trie = []
                for i in range(len(dicE[e]) // 2):
                    donnes = (dicE[e][i*2], dicE[e][(i*2) + 1])
                    trie.append(donnes)
                for info in trie:
                    if elt in info:
                        if elt not in tmp:
                            l = [elt, e, info[1]]
                            tmp.extend(l)
                        elif elt in tmp: 
                            l = e, info[1]
                            tmp.extend(l)
            if tmp != []:
                a = tmp.pop(0)
                dicE[a] = tmp
    for key in dicE:
        trie = []
        for i in range(len(dicE[key]) // 2):
            donnes = (dicE[key][i*2], dicE[key][(i*2) + 1])
            trie.append(donnes)
            for tri in trie:
                if key not in dicE[tri[0]]:
                    l = key, tri[1]
                    dicE[tri[0]].extend(l)
    dicE['34'].remove('92')
    dicE['34'].remove(37)
    dicE['248'].remove('34')
    dicE['248'].remove(36)
    dicE['280'].remove('248')
    dicE['280'].remove(57)
    dicE['92'].remove('280')
    dicE['92'].remove(43)
    dicE['36'].remove('259')
    dicE['36'].remove(84)
    dicE['198'].remove('36')
    dicE['198'].remove(105)
    dicE['52'].remove("198")
    dicE['52'].remove(42)
    dicE['201'].remove('52')
    dicE['201'].remove(20)
    dicE['145'].remove('201')
    dicE['145'].remove(46)
    dicE['373'].remove('145')
    dicE['373'].remove(55)
    dicE['196'].remove('373')
    dicE['196'].remove(37)
    dicE['259'].remove('196')    

bidirectionnel()

def ligne(i):
    """renvoie la ligne avec le numero des stations, et le numero de la ligne"""
    numero = dicgare[i][1]
    if numero == 'M10':
        terminus = dicgare[i][2].split(',')
        terminus = [f'{terminus[0]},{terminus[1]}',terminus[2]]
    elif numero == 'M13':
        terminus = dicgare[i][2].split(',')
        terminus[1] = ''.join(terminus[1][i] for i in range(len(terminus[1])) if i != 0)
        terminus.reverse()
    else:
        terminus = dicgare[i][2].split(',')
    ligne = [i for i in dicgare if dicgare[i][0] == terminus[0] and dicgare[i][1] == numero]
    adj = []
    tmp = []
    for elt in ligne:
        elt = str(int(elt))
        for i in range(len(dicE[elt]) // 2):
            adj.append(dicE[elt][i*2])
            for stat in adj:
                nouveaustat = stat
                ajout = stat
                while len(nouveaustat) != 4:
                    nouveaustat = '0' + ajout
                    ajout = nouveaustat
                if dicgare[nouveaustat][1] == numero:
                    if nouveaustat not in tmp:
                        tmp.append(nouveaustat)
        for st in tmp:
            if st not in ligne:
                ligne.append(st)
    if numero == 'M7' or numero == 'M7bis' or numero == 'M10' or numero == 'M13':
        ligne = cas_particulier(ligne, numero)
    return ligne, numero


def cas_particulier(ligne,numero):
    """créer les lignes des cas particuliers"""
    if numero == 'M7':
        direction1 = []
        direction2 = []
        index = 0
        for station in ligne[:29]:
            direction1.append(station)
            direction2.append(station)
        for station in ligne[29:]:
            if index % 2 == 0:
                direction1.append(station)
            if index % 2 != 0:
                direction2.append(station)
            index += 1
        direction=[direction1,direction2]
        return direction
    if numero == 'M7bis':
        direction1 = [elt for elt in ligne if elt !='0248']
        direction2 = [elt for elt in ligne if elt !='0092']
        direction = [direction1,direction2]
        return direction
    if numero == 'M10':
        direction1 = []
        direction2 = []
        index = 0
        for station in ligne[:2]:
            direction1.append(station)
            direction2.append(station)
        for station in ligne[2:8]:
            if index % 2 == 0:
                direction1.append(station)
            if index % 2 != 0:
                direction2.append(station)
            index += 1
        for station in ligne[8:]:
            direction1.append(station)
            direction2.append(station)
        direction = [direction1,direction2]
        return direction
    if numero == 'M13':
        direction1 = []
        direction2 = []
        index = 0
        for station in ligne[:18]:
            direction1.append(station)
            direction2.append(station)
        for station in ligne[18:26]:
            if index % 2 == 0:
                direction1.append(station)
            if index % 2 != 0:
                direction2.append(station)
            index += 1
        for station in ligne[26:]:
            direction2.append(station)
        direction =[direction1,direction2]
        return direction


#################CONNEXITE#################
def connexe(sdepart,dic_adj):
    """fonction récursive vérifier la connexité des stations"""
    global noeuds, visites
    if sdepart not in visites :
        visites.append(sdepart)
    for i in dic_adj[sdepart]:
        if i not in visites:
            connexe(i,dic_adj)

#sdepart='0'
#connexe(sdepart,dico_adj())

def verif_connexe_fin():
    """indique si le graphe est connexe ou non"""
    global visites,noeuds,bloque
    if len(visites) == 375:
        print('Ce graphe est connexe.')
    else:
        for elt in noeuds:
            if elt not in visites:
                bloque.append(elt)
        print('Pas connexe à :', bloque)

#verif_connexe_fin()

#####################DIJKSTRA#########################
def Dijkstra(SDepart,SArrive):
    """chemin le plus court entre 2 stations avec le temps en secondes"""
    SDepart = str(int(SDepart))
    SArrive = str(int(SArrive))
    dist = {}  # dictionnaire des distances finales
    pred = {}  # dictionnaire des prédécesseurs
    stock = {}
    stock[SDepart] = 0
    Traites = [SDepart]
    for elt in Traites:
        dist[elt] = stock[elt]
        if elt == SArrive:
            break
        adj = {}
        for i in range(len(dicE[elt]) // 2):
            adj[dicE[elt][i*2]] = dicE[elt][(i*2) + 1]
        for stat in adj:
            if stat in Traites:
                pass
            if stat not in Traites:
                Traites.append(stat)
            distance = stock[elt] + int(adj[stat])
            if stat not in stock.keys() or distance < stock[stat]:
                stock[stat] = distance
                pred[stat] = elt
    chemin, add = est_chemin(pred,SDepart,SArrive)
    if add == 1:
        dist[SArrive] +=78
    temps = TempsTrajet(dist[SArrive])
    return temps, chemin


def est_chemin(p, SDepart, SArrive):
    """recupere les chemins existants"""
    chemin = [SArrive]
    add = 0
    while p[SArrive] != SDepart:
        chemin.append(p[SArrive])
        SArrive = p[SArrive]
    chemin.append(SDepart)
    chemin.reverse()
    # Cas particulier pour la M10   
    if '198' in chemin and '36' in chemin and '259' in chemin:
        for i in range(len(chemin)):
            if chemin[i] == '36':
                chemin.insert(i+1,'37')
                chemin.insert(i+2,'36')
                add = 1
                break
    return chemin, add


def ShortestDijkstra(c):
    """si dikjstra renvoie plusieurs stations du meme métro d'affilé,
    réduit la liste en ne prenant que la premiere et dernière station"""
    m10 = 0
    for i in range(len(c)):
        while len(c[i]) != 4:
            c[i] = '0' + c[i]
    longueur = {}
    chemin = []
    gareproximité = {}
    while c != []:
        if len(c) ==1 :
            chemin.append(c[0])
            longueur[dicgare[c[0]][1]]= 0
            gareproximité[dicgare[c[0]][1]] = 'Aucun'
            c.remove(c[0])
        elif len(c) != 1:
            ctmp = [station for station in c if dicgare[station][1]== dicgare[c[0]][1]]
            if '0259' in ctmp and '0036' in ctmp and '0198' in ctmp: #Cas particulier de la M10
                for i in range(len(ctmp)):
                    if ctmp[i]=='0036':
                        i += 2
                        m10=1
                        break
                ctmp2 = ctmp[0:i]
            if m10 == 1: #Cas particulier de la M10
                chemin.append(c[0])
                chemin.append(c[len(ctmp2)-1])
                chemin.append(c[len(ctmp)-1])
                m10 = 0
            else:
                chemin.append(c[0])
                chemin.append(c[len(ctmp)-1])
            longueur[dicgare[c[0]][1]]=len(ctmp)-1
            gareproximité[dicgare[c[0]][1]] = c[1]
            c = c[len(ctmp):len(c)]
    return chemin, longueur, gareproximité


def Intermediaire(SDepart, SArrive):
    """si une station possède plusieurs numeros, on traite au cas par cas pour l'appliquer sur dikjstra"""
    liste_chemins = [] 
    if len(SDepart) == 1 and len(SArrive) == 1:
        SDepart = SDepart[0]
        SArrive = SArrive[0]
        temps, path = Dijkstra(SDepart, SArrive)
        path = (path,temps)
        liste_chemins.append(path)
    else:
        if len(SDepart) > 1 and len(SArrive) > 1:
            for station_d in SDepart:
                for station_a in SArrive:
                    temps, path = Dijkstra(station_d, station_a)
                    path = (path,temps)
                    liste_chemins.append(path)
        elif len(SArrive) > 1:
            SDepart = SDepart[0]
            for station_a in SArrive:
                temps, path = Dijkstra(SDepart, station_a)
                path = (path,temps)
                liste_chemins.append(path)
        elif len(SDepart) > 1:
            SArrive = SArrive[0]
            for station_d in SDepart:
                temps, path = Dijkstra(station_d, SArrive)
                path = (path,temps)
                liste_chemins.append(path)
    min=liste_chemins[0]
    for p in liste_chemins:
        if len(p[0])<len(min[0]):
            min = p
    temps = min[1]
    tps, cvn, gare = ShortestDijkstra(min[0])
    fin = temps
    affichage(tps, cvn, gare, fin)
    return temps


def TempsTrajet(p):
    """on récupère le trajet en sec et on le convertit pour l'affichage"""
    if p < 3600:
        min = p//60
        seconde = p%60
        temps = f'{min} minutes et {seconde} secondes.'
    else:
        heure = p//60
        min = p//360
        seconde = p%360
        temps = f'{heure} heure et {min} minutes et {seconde} secondes.'
    return temps

################INTERFACE GRAPHIQUE#################
def affichage(tps, longdic, gare, end):
    """affichage des phrases sur l'interface selon les cas possibles"""
    compt = 0
    for i in range(len(tps)):
        while len(tps[i]) != 4:
            tps[i] = '0' + tps[i]
    for i in range(len(tps)):
        while len(tps[i]) != 4:
            tps[i] = '0' + tps[i]
        if i != (len(tps) - 1):
            while len(tps[i + compt]) != 4:
                tps[i + compt] = '0' + tps[i + compt]
                if len(tps[i + compt])==4:
                    compt+=1
        metro, numero = ligne(tps[i])
        ter = 0
        if numero != "M7" and numero != "M7bis" and numero != "M10" and numero != "M13":
            for k in range(len(metro)):
                fin = len(metro) - 1
                if i == len(tps)-1:
                    return end
                if tps[i] == metro[k]:
                    if dicgare[tps[i]][1] == dicgare[tps[i+1]][1]:
                        add = longdic[dicgare[tps[i]][1]]
                        if k+add < len(metro):
                            if tps[i+1] == metro[k+add]:
                                terminus = metro[fin]
                            else :
                                terminus = metro[0]
                        if k+add > len(metro):
                            if tps[i + 1] == metro[k-add]:
                                terminus = metro[0]
                            else :
                                terminus = metro[fin]
                        if i == 0:
                            zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                                dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                        elif dicgare[tps[i]][0]==dicgare[tps[i+1]][0]:
                            zonetexte.insert("end", "Changez de ligne à " + str(dicgare[tps[i]][0]) + ".\n")
                        else:
                            zonetexte.insert("end", "Changez et prenez le " + str(numero) + ", direction " + str(
                                dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
        else :
            add = longdic[dicgare[tps[i]][1]]
            fin1 = len(metro[0]) - 1
            fin2 = len(metro[1]) - 1
            terminus1 = metro[0][fin1]
            terminus2 = metro[1][fin2]
            terminus = metro[0][0]
            if i == len(tps) - 1:
                return end
            if tps[i] in metro[0] and tps[i] in metro[1] and tps[i+1] in metro[0] and tps[i+1] in metro[1]: #cas 1 et 2
                for k in range(len(metro[0])):
                    if dicgare[tps[i]][1] == dicgare[tps[i + 1]][1]:
                        if i == 0:
                            if gare[dicgare[tps[i]][1]] == metro[0][k - 1]:
                                if tps[i + 1] == metro[0][k - add]:
                                    ter = 1
                            if ter == 1 :
                                zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break
                            else :
                                if numero == 'M7' or numero == 'M10':
                                    zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                                        dicgare[terminus1][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                    break
                                else :
                                    zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                                        dicgare[terminus1][0]) + " ou " + str(
                                        dicgare[terminus2][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                    break
                        elif dicgare[tps[i]][0] == dicgare[tps[i + 1]][0]:
                            zonetexte.insert("end", "Changez de ligne à " + str(dicgare[tps[i]][0]) + ".\n")
                            break
                        else:
                            if gare[dicgare[tps[i]][1]] == metro[0][k - 1]:
                                if tps[i + 1] == metro[0][k - add]:
                                    ter = 1
                            if ter == 1 :
                                zonetexte.insert("end", "Changez et prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break
                            else :
                                if numero == 'M7' or numero == 'M10':
                                    zonetexte.insert("end",
                                                     "Changez et prenez le " + str(numero) + ", direction " + str(
                                                         dicgare[terminus1][0]) + " jusqu'à " + str(
                                                         dicgare[tps[i + 1]][0]) + ".\n")
                                    break
                                else:
                                    zonetexte.insert("end",
                                                     "Changez et prenez le " + str(numero) + ", direction " + str(
                                                         dicgare[terminus1][0]) + " ou " + str(
                                                         dicgare[terminus2][0]) + " jusqu'à " + str(
                                                         dicgare[tps[i + 1]][0]) + ".\n")
                                    break
            elif tps[i] in metro[0] and tps[i] in metro[1] and tps[i+1] in metro[0] and tps[i+1] not in metro[1]: #cas 3
                if dicgare[tps[i]][1] == dicgare[tps[i + 1]][1]:
                    if i == 0:
                        zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                            dicgare[terminus1][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")

                    elif dicgare[tps[i]][0] == dicgare[tps[i + 1]][0]:
                        zonetexte.insert("end", "Changez de ligne à " + str(dicgare[tps[i]][0]) + ".\n")
                    else:
                        zonetexte.insert("end", "Changez et prenez le " + str(numero) + ", direction " + str(
                            dicgare[terminus1][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
            elif tps[i] in metro[0] and tps[i] in metro[1] and tps[i + 1] not in metro[0] and tps[i + 1] in metro[1]:#cas 4
                if dicgare[tps[i]][1] == dicgare[tps[i + 1]][1]:
                    if i == 0:
                        zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                            dicgare[terminus2][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                    elif dicgare[tps[i]][0] == dicgare[tps[i + 1]][0]:
                        zonetexte.insert("end", "Changez de ligne à " + str(dicgare[tps[i]][0]) + ".\n")
                    else:
                        zonetexte.insert("end", "Changez et prenez le " + str(numero) + ", direction " + str(
                            dicgare[terminus2][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
            elif (tps[i] not in metro[0] or tps[i] not in metro[1]) and tps[i + 1] in metro[0] and tps[i + 1] in metro[1]:# cas 5 et 6
                if dicgare[tps[i]][1] == dicgare[tps[i + 1]][1]:
                    if i == 0:
                        zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                            dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                    elif dicgare[tps[i]][0] == dicgare[tps[i + 1]][0]:
                        zonetexte.insert("end", "Changez de ligne à " + str(dicgare[tps[i]][0]) + ".\n")
                    else:
                        zonetexte.insert("end", "Changez et prenez le " + str(numero) + ", direction " + str(
                            dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
            elif tps[i] in metro[0] and tps[i] not in metro[1] and tps[i + 1] in metro[0] and tps[i + 1] not in metro[1]:#cas 7 et 8
                for k in range(len(metro[0])):
                    if dicgare[tps[i]][1] == dicgare[tps[i + 1]][1]:
                        if i == 0:
                            if gare[dicgare[tps[i]][1]] == metro[0][k - 1]:
                                if tps[i + 1] == metro[0][k - add]:
                                    ter = 1
                            if ter == 1 :
                                zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break
                            else :
                                zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus1][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break
                        elif dicgare[tps[i]][0] == dicgare[tps[i + 1]][0]:
                            zonetexte.insert("end", "Changez de ligne à " + str(dicgare[tps[i]][0]) + ".\n")
                            break
                        else:
                            if gare[dicgare[tps[i]][1]] == metro[0][k - 1]:
                                if tps[i + 1] == metro[0][k - add]:
                                    ter = 1
                            if ter == 1 :
                                zonetexte.insert("end", "Changez et prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break
                            else :
                                zonetexte.insert("end", "Changez et prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus1][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break
            elif tps[i] not in metro[0] and tps[i] in metro[1] and tps[i + 1] not in metro[0] and tps[i + 1] in metro[1]: #cas 9 et 10
                for k in range(len(metro[1])):
                    if dicgare[tps[i]][1] == dicgare[tps[i + 1]][1]:
                        if i == 0:
                            if gare[dicgare[tps[i]][1]] == metro[1][k - 1]:
                                if tps[i + 1] == metro[1][k - add]:
                                    ter = 1
                            if ter == 1 :
                                zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break
                            else :
                                zonetexte.insert("end", "Prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus2][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break
                        elif dicgare[tps[i]][0] == dicgare[tps[i + 1]][0]:
                            zonetexte.insert("end", "Changez de ligne à " + str(dicgare[tps[i]][0]) + ".\n")
                            break
                        else:
                            if gare[dicgare[tps[i]][1]] == metro[1][k - 1]:
                                if tps[i + 1] == metro[1][k - add]:
                                    ter = 1
                            if ter == 1 :
                                zonetexte.insert("end", "Changez et prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break
                            else :
                                zonetexte.insert("end", "Changez et prenez le " + str(numero) + ", direction " + str(
                                    dicgare[terminus2][0]) + " jusqu'à " + str(dicgare[tps[i + 1]][0]) + ".\n")
                                break


def Stations_Menu():
    """permet le choix des stations sur le menu déroulant"""
    global dicgare, dicoregroupe
    for elt in dicgare:
        if dicgare[elt][0] not in dicoregroupe:
            dicoregroupe[dicgare[elt][0]] = [elt]
        else:
            dicoregroupe[dicgare[elt][0]].append(elt)
    for i in dicoregroupe:
        choix.append(i)
    return choix, dicoregroupe


Stations_Menu()


def relie(D,A):
    """relie press et dijkstra et permet le début et la fin de l'affichage"""
    if D == A :
        zonetexte.insert("end", "Vous êtes déjà à votre gare.")
    else :
        zonetexte.insert("end", "Vous êtes à " + str(D) + ".\n")
        for j in dicoregroupe:
            if j == D:
                    numD=dicoregroupe[j]
            if j == A:
                    numA=dicoregroupe[j]
        recup = Intermediaire(numD, numA)
        zonetexte.insert("end", "Vous êtes bien arrivés à " + str(A) + "!\nVotre temps de trajet est de " + str(recup))


def clearTextInput():
    """réinitalise l'affichage"""
    zonetexte.delete("1.0","end")


def press():
    """commande bouton"""
    racine.geometry("950x450")
    racine.minsize(400, 450)
    zonetexte.pack()
    clearTextInput()
    RechercheBt['text']="Encore un tour?"
    ldepart['text']="Veuillez choisir une autre station de départ."
    larrivee['text'] = "Veuillez choisir une autre station d'arrivée."
    D = depart.get()
    A = arrivee.get()
    relie(D,A)


racine = tk.Tk()
racine.title("Métro - Paris")
racine.geometry("950x200")
racine.minsize(400, 200)
racine.config(bg="black")
zonetexte = tk.Text(racine,bd=0, bg="black", fg="white", font=("Century Gothic", 12, 'normal'))

ldepart = tk.Label(racine,fg="white", bg="black", font=("Century Gothic",10,'normal'), text="Veuillez choisir une station de départ.")
ldepart.pack(pady=5)
depart = ttk.Combobox(racine, font=("Century Gothic",10,'normal'), values=choix)
depart.current(0)
depart.pack()

larrivee = tk.Label(racine, fg="white", bg="black", font=("Century Gothic",10,'normal'), text="Veuillez choisir une station d'arrivée.")
larrivee.pack(pady=5)
arrivee = ttk.Combobox(racine, font=("Century Gothic",10,'normal'), values=choix)
arrivee.current(0)
arrivee.pack()

RechercheBt = tk.Button(racine, font=("Century Gothic",12,'normal'),bg="black",fg="white", text="Rechercher", bd='5', command = lambda : press())
RechercheBt.pack(pady = 20)

racine.iconphoto(False, tk.PhotoImage(file='metro.png'))

racine.mainloop()