# -*- coding: utf-8 -*-
############################################
# Descripción: Recursos Humanos - Entradas y Salidas y registro de asistencia
# Ruta: Recursos humanos/entradas y salidas
# Modulo: Estadistica Aplicada
# Desarrollador: CMG
# HYD México 2014
############################################
from openerp.osv import fields, osv


#### clase para entradas y salidas de Recursos humanos ####
class recursos_humano(osv.Model):
    _inherit = 'hr.es'
    _order = "empleado,fecha,hora"

    def _funcion_empleados(self, cr, uid, ids, field_name, arg, context=None):
        #Diccionario para el resultado
        res = {}
        #Lista para empleados
        empleados = []
        #Recorre la lista de empleados
        for record in self.browse(cr, uid, ids, context):
            if record.empleado.name not in empleados:
                empleados.append(record.empleado.name)
        #Ordenamos la lista de empleados
        empleados.sort()
        #Se guarda el total de los empleados
        total = len(empleados)
        #Se inicializa el contador
        contador = 0
        #Diccionario para las fechas del empleado
        empleadoFechas = {}
        #Lista para guardar los días que entro por la noche
        fechaUnica = []
        while contador < total:
            #Lista para guardar fechas
            fechas = []
            #Se recorren los registros del tree
            for registros in self.browse(cr, uid, ids, context):
                #Verifica que los registos correspondan al mismo empleado
                if empleados[contador] == registros.empleado.name:
                    #Si no se encuentra la fecha la guarda en lalista
                    if registros.fecha not in fechas:
                        fechas.append(registros.fecha)
                        fechaUnica.append(registros.fecha)
                    else:
                        #Si ya se encuentra la borra
                        if len(fechaUnica) > 0:
                            fechaUnica.pop()
            #Guarda en el dccionario en base al numero de empleado
            empleadoFechas[empleados[contador]] = fechas
            #Contador para fechas
            contadorFechas = 0
            #bandera para saber si es entrada o salida
            banderaFecha = True
            #Se recorren los registros
            while contadorFechas < len(empleadoFechas[empleados[contador]]):
                for registros in self.browse(cr, uid, ids, context):
                    #Se recorren los registros del empleado
                    if empleados[contador] == registros.empleado.name:
                        #Verifica que sean de la misma fecha
                        if empleadoFechas[empleados[contador]][contadorFechas]\
                            == registros.fecha:
                            if banderaFecha:
                                #Envía el mensaje de entrada
                                res[registros.id] = 'entrada'
                                banderaFecha = False
                            else:
                                #Envía el mensaje de salida
                                res[registros.id] = 'salida'
                                banderaFecha = True
                contadorFechas += 1
            contador += 1
        return res

    _columns = {
        'tipo': fields.function(_funcion_empleados,
                                type='selection',
                                string='Tipo de registro',
                                selection=[('entrada', ('Entrada')),
                                           ('salida', ('Salida'))])
    }


#Agrega el boton en personal de tipo de contrato
class personal_contrato(osv.Model):
    _inherit = 'hr.employee'
    _columns = {
        'tipo_contrato': fields.selection([('Nomina', 'Nomina'),
                                           ('Honorarios', 'Honorarios')],
                                          "Tipo de contrato"),
        'dias_labora': fields.selection([('L-V', 'Lunes a Viernes'),
                                           ('L-S', 'Lunes a Sábado')],
                                          "Dias laborables")
    }


