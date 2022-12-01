import pandas as pd
from git import Repo

import re, signal, sys, time
from progress.bar import Bar

import json

def handler_signal(signal, frame):

    print('You pressed Ctrl+C!')
    sys.exit(0)


#¿Por qué no se puede hacer un main?
#Asigno la señal de interrupción a la función handler_signal para que se ejecute cuando se pulse Ctrl+C
signal.signal(signal.SIGINT, handler_signal)

REPO_DIR = "./skale-manager"


def extract(url):
    repo = Repo(url) # Clono el repositorio
    commits = list(repo.iter_commits('HEAD'))  #Es una lista con objetos commit (el mensaje, la fecha, ect)
    return commits


def transform(commits):
    
    lista = [] #Lista donde se van a guardar los commits

    barra = Bar('Cargando', max=len(commits)) #Barra de progreso

    #Itero en los commits y busco palabras clave en el mensaje
    for commit in commits:
        clave = re.findall('pass|key|KEY|secret|token|password|pwd|private|PRIVATE|priv|auth|cred|credencial', commit.message, re.IGNORECASE)
        #Si encuentra alguna palabra clave, la añade a la lista junto con el mensaje
        if clave:
            lista.append([clave, commit])
        barra.next()
    barra.finish()
    return lista

def load(lista_datos):
    
    archivo = {}
    for registro in lista_datos:
        archivo[f"{registro[1]}"] = registro[0],

    

    #Guardo el archivo json
    with open('datos_json.json', 'w') as file:
        json.dump(archivo, file, indent=4)
    

if __name__ == '__main__':

    c = extract(REPO_DIR)

    l = transform(c)

    print('\n')

    load(l)
    
    sys.exit(0)