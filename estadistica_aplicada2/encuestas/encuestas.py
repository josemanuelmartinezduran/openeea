# -*- coding: utf-8 -*-
from osv import osv, fields

#Estadistica aplicada: Control de Encuestas


class editor_variables(osv.Model):
    _name = 'editor_variables'
    _columns = {
        'id_variable': fields.integer('Clave', readonly=True),
        'nombre_variable': fields.char('Variable', size=120, required=True),
        'comparador': fields.selection((('=', 'Igual a'),
            ('>=', 'Mayor o igual a'), ('<', 'Menor a')), 'Comparador'),
        'valor': fields.char('Valor', size=50),
    }


class editor_cuotas_fve(osv.Model):
    _name = 'editor_cuotas_fve'
    _columns = {
        'id_editor_cuota': fields.integer('Id editor cuotas'),
        'name': fields.char('Nombre de la cuota', size=120, required=True),
        'variables': fields.one2many('editor_variables',
            'id_variable', 'Variables'),
    }


class plazas(osv.Model):
    _name = 'ea.plaza'
    _columns = {
        'name': fields.char("Nombre", 25),
    }


class editor_encuestas(osv.Model):
    _name = 'editor_encuestas'
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char(string="Nombre", size=40),
        'id_encuesta': fields.many2one('control_encuestas',
            'Relacion con el proyecto'),
        'plaza': fields.many2one('ea.plaza', 'Plaza'),
        'complejidad': fields.selection([('alta', 'Alta'), ('media', 'Media'),
            ('baja', 'Baja')], 'Complejidad'),
        'cuota': fields.one2many('editor_cuotas_fve',
            'id_editor_cuota', 'Cuota'),
        'cantidad': fields.integer('Cantidad'),
        'clave': fields.many2one('survey', 'Cuestionario'),
        'realizadas': fields.integer('Realizadas'),
        'restantes': fields.integer('Restantes'),
    }


''' Control Encuestas
    Clase principal que controla las Cuotas del proyecto
    Tiene dos entidades débiles aociadas ea.tiraje y ea.cuotas
    el nombre es obsoleto
'''


class control_encuestas(osv.osv):
    _name = 'control_encuestas'
    _inherit = "mail.thread"

    def on_change_setname(self, cr, uid, ids, cotizacion_id, context=None):
        ret = {}
        values = {}
        for i in self.browse(cr, uid, ids, context):
            values['name'] = i.cotizacion_id.nombre_corto
        ret['value'] = values
        return ret

    _columns = {
        'id_control': fields.integer('Id control encuesta'),
        'nombre_estudio': fields.char('Nombre del estudio', sizze=120),
        'responsable': fields.many2one('res.users', 'responsible_id',
            'Responsable'),
        'encuesta': fields.one2many('editor_encuestas',
            'id_encuesta', 'Cuota'),
                'plaza': fields.many2one('ea.plaza', 'Plaza'),
    }