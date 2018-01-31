# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class jmdpresupuestos(osv.Model):
    _name = 'ea.presupuesto'
    _description = 'Modelo de presupuesto'
    _inherit = "mail.thread"

    def calculate_total(self, cr, uid, ids, field_name, args, context=None):
        ret = {}
        total = 0.0
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = total
            #print("haciendo la suma para toda la cotización")
            for j in i.presupuesto_linea:
               # print("haciendo la suma para la plaza " + j.plaza.name)
                total += j.total
                #print("El total de la plaza es " + str(total))
                ret[i.id] = total
                #print("El valor de retorno es")
        return ret

    def aprobar(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            self.write(cr, uid, [i.id], {'aprobado': 'True'})
            1 == 1
        return ret

    def calculate_suggestion(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            #print("Id del registro = " + str(i.id))
            ret[i.id] = 0
            try:
                ret[i.id] = i.total * i.factor
            except ValueError:
                print("Error en los datos")
        return ret

    def set_ncorto(self, cr, uid, ids, proyecto, context=None):
            ret = {}
            values = {}
            for i in self.browse(cr, uid, ids, context):
                proj_obj = self.pool.get("project.project")
                for j in proj_obj.browse(cr, uid, proj_obj.search(cr, uid,
                    [("id", "=", proyecto)])):
                    values['claveproyecto'] = j.nombre_corto
            ret['value'] = values
            return ret

    _columns = {
        'name': fields.char(string="Nombre de la Planeación",
        size=80, translate=True),
        'proyecto': fields.many2one("project.project",
            string="Clave del Proyecto"),
        'claveproyecto': fields.char("Nombre Corto"),
        'fechadepresupuesto': fields.date("Fecha de la Planeación"),
        'presupuesto_linea': fields.one2many('ea.presupuesto_linea',
        'realtion_presupuesto', 'Linea de la Planeación'),
        'relation_saleorder': fields.one2many("sale.order", "budget",
        string="Orden de venta", ),
        'total': fields.function(calculate_total,
            string="Total presupuestado", type="float", digits=(9, 2)),
        'factor': fields.float("Factor Sugerido", digits=(4, 2)),
        'total_sugerido': fields.function(calculate_suggestion,
            string="Total sugerido", type="float", digits=(9, 2)),
        'deposito_ids': fields.one2many("ea_solicitud", "relation_presupuesto",
                string="Depósitos"),
        'aprobado': fields.boolean("Aprobado"),
        'productividad_estimada_gea': fields.float("Productividad estimada GEA"),
        'productividad_estimada_sea': fields.float("Productividad estimada SEA")
    }
    _defaults = {
            'factor': 1.0
        }


class jmdpresupuestoslinea(osv.Model):
    _name = 'ea.presupuesto_linea'
    _description = 'Linea del presupuesto'

    def calculate_total(self, cr, uid, ids, field_name, args, context=None):
        ret = {}
        total = 0.0
        try:
            for i in self.browse(cr, uid, ids, context):
                total = 0.0
                ret[i.id] = total
                for j in i.nosedeposita:
                    total += j.total
                for k in i.adepositar:
                    total += k.total
                for l in i.nominagea:
                    total += l.total
                for m in i.otros:
                    total += m.total
                ret[i.id] = total
        except ValueError:
            print("Error en los datos")
            total = 0.0
        return ret

    def get_name(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = str(i.plaza.name) + " " +\
                str(i.realtion_presupuesto.name)
        return ret

    def duplicate(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            linea_id = self.create(cr, uid, {'name': i.name,
        'realtion_presupuesto': i.realtion_presupuesto.id,
        'plaza_id': i.plaza_id.id,
        'ejecutivo': i.ejecutivo.id,
        'capacitacion': i.capacitacion.id,
        'piloto': i.piloto,
        'inicio': i.inicio,
        'fin': i.fin,
        }, context)
            for j in i.nosedeposita:
                self.pool.get("ea.concepto_nosedeposita").copy(
                cr, uid, j.id, {
                    'relation_presupuesto_linea': linea_id,
                    'cantidad': j.cantidad,
                    'dias': j.dias,
                    'costo': j.costo,
                })
            for j in i.adepositar:
                self.pool.get("ea.concepto_adepositar").copy(
                cr, uid, j.id, {
                    'relation_presupuesto_linea': linea_id,
                    'cantidad': j.cantidad,
                    'dias': j.dias,
                    'costo': j.costo,
                })
            for j in i.nominagea:
                self.pool.get("ea.concepto_nominagea").copy(
                cr, uid, j.id, {
                    'relation_presupuesto_linea': linea_id,
                    'cantidad': j.cantidad,
                    'dias': j.dias,
                    'costo': j.costo,
                })
            for j in i.otros:
                self.pool.get("ea.concepto_otros").copy(
                cr, uid, j.id, {
                    'relation_presupuesto_linea': linea_id,
                    'cantidad': j.cantidad,
                    'dias': j.dias,
                    'costo': j.costo,
                })
        return ret

    def autoload(self, cr, uid, ids, context=None):
        ret = {}
        #print("Autoloading")
        concepto_obj = self.pool.get("ea.presupuesto.concepto")
        for i in self.browse(cr, uid, ids, context):
            #A Depositar
            for j in concepto_obj.browse(cr, uid, concepto_obj.search(cr,
                uid, [('tipo', '=', 'adepositar')]), context):
                print(("Iterando en " + str(j.name).encode('ascii',
                    'ignore').decode('ascii')))
                vals = {
                        'name': str(j.name).encode('ascii',
                            'ignore').decode('ascii'),
                        'relation_presupuesto_linea': i.id,
                        'costo': j.monto,
                    }
                self.pool.get("ea.concepto_adepositar").create(cr,
                    uid, vals, context)
            #No se deposita
            for j in concepto_obj.browse(cr, uid, concepto_obj.search(cr,
                uid, [('tipo', '=', 'nosedeposita')]), context):
                print(("Iterando en " + str(j.name).encode('ascii',
                    'ignore').decode('ascii')))
                vals = {
                        'name': str(j.name).encode('ascii',
                            'ignore').decode('ascii'),
                        'relation_presupuesto_linea': i.id,
                        'costo': j.monto,
                    }
                self.pool.get("ea.concepto_nosedeposita").create(cr,
                    uid, vals, context)
            #Nomina GEA
            for j in concepto_obj.browse(cr, uid, concepto_obj.search(cr,
                uid, [('tipo', '=', 'nominagea')]), context):
                print(("Iterando en " + str(j.name).encode('ascii',
                    'ignore').decode('ascii')))
                vals = {
                        'name': str(j.name).encode('ascii',
                            'ignore').decode('ascii'),
                        'relation_presupuesto_linea': i.id,
                        'costo': j.monto,
                    }
                self.pool.get("ea.concepto_nominagea").create(cr,
                    uid, vals, context)
            #Otros
            for j in concepto_obj.browse(cr, uid, concepto_obj.search(cr,
                uid, [('tipo', '=', 'otros')]), context):
                print(("Iterando en " + str(j.name).encode('ascii',
                    'ignore').decode('ascii')))
                vals = {
                        'name': str(j.name).encode('ascii',
                            'ignore').decode('ascii'),
                        'relation_presupuesto_linea': i.id,
                        'costo': j.monto,
                    }
                self.pool.get("ea.concepto_otros").create(cr,
                    uid, vals, context)
        return ret

    def get_project(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.realtion_presupuesto.proyecto.id
        return ret

    def get_nproject(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.realtion_presupuesto.proyecto.name
        return ret

    def get_ncproject(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.realtion_presupuesto and i.realtion_presupuesto.proyecto:
                ret[i.id] = i.realtion_presupuesto.proyecto.nombre_corto
            else:
                ret[i.id] = "No Definido"
        return ret

    _columns = {
        'name': fields.function(get_name, string="ID", type="char"),
        'realtion_presupuesto': fields.many2one("ea.presupuesto",
        string="Presupuesto", ondelete="set null"),
        'plaza': fields.many2one('res.country.state.city', 'Plaza'),
        'ejecutivo': fields.many2one('hr.employee', 'Ejecutivo GEA'),
        'capacitacion': fields.many2one('event.event', 'Capacitacion'),
        'piloto': fields.date("Piloto"),
        'inicio': fields.date("Inicio"),
        'fin': fields.date('Fin'),
        'idproyecto': fields.function(get_project, string="Proyecto",
            type="integer"),
        'nproyecto': fields.function(get_nproject, string="Clave",
            type="char", store=True),
        'ncproyecto': fields.function(get_ncproject, string="Nombre Corto",
            type="char", store=False),
        'nosedeposita': fields.one2many('ea.concepto_nosedeposita',
            'relation_presupuesto_linea', string="Relacional con concepto",
            required=True),
        'adepositar': fields.one2many('ea.concepto_adepositar',
            'relation_presupuesto_linea', string="Relacional con concepto",
            required=True),
        'nominagea': fields.one2many('ea.concepto_nominagea',
            'relation_presupuesto_linea', string="Relacional con concepto",
            required=True),
        'otros': fields.one2many('ea.concepto_otros',
            'relation_presupuesto_linea', string="Relacional con concepto",
            required=True),
        'total': fields.function(calculate_total, method=True,
            type="float", digits=(9, 2), string="Total por plaza"),
        'plaza_id': fields.many2one('plaza', 'Plaza'),
   }


class jmdpresupuestoconcepto(osv.Model):
    def calculate_units(self, cr, uid, ids, field_name, args, context=None):
        ret = {}
        val = 0
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = val
            #print(("Intentado calcular el subtotal por concepto" +
            #str(i.cantidad) + "*" + str(i.dias)))
            val = 0
            try:
                val = i.cantidad * i.dias
                ret[i.id] = val
            except ValueError:
                print(("Valor no valido" + ValueError))

        return ret

    def calculate_total(self, cr, uid, ids, field_name, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            val = 0
            ret[i.id] = 0
            try:
                #print(("Intentado calcular el total por concepto" +
                #str(i.unidades) + "*" + str(i.costo)))
                val = i.unidades * i.costo
                ret[i.id] = val
            except ValueError:
                print(("Valor no válido" + ValueError))

        return ret

    _name = 'ea.presupuesto_concepto'

    _description = 'Conceptos de cada linea de presupuesto'
    _columns = {
        'name': fields.char(string="Concepto", size=40),
        'cantidad': fields.float('Cantidad'),
        'dias': fields.float('Dias'),
        'unidades': fields.function(calculate_units, method=True,
            type='float', string='Unidades'),
        'costo': fields.float('Costo', digits=(9, 2)),
        'total': fields.function(calculate_total, method=True, type='float',
            digits=(9, 2), args=None, string='Total'),
        }


class concepto_nosedeposita(osv.Model):
    _inherit = "ea.presupuesto_concepto"
    _name = "ea.concepto_nosedeposita"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_presupuesto_linea:
                ret[i.id] = i.relation_presupuesto_linea.\
                    realtion_presupuesto.proyecto.id
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_presupuesto_linea:
                ret[i.id] = i.relation_presupuesto_linea.\
                    plaza_id.id
        return ret

    def get_gastado(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.gasto_ids:
                ret[i.id] = ret[i.id] + j.monto
        return ret

    _columns = {
        'relation_presupuesto_linea': fields.many2one("ea.presupuesto_linea",
        string="No se deposita", ondelete="set null"),
        'gasto_ids': fields.one2many("ea.gasto.line.nosedeposita",
            'presupuestado_id', string="Ejercido"),
        'idproyecto': fields.function(get_proyecto, string="Id Proyecto",
            type="integer", store=True),
        'idplaza': fields.function(get_plaza, string="Id Plaza",
            type="integer", store=True),
        'gastado': fields.function(get_gastado, string="Total Ejercido",
            type="float", store=True),
        }


class concepto_adepositar(osv.Model):
    _inherit = "ea.presupuesto_concepto"
    _name = "ea.concepto_adepositar"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_presupuesto_linea:
                ret[i.id] = i.relation_presupuesto_linea.\
                    realtion_presupuesto.proyecto.id
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_presupuesto_linea:
                ret[i.id] = i.relation_presupuesto_linea.\
                    plaza_id.id
        return ret

    def get_gastado(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.gasto_ids:
                ret[i.id] = ret[i.id] + j.monto
        return ret

    _columns = {
        'relation_presupuesto_linea': fields.many2one("ea.presupuesto_linea",
        string="A depositar", ondelete="set null"),
        'gasto_ids': fields.one2many("ea.gasto.line.adepositar",
            'presupuestado_id', string="Ejercido"),
        'idproyecto': fields.function(get_proyecto, string="Id Proyecto",
            type="integer", store=True),
        'idplaza': fields.function(get_plaza, string="Id Plaza",
            type="integer", store=True),
        'gastado': fields.function(get_gastado, string="Total Ejercido",
            type="float", store=True),
        }


class concepto_nominagea(osv.Model):
    _inherit = "ea.presupuesto_concepto"
    _name = "ea.concepto_nominagea"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_presupuesto_linea:
                ret[i.id] = i.relation_presupuesto_linea.\
                    realtion_presupuesto.proyecto.id
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_presupuesto_linea:
                ret[i.id] = i.relation_presupuesto_linea.\
                    plaza_id.id
        return ret

    def get_gastado(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.gasto_ids:
                ret[i.id] = ret[i.id] + j.monto
        return ret

    _columns = {
        'relation_presupuesto_linea': fields.many2one("ea.presupuesto_linea",
        string="Nomina GEA", ondelete="set null"),
        'gasto_ids': fields.one2many("ea.gasto.line.nominagea",
            'presupuestado_id', string="Ejercido"),
        'idproyecto': fields.function(get_proyecto, string="Id Proyecto",
            type="integer", store=True),
        'idplaza': fields.function(get_plaza, string="Id Plaza",
            type="integer", store=True),
        'gastado': fields.function(get_gastado, string="Total Ejercido",
            type="float", store=True),
        }


class concepto_otros(osv.Model):
    _inherit = "ea.presupuesto_concepto"
    _name = "ea.concepto_otros"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_presupuesto_linea:
                ret[i.id] = i.relation_presupuesto_linea.\
                    realtion_presupuesto.proyecto.id
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_presupuesto_linea:
                ret[i.id] = i.relation_presupuesto_linea.\
                    plaza_id.id
        return ret

    def get_gastado(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.gasto_ids:
                ret[i.id] = ret[i.id] + j.monto
        return ret

    _columns = {
        'relation_presupuesto_linea': fields.many2one("ea.presupuesto_linea",
        string="Otros", ondelete="set null"),
        'gasto_ids': fields.one2many("ea.gasto.line.otros",
            'presupuestado_id', string="Ejercido"),
        'idproyecto': fields.function(get_proyecto, string="Id Proyecto",
            type="integer", store=True),
        'idplaza': fields.function(get_plaza, string="Id Plaza",
            type="integer", store=True),
        'gastado': fields.function(get_gastado, string="Total Ejercido",
            type="float", store=True),
        }