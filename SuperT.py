import os
import cmd
import git
import sys
import json
import shutil
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

        self.clear           = lambda : [os.system("cls") if os.name == "nt" else os.system("clear")]
        self.prompt          = "#> "
        self.mirror          = open("mirror.txt", "r").readlines()
        self.doc_header      = "Comandos documentados (escriba help <comando>):"
        self.misc_header     = "Temas de ayuda diversos:"
        self.nohelp          = "*** No hay ayuda en %s"
        self.undoc_header    = 'Comandos no documentados: ' 
        self.__hiden_methods = ['do_EOF', 'do_help']
        self.modules         = "modules"
        self.autor           = "p1ngu1n0"
        self.requiere        = json.loads(open("update.json", "r").read())
        self.Nmodules        = len([name for name in os.listdir(self.modules) if os.path.isdir(os.path.join(self.modules, name))])
        self.Ntools          = len([z for x in self.requiere.keys() for z in self.requiere[x].keys()])
        
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
                        os.chdir(os.path.join(self.modules, command.split()[1]))
                    else:
                        try:
                            subprocess.call(command, shell=True)
                        except FileNotFoundError:
                            print("***No es posible ejecutar el comando {}".format(command))
                    
            except git.exc.GitCommandError:
                print("Ya esta instalado")

        elif len(_.split()) == 1:
            for nombre, des in self.requiere[_].items():
                print("{}     {}".format(nombre, des[1]))
        
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
                os.chdir(os.path.join("modules", _))
            except FileNotFoundError:
                print("***Error en el nombre de la tool")
            tmp = dict()

            for x in self.requiere.keys():
                tmp.update(self.requiere[x])
            subprocess.call((''.join(tmp[_][3])).split(), shell=True)
        else:
            for x in [name for name in os.listdir("modules") if os.path.isdir(os.path.join("modules", name))]:
                print(x)

    def do_remove(self, _):
        "***Elimina la tool"
        if _ == "all":
            for x in os.listdir(self.modules):
                if os.path.isdir(os.path.join(self.modules, x)):
                    print("***Eliminando "+x)
                    try:
                        shutil.rmtree(os.path.join(self.modules, x))
                    except PermissionError as s:
                        print("***No es posible borrar '{0}' motivo: {1}".format(x, s))

        elif _ in [name for name in os.listdir(self.modules) if os.path.isdir(os.path.join(self.modules, name))]:
            try:
                shutil.rmtree(os.path.join(self.modules, _))
            except PermissionError as s:
                print("***No es posible borrar '{0}' motivo: {1}".format(_, s))

        else:
            for x in [name for name in os.listdir(self.modules) if os.path.isdir(os.path.join(self.modules, name))]:
                print(x)

banner = Fore.RED+r"""
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

"""

if __name__ == '__main__':
    st = SuperTool()
    print(hashlib.md5(banner.encode()).hexdigest())
    st.clear()
    if hashlib.md5(banner.encode()).hexdigest() == "c3ebf0599dc899f6c0fc0f5a605885bc":
        st.cmdloop(intro=banner.format(st.Ntools, st.Nmodules, st.autor))
    else:
        print("[Error] El Programa a sido modificado")