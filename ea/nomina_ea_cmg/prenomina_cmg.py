# -*- coding: utf-8 -*-
############################################
# Descripción: Calculo de la prenomina
# Ruta: Recursos Humanos /Nomina / Calculo de prenomina
# Modulo: Estadistica Aplicada
# Desarrollador: CMG
# HYD México 2014
############################################
from openerp.osv import fields, osv
from datetime import date


#### Clase para agregar los datos de validación ####
class generacion_lineas_prenomina(osv.Model):
    _inherit = 'hr.prenomina'

    def action_borrador(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'borrador'})
        return True

    #Cambia al estado aprobado e inserta los datos en nominas de empleado
    def action_aprobado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'aprobado'})
        #insertar los datos de la prenomina
        prenomina_obj = self.pool.get('hr.prenomina.linea')
        self.pool.get('hr_payslip_line')
        valores = {}
        for pre in prenomina_obj.browse(cr, uid, prenomina_obj.search(cr,
            uid, [('relation', '=', ids)])):
            # Datos para Nomina de emopleado obj = hr.payslip
            valores = {
                'date_to': pre.relation.fin,
                'date_from': pre.relation.inicio,
                'name': 'Nomina salarial de ' + str(pre.empleado.id) + ' ' +
                    str(pre.relation.name),
                'employee_id': pre.empleado.id,
                'number': 'SLIP/' + str(pre.empleado.id) + '' +
                    str(pre.relation.name),
            }
            # se inserta datos para hr.payslip
            recibo_obje = self.pool.get('hr.payslip').create(cr, uid, valores)

            #print recibo_obje
            #print " pre.tipo_contrato  -- " + str(pre.tipo_contrato)
            if pre.tipo_contrato == 'Nomina':
                dinero_pesos = pre.nomina
            elif pre.tipo_contrato == 'Honorarios':
                dinero_pesos = pre.dinero

            #print " dinero -- " + str(dinero_pesos)

            #inserta los datos en hr.payslip.line
            valoresNomina = {
                    'code': 'Gross',
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'sequence': 1,
                    'quantity': 1.0,
                    'contract_id': 1,
                    'employee_id': pre.empleado.id,
                    'condition_python': '',
                    'name': 'Gross',
                    'amount': dinero_pesos,
                    'salary_rule_id': 1,
                    'category_id': 3,
                    'slip_id': int(recibo_obje)
            }
            self.pool.get('hr.payslip.line').create(cr, uid, valoresNomina)
        return True


