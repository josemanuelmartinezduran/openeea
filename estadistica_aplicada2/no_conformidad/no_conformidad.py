# -*- coding: utf-8 -*-
#Fixed By JMD #IStandForFreedom
from osv import osv, fields


class no_conformidad(osv.osv):
    _name = 'no_conformidad'
    _inherit = "mail.thread"

    def action_generada(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'generada'})
            return True

    def action_validada(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'validada'})
            return True

    def action_resuelta(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'resuelta'})
            return True

    _columns = {
        'name': fields.char('Clave', required=True),
        'generador': fields.many2one('hr.employee', string='Generador'),
        'gnombre': fields.related("generador", "nombre", type="char",
            string="Nombre", readonly=True, store=False),
        'responsable': fields.many2one('hr.employee', string='Responsable'),
        'rnombre': fields.related("responsable", "nombre", type="char",
            string="Nombre", readonly=True, store=False),
        'jefe_del_responsable': fields.many2one('hr.employee',
            string='Jefe del responsable'),
        'jnombre': fields.related("jefe_del_responsable", "nombre", type="char",
            string="Nombre", readonly=True, store=False),
        'area': fields.many2one("hr.department", string="Departamento"),
        'fecha': fields.date('Fecha'),
        'prioridad': fields.selection([('baja', 'Baja'), ('media', 'Media'),
            ('alta', 'Alta')], 'Prioridad'),
        'state': fields.selection([('generada', 'Generada'),
            ('validada', 'Validada'), ('resuelta', 'Resuelta')], 'Estado'),
        'descripcion': fields.text('Descripcion'),
        'acciones': fields.one2many('no_conformidad.acciones',
             'relation_no_confomidad', 'Acciones'),
        'consecuencias': fields.text("Consecuencias"),
        'concepto': fields.char("Concepto"),
        'auditoria': fields.many2one('auditoria', string='Auditoria de Origen'),
    }


class acciones(osv.osv):
    _name = 'no_conformidad.acciones'
    _columns = {
        'name': fields.char(string="Nombre", size=40),
        'persona': fields.many2one('hr.employee', string='Empleado'),
        'nombre': fields.related("persona", "nombre", type="char",
            string="Nombre", readonly=True, store=False),
        'accion': fields.char('Accion'),
        'fecha': fields.date('Fecha'),
        'horas_dedicas': fields.boolean('Realizado'),
        'relation_no_confomidad': fields.many2one("no_conformidad",
            string="Relacion con no conformidad", ondelete="set null")
    }
