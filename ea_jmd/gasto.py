# -*- coding: utf-8 -*-
#IStandForFreedom
from osv import osv, fields
import time


class jmdgastos(osv.Model):
    _inherit = "mail.thread"
    _name = "ea.gasto"
    
    def copy(self, cr, uid, id, default=None, context=None): 
        return False 

    def action_solicitado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'solicitado'})
        return True

    def action_capturado(self, cr, uid, ids):
        self.write(cr, uid, ids, {
            'state': 'capturado',
            'fecha': time.strftime('%Y-%m-%d'),
            })
        return True

    def action_capturado2(self, cr, uid, ids):
        print("Capturando otra vez")
        return True

    def action_aprobado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'aprobado'})
        return True

    def action_enviado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'enviado'})
        return True

    def action_comprobaciones(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'comprobaciones'})
        return True

    def action_contabilidad(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'contabilidad'})
        return True
    
    def action_cancelado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'cancelado'})
        return True

    def calculate_total(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        total = 0
        for i in self.browse(cr, uid, ids, context):
            total += i.total_deducible
            total += i.total_no_deducible
            total += i.reembolso
        ret[i.id] = total
        return ret
    
    def put_monto(self, cr, uid, ids, context=None):
        monto = 0
        for i in self.browse(cr, uid, ids, context):
            for j in i.gasto_adepositar:
                monto += j.monto
            for j in i.gasto_nosedeposita:                
                monto += j.monto
            for j in i.gasto_nominagea:
                monto += j.monto
            for j in i.gasto_otros:
                monto += j.monto
            self.write(cr, uid, [i.id], {'total_comprobaciones': monto})

    def calculate_campo(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        total = 0
        #monto = 0
        for i in self.browse(cr, uid, ids, context):
            for j in i.gasto_adepositar:
                total += j.monto_campo
                #monto += j.monto
            for j in i.gasto_nosedeposita:
                total += j.monto_campo
                #monto += j.monto
            for j in i.gasto_nominagea:
                total += j.monto_campo
                #monto += j.monto
            for j in i.gasto_otros:
                total += j.monto_campo
                #monto += j.monto
            #self.write(cr, uid, [i.id], {'total_comprobaciones': monto})
        ret[i.id] = total
        return ret

    def calculate_comprobaciones(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        total = 0
        #monto = 0
        for i in self.browse(cr, uid, ids, context):
            for j in i.gasto_adepositar:
                total += j.monto_original
                #monto += j.monto
            for j in i.gasto_nosedeposita:
                total += j.monto_original
                #monto += j.monto
            for j in i.gasto_nominagea:
                total += j.monto_original
                #monto += j.monto
            for j in i.gasto_otros:
                total += j.monto_original
                #monto += j.monto
            #self.write(cr, uid, [i.id], {'total_comprobaciones': monto})
        ret[i.id] = total
        return ret

    def copia_montos(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            for j in i.gasto_adepositar:
                self.pool.get("ea.gasto.line.adepositar").write(cr, uid, [j.id], {
                    'monto': j.monto_campo,
                    'monto_original': j.monto_campo,
                    })
            for j in i.gasto_nosedeposita:
                self.pool.get("ea.gasto.line.nosedeposita").write(cr, uid, [j.id], {
                    'monto': j.monto_campo,
                    'monto_original': j.monto_campo,
                    })
            for j in i.gasto_nominagea:
                self.pool.get("ea.gasto.line.nominagea").write(cr, uid, [j.id], {
                    'monto': j.monto_campo,
                    'monto_original': j.monto_campo,
                    })
            for j in i.gasto_otros:
                self.pool.get("ea.gasto.line.otros").write(cr, uid, [j.id], {
                    'monto': j.monto_campo,
                    'monto_original': j.monto_campo,
                    })
        return ret


    def get_name(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = str(i.proyecto.name) + " " + str(i.plaza_id.name) +\
                " " + str(i.fecha)
        return ret
    
    def get_empresa(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = "No definido"
            if i.responsable and i.responsable.enterprise_id:
                ret[i.id] = i.responsable.enterprise_id.name
        return ret

    def get_diferencia(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        total_comprobado = 0
        total_depositado = 0
        for i in self.browse(cr, uid, ids, context):
            try:
                for j in i.gasto_adepositar:
                    if j.monto:
                        total_comprobado += j.monto
                for k in i.gasto_nosedeposita:
                    if k.monto:
                        total_comprobado += k.monto
                for l in i.gasto_nominagea:
                    if l.monto:
                        total_comprobado += l.monto
                for m in i.gasto_otros:
                    if m.monto:
                        total_comprobado += m.monto
                for n in i.solicitud_ids:
                    total_depositado += n.total_solicitud
            except:
                total_depositado = 0
                total_comprobado = 0
            ret[i.id] = total_depositado - total_comprobado
        return ret
    
    def copia_vales(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            self.write(cr, uid, ids, {
                'vales_comprobaciones': i.vales_campo,
                'total_comprobado_vales': i.vales.campo})

    _columns = {
            'name': fields.function(get_name, type="char",
                string="Proyecto Plaza Fecha", size=40, store=True),
            'fecha': fields.date("Fecha de Elaboración de Comprobación"),
            'plaza': fields.many2one("res.country.state.city", string="Plaza"),
            'plaza_id': fields.many2one("plaza", string="Plaza"),
            'proyecto': fields.many2one("project.project", string="Clave"),
            'nombre_corto': fields.related('proyecto', 'nombre_corto',
                string="Nombre Corto", type="char", store=True),
            'ok_contabilidad': fields.date("Ok Contabilidad"),
            'pid': fields.related("proyecto", "id", type="integer",
                string="Id Proyecto", readonly=True, store=True),
            'plid': fields.related("plaza_id", "id", type="integer",
                string="Id Plaza", readonly=True, store=True),
            'tipo': fields.selection([("Vales", "Vales"),("Efectivo", "Efectivo")], string="Tipo"),
            'state': fields.selection([('solicitado', 'Preliminar'),
                ('capturado', 'A Comprobar'),
                ('enviado', 'Ok GAC'), ('comprobaciones', 'Ok Contabilidad'),
                ('contabilidad', 'Ok Final'),
                ('aprobado', 'Aprobado'),
                ('cancelado', 'Cancelado')],
                "Estado", readonly=True),
            'gasto_adepositar': fields.one2many("ea.gasto.line.adepositar",
                "relation_gasto", string="Gastos"),
            'gasto_nosedeposita': fields.one2many("ea.gasto.line.nosedeposita",
                "relation_gasto", string="Gastos"),
            'gasto_nominagea': fields.one2many("ea.gasto.line.nominagea",
                "relation_gasto", string="Gastos"),
            'gasto_otros': fields.one2many("ea.gasto.line.otros",
                "relation_gasto", string="Gastos"),
            'empresa': fields.function(get_empresa, string="Empresa", type="string", store=False),
            'total_campo': fields.function(calculate_campo, string="Total Campo",
                 type="float", digits=(9, 2), store=True),
            'total_comprobaciones': fields.function(calculate_comprobaciones, string="Total Comprobaciones",
                 type="float", digits=(9, 2), store=True),
            'total': fields.function(calculate_total, string="TOTAL Aprobado Contabilidad",
                 type="float", digits=(9, 2), store=True),
            'responsable': fields.many2one("hr.employee", "Responsable"),
            'solicitud_ids': fields.many2many("ea_solicitud", "gas2sol",
                string="Depósitos"),
            'diferencia': fields.function(get_diferencia,
                string="Diferencia", type="float", store=True),
            'numero_poliza': fields.char("Número de Póliza"),
            'total_deducible': fields.float("Total Deducible"),
            'total_no_deducible': fields.float("Total No Deducible"),
            'reembolso': fields.float("Reembolso"),
            'notas': fields.text("Notas"),
            'formato_vales': fields.binary("Formato Vales"),
            'nformato': fields.char("Nombre del Formato"),
            'vales_campo': fields.float("Monto de Vales Campo"),
            'vales_comprobaciones': fields.float("Monto de Vales Comprobaciones"),
            'total_comprobado_vales': fields.float("Monto de Vales Autorizado Contabilidad"),
            'folio': fields.char("Folio"),
            'es_vale': fields.boolean("Vales"),
            'es_dinero': fields.boolean("Dinero"),
            'plaza': fields.many2one("plaza", string="Plaza de Origen"),
            'provincia_id': fields.many2one("ea.provincia", string="Plaza de Origen")
        }

    _defaults = {
        'folio': lambda self, cr, uid, context={}:
            self.pool.get('ir.sequence').get(cr, uid, 'ea.gasto'),
        }


class jmdgastosad(osv.Model):
    _name = "ea.gasto.line.adepositar"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_gasto and i.relation_gasto.proyecto:
                ret[i.id] = i.relation_gasto.proyecto.id
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_gasto and i.relation_gasto.proyecto:
                ret[i.id] = i.relation_gasto.plaza_id.id
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'presupuesto_linea_id': fields.many2one("ea.presupuesto.concepto",
                string="Concepto"),
            'monto': fields.float(digits=(9, 2), string="Monto Contabilidad"),
            'rechazado': fields.boolean("Modificado"),
            'monto_original': fields.float("Monto Comprobaciones"),
            'monto_campo': fields.float("Monto Campo"),
            'numero_comprobante': fields.char(string="Numero de Comprobante",
                size=40),
            #'documento': fields.binary("Comprobante"),
            'documento': fields.many2one("ir.attachment", string="Comprobante"),
            'ndocumento': fields.char("Nombre Comprobante"),
            'is_documento': fields.boolean("Comprobante"),
            'relation_gasto': fields.many2one("ea.gasto"),
            'observaciones': fields.text("Observaciones"),
            'state': fields.related('relation_gasto', 'state', type="char", string="Estado"),
            'presupuestado_id': fields.many2one("ea.concepto_adepositar",
                string="Presupuesto"),
            'idproyecto': fields.function(get_proyecto, string="Id Proyecto",
                type="integer"),
            'idplaza': fields.function(get_plaza, string="Id Plaza",
                type="integer"),
        }


class jmdnosedeposita(osv.Model):
    _name = "ea.gasto.line.nosedeposita"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_gasto and i.relation_gasto.proyecto:
                ret[i.id] = i.relation_gasto.proyecto.id
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_gasto and i.relation_gasto.proyecto:
                ret[i.id] = i.relation_gasto.plaza_id.id
        return ret

    def create(self, cr, uid, vals, context=None):
        vals['monto_original'] = 0
        vals['monto'] = 0
        return super(jmdnosedeposita,self).create(cr, uid, vals, context=context)

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'presupuesto_linea_id': fields.many2one("ea.presupuesto.concepto",
                string="Concepto"),
            'monto': fields.float(digits=(9, 2), string="Monto Contabilidad"),
            'rechazado': fields.boolean("Modificado"),
            'monto_original': fields.float("Monto Comprobaciones"),
            'monto_campo': fields.float("Monto Campo"),
            'numero_comprobante': fields.char(string="Numero de Comprobante",
                size=40),
            # 'documento': fields.binary("Comprobante"),
            'documento': fields.many2one("ir.attachment", string="Comprobante"),
            'ndocumento': fields.char("Nombre Comprobante"),
            'is_documento': fields.boolean("Comprobante"),
            'relation_gasto': fields.many2one("ea.gasto"),
            'observaciones': fields.text("Observaciones"),
            'state': fields.related('relation_gasto', 'state', type="char", string="Estado"),
            'presupuestado_id': fields.many2one("ea.concepto_nosedeposita",
                string="Presupuesto"),
            'idproyecto': fields.function(get_proyecto, string="Id Proyecto",
                type="integer"),
            'idplaza': fields.function(get_plaza, string="Id Plaza",
                type="integer"),
        }


class jmdnominagea(osv.Model):
    _name = "ea.gasto.line.nominagea"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_gasto and i.relation_gasto.proyecto:
                ret[i.id] = i.relation_gasto.proyecto.id
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_gasto and i.relation_gasto.proyecto:
                ret[i.id] = i.relation_gasto.plaza_id.id
        return ret

    def create(self, cr, uid, vals, context=None):
        vals['monto_original'] = 0
        vals['monto'] = 0
        return super(jmdnominagea,self).create(cr, uid, vals, context=context)

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'presupuesto_linea_id': fields.many2one("ea.presupuesto.concepto",
                string="Concepto"),
            'monto': fields.float(digits=(9, 2), string="Monto Contabilidad"),
            'rechazado': fields.boolean("Modificado"),
            'monto_original': fields.float("Monto Comprobaciones"),
            'monto_campo': fields.float("Monto Campo"),
            'numero_comprobante': fields.char(string="Numero de Comprobante",
                size=40),
            #'documento': fields.binary("Comprobante"),
            'documento': fields.many2one("ir.attachment", string="Comprobante"),
            'ndocumento': fields.char("Nombre Comprobante"),
            'is_documento': fields.boolean("Comprobante"),
            'relation_gasto': fields.many2one("ea.gasto"),
            'observaciones': fields.text("Observaciones"),
            'state': fields.related('relation_gasto', 'state', type="char", string="Estado"),
            'presupuestado_id': fields.many2one("ea.concepto_nominagea",
                string="Presupuesto"),
            'idproyecto': fields.function(get_proyecto, string="Id Proyecto",
                type="integer"),
            'idplaza': fields.function(get_plaza, string="Id Plaza",
                type="integer"),
        }


class jmdotros(osv.Model):
    _name = "ea.gasto.line.otros"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_gasto and i.relation_gasto.proyecto:
                ret[i.id] = i.relation_gasto.proyecto.id
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_gasto and i.relation_gasto.proyecto:
                ret[i.id] = i.relation_gasto.plaza_id.id
        return ret

    def create(self, cr, uid, vals, context=None):
        vals['monto_original'] = 0
        vals['monto'] = 0
        return super(jmdotros,self).create(cr, uid, vals, context=context)

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'presupuesto_linea_id': fields.many2one("ea.presupuesto.concepto",
                string="Concepto"),
            'monto': fields.float(digits=(9, 2), string="Monto Contabilidad"),
            'rechazado': fields.boolean("Modificado"),
            'monto_original': fields.float("Monto Comprobaciones"),
            'monto_campo': fields.float("Monto Campo"),
            'numero_comprobante': fields.char(string="Numero de Comprobante",
                size=40),
            #'documento': fields.binary("Comprobante"),
            'documento': fields.many2one("ir.attachment", string="Comprobante"),
            'ndocumento': fields.char("Nombre Comprobante"),
            'is_documento': fields.boolean("Comprobante"),
            'relation_gasto': fields.many2one("ea.gasto"),
            'observaciones': fields.text("Observaciones"),
            'state': fields.related('relation_gasto', 'state', type="char", string="Estado"),
            'presupuestado_id': fields.many2one("ea.concepto_otros",
                string="Presupuesto"),
            'idproyecto': fields.function(get_proyecto, string="Id Proyecto",
                type="integer"),
            'idplaza': fields.function(get_plaza, string="Id Plaza",
                type="integer"),
        }
