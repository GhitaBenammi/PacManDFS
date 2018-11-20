import collections
import sys
class ProblemeRecherche(object):
    def __init__(self, etat_initial=None):
        self.etat_initial = etat_initial
    def actions(self, etat):
        raise NotImplementedError
    def resultat(self, etat, action):
        raise NotImplementedError
    def est_objectif(self, etat):
        raise NotImplementedError
class SolveurPacMan(ProblemeRecherche):
    def __init__(self, plateau):
        self.plateau=plateau
        for x in range(len(plateau)):
            for y in range(len(plateau[x])):
                if(plateau[x][y].lower()=='.'):
                    etat_final = (x,y)
                if(plateau[x][y].lower()=='p'):
                    etat_initial = (x,y)
        self.objectif = etat_final
        super(SolveurPacMan, self).__init__(etat_initial)
    def actions(self , etat):
        actions=[]
        list_action=["UP" , "DOWN" , "LEFT" , "RIGHT"]
        for action in list_action:
            newx,newy = self.resultat(etat,action)
            if(self.plateau[newx][newy]!='%'):
                actions.append(action)
        return actions
    def resultat(self , etat , action):
        x,y=etat
        x,y={
            'UP':(x,y-1) ,
            'DOWN':(x,y+1) ,
            'RIGHT':(x+1,y), 
            'LEFT':(x-1,y)
        }[action]
        nouvel_etat= (x , y)
        return nouvel_etat
    def est_objectif(self, etat):
        return self.objectif == etat
class NoeudRecherche(object):
    def __init__(self, etat, parent = None, action = None , probleme= None):
        self.etat = etat
        self.parent = parent
        self.action = action
        self.probleme = parent.probleme if parent!=None and parent.probleme != None else probleme
    def noeudFils(self, probleme, action):
        etatFils=probleme.resultat(self.etat , action)
        return NoeudRecherche(etatFils , self , action , probleme)
    def etendre(self , probleme):
        list_noeud_att=()
        for a in probleme.actions(self.etat):
            list_noeud_att.append(self.noeudFils(probleme , a))
        return list_noeud_att
    def chemin(self):
        liste = []
        noeud = self
        while(noeud.parent!=None):
            liste.append(noeud.parent)
            noeud = noeud.parent
        return reversed(liste)
    def __repr__(self):
        return "<Node {}>".format(self.etat)
    def __repr__(self):
        return "<Node {}>".format(self.etat)
def dfs(probleme):
    noeud=NoeudRecherche(probleme.etat_initial)
    if probleme.est_objectif(noeud.etat):
        return noeud 
    frontiere=collections.deque()
    frontiere.append(noeud)
    explores=[]
    while(len(frontiere)!=0):
        noeud=frontiere.pop()
        explores.append(noeud.etat)
        for action in probleme.actions(noeud.etat):
            fils = noeud.noeudFils(probleme,action)
            if (fils.etat not in explores) or (fils.etat not in frontiere):
                if probleme.est_objectif(fils.etat):
                    return fils
                frontiere.appendleft(fils)
def main():
    PLATEAU=""""
    %%%%%%%%%%%%%%%%%%%%
    %--------------%---%  
    %-%%-%%-%%-%%-%%-%-%  
    %--------P-------%-%  
    %%%%%%%%%%%%%%%%%%-%  
    %.-----------------%  
    %%%%%%%%%%%%%%%%%%%%
    """
    PLATEAU = [list(x) for x in PLATEAU.split("\n")]
    probleme=SolveurPacMan(PLATEAU)
    noeudSolution = dfs(probleme)
    if(noeudSolution == None):
        print("Problème n'accepte aucune solution")
        return sys.exit()
    cheminNoeuds = noeudSolution.chemin()
    chemin = [noeud.etat for noeud in cheminNoeuds]
    print()
    for x in range(len(PLATEAU)):
        for y in range(len(PLATEAU[x])):
            if (x, y) == probleme.etat_initial:
                print('p', end='')
            elif (x, y) == probleme.objectif:
                print('.', end='')
            elif (x, y) in chemin:
                print('n', end='')
            else:
                print(PLATEAU[x][y], end='')
        print()

    
if __name__ == "__main__":
    main()
    
