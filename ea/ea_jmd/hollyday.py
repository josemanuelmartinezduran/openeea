# -*- coding: utf-8 -*-
from osv import osv, fields
import datetime


class jmdhollyday(osv.Model):
    _inherit = "hr.holidays"
    
    _columns={
            'periodo_dias': fields.date("Periodo Días"),
            'limite': fields.date("Fecha Límite")
        }
    #def send_hollyday(self,  cr,  uid,  ids,  context=None):
    #    for i in self.browse(cr,  uid,  ids,  conext):
    #        if(i.hollyday_status_id.genera_bono):
                #Generamos en bono
                
    
    
    #class jmdhollydystatuss(osv.Model):
    #    _inherit="hr.hollyday.status"
    #    _columns = {
    #'genera_bono': fields.boolean("Genera Bono"), 
    #'tipo_bono': fields.selection([("Monto",  "Monto"),  ("Dias",  "Dias")],  string="Tipo de Bono"), 
    # 'cantidad': fields.float("Monto/Diás Otorgados") 
    #}
