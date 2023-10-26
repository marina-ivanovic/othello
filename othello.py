import copy
import time
import math

CRNI = "B"
BELI = "W"
MOGUCI = "*"

X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
PRAVCI = [[0,1], [1,0], [1,1], [-1,0], [0,-1], [-1,-1], [1,-1], [-1,1]]

#POMOCNE METODE

def naTabli(x,y):
    return 0<=x<8 and 0<=y<8

def proveraPoteza(tabla, token, xpoteza, ypoteza):
    if not naTabli(xpoteza,ypoteza):
        return False
    
    if tabla[xpoteza][ypoteza]=="*":
        tabla[xpoteza][ypoteza]="-"
    
    if tabla[xpoteza][ypoteza]!="-":
        return False
    
    if token == "B": protivnik ="W"
    else: protivnik = "B"
    tokeniZaOkretanje = []

    for koordinate in PRAVCI:
        xpravac = koordinate[0]
        ypravac = koordinate[1]

        x = xpoteza+xpravac
        y = ypoteza+ypravac

        if naTabli(x,y) and tabla[x][y] == protivnik:
            x += xpravac
            y += ypravac

            while naTabli(x,y) and tabla[x][y] == protivnik:
                x += xpravac
                y += ypravac
                if not naTabli(x,y) or tabla[x][y] == token:
                    break
            if not naTabli(x,y):
                continue
            if tabla[x][y] == token:
                while True:
                    x -= xpravac
                    y -= ypravac
                    if x==xpoteza and y==ypoteza:
                        break
                    tokeniZaOkretanje.append([x,y])

    if len(tokeniZaOkretanje)==0:
        return False
    return tokeniZaOkretanje
            
def dozvoljeniPotezi(tabla, token):
    dozvoljeniPotezi = []
    for x in range(8):
        for y in range(8):
            if proveraPoteza(tabla,token,x,y) != False:
                dozvoljeniPotezi.append([x,y])
    return dozvoljeniPotezi

def postaviToken(tabla, igrac, potez):
    x = potez[0]
    y = potez[1]
    tokeniZaOkretanje = proveraPoteza(tabla,igrac,x,y)
    tabla[x][y] = igrac
    if igrac!=MOGUCI:
        for token in tokeniZaOkretanje:
            tabla[token[0]][token[1]] = igrac

#HEURISTIKA

