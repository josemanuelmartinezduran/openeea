# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdasistencias(osv.Model):
    _name = "hr.asistencias"

    def action_borrador(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'borrador'})
        return True

    def action_aprobado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'aprobado'})
        return True

    def generate_asistencias_line(self, cr, uid, ids, context=None):
        ret = {}
        #Arrelgar que sean varios empleados todo checany salen cuando quieren
        #Creando un diccionario
        dict_es = {}
        for i in self.browse(cr, uid, ids, context):
            es_object = self.pool.get("hr.es")
            entrada = 0.0
            salida = 0.0
            resta = 0.0
            for j in es_object.browse(cr, uid, es_object.search(cr, uid,
                [('fecha', '>', i.inicio), ('fecha', '<', i.fin)])):
                if str(j.empleado.id) in dict_es:
                    salida = j.hora
                    entrada = dict_es[str(j.empleado.id)]["entrada"]
                    resta = salida - entrada
                    del dict_es[str(j.empleado.id)]
                    values = {
                        'empleado': j.empleado.id,
                        'fecha': j.fecha,
                        'horas': resta,
                        'relation': i.id
                        }
                    self.pool.get("hr.asistencias.linea").create(cr, uid,
                        values, context)
                else:
                    dict_es[str(j.empleado.id)] = {'entrada': j.hora}
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=80),
            'inicio': fields.date("Inicio"),
            'fin': fields.date("Fin"),
            'lineas': fields.one2many("hr.asistencias.linea", 'relation',
                "Lineas de asistencia"),
            'retardos': fields.one2many("hr.retardo", 'relation',
                'Retardos'),
            'state': fields.selection([('borrador', 'Borrador'),
                ('aprobado', 'Aprobado')], "Estado", readonly=True),
            'generada': fields.boolean("Generada"),
        }


class jmdasistencia_linea(osv.Model):
    _name = "hr.asistencias.linea"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'empleado': fields.many2one("hr.employee", "Empleado"),
            'nombre': fields.related("empleado", "nombre",
                type="char", string="Nombre", readonly=True, store=False),
            'fecha': fields.date("Fecha"),
            'horas': fields.float(digits=(4, 2), string="Horas Trabajadas"),
            'relation': fields.many2one("hr.asistencias")
        }


class jmdretardo(osv.Model):
    _name = "hr.retardo"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'empleado': fields.many2one("hr.employee", "Empleado"),
            'fecha': fields.date(string="Fecha del Retardo"),
            'hora_entrada': fields.float(string="Hora de Entrada"),
            'hora_real': fields.float(string="Hora Real"),
            'relation': fields.many2one("hr.asistencias")
        }


class jmdfaltas(osv.Model):
    _name = "hr.faltas"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'empleado': fields.many2one("hr.employee", "Empleado"),
            'faltas': fields.float(string="Número de Faltas", digits=(9, 2)),
            'relation': fields.many2one("hr.asistencias")
        }