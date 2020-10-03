"""
Ce programme a pour but de simuler un système d'exploitation
"""
# import random as rd
import time

def afficher_joliment(p_li):
    for p in p_li:
        print(p, end  = '\n')

def est_vide(chaine : str):
 
    for car in chaine : 
        if car != ' ':
            return False
    return True

def remove_espace_liste(liste):
    for i in range(len(liste)):
        if i >= len(liste):
            return
        if liste[i] == ' ':
            liste.pop(i)

def evaluer_ligne(ligne):
    ligne.lower()
    tab_ligne = ligne.split(' ')
    remove_espace_liste(tab_ligne)
    if tab_ligne[0] == 'busy':
        return 'busy', int(tab_ligne[1])
    if tab_ligne[0] == "fork":
        return "fork", 0
    if tab_ligne[0] == "exec":
        return "exec", tab_ligne[1]
    if tab_ligne[0] == "print":
        return "print", tab_ligne[1:]
    if tab_ligne[0] == "print_status":
        return "print_status",0

class Process :

    def recuperer_le_code(self):
        """ va prendre le code depuis le fichier, et le nettoyer"""
       
        with open(self.nom, 'r') as ce_script :
            code = ce_script.read().split('\n')
            # print(len(code),code)
            # on va maintenant épurer le code
            # print(len(code))
            i = 0
            while i < len(code):
                # print(i, len(code))
                if est_vide(code[i]):
                    code.pop(i)
                    i -= 1
                elif code[i][0] == '#' : 
                    code.pop(i)
                    i -= 1
                i += 1
            # print(code, len(code))
            return code

    def __init__(self,nom_du_fichier,pid, scheduler_en_cours):
        self.pid = pid
        self.nom = nom_du_fichier
        self.temps_de_calcul = 0
        self.sd_ut = scheduler_en_cours
        self.program_counter = 0
        self.code = self.recuperer_le_code()
        self.nb_instructions = len(self.code)
        self.ligne_en_cours_d_execution = 0       # PARCE QU'ON A PAS ENCORE COMMENCE LE CODE

    def __repr__(self):
        return f"Process {self.nom[:-2]} de pid {self.pid}" # \n et voici son code : {self.code}"

    def execute(self, nb_lignes_a_executer = -1):
        if nb_lignes_a_executer == -1 : 
            nb_lignes_a_executer = self.nb_instructions

        i  = 0
        while i < nb_lignes_a_executer and self.ligne_en_cours_d_execution < self.nb_instructions :
            # on va maintenant evaluer la ligne à executer
            # print("i == ",i)
            commande , arg = evaluer_ligne(self.code[self.ligne_en_cours_d_execution])
            # print(commande,arg)
            if commande == 'busy':
                self.sd_ut.heure += arg
            if commande == 'print':
                print(" ".join(arg))
                self.sd_ut.heure += 1
            if commande == "fork":
                self.sd_ut.heure += 1
            if commande == "exec" :
                self.sd_ut.heure += 1
                print(arg)
                self.sd_ut.run(arg)

            if commande == "print_status":
                self.sd_ut.heure += 1
                self.sd_ut.afficher_etat()
                # pas besoin des 2 lignes suivantes...
                # self.sd_ut.process_list.append(Process(arg,len(self.sd_ut.process_list)+1,sd_ut))
                # self.sd_ut.execution_en_cours = len(self.sd_ut.process_list)
            i += 1 
            self.ligne_en_cours_d_execution += 1
            self.sd_ut.afficher_etat()
            # print(nb_lignes_a_executer)
        if self.ligne_en_cours_d_execution ==  self.nb_instructions  : 
            print("je suis au bon endroit ca marche !!!")
            if len(self.sd_ut.process_list) == 1:
                print("FIN DE LA SIMULATION")

            self.sd_ut.process_list.pop()

###############################################################################


class Scheduler :
    
    def __init__(self):
        #on va démarrer le premier processus qui est init
        # pr_init = Process("init.s",1,self)
        self.process_list = []      #
        self.nom_pcs = []
        self.heure = 0                     # la clock du système 
        self.execution_en_cours = None  # pid du process en cours d'exécution

    def c_est_parti(self,process_init):
        self.run(process_init)


    def detect_recursion(self,p_a_lancer):
        # print(p_a_lancer,self.nom_pcs)
        # input("entrée pour continuer...")                                                     #############
        if p_a_lancer in self.nom_pcs:
            # print("nous sommes dans detect_recursion")
            return True

    def run(self,fichier_de_script):   
        """cette fonction va créer un nouveau Process correspondant au fichier .s
        qu'on lui a fourni, l'ajouter à la process_list, l'exécuter"""
        if self.detect_recursion(fichier_de_script):
            return
        self.nom_pcs.append(fichier_de_script)
        self.process_list.append(Process(fichier_de_script, len(self.process_list)+1,self))
        self.execution_en_cours = self.process_list[-1]
        self.execution_en_cours.execute()
        

    def afficher_etat(self):
        print(f"temps d'utilisation : {self.heure}, \nProgrammes en cours d'utilisation :") 
        afficher_joliment(self.process_list)
        print("\n")

sd1 = Scheduler()
sd1.c_est_parti("init.s")

# process1 = Process("init.s",0,sd1)

# print(sd1.process_list)                      # on fait des tests
# process1.execute()
# sd1.run("init.s") 



