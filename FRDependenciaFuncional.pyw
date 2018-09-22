# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 02:24:11 2018

@author: Cristhiam Reina
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic

#Clase que hereda de QMainWindow (Constructor de ventanas)
class Ventana(QMainWindow):
    #Metodo Constructor de la clase
    def __init__(self):
        #Se declaran los arreglos L (Conjunto) y R (Dependencias)
        self.limpiarVariables()
        
        QMainWindow.__init__(self)
        #Cargar la configuracion del archivo .ui en el objeto
        uic.loadUi("FRDependenciaFuncional.ui",self)
        self.analizaJson.clicked.connect(self.validar_json)
        
    def limpiarVariables(self):
        self.L = []
        self.T = []
        self.dependencias_elementales = []
        self.extranos = []
        self.dependenciasPaso2 = []
        self.dependenciasPaso3 = []
        self.redundantes = []
        self.m2 = []
        self.sFomaNormal = []
        self.dependenciaSredundancia = []
        self.dependenciaTransformada = []
        self.segundaForma = []
    def ordenarCadena(self, cadena):
        listTemp = []
        
        for elemento in cadena:
            if elemento != " ":
                listTemp.append(elemento)
            
        listTemp.sort()
        
        return "".join(listTemp)
    def validar_json(self):
        #Se recoje el json del campo     
        conjuntoText = self.conjuntoText.text()
        dependenciaText = self.dependenciasText.text()
        
        self.limpiarVariables()
        #Se valida que el campo no se encuentra vacio
        if conjuntoText.strip(" ") == "" or dependenciaText.strip(" ") == "":
            QMessageBox.information(self, "Error", "El campo 'conjunto' o el campo 'dependencias funcionales, se encuentran vacios, por favor ingrese la informacion e intente de nuevo!", QMessageBox.Discard)
            self.textEdit.setText("")
        else:
            
            
            conjuntoList = conjuntoText.split(",")
            
            for text in conjuntoList:
                text = text.strip(" ")
                if text != "":
                    self.L.append(text)
                    
            
            dependenciasList = dependenciaText.split(",")
            
            for dependencia in dependenciasList:
                dependenciaList = dependencia.split("->")
                implicante = dependenciaList[0]
                implicado = dependenciaList[1]
                
                implicante = implicante.strip(" ")
                implicado = implicado.strip(" ")
                
                dep = []
                dep.append(implicante)
                dep.append(implicado)
                
                self.T.append(dep)
                

            result = ""
            
            banderaComa = True;
            result = result + '\n' + "Conjunto de todos los elementos (T): {"
            for elemento in self.L:
                coma = ", ";
                
                if banderaComa:
                    coma = ""
                    
                result = result + coma + " " + elemento
                banderaComa = False
            result = result + "}"
            
            banderaComa = True;
            result = result + '\n' + "Dependencias Funcionales ingresadas (L): {"
            for elemento in self.T:
                
                coma = ", ";
                
                if banderaComa:
                    coma = ""
                    
                result = result + coma + " " + elemento[0] + "->" + elemento[1]
                banderaComa = False
            result = result + "}"
            
            self.encuentraDFElementales()
            
            banderaComa = True;
            result = result + '\n' + "Dependencias elementales: {"
            for elemento in self.dependencias_elementales:
                
                coma = ", ";
                
                if banderaComa:
                    coma = ""
                    
                result = result + coma + " " + elemento[0] + "->" + elemento[1]
                banderaComa = False
            result = result + " }"
                
            
            self.encuentraRedundantes()
            
            result = result + '\n' + "Dependencias paso 2 (Quitar redundancia): {"
            banderaComa = True
            for elemento in self.dependenciasPaso2:
                coma = ", ";
                
                if banderaComa:
                    coma = ""
                    
                result = result + coma + " " + elemento[0] + "->" + elemento[1]
                banderaComa = False
            result = result + "}"
                
            
            
            self.eliminaDependencias()
            
            result = result + '\n' + "Dependencias paso 3 (Eliminacion): {"
            banderaComa = True
            for elemento in self.dependenciasPaso3:

                coma = ",";
                
                if banderaComa:
                    coma = ""
                    
                result = result + coma + " " + elemento[0] + "->" + elemento[1]
                banderaComa = False
            result = result + "}"
                
            self.calcularClaves()
            
            result = result + '\n' + "Calculo de claves: {"
            banderaComa = True
            
            for elemento in self.m2:

                coma = ",";
                
                if banderaComa:
                    coma = ""
                    
                result = result + coma + " " + elemento
                banderaComa = False
            result = result + "}"
                
                
            """self.esSegundaForma()    
            
            result = result + '\n' + "Segunda forma normal: {"
            banderaComa = True
            
            for elemento in self.segundaForma:

                coma = ", ";
                
                if banderaComa:
                    coma = ""
                    
                result = result + coma + " " + elemento[0] + ":" + elemento[1]
                banderaComa = False
            result = result + "}"""
                
            
            self.textEdit.setText(result)
            
    
    def insertaElementales(self, dep_temp1):
        bandera = True
        for dep in self.dependencias_elementales:
            if dep_temp1[0] == dep[0] and dep_temp1[1] == dep[1]:
                bandera = False
                break
            
        if bandera:
            self.dependencias_elementales.append(dep_temp1)
    def encuentraDFElementales(self):
        for dependencia in self.T:
            implicante = dependencia[0]
            implicado = dependencia[1]

            if len(implicado) > 1:
                for ca in implicado:
                    dependencia_resultante = []
                    dependencia_resultante.append(implicante)
                    dependencia_resultante.append(ca)
                    self.insertaElementales(dependencia_resultante)
            else:  
                dependencia_resultante = []
                dependencia_resultante.append(implicante)
                dependencia_resultante.append(implicado)
                self.insertaElementales(dependencia_resultante)
    
        
    def calcularCierre(self, descriptor_busqueda, dependencia_evaluacion):
        agregar = []
        combinaciones = self.combinaciones(descriptor_busqueda)
        for com in combinaciones:
            for dependencia in self.dependencias_elementales:
                if  not (dependencia_evaluacion[0] == dependencia[0] and dependencia_evaluacion[1] == dependencia[1]):
                    
                    if dependencia[0] == com and dependencia[1] == dependencia_evaluacion[1] and len(dependencia[0]) < len(dependencia_evaluacion[0]):
                        nuevo_implicante = com
                        nuevo_implicado = dependencia_evaluacion[1]
                        dependencia_evaluacion = []
                        dependencia_evaluacion.append(nuevo_implicante)
                        dependencia_evaluacion.append(nuevo_implicado)
                    if com == dependencia[0]:
                        if dependencia_evaluacion[0].find(com) != -1:
                            nuevo_implicante = dependencia_evaluacion[0]
                            nuevo_implicante = dependencia_evaluacion[0].replace(dependencia[1], "")
                            nuevo_implicado = dependencia_evaluacion[1]
                            dependencia_evaluacion = []
                            dependencia_evaluacion.append(nuevo_implicante)
                            dependencia_evaluacion.append(nuevo_implicado)
                
                        if dependencia_evaluacion[0].find(com) -1:
                            agregar.append(dependencia[1])

        
        self.dependenciaTransformada = dependencia_evaluacion
        
        bandera = False
        for a in agregar:
            if descriptor_busqueda.find(a) == -1:
                bandera = True
                descriptor_busqueda = self.ordenarCadena(descriptor_busqueda + a)
        
       
        if bandera:
            descriptor_busqueda = self.calcularCierre(descriptor_busqueda, dependencia_evaluacion)
        
        descriptor_busqueda = self.ordenarCadena(descriptor_busqueda)
        return descriptor_busqueda
            
    
    def insertaPaso2(self, dependencia):
        bandera = True
        
        for dep_actual in self.dependenciasPaso2:
            if dependencia[0] == dep_actual[0] and dependencia[1] == dep_actual[1]:
                bandera = False
        
        if bandera:
            self.dependenciasPaso2.append(dependencia)
    def encuentraRedundantes(self):
        for dependencia in self.dependencias_elementales:
            implicante = dependencia[0]
            implicado = dependencia[1]
            
            dependencia_resultante = []
            if len(implicante) > 1:
                self.calcularCierre(implicante, dependencia)                
                self.insertaPaso2(self.dependenciaTransformada)
            else:
                dependencia_resultante.append(implicante)
                dependencia_resultante.append(implicado)
                self.insertaPaso2(dependencia_resultante)
                

    def combinaciones(self, lista):
        list_password = []
        contaPalabras = len(lista) + 1;
 
        for num in range(contaPalabras):
            condicion = True
            contador = -1
            while condicion:
                contador = contador + 1
                ele = lista[contador:(contador + num)]
                list_password.append(ele)
                if contaPalabras == (contador + num):
                    condicion = False
        
        return list_password
    def calcularCierrePaso3(self, descriptor_busqueda, dependencia_evaluacion):
        agregar = []
        combinaciones = self.combinaciones(descriptor_busqueda)
        for com in combinaciones:
            for dependencia in self.dependenciasPaso2:
                if  not (dependencia_evaluacion[0] == dependencia[0] and dependencia_evaluacion[1] == dependencia[1]):
                    
                    if dependencia[0] == com and dependencia[1] == dependencia_evaluacion[1] and len(dependencia[0]) < len(dependencia_evaluacion[0]):
                        nuevo_implicante = com
                        nuevo_implicado = dependencia_evaluacion[1]
                        dependencia_evaluacion = []
                        dependencia_evaluacion.append(nuevo_implicante)
                        dependencia_evaluacion.append(nuevo_implicado)
                    if com == dependencia[0]:
                        if dependencia_evaluacion[0].find(com) != -1:
                            nuevo_implicante = dependencia_evaluacion[0]
                            nuevo_implicante = dependencia_evaluacion[0].replace(dependencia[1], "")
                            nuevo_implicado = dependencia_evaluacion[1]
                            dependencia_evaluacion = []
                            dependencia_evaluacion.append(nuevo_implicante)
                            dependencia_evaluacion.append(nuevo_implicado)
                
                        if dependencia_evaluacion[0].find(com) -1:
                            agregar.append(dependencia[1])

        
        self.dependenciaTransformada = dependencia_evaluacion
        
        bandera = False
        for a in agregar:
            if descriptor_busqueda.find(a) == -1:
                bandera = True
                descriptor_busqueda = self.ordenarCadena(descriptor_busqueda + a)
        
       
        if bandera:
            descriptor_busqueda = self.calcularCierre(descriptor_busqueda, dependencia_evaluacion)
        
        descriptor_busqueda = self.ordenarCadena(descriptor_busqueda)
        return descriptor_busqueda
    
    def calcularCierrePaso3SinDep(self, descriptor_busqueda):
        combinaciones = self.combinaciones(descriptor_busqueda)
        agregar =[]
        
        for com in combinaciones:
            for dep in self.dependenciasPaso3:
                implicante = dep[0]
                implicado = dep [1]
                
                if com.strip() == implicante.strip():
                    agregar.append(implicado.strip())
                    break
        
        evaluarOtraVez = False
        for a in agregar:
            if descriptor_busqueda.find(a) == -1:
                descriptor_busqueda = descriptor_busqueda + a
                evaluarOtraVez = True
                
        if evaluarOtraVez:
            descriptor_busqueda = self.calcularCierrePaso3SinDep(descriptor_busqueda)
            
        return descriptor_busqueda
    def eliminaDependencias(self):  
        temporal = []
        
        for d in self.dependenciasPaso2:
            temporal.append(d)
        for dep in temporal:
            implicante = dep[0]
            implicado = dep[1]
            cierre = self.calcularCierrePaso3(implicante, dep)

            permanece = True
            if cierre.find(implicado) != -1:
                permanece = False
                
            if permanece:
                self.dependenciasPaso3.append(dep)
            else:
                nuevaDependenciasPaso2 = []
                for deptemporal in self.dependenciasPaso2:
                    if not(dep[0] == implicante and dep[1] == implicado):
                        nuevaDependenciasPaso2.append(deptemporal)
                
                self.dependenciasPaso2 = nuevaDependenciasPaso2

    def agregaClave(self, clave):
        agregar = True
        
        for m in self.m2:
            if clave == m:
                agregar = False
                break
        
        if agregar:
            self.m2.append(clave)

    def calcularClaves(self):
        
        todoImplicantes = []
        todoImplicados = []
        todoImplicantesImplicados = []
              
        for dep in self.dependenciasPaso3:
            implicante = dep[0]
            implicado = dep[1]
            
            for impe in implicante:
                
                banderaImplicantes = True
                
                for elemento in todoImplicantes:
                    if elemento == impe:
                        banderaImplicantes = False
                        break
                    
                if banderaImplicantes:
                    todoImplicantes.append(impe)

            
            for impe in implicado:
                banderaImplicados = True
                
                for elemento in todoImplicados:
                    if elemento == impe:
                        banderaImplicados = False
                        break
                    
                if banderaImplicados:
                    todoImplicados.append(impe)
            
        
        contTodoImplicantes = len(todoImplicantes)
        contTodoImplicados = len(todoImplicados)
        
        if contTodoImplicantes > contTodoImplicados:
            
            for implicante in todoImplicantes:
                bandera = False
                
                for implicado in todoImplicados:
                    if implicante == implicado:
                        bandera = True
                        break
                
                if bandera:
                    todoImplicantesImplicados.append(implicante)
            
        else:
            for implicado in todoImplicados:
                bandera = False
                
                for implicante in todoImplicantes:
                    if implicante == implicado:
                        bandera = True
                        break
                    
                if bandera:
                    todoImplicantesImplicados.append(implicado)

        
        z = []
        
        for elemento in self.L:
            bandera = True
            
            for implicado in todoImplicados:
                if elemento == implicado:
                    bandera = False
                    break
            
            if bandera:
                z.append(elemento)
        
                
        if len(z) > 0:
            cierreDescriptor = self.cierreDescriptorPaso3(''.join(z));
            
            if self.ordenarCadena(cierreDescriptor) == self.ordenarCadena(''.join(self.L)):
                self.m2.append(''.join(z))
                return "";
        
        
        w = []
        
        for elemento in self.L:
            bandera = True
            
            for implicante in todoImplicantes:
                if elemento == implicante:
                    bandera = False
                    break
            
            if bandera:
                w.append(elemento)
        
  
        if len(w) > 0:
            cierreDescriptor = self.cierreDescriptorPaso3(''.join(w));
            
            if self.ordenarCadena(cierreDescriptor) == self.ordenarCadena(''.join(self.L)):
                self.m2.append(''.join(w))
                return "";
            
        v = []
        
        for elemento in self.T:
            bandera = True
            
            for ele in todoImplicantesImplicados:
                if elemento == ele:
                    bandera = False
                    break
            
            if bandera:
                w.append(elemento)
        
        if len(v) > 0:
            cierreDescriptor = self.cierreDescriptorPaso3(''.join(v));
            
            if self.ordenarCadena(cierreDescriptor) == self.ordenarCadena(''.join(self.L)):
                self.m2.append(''.join(v))
                return ""
        
        print(todoImplicantesImplicados)
    
        m1 = ''.join(todoImplicantesImplicados)
        m1 = self.ordenarCadena(m1)
        m1a = m1
        m1b = " " + m1
        
        for a in m1a:
            for num in range(len(m1b)):
                descriptor = m1b[0:(num + 1)]
                descriptor = descriptor.replace(a,"")
                descriptor = a + descriptor;
                descriptor = descriptor.replace(" ", "")
                descriptor = self.ordenarCadena(descriptor)
                
                banderaEncontreLLave = False
                
                combinaciones = self.combinaciones(descriptor)
                
                for com in combinaciones:
                    cierreDescriptor = self.calcularCierrePaso3SinDep(com)
                    conjuntoTodo = ''.join(self.L)
                    
                    if self.ordenarCadena(conjuntoTodo) == self.ordenarCadena(cierreDescriptor):
                        self.agregaClave(com)
                        m1b = m1b.replace(a, "")
                        banderaEncontreLLave = True
                        break
                
                if banderaEncontreLLave:
                    break
    def esSegundaForma(self):                
        
        for m in self.m2:
            cierreDescriptor = self.calcularCierrePaso3SinDep(m)
            conjuntoTodo = ''.join(self.L)
            evaluacion = []
            evaluacion.append(m)
            if self.ordenarCadena(conjuntoTodo) == self.ordenarCadena(cierreDescriptor):
                evaluacion.append("Si")
            else:
                evaluacion.append("No")

            self.segundaForma.append(evaluacion)
                        
#Instancia para iniciar la aplicacion
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = Ventana()
#Mostrar la ventana 
_ventana.show()
#Ejecutar la aplicacion 
app.exec_() 