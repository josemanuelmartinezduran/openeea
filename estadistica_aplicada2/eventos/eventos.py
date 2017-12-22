# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class eventos(osv.Model):
    _inherit = 'event.event'
    _description = 'Campos nuevos para tabla Event'
    _columns = {
        'proyecto': fields.many2one("project.project", "Estudio"),
        'tipo': fields.selection([('nuevo', 'Nuevo ingreso'),
            ('estudio', 'Estudio'), ('entrenamiento', 'Entrenamiento'),
            ('conferencia', 'Conferencia'), ('otro', 'Otro'),
            ('Curso', 'Curso')], 'Tipo'),
        'ok': fields.boolean("OK (DC-3)"),
        'nombre_corto': fields.related("proyecto", "nombre_corto",
            type="char", string="Nombre Corto", readonly=True, store=True)

    }


class jmdregistro(osv.Model):
    _inherit = 'event.registration'
    _columns = {
        'tipo': fields.selection([('Persona', 'Persona'),
            ('Empresa', 'Empresa')], string="Tipo")
    }


#Corregido por JMMD
class asistencia(osv.Model):
    _inherit = 'event.event'
    _description = 'Campos para asistentes de un evento'
    _columns = {
        'asistencia_ids': fields.one2many('ea.asistencia',
            'relation_event', 'Lista de Asistencia')
    }


class myclass(osv.Model):
    _name = "ea.asistencia"
    _columns = {
            'name': fields.many2many("hr.employee", 'relation_event',
                'Participante'),
            'empresa': fields.one2many('res.partner', 'relation_event',
                'Empresa'),
            'asistente': fields.many2one("hr.employee", 'Asistente'),
            'nombre': fields.related("asistente", "nombre", type="char",
                string="Nombre", readonly=True, store=True),
            'company': fields.many2one("res.partner", "Empresa"),
            'relation_event': fields.many2one("event.event"),
            'ciudad': fields.char("Ciudad"),
        }


#JMMD
class respartnerasistencia(osv.Model):
    _inherit = "res.partner"
    _columns = {
        'relation_event': fields.many2one("ea.asistencia"),
    }


#JMMD
class hrasistencia(osv.Model):
    _inherit = "hr.employee"
    _columns = {
        'relation_event': fields.many2many("ea.asistencia"),
    }