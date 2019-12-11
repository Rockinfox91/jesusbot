import discord

TOKEN = "MzAzMzI3MDk4NDc3NzQwMDMy.Xe-p2g.ePp-EbWI7C5_iRs9N-P4f8_jXpI"

client = discord.Client()

dictionnaire = ["Babouin","Hitler","Pomme","Poire","Prune","Pierre","Caca","Pipi","Nutella","Cafe","Staline"]

from random import randint
import math as m

def pickword(dictionnaire):    
    n = randint(0,len(dictionnaire)-1)
    mot = dictionnaire[n]
    
    compteur = 7
    nbVisible = int(len(mot)/3)
    
    listVisible = [0 for i in range(len(mot))]
    for i in range(nbVisible):
            place = randint(0,len(mot)-1)
            while listVisible[place] == 0:
                listVisible[place] = 1
    return mot,listVisible,compteur

def bonmot(list):
    for i in list:
        if i == 0:
            return False
    return True
            
def chercheplace(car,mot,listVisible,compteur):  
    A = False
    for i in range(len(listVisible)):
        if mot[i] == car.upper() or mot[i] == car.lower():
            listVisible[i] = 1
            A = True
    if A:
        if bonmot(listVisible):
            return 2,listVisible
        else:
            return 1,listVisible
    else:
        if compteur == -1:
            return -1,listVisible
        else:
            return 0,listVisible
    

def affiche(mot,listVisible,compteur):
    word = ''
    for i in range(len(listVisible)):
        if listVisible[i] == 0:
            word += ' - '
        else:
            word += ' ' + mot[i] + " "
    return ("Tentative restante : " + ":green_circle:"*(compteur+1) + ":red_circle:"*(6-compteur)+" \n\n "+ word)

#Démineur
from random import randint

def new_list(n):
    L = []
    for i in range(n):
        l = []
        for j in range(n):
            l.append(0)
        L.append(l)
    return L
    


def add_bomb(l):
    n = len(l)
    N = n**2 // 3
    for i in range(N):
        A = True
        while A:
            x = randint(0,n-1)
            y = randint(0,n-1)
            
            if l[x][y] != 'b':
                l[x][y] = 'b'
                if x!=0 and l[x-1][y] != 'b':
                    l[x-1][y] += 1
                    if y!= 0 and l[x-1][y-1] != 'b': l[x-1][y-1] += 1
                    if y != n-1 and l[x-1][y+1] != 'b': l[x-1][y+1] += 1
                if x!=n-1 and l[x+1][y] != 'b':
                    l[x+1][y] += 1
                    if y != 0 and l[x+1][y-1] != 'b': l[x+1][y-1] += 1
                    if y != n-1 and l[x+1][y+1] != 'b': l[x+1][y+1] += 1
                if y!=0 and l[x][y-1] != 'b':
                    l[x][y-1] += 1
                if y!=n-1 and l[x][y+1] != 'b':
                    l[x][y+1] += 1
                A = False
    return  l
    
def to_discordMessage(blist):
    message = ""
    for i in blist:
        for j in i:
            message += "||"
            if j == 0:
                message += ":zero:"
            if j == 1:
                message += ":one:"
            if j == 2:
                message += ":two:"
            if j == 3:
                message += ":three:"
            if j == 4:
                message += ":four:"
            if j == 5:
                message += ":five:"
            if j == 6:
                message += ":six:"
            if j == 7:
                message += ":seven:"
            if j == 8:
                message += ":eight:"
            if j == 'b':
                message += ":boom:"
            message += "||"
        message += "\n"
    return message

#general

trouveactif = False
PenduActivate = False
mot = ''
listVisible = []
compteur = 0

@client.event
async def on_message(message):
    global PenduActivate
    global trouveactif
    global mot
    global listVisible
    global compteur
    # we do not want the bot to reply to itself
    
    
    if message.author == client.user:
        return
    
    if message.content.startswith('?stop'): #Mettre les variable bool à éteindre pour redémarer
        await message.channel.send("okayyyy")
        trouveactif = False
        PenduActivate = False
    
    if message.content.startswith('?help'):
        await message.channel.send("Rejoins moi en DM mon coquin :see_no_evil::ok_hand:")
        await message.author.send("Je ne peux pas encore faire énormément de chose à part marcher sur l'eau et passer la nuit avec des petits garçon :hugging: Pour le moment je peux :\n - Jouer au pendu avec toi avec ?pendu. Si tu veux rajouter un mot fait ?pendu add [mot]\n - Jouer au démineur avec ?démineur [taille liste]\n - Jouer au devine quel nombre avec ?devine")
        
        
        
    if message.content.startswith('?pendu'):
        if not PenduActivate and not trouveactif:
            mot,listVisible,compteur = pickword(dico("dico_pendu.txt"))
            await message.channel.send("Très bien, le seigneur a choisi un mot et vous devez le trouver à l'aide du PENDUUUUUU, vous avez 7 vies.\n Pour répondre envoyez ?pendu [lettre].")
            PenduActivate = True
            await message.channel.send(affiche(mot,listVisible,compteur))

        elif PenduActivate and not trouveactif:
            a,listVisible = chercheplace(message.content[7],mot,listVisible,compteur)
            if a == 0:
                await message.channel.send("Eh non ce n'est pas la bonne lettre, retente :)")
                compteur -= 1
                await message.channel.send(affiche(mot,listVisible,compteur))
            if a == -1:
                await message.channel.send("C'est perdu !! Désolé tu vas aller en enfer")
                PenduActivate = False
                mot = ''
                listVisible = []
                compteur = 0
            if a == 1:
                await message.channel.send("Bien joué {0}, tu a trouvé une lettre!".format(message.author.mention))
                await message.channel.send(affiche(mot,listVisible,compteur))
            if a == 2:
                await message.channel.send("{0} TU AS GAGNÉ BRAVO !!! :clap::clap: Tu vas au paradis mon ami".format(message.author.mention))
                PenduActivate = False
                mot = ''
                listVisible = []
                compteur = 0
        
        
        
    if message.content.startswith("?démineur") and not PenduActivate:
        if len(message.content) <= 9:
            await message.channel.send("Il me manque la taille de la liste ! Si tu as besoin d'aide tape ?help")
        n = int(message.content[10:])
        if n < 14:
            msg = to_discordMessage(add_bomb(new_list(n)))
            await message.channel.send("Qui mieux que l'église pour te donner des mineurs :ok_hand::tongue:")
            await message.channel.send(msg)
        else:
            await message.channel.send("walah j'en ai pa autan gro")
            
            
            
            
    if message.content.startswith('?trouve') and not PenduActivate:
        global nbr
        nbr = randint(0,50)
        await message.channel.send("Le saint dieu a un nombre entre un et 50 en tête et tu dois le deviner :smiling_imp:")
        trouveactif = True
        
        
        
    if trouveactif and not PenduActivate:
        msg = int(message.content)
        if msg > nbr:
            await message.channel.send("Trop grand mon chou")
        if msg < nbr:
            await message.channel.send("Trop petit bébé")
        if msg == nbr:
            await message.channel.send("WOW BRAVO :scream::eggplant::sweat_drops:")
            trouveactif = False
            
    
     
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)



    
