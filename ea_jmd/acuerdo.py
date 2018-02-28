# -*- coding: utf-8 -*-
from osv import osv, fields

class jmdacuerdo(osv.Model):
    _name = "ea.acuerdo"
    _inherit = "mail.thread"

    def get_cantidad(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            cantidad = 0
            for j in i.linea_ids:
                cantidad += j.cantidad
            ret[i.id] = cantidad
        return ret

    _columns = {
        'name': fields.char("Acuerdos"),
        'partner_id': fields.many2one("res.partner", string="SEA"),
        'proyecto_id': fields.many2one("project.project", string="Proyecto"),
        'fecha': fields.date("Fecha"),
        'parcialidades': fields.integer("Número de Parcialidades"),
        'precio_entrevista': fields.float("Precio por Entrevista"),
        'linea_ids': fields.one2many("ea.acuerdo.linea", "acuerdo_id", string="Lineas"),
        'nombre_corto': fields.related('proyecto_id', 'nombre_corto',
                string="Nombre Corto", type="char"),
        'cantidad': fields.function(get_cantidad, string="Cantidad", type="integer"),
        #contrato
        'solicitante': fields.char("Solicitante"),
        'prestador': fields.char("Prestador"),
        'para': fields.char("Para"),
        #Proyecto
        'fecha_hora': fields.datetime("Fecha y hora de capacitación"),
        'metodologia': fields.text("Metodología"),
        'tipo_entrevista': fields.char("Tipo de Entrevista"),
        'inicio': fields.date("Fecha de Inicio"),
        'termino': fields.char("Fecha de Fin"),
        'equipos': fields.integer("Equipos a participar"),
        'suervisores': fields.integer("Supervisores"),
        'investigadores': fields.integer("Investigadores"),
        'cuestionario_id': fields.many2one("ea.encuesta", string="Costos"),
        #Pagos
        'parcialidades': fields.integer("Número de Parcialidades"),
        'costo': fields.char("Costo por dispositivo móvil/internet"),
        }

class jmdacerdolinea(osv.Model):
    _name = "ea.acuerdo.linea"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.date("Fecha"),
        'cantidad': fields.float("Cantidad"),
        'acuerdo_id': fields.many2one("ea.acuerdo")
        }