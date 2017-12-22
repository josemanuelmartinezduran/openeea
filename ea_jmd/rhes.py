# -*- coding: utf-8 -*
from osv import osv, fields


class jmdes(osv.Model):
    _name = "hr.es"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'nombre': fields.related("empleado", "nombre", type="char",
                string="Nombre", readonly=True, store=False),
            'empleado': fields.many2one("hr.employee", string="Empleado"),
            'fecha': fields.date("Fecha"),
            'hora': fields.float(digits=(4, 2), string="Hora"),
            'tipo': fields.selection([('entrada', 'Entrada'), ('salida',
                'Salida')], "Tipo de registro")
        }
#IStandForFreedom