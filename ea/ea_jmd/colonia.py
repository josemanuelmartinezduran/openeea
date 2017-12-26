# -*- coding: utf-8 -*-
from osv import osv, fields

class jmdcolonia(osv.Model):
    _inherit = "mail.thread"
    _name = "utils.colonia"
    _columns = {
        'name':fields.char("Nombre"),
        'tipo': fields.char("Tipo"),
        'cp': fields.char("Codigo Postal"),
        'estado': fields.char("Estado"),
        'municipio': fields.char("Municipio"),
        'ciudad': fields.char("Ciudad")
    }