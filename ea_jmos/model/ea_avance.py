#-*- coding: utf-8 -*-
from openerp.osv import fields, osv
from datetime import *


class ea_avance_jmos(osv.Model):

    _inherit = 'ea.avance'

    def name_onchange(self, cr, uid, ids, proyecto, plaza_id, fecha,
        context=None):

        res = {}

        proyecto_str = ''
        plaza_str = ''
        fecha_str = ''
        nombre = ''

        obj_project = self.pool.get('project.project')
        obj_plaza = self.pool.get('plaza')

        search_project = obj_project.search(cr, uid, [('id', '=', proyecto)],
            context)
        search_plaza = obj_plaza.search(cr, uid, [('id', '=', plaza_id)],
            context)

        for proyect in obj_project.browse(cr, uid, search_project, context):
            proyecto_str = proyect.name

        for plaz in obj_plaza.browse(cr, uid, search_plaza, context):
            plaza_str = str(plaz.codigo)

        fecha_str = fecha

        nombre = proyecto_str + '/' + plaza_str + '/' + fecha_str

        res = {'name': nombre}

        return {'value': res}

    #def _get_hora(self, cr, uid, ids, field_name, args, context=None):
        #print('Oteniendo la hora')

        #ret = {}

        #for move in self.browse(cr, uid, ids, context):
            #fecha_hora = datetime.today().time().strftime('%H:%M')
            #ret[move.id] = fecha_hora

        #print('La fecha_hora es: ', ret)

        #return ret

    _columns = {
        'plaza_id': fields.many2one('plaza', 'Plaza'),
        #'hora_envio': fields.float('Hora de envio'),
    }