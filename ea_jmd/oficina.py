# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdoficina(osv.Model):
    _name = "ea.oficina"
    _inherit = "mail.thread"
    _columns = {
            'name': fields.char("Nombre"),
            'direccion': fields.char("Dirección"),
            'ciudad': fields.char("Ciudad")
        }


class jmdplaza(osv.Model):
    _name = "ea.provincia"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Nombre"),
        'direccion': fields.char("Dirección"),
        }


class jmdcnomina(osv.Model):
    _name = "ea.ciudadnomina"
    _inherit = "mail.thread"
    _columns = {
            'name': fields.char("Nombre"),
        }