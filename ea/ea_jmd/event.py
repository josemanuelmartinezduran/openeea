# -*- coding: utf-8 -*-
from osv import osv, fields

class jmdoficinas(osv.Model):
    _inherit = "event.event"
    _columns = {
            'oficina': fields.many2one("event.oficina", string="Oficina"),
            'sala': fields.many2one("event.sala", string="Sala"),
        }

class jmdoffice(osv.Model):
    _name="event.oficina"
    _columns = {
        'name': fields.char("Nombre de la Oficina"),
        'direccion': fields.char("Dirección")
        }


class jmdsala(osv.Model):
    _name="event.sala"
    _columns = {
        'name': fields.char("Nombre de la Sala"),
        'ubicacion': fields.char("Ubicación")
        }