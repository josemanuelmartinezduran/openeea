# -*- coding: utf-8 -*-
from osv import osv, fields

class jmdconcliacion(osv.Model):
    _name = "ea.conciliacion"
    _inherit = "mail.thread"

    def actualiza(self, cr, uid, ids, context=None):
        facturas_obj = self.pool.get("ea.conciliacion.facturas")
        inv_obj = self.pool.get("account.invoice")
        acuerdo_obj = self.pool.get("ea.acuerdo")
        solicitadas_obj = self.pool.get("ea.conciliacion.solicitadas")
        avance_obj = self.pool.get("ea.avance")
        realizadas_obj = self.pool.get("ea.conciliacion.realizadas")
        for i in self.browse(cr, uid, ids, context):
            #Buscamos las facturas de provedor
            for j in inv_obj.browse(cr, uid, inv_obj.search(cr, uid, [('partner_id', '=', i.name.id)])):
                facturas_obj.create(cr, uid, {
                    'name': j.name,
                    'fecha': j.date_invoice,
                    'monto': j.amount_total,
                    'conciliacion_id': i.id})
            #Entrevistas solicitadas
            for j in acuerdo_obj.browse(cr, uid, acuerdo_obj.search(cr, uid, [('partner_id', '=', i.name.id)])):
                solicitadas_obj.create(cr, uid, {
                    'name': j.name,
                    'cantidad': j.cantidad,
                    'conciliacion_id': i.id})
            #Entrevistas realizadas
            for j in avance_obj.browse(cr, uid, avance_obj.search(cr, uid, [('codigo_sea', '=', i.name.id)])):
                realizadas_obj.create(cr, uid, {
                    'name': j.name,
                    'conciliacion_id': i.id})


    _columns = {
        'name': fields.many2one("res.partner", string="Nombre del SEA"),
        'proyecto_id': fields.many2one("project.project", string="Proyecto"),
        'nombre_corto': fields.related('proyecto_id', 'nombre_corto',
                string="Nombre Corto", type="char"),
        'cantidad_solicitada': fields.integer("Cantidad Solicitada"),
        'precio_entrevista': fields.float("Precio por Entrevista"),
        'monto_planeado': fields.float("Monto Planeado"),
        'cantidad_realizada': fields.float("Cantidad Realizada"),
        'monto_facturado': fields.float("Monto Facturado"),
        'diferencia': fields.integer("Diferencia"),
        'factura_ids': fields.one2many("ea.conciliacion.facturas", "conciliacion_id", string="Facturas"),
        'realizadas_ids': fields.one2many("ea.conciliacion.realizadas", "conciliacion_id", string="Realizadas"),
        'solicitadas_ids': fields.one2many("ea.conciliacion.solicitadas", "conciliacion_id", string="Solicitadas"),
        }


class jmdfacturas(osv.Model):
    _name = "ea.conciliacion.facturas"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Numero"),
        'fecha': fields.date("Fecha"),
        'monto': fields.float("Monto"),
        'conciliacion_id': fields.many2one("ea.conciliacion", string="Conciliación"),
        }


class jmdrealizadas(osv.Model):
    _name = "ea.conciliacion.realizadas"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Numero de Reporte"),
        'fecha': fields.date("Fecha"),
        'cantidad': fields.float("Cantidad"),
        'conciliacion_id': fields.many2one("ea.conciliacion", string="Conciliación"),
        }

class jmdsolicitadas(osv.Model):
    _name = "ea.conciliacion.solicitadas"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Reporte de Campo"),
        'cantidad': fields.integer("Cantidad"),
        'conciliacion_id': fields.many2one("ea.conciliacion", string="Conciliación"),
        }