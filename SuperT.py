import os
import cmd
import git
import sys
import json
import shutil
import random
import base64
import hashlib
import requests
import subprocess
from colorama import Fore, Style
from progress.bar import FillingCirclesBar

if not os.path.exists("update.json"):
    with open("update.json", "w+") as f:
        f.write("{}")
        print("***Archivo 'update.json' creado !")

class SuperTool(cmd.Cmd):
    def __init__(self):
        "Funcion de invocacion"
        cmd.Cmd.__init__(self)

        try:
            os.stat("modules")
        except:
            os.mkdir("modules")

        self.banner          = "{3}"+r"""
                                ___________           .__   
  ________ ________   __________\__    ___/___   ____ |  |  
 /  ___/  |  \____ \_/ __ \_  __ \|    | /  _ \ /  _ \|  |  
 \___ \|  |  /  |_> >  ___/|  | \/|    |(  <_> |  <_> )  |__
/____  >____/|   __/ \___  >__|   |____| \____/ \____/|____/
     \/      |__|        \/                                     
"""+Fore.RESET+""" 
        -------)   Tools disponibles: {0}  (------
        -------)   Tools instaladas:  {1}  (------
        -------)   Autor: {2}       (------
{4}
"""

        self.clear           = lambda : [os.system("cls") if os.name == "nt" else os.system("clear")]
        self.ruta            = os.getcwd()
        self.prompt          = "#> "
        self.mirror          = open("mirror.txt", "r").readlines()
        self.doc_header      = "Comandos documentados (escriba help <comando>):"
        self.misc_header     = "Temas de ayuda diversos:"
        self.nohelp          = "***No hay ayuda en %s"
        self.undoc_header    = 'Comandos no documentados: ' 
        self.__hiden_methods = ['do_EOF', 'do_help']
        self.modules         = "modules"
        self.autor           = "p1ngu1n0"
        self.requiere        = json.loads(open("update.json", "r").read())
        self.Nmodules        = len([name for name in os.listdir(self.modules) if os.path.isdir(os.path.join(self.ruta, self.modules, name))])
        self.Ntools          = len([z for x in self.requiere.keys() for z in self.requiere[x].keys()])
        self.hash            = hashlib.md5(self.banner.encode()).hexdigest()
        self.intro           = self.banner.format(self.Ntools, self.Nmodules, self.autor, random.choice([Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW]), "\n      Comandos documentados (escriba help <comando>): \n      ===============================================\n         clear  exit  install  remove  run  update  ")
        
        
        
    def emptyline(self):
        self.do_help("")

    def default(self, _):
        "hola"
        print("***Comando '%s' no valido" % _)

    def get_names(self):
        return [n for n in dir(self.__class__) if n not in self.__hiden_methods]

    def do_exit(self, s):
        "***Salir del programa"
        self.clear()
        sys.exit(1)

    def do_clear(self, s):
        "***Limpia la pantalla"
        self.clear()
        print(self.intro)
    
    def do_EOF(self, arg):
        "crtl+z"
        return True
    
    def do_install(self, _):
        "***Instalar tool"

        if len(_.split()) == 2:
            categoria, nombre = _.split()
            try:
                
                git.Git("modules").clone(self.requiere[categoria][nombre][0])
                
                for command in self.requiere[categoria][nombre][2]:
                    if command.split()[0] == "cd":
                        os.chdir(os.path.join(self.ruta, self.modules, command.split()[1]))
                    else:
                        try:
                            subprocess.call(command, shell=True)
                        except FileNotFoundError:
                            print("***No es posible ejecutar el comando {}".format(command))
                    
            except git.exc.GitCommandError:
                print("Ya esta instalado")

            except KeyError as s:
                print("***Error en el nombre de la tool {}".format(s))

        elif len(_.split()) == 1:
            try:
                for nombre, des in self.requiere[_].items():
                    print("{}     {}".format(nombre, des[1]))
            except KeyError as s:
                print("***Error en la categoria '{}'".format(s))
        
        else:
            for x in self.requiere.keys():
                print(x)
    
    def do_update(self, _):
        "***Actualiza las tools"
        resultado = dict()
        for x in open("mirror.txt", "r").readlines():
            print(x)
            resultado.update(json.loads((requests.get(x+".json").content).decode()))

        bar = FillingCirclesBar('Actualizando', max=len(resultado))
        for i in range(len(resultado)):
            with open('update.json', 'w') as upt:
                json.dump(resultado, upt)
                bar.next()
        bar.finish()
        self.requiere = json.loads(open("update.json", "r").read())
    

    def do_run(self, _):
        "***Ejecuta la tool seleccionada"
        if _:
            try:
                os.chdir(os.path.join(self.ruta, self.modules, _))
            except FileNotFoundError:
                print("***Error en el nombre de la tool")
            tmp = dict()

            for x in self.requiere.keys():
                tmp.update(self.requiere[x])
            try:
                subprocess.call((''.join(tmp[_][3])).split(), shell=True)
            except KeyError as s:
                print("***No se puede ejecutar 'comandos' motivo: {}".format(_, s))
        else:
            for x in [name for name in os.listdir("modules") if os.path.isdir(os.path.join(self.ruta, self.modules, name))]:
                print(x)

    def do_remove(self, _):
        "***Elimina la tool [Nombre|all]"
        if _ == "all":
            for x in os.listdir(self.modules):
                if os.path.isdir(os.path.join(self.ruta, self.modules, x)):
                    print("***Eliminando "+x)
                    try:
                        shutil.rmtree(os.path.join(self.ruta, self.modules, x))
                    except PermissionError as s:
                        print("***No es posible borrar '{0}' motivo: {1}".format(x, s))

        elif _ in [name for name in os.listdir(self.modules) if os.path.isdir(os.path.join(self.ruta, self.modules, name))]:
            try:
                shutil.rmtree(os.path.join(self.ruta, self.modules, _))
            except PermissionError as s:
                print("***No es posible borrar '{0}' motivo: {1}".format(_, s))

        else:
            for x in [name for name in os.listdir(self.modules) if os.path.isdir(os.path.join(self.ruta, self.modules, name))]:
                print(x)

if __name__ == '__main__':
    st = SuperTool()
    st.clear()
    if st.hash == "5cd295eb11b836ffdf5cc125ab4e4b84":

        st.cmdloop()
    else:
        print("[Error] El Programa a sido modificado")