# -*- coding: utf-8 -*-
from osv import osv
from osv import fields

class JmdCostos(osv.osv):
    _name = 'ea.costos'
    _inherit = "mail.thread"
    _description = 'ea.costos'
    
    def calcula_costos(self, cr, uid, ids, context=None):
        ret = {}
        bono_obj = self.pool.get("hr.bonos")
        avance_obj = self.pool.get("ea.avance")
        proyecto_obj = self.pool.get("project.project")
        line_obj = self.pool.get("ea.costos.line")
        cr.execute("DELETE FROM ea_costo_detail")
        for i in self.browse(cr, uid, ids, context):
            for p in proyecto_obj.browse(cr, uid, proyecto_obj.search(cr, uid, [('etapa', '=', 'proyecto')])):
                try:
                    print("Proyecto " + str(p.name))
                except:
                    print("Proyecto nombre raro")
                total_bonos = 0
                total_nomina = 0
                for b in bono_obj.browse(cr, uid, bono_obj.search(cr, uid, [('proyecto_id', '=', p.id)])):
                    print("Encontre un bono")
                    self.pool.get("ea.costo.detail").create(cr, uid, {
                        'name': p.id,
                        'persona': b.empleado.id,
                        'fecha': b.fecha,
                        'monto': b.monto})
                    total_bonos += b.monto
                    print("Valgo " + str(total_bonos))
                    print("El bono fue de " + str(b.monto))
                for a in avance_obj.browse(cr, uid, avance_obj.search(cr, uid, [('proyecto', '=', p.id)])):
                    for c in a.costo_ids:
                        total_nomina += c.salario_diario
                        self.pool.get("ea.costo.detail").create(cr, uid, {
                            'name': p.id,
                            'persona': c.id,
                            'fecha': a.fecha,
                            'monto': c.salario_diario})
                line_obj.create(cr, uid, {
                    'name': p.id,
                    'bonos': total_bonos,
                    'nomina': total_nomina,
                    'costo_id': i.id})
            
        return ret
 
    _columns = {
            'name':fields.char("Distribución de Costos"),
            'inicio': fields.date("Fecha de Inicio"),
            'fin': fields.date("Fecha de Fin"),
            'line_ids': fields.one2many("ea.costos.line", "costo_id", string="Lineas")
        }
JmdCostos()

class JMDCostoLine(osv.osv):
    _name="ea.costos.line"
    _columns = {
            'name': fields.many2one("project.project", string="Proyecto"),
            'bonos': fields.float("Monto en Bonos"),
            'nomina': fields.float("Monto por Nóminas"),
            "costo_id": fields.many2one("ea.costos", strin="Costo")
                    }
    

class JMDCostoDetail(osv.osv):
    _name = 'ea.costo.detail'
    _description = 'Detalle de los costos'
 
    _columns = {
            'name': fields.many2one("project.project", string="Proyecto"),
            'persona': fields.many2one("hr.employee", string="Persona"),
            'fecha': fields.date("Fecha"),
            'monto': fields.float("Monto")
        }
JMDCostoDetail()
