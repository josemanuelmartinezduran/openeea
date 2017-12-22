# -*- coding: utf-8 -*-
from osv import osv, fields


class TipoEstudio(osv.Model):
    _name = "ea.tipoestudio"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'descripcion': fields.char(string="Descripción", size=40)
        }