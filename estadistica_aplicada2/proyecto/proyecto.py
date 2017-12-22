# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class proyecto(osv.Model):
    _inherit = 'project.project'
    _description = 'Modulo de proyecto para Estadistica Aplicada'
    _columns = {
        'clave_proyecto': fields.char("Clave de Proyecto", size=20),
        'ejecutivo_id': fields.many2one('hr.employee', 'Ejecutivo'),
        'tamano_cuenta': fields.selection([('chica', 'Chica'),
            ('mediana', 'Mediana'), ('grande', 'Grande')],
            string='Tamaño de cuenta'),
        'num_encuestas': fields.integer('Numero de encuestas'),
        'fecha_inicio': fields.date('Fecha de inicio'),
        'fecha_final': fields.date('Fecha final'),
        'arranques_line': fields.one2many('project.arranques', 'name',
            'Arranques'),
        'etapa': fields.selection([('arranques', 'Arranques'),
            ('campo', 'Campo'), ('pi', 'Procesos intermedios'),
            ('procesamiento', 'Procesamientos'), ('analisis', 'Analisis'),
            ('entrega', 'Entrega'), ('proyecto', 'Proyecto'),
            ('diseno', 'Diseño'), ('supervision', 'Supervisión de Oficina')],
            'Etapa')
    }


class tarea(osv.Model):
    _inherit = 'project.task'
    _description = 'Modulo de proyecto tarea para Estadistica Aplicada'
    _columns = {
        'area': fields.selection([('arranques', 'Arranques'),
            ('campo', 'Campo'), ('procesos_intermedios',
            'Procesos intermedios'), ('procesamiento', 'Procesamiento'),
            ('analisis', 'Analisis'), ('entrega', 'Entrega')], 'Area'),
    }