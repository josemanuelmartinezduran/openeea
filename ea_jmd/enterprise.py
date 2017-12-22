# -*- coding: utf-8 -*-
from osv import osv, fields


class myclass(osv.Model):
    _name = "ea.enterprise"
    _columns = {
            'name': fields.char(string="Nombre", size=40)
        }