def dynamic_heuristic_evaluation_function(grid, my_color, opp_color):
    my_tiles = opp_tiles = my_front_tiles = opp_front_tiles = 0
    p = c = l = m = f = d = 0

    V = [
        [20, -3, 11, 8, 8, 11, -3, 20],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [20, -3, 11, 8, 8, 11, -3, 20]
    ]

    for i in range(8):
        for j in range(8):
            if grid[i][j] == my_color:
                d += V[i][j]
                my_tiles += 1
            elif grid[i][j] == opp_color:
                d -= V[i][j]
                opp_tiles += 1
            if grid[i][j] != '-':
                for k in range(8):
                    x = i + X1[k]
                    y = j + Y1[k]
                    if 0 <= x < 8 and 0 <= y < 8 and grid[x][y] == '-':
                        if grid[i][j] == my_color:
                            my_front_tiles += 1
                        else:
                            opp_front_tiles += 1
                        break

    if my_tiles > opp_tiles:
        p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
        p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
    else: p=0

    if my_front_tiles > opp_front_tiles:
        f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
    elif my_front_tiles < opp_front_tiles:
        f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
    else: f=0

    my_tiles = opp_tiles = 0

    if grid[0][0] == my_color: my_tiles += 1
    elif grid[0][0] == opp_color: opp_tiles += 1

    if grid[0][7] == my_color: my_tiles += 1
    elif grid[0][7] == opp_color: opp_tiles += 1

    if grid[7][0] == my_color: my_tiles += 1
    elif grid[7][0] == opp_color: opp_tiles += 1

    if grid[7][7] == my_color: my_tiles += 1
    elif grid[7][7] == opp_color: opp_tiles += 1

    c = 25 * (my_tiles - opp_tiles)

    my_tiles = opp_tiles = 0
    if grid[0][0] == '-':
        if grid[0][1] == my_color: my_tiles += 1
        elif grid[0][1] == opp_color: opp_tiles += 1

        if grid[1][1] == my_color: my_tiles += 1
        elif grid[1][1] == opp_color: opp_tiles += 1
       
        if grid[1][0] == my_color: my_tiles += 1
        elif grid[1][0] == opp_color: opp_tiles += 1

    if grid[0][7] == '-':
        if grid[0][6] == my_color: my_tiles += 1
        elif grid[0][6] == opp_color: opp_tiles += 1

        if grid[1][6] == my_color: my_tiles += 1
        elif grid[1][6] == opp_color: opp_tiles += 1

        if grid[1][7] == my_color: my_tiles += 1
        elif grid[1][7] == opp_color: opp_tiles += 1

    if grid[7][0] == '-':
        if grid[7][1] == my_color:  my_tiles += 1
        elif grid[7][1] == opp_color: opp_tiles += 1
        
        if grid[6][1] == my_color: my_tiles += 1
        elif grid[6][1] == opp_color: opp_tiles += 1
        
        if grid[6][0] == my_color: my_tiles += 1
        elif grid[6][0] == opp_color: opp_tiles += 1
    
    if grid[7][7] == '-':
        if grid[6][7] == my_color: my_tiles += 1
        elif grid[6][7] == opp_color: opp_tiles += 1
        
        if grid[6][6] == my_color: my_tiles += 1
        elif grid[6][6] == opp_color: opp_tiles += 1
        
        if grid[7][6] == my_color: my_tiles += 1
        elif grid[7][6] == opp_color: opp_tiles += 1
    
    l = -12.5 * (my_tiles - opp_tiles)

    num_valid_moves_crni = len(dozvoljeniPotezi(grid, CRNI))
    num_valid_moves_beli = len(dozvoljeniPotezi(grid, BELI))

    my_tiles = num_valid_moves_crni
    opp_tiles = num_valid_moves_beli
    
    if my_tiles > opp_tiles:
        m = (100.0 * my_tiles) / (my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
        m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
    else: m = 0

    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
    return score

class Kompjuter:
    def __init__(self, tabla):
        self._tabla = tabla
        self._scoreovi = {} #hashmapa

    def potezKompjutera(self, tabla, dubina, alpha, beta, igrac, vreme):
        probnaTabla = copy.deepcopy(tabla)
        dozvoljeni = dozvoljeniPotezi(probnaTabla, igrac)
        if dubina == 0 or len(dozvoljeni) == 0 or time.time()-vreme>3:
            najboljiPotez, score = None, dynamic_heuristic_evaluation_function(tabla, BELI, CRNI)
            self._scoreovi[str(probnaTabla)] = score
            return najboljiPotez, score
        #maximizer
        if igrac==BELI:
            najboljiScore = -math.inf
            najboljiPotez = None

            for potez in dozvoljeni:
                postaviToken(probnaTabla, igrac, potez)
                if str(probnaTabla) in self._scoreovi:
                    vrednost = self._scoreovi[str(probnaTabla)]
                else:
                    sledeciPotez, vrednost = self.potezKompjutera(probnaTabla, dubina-1, alpha, beta, CRNI,vreme)
                    self._scoreovi[str(probnaTabla)] = vrednost

                if vrednost > najboljiScore:
                    najboljiScore = vrednost
                    najboljiPotez = potez
                alpha = max(alpha, najboljiScore)
                if beta <= alpha:
                    break

                probnaTabla = copy.deepcopy(tabla)
            return najboljiPotez, najboljiScore
        #minimizer
        if igrac==CRNI:
            najboljiScore = math.inf
            najboljiPotez = None

            for potez in dozvoljeni:
                postaviToken(probnaTabla, igrac, potez)
                if str(probnaTabla) in self._scoreovi:
                    vrednost = self._scoreovi[str(probnaTabla)]
                else:
                    sledeciPotez, vrednost = self.potezKompjutera(probnaTabla, dubina-1, alpha, beta, BELI,vreme)
                    self._scoreovi[str(probnaTabla)] = vrednost

                if vrednost < najboljiScore:
                    najboljiScore = vrednost
                    najboljiPotez = potez

                beta = min(beta, najboljiScore)
                if beta <= alpha:
                    break

                probnaTabla = copy.deepcopy(tabla)
            return najboljiPotez, najboljiScore

class Table:
    def __init__(self):
        #Inicijalizacija/pocetno stanje table
        tabla = []
        for x in range(8):
            tabla.append([""]*8)
            for y in range(8):
                tabla[x][y] = "-"

        self._tabla = tabla

        self._tabla[3][4]=self._tabla[4][3]="B"
        self._tabla[3][3]=self._tabla[4][4]="W"

        if dozvoljeniPotezi(self._tabla, CRNI)!=[]:
            for potez in dozvoljeniPotezi(self._tabla, CRNI):
                postaviToken(self._tabla, MOGUCI, potez)
        
    def ispisTable(self):
        print()
        print('  | A | B | C | D | E | F | G | H |')
        for i in range(len(self._tabla)):
            line = str(i+1)+" | "
            row = self._tabla[i]
            for item in row:
                line += str(item)+" | "
            print(line+str(i+1))
        print()

class Igra:
    def __init__(self):
        self._tabla = Table()
        self._kompjuter = Kompjuter(self._tabla._tabla)
        self._poeni1 = self._poeni2 = 2    

    def azurirajTablu(self):
        self._tabla.ispisTable()
        print("BROJ POENA: "+str(self._poeni1)+"          PROTIVNIK: "+str(self._poeni2))
    
    def igracIgra(self):
        dozvoljeno=dozvoljeniPotezi(self._tabla._tabla, CRNI)
        for potez in dozvoljeniPotezi(self._tabla._tabla, CRNI):
            postaviToken(self._tabla._tabla, MOGUCI, potez)
        self.azurirajTablu()
        odabir = input("Vi ste igrac B. Izaberite neko od označenih polja u obliku slovo pa broj (npr. A1): ")

        try:
            red = int(odabir[1])-1
            kolona = ord(odabir[0].capitalize())-65
            if [red,kolona] in dozvoljeno:
                tokeniZaOkretanje = proveraPoteza(self._tabla._tabla, CRNI, red, kolona)
                postaviToken(self._tabla._tabla, CRNI, [red,kolona])
                poeni = len(tokeniZaOkretanje)
                self._poeni1+=poeni+1
                self._poeni2-=poeni
                return False
            else:
                raise Exception()
        except:
            print("Potez koji ste izabrali nije dozvoljen.")
            time.sleep(1)
            

    def kompjuterIgra(self):
        self.azurirajTablu()
        print("Kompjuter razmislja...")
        vreme = time.time()
        dubina = 5
        if len(dozvoljeniPotezi(self._tabla._tabla, BELI))>8:
            dubina = 4
        elif len(dozvoljeniPotezi(self._tabla._tabla, BELI))<5:
            dubina = 6
        potez, score = self._kompjuter.potezKompjutera(self._tabla._tabla, dubina,-math.inf,math.inf,BELI, vreme)
        tokeniZaOkretanje = proveraPoteza(self._tabla._tabla, BELI, potez[0], potez[1])
        postaviToken(self._tabla._tabla, BELI, potez)
        poeni = len(tokeniZaOkretanje)
        self._poeni2+=poeni+1
        self._poeni1-=poeni
        print("Odigrano za "+str(time.time()-vreme)+"s")
        print("------------------------------------------------------")




if __name__=='__main__':
    print("---------------OTHELLO----------------")
    othello = Igra()
    igrac = CRNI
    while True:
        if othello._poeni1==0 or othello._poeni2==0 or othello._poeni1+othello._poeni2==64:
            break
        if igrac==CRNI:
            if dozvoljeniPotezi(othello._tabla._tabla, CRNI)==[]:
                break
            while True:
                if othello.igracIgra()==False:
                    break
            igrac = BELI
        elif igrac == BELI:
            if dozvoljeniPotezi(othello._tabla._tabla,BELI)==[]:
                break
            othello.kompjuterIgra()
            igrac = CRNI
    othello.azurirajTablu()
    print("==========================================")
    print("Igra je gotova.")
    if(othello._poeni1>othello._poeni2) or (dozvoljeniPotezi(othello._tabla._tabla,BELI)==[] and othello._poeni1+othello._poeni2!=64):
        if dozvoljeniPotezi(othello._tabla._tabla,BELI)==[] and othello._poeni1+othello._poeni2!=64:
            print("Kompjuter nema vise poteza")
        print("Čestitamo! Pobedili ste sa rezultatom "+str(othello._poeni1)+":"+str(othello._poeni2))

    elif(othello._poeni1<othello._poeni2) or (dozvoljeniPotezi(othello._tabla._tabla,CRNI)==[] and othello._poeni1+othello._poeni2!=64):
        if dozvoljeniPotezi(othello._tabla._tabla,CRNI)==[] and othello._poeni1+othello._poeni2!=64:
            print("Nemate vise poteza")
        print("Izgubili ste. Rezultat:  "+str(othello._poeni1)+":"+str(othello._poeni2))

    else: print("Nerešeno: "+str(othello._poeni1)+":"+str(othello._poeni2))