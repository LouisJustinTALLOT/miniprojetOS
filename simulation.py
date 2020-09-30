"""

Ce programme a pour but de simuler un système d'exploitation

"""
# import random as rd
nombreexec = 0 

def est_vide(chaine : str):
 
    for car in chaine : 
        if car != ' ':
            return False
    return True

def evaluer_ligne(ligne):
    try : 
        if ligne[:4].lower() == 'busy':
            return 'busy', int(ligne[5:])
    except:
        pass




class Process :

    def recuperer_le_code(self):
        global nombreexec 
        nombreexec += 1
        with open(self.nom+'.s', 'r') as ce_script :
            code = ce_script.read().split('\n')

            # print(len(code),code)
            # on va maintenant épurer le code
            # print(len(code))
            i = 0
            while i < len(code):

                if est_vide(code[i]):
                    code.pop(i)
                    i -= 2
                elif code[i][0] == '#' : 
                    code.pop(i)
                    i -= 2
                i += 1
            # print(code, len(code))
            return code


    def __init__(self,nom_du_fichier,pid, scheduler_en_cours):
        self.pid = pid
        self.nom = nom_du_fichier[:-2]
        self.temps_de_calcul = 0
        self.scheduler_en_cours_d_utilisation = scheduler_en_cours
        self.program_counter = 0
        self.code = self.recuperer_le_code()
        self.nb_instructions = len(self.code)
        self.ligne_en_cours_d_execution = 0       # PARCE QU'ON A PAS ENCORE COMMENCE LE CODE
        

    def __repr__(self):
        return f"Process {self.nom} de pid {self.pid}" # \n et voici son code : {self.code}"

    def execute(self, nb_lignes_a_executer = -1):
        if nb_lignes_a_executer == -1 : 
            nb_lignes_a_executer = self.nb_instructions

        i  = 0
        while i < nb_lignes_a_executer and self.ligne_en_cours_d_execution < self.nb_instructions :
            # on va maintenant evaluer la ligne à executer

            commande , arg = evaluer_ligne(self.code[self.ligne_en_cours_d_execution])

            if commande == 'busy':
                self.scheduler_en_cours_d_utilisation.heure += arg

            i += 1 
            self.ligne_en_cours_d_execution += 1
            self.scheduler_en_cours_d_utilisation.afficher_etat()


        




class Scheduler :
    
    def __init__(self):

        #on va démarrer le premier processus qui est init
        pr_init = Process("init.s",1,self)

        self.process_list = [pr_init]      #
        self.heure = 0                     # la clock du système 
        self.execution_en_cours = pr_init  # pid du process en cours d'exécution
    


    def run(self,fichier_de_script):     
        """
        cette fonction va créer un nouveau Process correspondant au fichier .s
        qu'on lui a fourni, l'ajouter à la process_list, l'exécuter
        """
        self.process_list.append(Process(fichier_de_script, len(self.process_list)+1,self))
        self.execution_en_cours = self.process_list[-1]
        self.execution_en_cours.execute()

    def afficher_etat(self):
        print(f"temps d'utilisation : {self.heure}, \n programmes en cours d'utilisation : {self.process_list}")


sd1 = Scheduler()


# process1 = Process("init.s",0,sd1)

# print(sd1.process_list)                      # on fait des tests
# process1.execute()
sd1.run("process_1.s")


