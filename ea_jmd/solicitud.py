# -*- coding: utf-8 -*-
from osv import osv, fields
import time
from datetime import datetime, timedelta


class account_solicitud(osv.Model):
    _name = "ea_solicitud"
    _inherit = "mail.thread"
    
    def copy(self, cr, uid, id, default=None, context=None): 
        return False

    def action_draft(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def action_cancelado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'cancelado'})
        return True

    def action_nuevo(self, cr, uid, ids):
        print("La fecha es")
        print(time.strftime('%Y-%m-%d'))
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        self.write(cr, uid, ids,
            {
                'state': 'new',
                'hora_solicitud': time.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return True

    def action_contraloria(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'contraloria'})
        return True

    def action_contabilidad(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'contabilidad'})
        return True
    
    def onchange_solicitante(self, cr, uid, ids, solicitante_id, context=None):
        vals = {}
        emp_obj = self.pool.get("hr.employee")
        for i in emp_obj.browse(cr, uid, emp_obj.search(cr, uid, [('id', '=', solicitante_id)])):
            vals['empresa'] = i.enterprise_id.id
        return {'value': vals}

    def action_gac(self, cr, uid, ids):
        print("La fecha es ------------------------------")
        a = lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
        print(a)
        now = datetime.now()
        #now -= timedelta(days=1)
        now2 = datetime.now()
        now2 += timedelta(hours=2)
        self.write(cr, uid, ids, {
            'state': 'gac',
            'fecha_autorizacion': now.strftime('%Y-%m-%d'),
            'hora_alerta': now2.strftime('%Y-%m-%d %H:%M:%S'),
            'autorizo_gac': uid,
            })
        return True

    def duplicar(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            self.copy(cr, uid, i.id, {
                'name': self.pool.get('ir.sequence').get(cr, uid, 'ea.solicitud')})
        return True

    def get_comprobado(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.gasto_ids:
                if j.state in ["capturado", "enviado", "aprobado", "contabilidad", "comprobaciones"]:
                    ret[i.id] += j.total
                    ret[i.id] += j.total_comprobado_vales
            if ret[i.id] >= i.total_solicitud:
                self.write(cr, uid, [i.id], {
                            'comprobado': True})
            else:
                self.write(cr, uid, [i.id], {
                            'comprobado': False})
        return ret

    def get_deducible(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.gasto_ids:
                if j.state in ["capturado", "enviado", "aprobado", "contabilidad", "comprobaciones"]:
                    ret[i.id] += j.total_deducible
        return ret

    def get_reembolso(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.gasto_ids:
                if j.state in ["capturado", "enviado", "aprobado", "contabilidad", "comprobaciones"]:
                    ret[i.id] += j.reembolso
        return ret

    def get_no_deducible(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.gasto_ids:
                if j.state in ["enviado", "aprobado", "contabilidad", "comprobaciones"]:
                    ret[i.id] += j.total_no_deducible
        return ret

    def get_vales(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.gasto_ids:
                if j.state in ["capturado","enviado", "aprobado", "contabilidad", "comprobaciones"]:
                    ret[i.id] += j.total_comprobado_vales
        return ret

    def ve_bancos(self, cr, uid, ids, fieldname, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = False
            print("El usuario puede ver nomina?")
            print((self.pool.get('res.users').has_group(cr, uid,
                'ea_jmd.ver_bancos')))
            if self.pool.get('res.users').has_group(cr, uid,
                'ea_jmd.ver_bancos'):
                res[i.id] = True
        return res

    def get_saldo_dinero(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            total = 0
            for j in i.gasto_ids:
                if j.state in ["capturado", "enviado", "aprobado", "contabilidad", "comprobaciones"]:
                    total += j.total
            ret[i.id] = i.monto - total
        return ret

    def get_saldo_vales(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            total = 0
            for j in i.gasto_ids:
                if j.state in ["capturado", "enviado", "aprobado", "contabilidad", "comprobaciones"]:
                    total += j.total_comprobado_vales
            ret[i.id] = i.total_vales - total
        return ret

    def get_saldo_total(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            total = 0
            for j in i.gasto_ids:
                if j.state in ["capturado", "enviado", "aprobado", "contabilidad", "comprobaciones"]:
                    total += j.total + j.total_comprobado_vales
            ret[i.id] = i.monto + i.total_vales - total
        return ret

    def set_bank(self, cr, uid, ids, data, context=None):
            ret = {}
            values = {}
            employee_obj = self.pool.get("hr.employee")
            for i in employee_obj.browse(cr, uid, [data], context):
                values['beneficiario'] = i.beneficiario
                values['banco'] = i.banco
                values['cuenta'] = i.cuenta
                values['empresa'] = i.enterprise_id.id
            ret['value'] = values
            return ret

    def calculate_vales(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.vales:
                ret[i.id] = ret[i.id] + j.name * j.cantidad
        return ret

    def calculate_solicitud(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.vales:
                ret[i.id] = ret[i.id] + j.name * j.cantidad
            ret[i.id] = ret[i.id] + i.monto
        return ret

    def corregir(self, cr, uid, ids, context=None):
        print("En el metodo corregir()")
        em_obj = self.pool.get("hr.employee")
        for i in self.browse(cr, uid, ids, context):
            if not i.beneficiario:
                return
            nip = i.beneficiario[:i.beneficiario.find(" ")]
            print("EL NIP ES: " + nip)
            id_empleado = 0
            if nip.isdigit():
                for j in em_obj.browse(cr, uid, em_obj.search(cr, uid, [('name', '=', nip)]), context):
                    id_empleado = j.id
                print("Es numérico")
            else:
                print("Son letras")
            self.write(cr, uid, [i.id], {'responsable': id_empleado}, context)

    def correct_all(self, cr, uid, ids, context):
        s_obj = self.pool.get("ea_solicitud");
        for i in s_obj.browse(cr, uid, s_obj.search(cr, uid, []), context):
            i.corregir()

    def set_deposito(self, cr, uid, ids, args, context=None):
        res = {}         
        res['fecha_deposito'] = args
        return {'value': res}
    
    def set_company(self, cr, uid, ids, args, context=None):
        res = {}
        for i in self.pool.get("hr.employee").browse(cr, uid, [args], context):
            res['empresa'] = i.enterprise_id.id
        return {'value': res}
    
    def set_total(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            total = 0
            for j in i.adepositar:
                total = total + (j.pu * j.ct)
            for j in i.nosedeposita:
                total = total + (j.pu * j.ct)
            for j in i.nominagea:
                total = total + (j.pu * j.ct)
            for j in i.otros:
                total = total + (j.pu * j.ct)
            self.write(cr, uid, [i.id], {'monto': total})
        return


    _columns = {
        'name': fields.char(string="Consecutivo", size=40),
        'motivo': fields.char(string="Motivo de la Solicitud"),
        'monto': fields.float(string="Total Dinero", digits=(9, 2)),
        'monto_ejercido': fields.float(string="Monto Ejercido"),
        'fecha_limite': fields.date(string="Fecha de Programación de Depósito"),
        'beneficiario': fields.char(string="Beneficiario (Obsoleto)"), #Debe ser Solicitante
        'solicitante_id': fields.many2one("hr.employee", string="Solicitante"),
        'hora_alerta': fields.datetime("Hora de Alerta"),
        'fecha_autorizacion': fields.date(string="Fecha de Autorización"),
            'fecha_deposito': fields.date("Fecha de Depósito/Entrega"),
            'state': fields.selection([('draft', 'Borrador'),
                ('new', 'Enviado'),
                ('contraloria', 'Ok Comprobaciones'),
                ('gac', 'Ok GAC/DPYA'),
                ('contabilidad', 'Ok Contraloría'), ('cancelado', 'Cancelado')],
                "Estado", readonly=True),
            'observaciones': fields.text("Observaciones"),
            'vales': fields.one2many("ea.vales", 'relation_solicitud', 'Vales'),
            'relation': fields.many2one("ea.gasto"),
            'relation_presupuesto': fields.many2one("ea.presupuesto"),
            'total_vales': fields.function(calculate_vales,
                string="Total de Vales", type="float", store=True),
            'comprobado_vales': fields.function(get_vales,
                type="float", string="Total de Vales Comprobado"),

            'total_deducible': fields.function(get_deducible,
                type="float", string="Total Deducible"),
            'reembolso': fields.function(get_reembolso,
                type="float", string="Reembolso"),
            'total_no_deducible': fields.function(get_no_deducible,
                type="float", string="Total no Deducible"),
            'total_solicitud': fields.function(calculate_solicitud,
                string="Total", type="float", store=True),
            'proyecto': fields.many2one("project.project", string="Proyecto"),
            'nombre_corto': fields.related('proyecto', 'nombre_corto',
                string="Nombre Corto", type="char"),
            'plaza': fields.many2one("plaza", string="Plaza/Ruta a Trabajar"),
            'plazao': fields.many2one("plaza", string="Plaza de Origen"),
            'empresa': fields.many2one("ea.enterprise", string="Empresa"),
            'responsable': fields.many2one("hr.employee", string="Beneficiario"),
            'tipo': fields.char("Tipo de Depósito"),
            'banco': fields.char("Banco"),
            'cuenta': fields.char("Número de Cuenta"),
            'comprobado': fields.boolean("Comprobación OK"),
            'tipo': fields.selection([("anticipo", "Anticipo"),
                ("reembolso", "Reembolso")], string="Tipo de Depósito"),
            'requiere_vales': fields.boolean("Requiere Vales"),
            'requiere_efectivo': fields.boolean("Requiere Efectivo"),
            'gasto_ids': fields.many2many("ea.gasto", "gas2sol",
                string="Registro de Gastos"),
            'total_comprobado': fields.function(get_comprobado,
                string="Total Comprobado", type="float"),
            'adepositar': fields.one2many("ea.solicitud.adepositar",
                "solicitud_id", string="A Depositar"),
            'nosedeposita': fields.one2many("ea.solicitud.nosedeposita",
                "solicitud_id", string="No Se Deposita"),
            'nominagea': fields.one2many("ea.solicitud.nominagea",
                "solicitud_id", string="Nomina GEA"),
            'otros': fields.one2many("ea.solicitud.otros",
                "solicitud_id", string="DHPROD"),
            'autorizo_gac': fields.many2one("res.users", string="Autorizado por"),
            'hora_solicitud': fields.datetime("Hora de Solicitud"),
            'solicitud_extra': fields.boolean("Solicitud Extraordinaria"),
            'saldo_dinero': fields.function(get_saldo_dinero,
                type="float", string="Saldo en Dinero"),
            'saldo_vales': fields.function(get_saldo_vales,
                type="float", string="Saldo en Vales"),
            'saldo_total': fields.function(get_saldo_total,
                type="float", string="Saldo General"),
            've_bancos': fields.function(ve_bancos, string="Ve Bancos",
                type="boolean", store=False),
            'provincia_id': fields.many2one("ea.provincia", string="Plaza Origen")
        }

    _defaults = {
        'name': lambda self, cr, uid, context={}:
            self.pool.get('ir.sequence').get(cr, uid, 'ea.solicitud'),
        'hora_solicitud': lambda *a:
            time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class jmdvale(osv.Model):
    _name = "ea.vales"

    def calculate_monto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.cantidad * i.name
        return ret

    def getproject(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.relation_solicitud.proyecto.name
        return ret

    _columns = {
            'name': fields.float(string="Denominación"),
            'cantidad': fields.integer("Cantidad"),
            'monto': fields.function(calculate_monto, string="Monto",
                type="float", store=False),
            'tipo': fields.selection([("Stock", "Stock"),
                    ("Comprado", "Comprado")], string="Tipo de Vale"),
            'relation': fields.many2one("purchase.moneyrequest"),
            'relation_solicitud': fields.many2one("ea_solicitud"),
            'project': fields.function(getproject, string="Proyecto",
                type="char")
        }


class jmdadepositar(osv.Model):
    _name = "ea.solicitud.adepositar"

    def get_total(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.ct * i.pu
        return ret

    _columns = {
            'name': fields.many2one("ea.presupuesto.concepto",
                string="Concepto"),
            'descripcion': fields.char("Descripcion"),
            'pu': fields.float("Costo Unitario"),
            'ct': fields.float("Cantidad"),
            'monto': fields.function(get_total, type="float",
                string="Total"),
            'solicitud_id': fields.many2one("ea_solicitud")
        }


class jmdnsd(osv.Model):
    _name = "ea.solicitud.nosedeposita"

    def get_total(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.ct * i.pu
        return ret

    _columns = {
            'name': fields.many2one("ea.presupuesto.concepto",
                string="Concepto"),
            'descripcion': fields.char("Descripcion"),
            'pu': fields.float("Costo Unitario"),
            'ct': fields.float("Cantidad"),
            'monto': fields.function(get_total, type="float",
                string="Total"),
            'solicitud_id': fields.many2one("ea_solicitud")
        }


class jmdnomina(osv.Model):
    _name = "ea.solicitud.nominagea"

    def get_total(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.ct * i.pu
        return ret

    _columns = {
            'name': fields.many2one("ea.presupuesto.concepto",
                string="Concepto"),
            'descripcion': fields.char("Descripcion"),
            'pu': fields.float("Costo Unitario"),
            'ct': fields.float("Cantidad"),
            'monto': fields.function(get_total, type="float",
                string="Total"),
            'solicitud_id': fields.many2one("ea_solicitud")
        }


class jmdotros(osv.Model):
    _name = "ea.solicitud.otros"

    def get_total(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.ct * i.pu
        return ret

    _columns = {
            'name': fields.many2one("ea.presupuesto.concepto",
                string="Concepto"),
            'descripcion': fields.char("Descripcion"),
            'pu': fields.float("Costo Unitario"),
            'ct': fields.float("Cantidad"),
            'monto': fields.function(get_total, type="float",
                string="Total"),
            'solicitud_id': fields.many2one("ea_solicitud")
        }