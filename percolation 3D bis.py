# Créé par cpetroff, le 28/11/2016 en Pytho
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Percolation.py: Un module python pour effectuer des percolations matricielles."""

from matplotlib    import pyplot
from matplotlib    import colors

#from randomisation import matrice

EAU_MOUVANTE = 3
EAU = 2
VIDE = 1
ROCHE = 0
NEANT = -1

couleurs = ['black', 'grey' , 'white', 'blue', 'cyan']
valeurs  = [ NEANT ,  ROCHE ,  VIDE  ,  EAU  ,  EAU_MOUVANTE]

def modelisation(n, p, indice=0.5):
    esp = espace(n, p, q, indice)
    esp = pluie(esp)
    return percolation(esp)


def percolation(espace):  # methode 2
    """ Indique s'il y a percolation ou pas """

    cmap = colors.ListedColormap(couleurs) # TODO: Relève du display, à mettre ailleurs.
    norm = colors.BoundaryNorm(valeurs + [max(valeurs)+1], cmap.N)
    pyplot.matshow([valeurs], 1, cmap=cmap, norm=norm)
    pyplot.pause(1)

    eau_mouvante = initialisation_eau_mouvante(espace)
    while eau_mouvante != []:

        pyplot.matshow(matrice, 1, cmap=cmap, norm=norm) # TODO: Séparer la logique de display de la logique de génération (threads ?)
        pyplot.pause(.0001)

        eau_mouvante = propagation(espace,eau_mouvante)
    return resultat(espace)


def propagation(espace, eau_mouvante):
     pores_vides = []
     pores_vides_locale = []
     for (x, y) in eau_mouvante:
        pores_vides_locale = regard(matrice, x, y)
        matrice = infiltration(matrice, pores_vides_locale)
        matrice[x][y] = EAU
        pores_vides += pores_vides_locale
     eau_mouvante = pores_vides[:]
     return eau_mouvante

def percolation_critique(n, p, N, P):
    proba = []
    indice = []
    for d in range(N+1):
        indice += [d/N]
    for i in indice:
        S = 0
        for e in range(P):
            if modelisation(n, p, i):
                S += 1
        proba += [S/P]
    pyplot.plot(indice, proba)
    return indice, proba
# EN FONCTION RAPPORT N/P


def resultat(espace):
    for matrice in espace:
        for coef in matrice[len(matrice)-2]: # on parcourt l'avant dernière ligne de la matrice
            if coef == EAU or coef == EAU_MOUVANTE:
                return True
    return False

def pluie(espace):
    """Ajoute de l'eau en surface."""
    for i, matrice in enumerate(espace):
        for j, coef in enumerate(matrice[0]): # enumerate renvoie une liste de tuples (indice, valeur)
            if coef == VIDE:
                matrice[0][j] = EAU_MOUVANTE
    return espace

def regard(espace, x, y, z):
    """Renvoie la liste des coordonnées des pores vides autour d'une case."""
    pores_vides_new = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i == 0 or j == 0) and matrice[x+i][y+j] == VIDE: # on ne regarde pas les cases en diagonale
                pores_vides_new.append((x+i, y+j)) # Les couples de coordonnées sont enregistrés en tuples ()
    return pores_vides_new
    

    



def vecteur_espace(dim):
    sens=[-1,1]
    liste_vecteurs = []
    for d in range(dim):
        direction=[]
        for v in range(2):
            vecteur = dim*[0]
            vecteur[d]= sens[v]
            direction.append(vecteur)
        liste_vecteurs.append(direction)
    return liste_vecteurs


def infiltration(espace, pores_vides):
    """Ajoute de l'eau dans les pores vides."""
    for (x, y) in pores_vides: # On itère sur la liste par tuples
        for matrice in espace :
            matrice[x][y] = EAU_MOUVANTE
    return espace


def initialisation_eau_mouvante(espace):
    eau_mouvante = []
    for i, matrice in enumerate(espace):
        for j, coef in enumerate(matrice[0]):
            if coef == EAU_MOUVANTE:
                eau_mouvante.append((i,0,j))
    return eau_mouvante




from random import random

def espace(n, p, q, indice=.5):
    """Création d'une matrice modélisant une roche poreuse aléatoire."""
    espace = zero(n, p, q)
    espace = pores(espace, indice)
    espace = bords(espace)
    return espace

def zero(n, p, q):
    """ crééer une matrice de zéros de taille n,p,q """
    matrice = [0]*n
    for i in range(n):
        matrice[i] = [0]*p
        for j in range(p):
            matrice[i][j]=[0]*q
    return matrice

def pores(espace, indice=.5):
    """Introduit des pores vides au hasard, en fonction de l'indice de porosité i."""
    for i, matrice in enumerate(espace):
        for j, ligne in enumerate(matrice):
            for k, coeff in enumerate(ligne):
                if random() < indice:
                    espace[i][j][k] = VIDE
    return espace

def bords(espace):
    """On borde la matrice de -1, sur trois côtés."""
    for matrice in espace:
        for ligne in matrice:
            ligne.insert(0, NEANT)
            ligne.append(NEANT)
        ligne_bas = [NEANT] * len(matrice[0])
        matrice.append(ligne_bas)
    matrice_fond=[ligne_bas]*len(espace[0])
    espace.insert(0,matrice_fond)
    espace.append(matrice_fond)
    return espace


#if __name__ == '__main__':
#    data = -1
#    while data != None:
#        data = input("Entrez 4 args ")
#        percolation(data[0], data[1], data[2], data[3])



#  ==[ COMMENTAIRES ]==

#Vous devez définir clairement vos variables par leur nom

#Ne jamais prendre de lettre majuscule en nom de variable.

#Utilisez xrange() au lieu de range() si la liste est statique. Ça passe un itérateur à la structure for au lieu de passer une liste, c'est bien bien bien plus efficace.

#Ne mélangez pas les fonctions et le display. Tout ce qui doit tourner de manière effective au lancement du script doit être dans "if __name__ == '__main__':", le reste c'est des fonctions. Vous pouvez ainsi concevoir et réutiliser votre code comme un module.