class linea_prenomina(osv.Model):
    _inherit = "hr.prenomina.linea"

    #Calcula el total de dias naturales de la nómina
    '''
    @returns integer, numero de días
    '''
    def _calculate_dias(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            #Asigna las fechas
            start_date = i.relation.inicio
            end_date = i.relation.fin

            # Fecha inicio
            if not start_date:
                ret[i.id] = 0
                return ret
            fechai = date(int(str(start_date).split('-')[0]),
                          int(str(start_date).split('-')[1]),
                          int(str(start_date).split('-')[2]))
            #Fecha de fin
            if not end_date:
                ret[i.id] = 0
                return ret
            fechaf = date(int(str(end_date).split('-')[0]),
                          int(str(end_date).split('-')[1]),
                          int(str(end_date).split('-')[2]))

            #Si no es nómina acumulada
            if start_date != end_date:
                #Resta de las 2 fechas
                restaFechas = fechaf - fechai
                ret[i.id] = int(str(restaFechas).split(' ')[0]) + 1
            else:
                #Es la misma fecha regresa 1
                ret[i.id] = 1
        return ret

    #Calcula los días acumulados
    ''' calculate_trabajado
    @return dict, dias trabajados
    @example: si el empleado con id 10 trabajo 8 días
    devuelve {10: 8.0}, si no tiene contrato y dias que trabaja
    devuelde 0
    '''
    def _calculate_trabajados(self, cr, uid, ids, fieldname, args,
        context=None):
        ret = {}

        return ret

    #Calcula los dias de la semana segun los descansos del empleado
    def calcula_semanas_empleado(self, cr, uid, ids, context,
        empleado_descansa):
        for i in self.browse(cr, uid, ids, context):
            #i.relation.inicio = '2015-02-16'
            #i.relation.fin = '2015-02-28'
            diaInicio = date(int(str(i.relation.inicio).split('-')[0]),
                             int(str(i.relation.inicio).split('-')[1]),
                             int(str(i.relation.inicio).split('-')[2]))
            diaFin = date(int(str(i.relation.fin).split('-')[0]),
                          int(str(i.relation.fin).split('-')[1]),
                          int(str(i.relation.fin).split('-')[2]))

            #Cuantos dias del periodo son
            diasPeriodo = diaFin - diaInicio

        cont_semana = 1
        #semana1 = []
        #descansos1 = []
        test = {}
        testSemana = []
        testDescansos = []
        # Se recorre dia a dia para el periodo de nomina
        for dia in range(int(str(diasPeriodo).split(' ')[0]) + 1):

            #Fecha para analizar
            testDia = date(int(str(diaInicio).split('-')[0]),
                           int(str(diaInicio).split('-')[1]),
                           int(str(diaInicio).split('-')[2]) + (dia))

            #Si descansa Sábado y Domingo
            if empleado_descansa == 'S-D':
                if testDia.strftime("%a") != 'sáb' and\
                    testDia.strftime("%a") != 'dom':
                    testSemana.append(testDia)
                else:
                    # print "Dia --- " + str(testDia.strftime("%a")[0])
                    testDescansos.append(testDia)
                    if testDia.strftime("%a") == 'dom' or (
                        str(i.relation.fin).split('-')[2] ==
                        str(testDia).split('-')[2]):
                        test[cont_semana] = {'semana': testSemana,
                            'descansos': testDescansos}
                        #aumenta el contador de la semana
                        cont_semana += 1
                        #Se reinician variables de semana y descansos
                        testDescansos = []
                        testSemana = []
            #Si descansa solo Domingo
            elif empleado_descansa == 'D':
                if testDia.strftime("%a") != 'dom':
                    testSemana.append(testDia)
                else:
                    # print "Dia --- " + str(testDia.strftime("%a")[0])
                    testDescansos.append(testDia)
                    if testDia.strftime("%a") == 'dom' or (
                        str(i.relation.fin).split('-')[2] ==
                        str(testDia).split('-')[2]):
                        test[cont_semana] = {'semana': testSemana,
                        'descansos': testDescansos}
                        #aumenta el contador de la semana
                        cont_semana += 1
                        #Se reinician variables de semana y descansos
                        testDescansos = []
                        testSemana = []

        #Si aun quedan dias de la semana
        if len(testSemana) > 0:
            test[cont_semana] = {'semana': testSemana,
                'descansos': testDescansos}
        #print "***** Test : ********"
        return test

    #Calcula los dias de vacaciones del empleado durante el periodo
    def _calculate_vacaciones(self, cr, uid, ids, fieldname, args,
        context=None):
        ret = {}
        vacaciones = self.pool.get('hr.holidays')
        for i in self.browse(cr, uid, ids, context):
            if i.relation.tipo is not 'especial':
                #print " noespecial ------------ "
                contador_vacaciones = 0
                for v in vacaciones.browse(cr, uid, vacaciones.search(cr, uid,
                    [('state', '=', 'validate'),
                    ('holiday_status_id', '=', 5),
                    ('date_from', '>=', i.relation.inicio),
                    ('date_to', '<=', i.relation.fin),
                    ('employee_id', '=', i.empleado.id),
                    ('number_of_days', '<', 0)])):
                    contador_vacaciones += abs(v.number_of_days_temp)
                ret[i.id] = contador_vacaciones
            else:
                ret[i.id] = 0.0
        return ret

    def _calculate_dinero(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        dinero = 0.0
        bonos_horas = 0.0
        descuentos_horas = 0.0
        for i in self.browse(cr, uid, ids, context):
            # print "Dias trabajados = " + str(i.dias_trabajados)
            #print "Salario" + str(i.salario_diario)
            if i.dias_trabajados > 0:
                dinero = (i.dias_trabajados + i.dias_acumulados) *\
                    i.salario_diario
                # Contabilizar los dias en bonos
                bonos = self.pool.get('hr.bonos')
                bonos_horas = 0.0
                for b in bonos.browse(cr, uid, bonos.search(cr, uid,
                    [('empleado', '=', i.empleado.id),
                    ('state', '=', 'aprobado'),
                    ('tipo', '=', 'monto'),
                    ('fecha', '>=', i.relation.inicio),
                    ('fecha', '<=', i.relation.fin)])):
                    bonos_horas += b.monto

                # Contabilizar los descuentos
                descuentos = self.pool.get('hr.descuentos')
                descuentos_horas = 0.0
                for b in descuentos.browse(cr, uid, descuentos.search(cr, uid,
                    [('empleado', '=', i.empleado.id),
                    ('state', '=', 'aprobado'),
                    ('tipo', '=', 'monto'),
                    ('fecha', '>=', i.relation.inicio),
                    ('fecha', '<=', i.relation.fin)])):
                    descuentos_horas += b.monto
            else:
                ret[i.id] = 00.0
            #Resultado
            ret[i.id] = (dinero + bonos_horas) - descuentos_horas
            dinero = 0.0
            bonos_horas = 0.0
            descuentos_horas = 0.0
        return ret

    #Calcula los días de incapacidad del empleado durante el periodo
    def _calculate_incapacidad(self, cr, uid, ids, fieldname,
        args, context=None):
        ret = {}
        vacaciones = self.pool.get('hr.holidays')
        for i in self.browse(cr, uid, ids, context):
            if i.relation.tipo != 'especial':
                contador_incapacidad = 0
                for inc in vacaciones.browse(cr, uid, vacaciones.search(cr, uid,
                    [('state', '=', 'validate'),
                    ('holiday_status_id', '=', 2),
                    ('employee_id', '=', i.empleado.id),
                    ('number_of_days_temp', '>', 0)])):
                    contador_incapacidad += inc.number_of_days_temp
                ret[i.id] = contador_incapacidad
            else:
                ret[i.id] = 0
        return ret

    '''
    @returns dict {<i.id>: 0.0}
    '''
    def _calculate_nomina(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            #Quincena Acumulada
            #Si es normal se paga lo que dice en el concepto de nómina
            # Si es especial se paga
            #print str(i.tipo_contrato) + " tipo contrato"
            if not i.empleado.tipo_contrato:
                ret[i.id] = 0.0
                continue
            if i.relation.tipo == 'normal':
                #Si tiene contrato nomina se le paga lo que dice en nomina
                if i.tipo_contrato == 'Nomina':
                    if i.dias_trabajados > 0:
                        dinero = (i.dias_trabajados) * i.salario_diario
                        ret[i.id] = dinero
                    else:
                        ret[i.id] = 00.0
                # Si tiene contrato honorarios se le paga
                elif i.tipo_contrato == 'Honorarios':
                    ret[i.id] = i.dinero
            elif i.relation.tipo == 'especial':
                for acumulados in self.browse(cr, uid, self.search(cr, uid,
                    [('relation', '=', i.relation.acumulada.id),
                    ('empleado', '=', i.empleado.id),
                    ('dias_acumulados', '>', 0)])):
                    i.dinero = acumulados.especial
                ret[i.id] = i.dinero
        return ret

    def _calculate_especial(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.dinero > i.nomina:
                resta = i.dinero - i.nomina
                ret[i.id] = resta
            else:
                ret[i.id] = 0.0
        return ret