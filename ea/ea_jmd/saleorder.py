# -*- coding: utf-8 -*-
from osv import osv, fields
from datetime import datetime


class jmdsaleorder(osv.Model):
    _inherit = "sale.order"

    def create(self, cr, uid, vals, context=None):
        now = datetime.now()
        cur_month = now.strftime("%m")
        cur_year = now.strftime("%y")
        partner_id = vals.get('partner_id')
        partner_object = self.pool.get("res.partner")
        partner_ref = ""
        max_id = "01"
        for i in partner_object.browse(cr, uid, [partner_id]):
            partner_ref = i.referencia
        #Buscando la ultima cotización del mes
        for j in self.browse(cr, uid, self.search(cr, uid, [(1, "=", 1)])):
            if j.name[-4:-2] == cur_month:
                try:
                    intval = int(j.name[-2:])
                    intmax = int(max_id)
                    if intval >= intmax:
                        intmax = intval + 1
                        max_id = str(intmax)
                        if intmax < 10:
                            max_id = "0" + str(intmax)
                except ValueError:
                    print("Warning wrong quotation code ")
        if vals.get('name', '/') == '/':
            vals['name'] = partner_ref + "-" + cur_year + cur_month + \
            max_id or '/'
        return super(jmdsaleorder, self).create(cr, uid, vals, context=context)

    def addversion(self, cr, uid, ids, context=None):
        print("Im duplicating the sale order right now!!!")
        default = {}
        duplicatename = ""
        for i in self.browse(cr, uid, ids, context):
            duplicatename = i.name
        if duplicatename[-2:-1] == "V":
            versionno = int(duplicatename[-1:])
            versionno = versionno + 1
            duplicatename = duplicatename[:-2] + "V" + str(versionno)
        else:
            duplicatename = duplicatename + "V1"
        for i in self.browse(cr, uid, self.search(cr, uid,
            [('name', '=', duplicatename)]), context):
                duplicatename = duplicatename + (versionno + 1)
        print(("The duplicate name should be" + duplicatename))
        default.update({
            'date_order': fields.date.context_today(self, cr,
            uid, context=context),
            'state': 'draft',
            'invoice_ids': [],
            'date_confirm': False,
            'name': duplicatename,
        })
        self.copy(cr, uid, ids[0], default, context=None)

    def create_cuotas(self, cr, uid, ids, context=None):
        ret = {}
        obj_cuotas = self.pool.get("control_encuestas")
        for i in self.browse(cr, uid, ids, context):
            id_cuotas = obj_cuotas.create(cr, uid, {
                       'name': i.name,
                       'cotizacion_id': i.id
                })
            self.write(cr, uid, [i.id], {
                    'cuotas': id_cuotas
                })
        return ret

    def request_budget(self, cr, uid, ids, context=None):
        ret = {}
        presupuesto_obj = self.pool.get("ea.presupuesto")
        for i in self.browse(cr, uid, ids, context):
            id_pres = presupuesto_obj.create(cr, uid, {
                    'name': i.name,
                    'claveproyecto': i.nombre_corto
                })
            self.write(cr, uid, [i.id], {'budget': id_pres})
        return ret

    def confirmar(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            self.write(cr, uid, [i.id], {'confirmada': True})
        return ret

    def facturar(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            self.write(cr, uid, [i.id], {'a_facturar': True})
        return ret

    def get_id(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.id
        return ret
    _columns = {
            'tipo': fields.many2one("ea.tipoestudio", string="Tipo de Estudio",
            ondelete="set null"),
            'nombre_corto': fields.char(string="Nombre Corto",
            size=40, translate=True),
            'budget': fields.many2one("ea.presupuesto", string="Presupuesto",
            ondelete="set null"),
            'current_id': fields.function(get_id, strgin="Id", type="integer"),
            'metodologia': fields.text("Metodología"),
            'objetivo': fields.text("Objetivo"),
            'tipo_levantamiento': fields.char("Tipo de Levantamiento"),
            'aprobada': fields.boolean("Aprobada por Control"),
            'cuotas': fields.many2one("control_encuestas", string="Cuotas"),
            'obj_img1': fields.binary("Imagen 1"),
            'obj_img2': fields.binary("Imagen 2"),
            'obj_img3': fields.binary("Imagen 3"),
            'obj_img4': fields.binary("Imagen 4"),
            'obj_img5': fields.binary("Imagen 5"),
            'met_img1': fields.binary("Imagen 1"),
            'met_name1': fields.char("Nombre Imagen 1"),
            'met_img2': fields.binary("Imagen 2"),
            'met_img3': fields.binary("Imagen 3"),
            'met_img4': fields.binary("Imagen 4"),
            'met_img5': fields.binary("Imagen 5"),
            'odt': fields.many2one("ea.project_wizard",
                string="Orden de Trabajo"),
            'creado': fields.related("odt", "creado", type="boolean",
                string="Proyecto Creado", readonly=True),
            'resp': fields.text(string="Responsabilidades de la\
             Agencia"),
            'rpoy': fields.text("Responsables del Proyecto"),
            'ent': fields.text("Entregables"),
            'ttiempos': fields.text("Tiempos"),
            'tmuestra': fields.text("Muestra"),
            'tiempos': fields.one2many("ea.tiempos", 'odv',
                string="Tiempos"),
            'muestra': fields.one2many("ea.muestra", 'odv',
                string="Muestra"),
            'observaciones': fields.text("Observaciones"),
            'director': fields.many2one("res.users", string="Director de Cuenta"),
            'confirmada': fields.boolean("Confirmada"),
            'a_facturar': fields.boolean("A Facturar"),
            'propuesta_ids': fields.one2many("ea.propuesta", "order_id", string="Propuestas")
        }

    _defaults = {
        'note': 'La cotización tiene validez de 90 días a partir de la fecha\
        de elaboración. Los precios NO incluyen el 16% de I.V.A. Se facturará \
        el 100% a la entrega de resultados. Cualquier cambio solicitado a la \
        presente cotización, puede afectar los parámetros de costo mencionado. \
        La cancelación una vez autorizado el estudio, puede incurrir en costos \
        de cancelación.',
        'resp': "<ol>\
      <li>Elaboración del cuestionario en conjunto con el cliente.</li>\
      <li>Adaptación y desarrollo del cuestionario.</li> \
      <li>Trabajo de campo objetivo\
      (con nuestro propio departamento de campo).</li>\
      <li>Supervisión permanente.</li>\
      <li>Procesamiento de la información (codificación, captura y tabulación).\
      </li>\
      <li>Los esquemas de codificación serán propuestos por la agencia. En caso\
        de requerir los marcos de codificación previo a la entrega del reporte,\
        favor de hacérmelo saber por escrito.</li>\
      <li>Análisis estadísticos y mercadológicos.</li>\
      <li>Elaboración del Reporte.</li>\
    </ol>\
    <i style='font-size: 13px;'>Nota: La agencia (Estadística Aplicada) se\
      compromete a que la información obtenida en este proyecto quede a\
      disposición del cliente en los siguientes medios: físicamente (durante 6\
      meses) y en medios magnéticos (3 años).</i>",
          'rpoy': "    <p>El proyecto estará a cargo de las siguientes\
          personas:<br>\
      &nbsp;</p>\
    <ol>\
      <li>Diseño del Cuestionario, Planeación y Logística: Dr. Javier Alagón y\
        Lucero López.</li>\
      <li>Conducción del Trabajo de Campo: Sergio García.</li>\
      <li>Análisis e Interpretación de Resultados: Dr. Javier Alagón y Lucero\
        López.</li>\
      <li>Comunicación permanente con clientes: Dr. Javier Alagón\
      y Lucero López</li>\
      <li>Responsable del proyecto: Lucero López.</li>\
    </ol>",
        'ent': '''<ol>
      <li>Tabulación de acuerdo con la estructura aprobada por el cliente
      cuando
        lo solicite (Por ejemplo: Excel o SPSS).</li>
      <li>Reporte de presentación (vía electrónica, FTP ó papel).</li>
    </ol>
    <p style='font-size:13px;'>Nota: Una vez entregados los resultados del
      estudio y/o llevada a cabo la presentación de los mismos, el cliente
      cuenta con un período&nbsp; de 30 días para hacer cualquier solicitud o
      tratamiento adicional de los datos. Cualquier requerimiento posterior a
      este lapso implicará su revisión en tiempo y costo.</p>'''
        }


class jmdtiempos(osv.Model):
    _name = 'ea.tiempos'
    _columns = {
    'name': fields.char("Etapa"),
    'fechas': fields.char("Fechas"),
    'odv': fields.many2one("sale.order", string="Orden"),
    'odt': fields.many2one("ea.project_wizard", string="OdT"),
    's1': fields.boolean("1"),
    's2': fields.boolean("2"),
    's3': fields.boolean("3"),
    's4': fields.boolean("4"),
    's5': fields.boolean("5"),
    's6': fields.boolean("6"),
    's7': fields.boolean("7"),
    's8': fields.boolean("8"),
    's9': fields.boolean("9"),
    's10': fields.boolean("10"),
    's11': fields.boolean("11"),
    's12': fields.boolean("12"),
    's13': fields.boolean("13"),
    's14': fields.boolean("14"),
    's15': fields.boolean("15"),
    's16': fields.boolean("16"),
    'w1': fields.selection([("completa", "Completa"), ("media", "Media")],
        string="1"),
    'w2': fields.selection([("completa", "Completa"), ("media", "Media")],
        string="2"),
    'w3': fields.selection([("completa", "Completa"), ("media", "Media")],
        string="3"),
    'w4': fields.selection([("completa", "Completa"), ("media", "Media")],
        string="4"),
    'w5': fields.selection([("completa", "Completa"), ("media", "Media")],
        string="5"),
    }


class jmdsoswitch(osv.Model):
    _name = "sale.order.switch"
    _inherit = "mail.thread"

    def set_state(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            state = i.state
            so_id = i.name.id
            cr.execute("UPDATE sale_order SET state = '"+state+"' WHERE id = " + str(so_id))
            for j in i.name.order_line:
                sol_id = j.id
                cr.execute("UPDATE sale_order_line SET state = '"+state+"' WHERE id = " + str(sol_id))

    _columns = {
        'name': fields.many2one("sale.order", string="Sale Order"),
        'state': fields.selection([('draft', "Reiniciar"), ('confirmed', "Confirmar")],string="Estado")
        }

class jmdcuots(osv.Model):
    _name = 'ea.muestra'
    _columns = {
    'name': fields.char("Entrevistas"),
    'porcentaje': fields.char("Porcentaje"),
    'cantidad': fields.char("Cantidad"),
    'odv': fields.many2one("sale.order", string="Orden"),
    'odt': fields.many2one("ea.project_wizard", string="OdT"),
    }


class jmdpropuesta(osv.Model):
    _name = "ea.propuesta"
    _inherit = "mail.thread"

    def _get_total(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.cantidad * i.costo
        return ret

    def convertir(self, cr, uid, ids, context):
        for i in self.browse(cr, uid, ids, context):
            line_obj = self.pool.get("sale.order.line")
            line_obj.create(cr, uid, {
                'product_id': i.name.id,
                'name': i.descripcion,
                'product_uom_qty': i.cantidad,
                'price_unit': i.costo,
                'order_id': i.order_id.id
                }, context)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            }

    _columns = {
        'id_opcion': fields.char("#"),
        'name': fields.many2one("product.product", string="Concepto"),
        'descripcion': fields.char("Descripción"),
        'cantidad': fields.float("Cantidad"),
        'costo': fields.float("Costo"),
        'total': fields.function(_get_total, string="Total", type="float", store=False),
        'order_id': fields.many2one("sale.order", string="OdV")
        }