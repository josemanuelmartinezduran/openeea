# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


##### Comentarios
##### CEMG
##### HyD 2014


#### Clase para la vista de Presentación ####
class project_presentacion(osv.Model):
    _name = 'project.presentacion'
    #Workflow functions
    #new state

    def action_new(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'nueva'})
        return True

    def action_aprobado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'aprobado'})
        return True

    def action_entregada(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'entregada'})
        return True

    _description = 'Campos para presentacion'
    _columns = {
        'name': fields.many2one('project.project','Nombre del proyecto'),
        'state': fields.selection([('nueva', 'Nueva'), ('aprobado', 'Aprobada'),
                                   ('entregada', 'Entregada')] , "Estado", readonly=True),
        'archivo': fields.binary(string="Archivo de la presentacion"),
        'filename': fields.char("Filename"),
        'fecha_entrega': fields.date('Fecha de entrega'),
        }