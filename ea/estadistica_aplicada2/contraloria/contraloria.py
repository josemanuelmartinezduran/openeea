# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class cajachica(osv.Model):
    _name = 'purchase.cajachica'
    _description = 'Modulo Resumen de Caja Chica para Estadistica Aplicada'
    _columns = {
        'name': fields.text("Nombre")
    }


class analisiscampo(osv.Model):
    _name = 'purchase.analisiscampo'
    _columns = {
        'name': fields.text("Nombre")
    }


class auditoria(osv.Model):
    _name = 'purchase.auditoria'
    _description = 'Modulo Auditoria para Estadistica Aplicada'
    _columns = {
        'name': fields.text("Nombre")
    }


class noconforme(osv.Model):
    _name = 'purchase.noconforme'
    _description = 'Modulo No Conformidad para Estadistica Aplicada'
    _columns = {
        'name': fields.text("Nombre")
    }


class racs(osv.Model):
    _name = 'purchase.racs'
    _description = 'Modulo RACs para Estadistica Aplicada'
    _columns = {
        'name': fields.text("Nombre")
    }


class presupuesto(osv.Model):
    _inherit = 'purchase.order'
    _descripction = 'Campos para orden de compra Estadistica Aplicada'
    _columns = {
        'proyecto': fields.many2one('project.project', 'Proyecto'),
        'justificacion': fields.text('Justifiacion de solicitud')
    }