# -*- coding: utf-8 -*-
#IStandForFreedom
from osv import osv, fields


class jmdconcepto(osv.Model):
    _name = "hr.concepto"
    _columns = {
            'name': fields.char(string="Clave", size=40),
            'descripcion': fields.char(string="Descripción", size=40),
            'linea_ids': fields.one2many("hr.concepto.linea", "relation",
                    string="Lineas del Concepto"),
        }


class jmdconceptolinea(osv.Model):
    _name = "hr.concepto.linea"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'relation': fields.many2one("hr.concepto"),
            'tipo': fields.selection([("dias", "Días"), ("monto", "Monto")],
                string=""),
            'dias': fields.float(digits=(6, 2), string="Días"),
            'monto': fields.float(digits=(9, 2), string="Monto")
        }