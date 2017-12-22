# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class soporte(osv.Model):
    _inherit = 'crm.helpdesk'
    _description = 'Campos adicionales para formulario de Helpdesk y soporte'
    _columns = {
        'usuario': fields.char('Usuario'),
        'solicitante': fields.many2one("hr.employee", string="Solicitante"),
        'area_id': fields.char('Area'),
        'tipo': fields.selection([('sistemas', 'Sistemas'),
            ('mantenimiento', 'Mantenimiento')], "Tipo"),
        'personal_id': fields.one2many("hr.employee", "asignado",
            string='Personal Asignado'),
        'asignado_id': fields.one2many("ea.asignado", "relation",
            string="Personal Asignado"),
        'lugar_id': fields.many2one("ea.lugar", "Area"),
        'numero_serie': fields.char("Numero de Serie"),
        'aplazamiento_ids': fields.one2many("ea.aplazamiento", "relation",
                string="Aplazamientos"),
        'aplazamiento1': fields.many2one("ea.aplazamiento",
            string="Primer Aplazamiento"),
        'aplazamiento2': fields.many2one("ea.aplazamiento",
            string="Segundo Aplazamiento"),
        'motivo': fields.char("Motivo"),
        'tipo_mto': fields.selection([('preventivo', 'Preventivo'),
            ('correctivo', 'Correctivo')], "Preventivo/Correctivo"),
        'h1': fields.boolean("Limpieza de Monitor"),
        'h2': fields.boolean("Limpieza de Chasis"),
        'h3': fields.boolean("Limpieza de Teclado"),
        'h4': fields.boolean("Limpieza de Mouse"),
        'h5': fields.boolean("Limpieza interna (sopleteo)"),
        'h6': fields.boolean("Reemplazo de Pieza Instalación de Aplicación"),
        's1': fields.boolean("Escaneo de Disco Duro"),
        's2': fields.boolean("Desfragmentado de Disco Duro"),
        's3': fields.boolean("Eliminar Archivos Temporales"),
        's4': fields.boolean("Eliminar Cookies"),
        's5': fields.boolean("Configuración TCP/IP"),
        's6': fields.boolean("Instalación de Impresora"),
        's7': fields.boolean("Correo Electrónico"),
    }

    _defaults = {
            'tipo': 'sistemas',
            'tipo_mto': 'preventivo',
            'name': lambda self, cr, uid, context={}:
                self.pool.get('ir.sequence').get(cr, uid, 'crm.helpdesk')
        }


class jmdasignado(osv.Model):
    _name = "ea.asignado"
    _columns = {
            'name': fields.many2one("hr.employee", string="NIP"),
            'nombre': fields.related("name", "nombre", type="char",
                string="Nombre", readonly=True, store=True),
            'relation': fields.many2one("crm.helpdesk")
        }


class jmdaplazamiento(osv.Model):
    _name = "ea.aplazamiento"
    _columns = {
            'name': fields.char(string="Motivo", size=80),
            'hora_planeada': fields.datetime(string="Día y Hora"),
            'aplazado_por': fields.many2one("hr.employee", "Aplazado por"),
            'nombre': fields.related("aplazado_por", "nombre", type="char",
                    string="Nombre", readonly=True, store=False),
            'relation': fields.many2one("crm.helpdesk"),
            'aceptado_por': fields.many2one("hr.employee", "Aceptado por"),
            'anombre': fields.related("aceptado_por", "nombre", type="char",
                    string="Nombre", readonly=True, store=False),
        }


class jmdemployeesporte(osv.Model):
    _inherit = "hr.employee"

    _columns = {
            'relation_mantenimiento': fields.many2many("crm.helpdesk",
                    string="Relacion"),
            'asignado': fields.many2many("crm.helpdesk",
                    string="Relacion"),
        }


class jmdlugar(osv.Model):
    _name = "ea.lugar"

    _columns = {
            'name': fields.char(string="Nombre", size=80),
            'field': fields.char(string="Descripcion", size=120)
        }