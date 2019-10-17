import numpy.matlib
import numpy as np
import sys
# numpy.set_printoptions(threshold=sys.maxsize)


# Classe Graph:
# Implémentation d'un modèle de graphe accompagné de méthodes de calculs
#       pour les deux algorithmes de rendez-vous
class Graph:

    # Constructeur de la classe Graph, on associe a l'objet le nombre de noeuds, le nom des sommets
    #       les points de rendez-vous, les sommets initiaux et les arcs du graphe associé à data.
    def __init__(self, data):
        self.size = data["nbNoeuds"]
        self.sommetsList = list(data["nomSommets"])
        self.rdvList = list(data["nomRdv"])
        self.sommetsIniList = list(data["nomSommetsInitiaux"])
        self.arcs = list(data["arcs"])
        self.error = 0
        if self.sommetsList.__len__() != data["nbNoeuds"]:
            self.error = 1
        if self.rdvList.__len__() != data["nbLieuxRdv"]:
            self.error = 2

    # Fonction renvoyant un code d'erreur, aucune erreur n'est apparu si cette fonction renvoie 0
    def error(self):
        return self.error

    # Fonction renvoyant la matrice des distances du graphe
    def mat_graph(self):
        mat = np.full((self.size, self.size), np.inf)
        for arc in self.arcs:
            mat[self.pos_sommet(arc["sommetInitial"])
                , self.pos_sommet(arc["sommetTerminal"])] = arc["duree"]
        return mat

    # Renvoie la position du sommet dans la liste des sommets selon son nom.
    def pos_sommet(self, char):
        return self.sommetsList.index(char)

    # Renvoie une matrice des distances d'un graphe dont les sommets sont paires de sommet
    #       du graphe initial, et les arcs sont des arcs du graphe initial, reliant deux paires
    #       ayant un sommet en commun
    def transform(self, mat):
        size_pair = self.size * self.size
        mat_pair = np.full((size_pair, size_pair), np.inf)
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    for l in range(self.size):
                        if i == k and j == l :
                            mat_pair[i * self.size + j, k * self.size + l] \
                                = np.inf
                        elif i == k :
                            mat_pair[i * self.size + j, k * self.size + l] \
                                = mat[j, l]
                        elif j == l :
                            mat_pair[i * self.size + j, k * self.size + l] \
                                = mat[i, k]
        return mat_pair

    def rdv_optimal(self):
        mat_pcd = self.mat_pcd(self.transform(self.mat_graph()))
        init = self.pos_sommet(self.sommetsIniList[0]) * self.size + self.pos_sommet(self.sommetsIniList[1])
        rdv = []
        for c in self.rdvList:
            rdv.append(self.pos_sommet(c) * self.size + self.pos_sommet(c))
        res = np.inf
        fin = np.inf
        for i in range(len(rdv)):
            if mat_pcd[init, rdv[i]] < res:
                res = mat_pcd[init, rdv[i]]
                fin = i
            if mat_pcd[init, rdv[i]] != np.inf:
                print("sommet : " + self.rdvList[i])
                print("distance : " + str(mat_pcd[init, rdv[i]]))
        if fin != np.inf:
            return str(self.rdvList[fin])
        else:
            return ""

    def mat_pcd(self, mat):
        size_pair = self.size * self.size
        for i in range(size_pair):
            mat[i, i] = 0
        for k in range(size_pair):
            for i in range(size_pair):
                for j in range(size_pair):
                    mat[i, j] = min(mat[i, j], mat[i, k]+mat[k, j])
        return mat

    def mat_pcc(self, mat):
        size_pair = self.size * self.size
        for i in range(size_pair):
            mat[i,i] = 0
        matpcc = np.full((size_pair, size_pair), 0)
        for i in range(size_pair):
            for j in range(size_pair):
                if i != j and mat[i, j] != np.inf:
                    matpcc[i, j] = i + 1
        for k in range(size_pair):
            for i in range(size_pair):
                for j in range(size_pair):
                    av = mat[i, j]
                    mat[i, j] = min(mat[i, j], mat[i, k]+mat[k, j])
                    if av != mat[i, j]:
                        matpcc[i, j] = k + 1
        return mat, matpcc

    def rdv_optimal2(self):
        doublemat = self.mat_pcc(self.transform(self.mat_graph()))
        init = self.pos_sommet(self.sommetsIniList[0]) * self.size + self.pos_sommet(self.sommetsIniList[1])
        rdv = []
        for c in self.rdvList:
            rdv.append(self.pos_sommet(c) * self.size + self.pos_sommet(c))
        res = []
        res2 = []
        for i in range(len(rdv)):
            k = 0
            pos = i
            while doublemat[1][init, pos] != 0 and k < (self.size ** 2):
                pos = doublemat[1][init, pos] - 1
                ++k
            if pos == init:
                res.append(k)
            else:
                res.append(np.inf)
            res2.append(doublemat[0][init, rdv[i]])
        minimum = np.inf
        candidat = []
        for i in range(len(res)):
            if res[i] < minimum:
                candidat.clear()
                candidat.append(i)
            elif res[i] == minimum:
                candidat.append(i)

        resfinal = candidat[0]
        if len(candidat) > 1:
            minfinal = np.inf
            for k in range(len(candidat)):
                if res2[candidat[k]] < minfinal:
                    resfinal = candidat[k]
                    minfinal = res2[candidat[k]]
        if resfinal != np.inf:
            return str(self.rdvList[resfinal])
        else:
            return ""

