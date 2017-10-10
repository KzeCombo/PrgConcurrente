from tkinter import *
from threading import Thread, RLock
from random import *
from math import *
import time


#importation des bibliotheque
largeur=500
hauteur=500
taille=((largeur+hauteur)/20) #taille de la balle


#liste de toute les couleurs disponibles
color=['snow', 'ghost white', 'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'old lace',
    'linen', 'antique white', 'papaya whip','LavenderBlush2', 'LavenderBlush3',
    'LavenderBlush4', 'blanched almond', 'bisque','DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'peach puff']
#Class Ball
class ball(object):
	liste=list()
	def __init__(self,name,x,y,col=choice(color)):
		ball.liste.append(self)
		self.name = name
		self.x = x
		self.y = y
		self.col=col
		self.dirx=randint(-1,0)
		self.diry=randint(-1,0)
		if self.dirx==0:self.dirx=1
		if self.diry==0:self.diry=1

class calcul(Thread):
	do=True #boolean qui gere la boucle de calcul
	def __init__(self):
		Thread.__init__(self)
		self.daemon=True
	def run(self):
		while 1:
			self.do=affichage.do
			if self.do:
				#pour chaque balle dans la liste, deplacer les balles
				for i in ball.liste:
					i.x+=i.dirx
					i.y+=i.diry
					#si la balle touche un bord, inverser sa direction
					if i.x<=0 or i.x>=largeur-taille:
						i.dirx=-i.dirx
					if i.y<=0 or i.y>=hauteur-taille:
						i.diry=-i.diry
					for element in ball.liste:
						if element!=i:
							affichage.x.collision(element,i)
			time.sleep(0.01)


#thread pour la fenetre
class affichage(Thread):
	x=None
	nb=0 #nombre de balle
	score = 0 #score
	do=True
	
	def __init__(self):
		Thread.__init__(self)
		self.fenetre=Tk()
		affichage.x=self
		self.daemon=True 		
		self.temps=0
		self.recall=0
		#texte nombre de balle
		self.nb_ball=Label(self.fenetre,text="nombre de balle: {}".format(self.nb))
		self.nb_ball.pack()

		self.n_score=Label(self.fenetre,text="score: {}".format(self.score))
		self.n_score.pack() 

		self.temps=Label(self.fenetre,text="temps: {}".format(self.temps))
		self.temps.pack()
	    
		self.canvas = Canvas(self.fenetre, width=largeur, height=hauteur, background='white')
		self.canvas.pack()
		
		self.bouton_quitter = Button(self.fenetre, text="Quitter", command=self.close)
		self.bouton_quitter.pack(side="bottom")
		
		self.Frame_balle=Frame(self.fenetre, borderwidth=2, relief=GROOVE)
		self.Frame_balle.pack()

		#boutton ajout
		self.ajout= Button(self.Frame_balle,text="+",command=self.ajout)
		self.ajout.pack(side=LEFT)
		#boutton retirer
		self.retrait= Button(self.Frame_balle,text="-",command=self.retrait)
		self.retrait.pack(side=RIGHT)
		#boutton pause
		self.pause= Button(self.fenetre,text="STOP",command=self.pause)
		self.pause.pack()

	# thread pour actualiser la fenetre
	def run(self):
		while 1:
			temps=int(time.clock())-self.recall
			for i in ball.liste: 
				self.canvas.coords(i.name,i.x+i.dirx,i.y+i.diry,i.x+i.dirx+taille,i.y+i.diry+taille)
			#actualisation des textes
			self.nb_ball["text"]=("nombre de balle: {}".format(affichage.nb))
			self.n_score["text"]=("score: {}".format(affichage.score))
			#controle du timer
			if affichage.do:
				self.temps["text"]=("temps: {}".format(temps))
			else:
				self.recall=int(time.clock())-temps

	#fonction qui active ou desactive le thread de calcul
	def pause(self):
		if affichage.do:
			affichage.do=False
			self.pause["text"]=("START")
		else:
			affichage.do=True
			self.pause["text"]=("STOP")

	#fonction qui ajoute les balles
	def ajout(self):
		if self.nb<5:
			x=randint(taille,hauteur-taille)
			y=randint(taille,largeur-taille)
			col=choice(color)
			name=self.canvas.create_oval(x,y,x+taille,y+taille,fill=col)
			ball(name,x,y,col)
			affichage.nb+=1
			self.nb_ball["text"]=("nombre de balle: {}".format(self.nb))
	
	#fonction qui retire la balles
	def retrait(self):
		if ball.liste!=[]:
			supp=self.canvas.find_all()
			self.canvas.delete(supp[len(supp)-1])
			ball.liste.pop(len(ball.liste)-1)
			affichage.nb-=1
			self.nb_ball["text"]=("nombre de balle: {}".format(self.nb))

	#fonction qui gere les collisions
	def collision(self,p,q):
		x=q.x-p.x
		y=q.y-p.y
		dist=x*x+y*y

		if (sqrt(dist))<=(taille):
			affichage.nb-=2
			affichage.score+=2
			ball.liste.remove(p)
			ball.liste.remove(q)
			self.canvas.delete(p.name)
			self.canvas.delete(q.name)

	#fonction qui ferme la fenetre
	def close(self):
		self.fenetre.quit()



#lancement du programme
main=affichage()
main.start()
c=calcul()
c.start()
main.fenetre.mainloop()
