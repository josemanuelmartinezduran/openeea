# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdinvoice(osv.Model):
    _inherit = "account.invoice"

    def register_invoice(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            a = 1
        return ret

    _columns = {
            'razon_social': fields.char("Razon Social"),
            'calle': fields.char("Calle"),
            'exterior': fields.char("Exterior"),
            'interior': fields.char("Interior"),
            'colonia': fields.char("Colonia"),
            'codigo_postal': fields.char("Código Postal"),
            'pais': fields.char("Pais"),
            'estado': fields.char("Estado"),
            'municipio': fields.char("Municiio"),
            'localidad': fields.char("Localidad"),
            'tarjeta': fields.char("Ultimos 4 Dígitos"),
            'forma': fields.char("Forma de Pago"),
            'enviada': fields.boolean("Enviada"),
            'compania_destino': fields.many2one("res.company")
        }