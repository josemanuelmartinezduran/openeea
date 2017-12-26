# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdconceptopresupuesto(osv.Model):
    _name = "ea.presupuesto.concepto"
    _columns = {
            'name': fields.char(string="Nombre", size=120),
            'tipo': fields.selection([("adepositar", "A Depositar"),
                ("nosedeposita", "No se deposita"),
                ("nominagea", "Nómina GEA"),
                ("otros", "D/HPROD./PAGADOS/A VIAJAR/MUESTRA")],
                string="Tipo de Dato"),
            'monto': fields.float("Monto"),
        }
    _defaults = {
            'monto': 0.0,
        }