#Se hereda la clase que estaba anteriormente desarrollada por JMD ##
#Clase que genera las listas de asistencias
class registro_asistencias(osv.Model):
    _inherit = "hr.asistencias"

    _columns = {
            'generada': fields.boolean("Generada"),
        }

    _defaults = {
            'generada': False
        }

    #Función que genera la linea de asistencias
    def generate_asistencias_line(self, cr, uid, ids, context=None):
        #print "Generar registros de asistencias"
        ret = {}
        dict_es = {}
        for i in self.browse(cr, uid, ids, context):
            if i.generada:
                return ret
            i.generada = True
            es_object = self.pool.get("hr.es")
            entrada = 0.0
            salida = 0.0
            resta = 0.0
            for j in es_object.browse(cr, uid, es_object.search(cr, uid,
                [('fecha', '>=', i.inicio), ('fecha', '<=', i.fin)])):

                if str(j.empleado.id) in dict_es:
                    entrada = dict_es[str(j.empleado.id)]["entrada"]
                    salida = j.hora

                    #Fechas
                    fecha_entrada = dict_es[str(j.empleado.id)]['fecha']
                    fecha_salida = j.fecha

                    fecha1 = int(fecha_entrada.split('-')[2]) * 10
                    fecha2 = int(fecha_salida.split('-')[2]) * 10
                    resta = ((fecha2 - fecha1) / 10)
                    if resta < 2:
                        if entrada > salida:
                            resta = self.calculo_horas(entrada, salida)
                        else:
                            resta = salida - entrada
                    else:
                        resta = self.calculo_horas_dias(resta, entrada, salida)

                    #borra del diccionario el empleado

                    del dict_es[str(j.empleado.id)]
                    values = {
                        'empleado': j.empleado.id,
                        'fecha': j.fecha,
                        'horas': resta,
                        'relation': i.id
                    }
                    repetido = self.pool.get("hr.asistencias.linea").\
                        search(cr, uid, [('empleado', '=', j.empleado.id),
                        ('fecha', '=', j.fecha)])
                    if len(repetido) > 0:
                        #print "Se ha repetido una vez"
                        empleado_anterior =\
                            self.pool.get("hr.asistencias.linea")
                        for ea in empleado_anterior.browse(cr, uid, repetido):
                            sumatoria = resta + ea.horas
                            self.pool.get("hr.asistencias.linea").write(cr,
                                uid, repetido, {'horas': sumatoria})
                    else:
                        self.pool.get("hr.asistencias.linea").create(cr,
                            uid, values, context)

                else:
                    dict_es[str(j.empleado.id)] = {'entrada': j.hora,
                        'fecha': j.fecha}

        return ret

    #Calcula el timpo de horas
    #cuando la hora de entrada es superior a la hora de salida
    def calculo_horas(self, horaEntrada, horaSalida):

        #Se guarda la hora entrante
        hora_entrada = int(str(horaEntrada).split('.')[0])
        #Se guarda el minuto de la hora entrante
        minutos_entrada = int(str(horaEntrada).split('.')[1])
        # se toma la hora de la fecha de salida
        hora_salida = int(str(horaSalida).split('.')[0])
        # Se toma el minuto de la feha de salida
        minutos_salida = int(str(horaSalida).split('.')[1])

        #Si es media hora 30min = 5 se agrega un 0
        if len(str(minutos_entrada)) < 2:
            minutos_entrada = int(str(minutos_entrada) + '0')
        # Si es media hora 30min = 5 se agrega un 0
        if len(str(minutos_salida)) < 2:
            minutos_salida = int(str(minutos_salida) + '0')

        #print ("--- Hora entrada " + str(hora_entrada))
        #print ("--- minutos entrada  " + str(minutos_entrada))
        #print ("--- Hora salida  " + str(hora_salida))
        #print ("--- minutos salida  " + str(minutos_salida))

        minutos_e = 0
        #Si los minutos de entrada son mayores a 0
        if minutos_entrada > 0:
            #Se resta a 100 ya que media hora en deciamal es = 50
            minutos_e = 100 - minutos_entrada
            hora_e = 23 - hora_entrada
            #print "Entrada _e " + entrada_e
        else:
            hora_e = 24 - hora_entrada

        if minutos_salida > 0:
            minutos_s = minutos_e + minutos_salida
        else:
            minutos_s = minutos_e

        #print "** Minutos ** " + str(minutos_s)

        #Calculo de las horas a retornar
        if minutos_s > 100:
            resta = minutos_s - 100
            hora = str(hora_e + hora_salida + 1) + '.' + str(resta)
        else:
            hora = str(hora_e + hora_salida) + '.' + str(minutos_s)
        return hora

    #Método para calcular las horas del empleado cuando
    #ha trabajado más de un día.
    def calculo_horas_dias(self, dias, horaEntrada, horaSalida):
        #print "chd dias -- " + str(dias)
        #print "chd hora entrada -- " + str(horaEntrada)
        #print "chd hora salida -- " + str(horaSalida)

        if horaSalida > horaEntrada:
            acumuladoHoras = dias * 24
            resta_horas = (horaSalida - horaEntrada)
            acumuladoHoras = acumuladoHoras + resta_horas
        else:
            acumuladoHoras = (dias - 1) * 24
            resta_horas = (horaEntrada - horaSalida)
            acumuladoHoras = acumuladoHoras + (24 - resta_horas)

        #print "Acumulador de horas " + str(acumuladoHoras)
        return acumuladoHoras

    _columns = {

    }