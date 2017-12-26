# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdpartner(osv.Model):
    _inherit = "res.partner"

    def has_reference(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = True
            if not i.referencia:
                ret[i.id] = False
        return ret

    def create(self, cr, uid, vals, context=None):
        print(vals)
        if vals['customer']:
            vals['opt_out'] = True
        return super(jmdpartner,self).create(cr, uid, vals, context=context)

    _columns = {
            'referencia': fields.char(string="Referencia (3 Caracteres)",
                size=3),
            'has_referencia': fields.function(has_reference,
                string="Tiene Referencia", type="boolean", store=True),
            'aditional_address': fields.text("Dirección Adicional"),
            'aditional_address_type': fields.selection([("fiscal", "Fiscal"),
                ("fisica", "Física"), ("entrega", "Entrega"), ("otra", "Otra")],
                string="Tipo de dirección"),
            'evaluaciones': fields.one2many("survey", "relation_partner",
                string="Evaluaciones"),
            'encuesta_preeliminar': fields.many2one("survey",
                string="Evaluación Preeliminar"),
            'razon_social': fields.char("Razon Social"),
            'calle': fields.char("Calle"),
            'exterior': fields.char("Exterior"),
            'interior': fields.char("Interior"),
            'colonia': fields.char("Colonia"),
            'codigo_postal': fields.char("Código Postal"),
            'pais': fields.char("Pais"),
            'estado': fields.char("Estado"),
            'municipio': fields.char("Municipio"),
            'localidad': fields.char("Localidad"),
            'tarjeta': fields.char("Ultimos 4 Dígitos"),
            'forma': fields.char("Forma de Pago"),
            'extension': fields.char("Extension"),
            'email': fields.text("Email"),
            'correo_e': fields.char("Correo Electrónico"),
            'telefono': fields.char("Teléfono"),
            'es_sea': fields.boolean("¿Es SEA?"),
        }

    _defaults = {
            'email': 'empty@me.com',
        }

_sql_constraints = [
        ('unique_name', 'unique(name)', 'Ya existe ese cliente.'),
        ]


class jmdsurvey(osv.Model):
    _inherit = "survey"
    _columns = {
            'relation_partner': fields.many2one("res.partner")
        }
