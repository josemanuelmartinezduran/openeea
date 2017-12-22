# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdencuestas(osv.Model):
    _name = "ea.encuesta"
    _inherit = "mail.thread"
    #Workflow functions
    #new state

    def action_new(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'new'})
        # ... perform other tasks
        return True

    def action_aprobado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'aprobado', 'usr_1': uid})
        # ... perform other tasks
        return True

    def action_segunda(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'segunda', 'usr_2': uid})
        # ... perform other tasks
        return True

    def action_tercera(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'tercera', 'usr_3': uid})
        # ... perform other tasks
        return True

    def action_cliente(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'cliente', 'usr_4': uid})
        # ... perform other tasks
        return True

    def action_cancelado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'cancelado'})
        # ... perform other tasks
        return True

    def action_ec(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'ec'})
        # ... perform other tasks
        return True

    def reiniciar(self, cr, uid, ids, context="None"):
        self.write(cr, uid, ids, {'state': 'new'})
        return True

    def on_change_odt(self, cr, uid, ids, odt_id, context=None):
        ret = {}
        values = {}
        odt_object = self.pool.get("ea.project_wizard")
        for i in odt_object.browse(cr, uid, [odt_id], context):
            values['name'] = i.name
        ret['value'] = values
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'state': fields.selection([('new', 'Nuevo'),
                ('aprobado', 'Kick Off'), ('segunda', 'Campo'),
                ('tercera', 'Procesamiento'),
                 ('ec', 'Ejecutivo de Cuenta'), ('cliente', 'Ok Cliente'),
                 ('cancelado', 'Cancelado')],
                 "Estado", readonly=True),
            'ejecutivo': fields.many2one("hr.employee", string="Ejecutivo"),
            'encuesta': fields.binary("Cuestionario aprobado"),
            'fieldname': fields.char("Nombre del Archivo"),
            'proyecto': fields.many2one("project.project", "Clave"),
            'nombre_corto': fields.related('proyecto', 'nombre_corto',
                string="Nombre Corto", type="char"),
            'aprobadopor': fields.char(string="Aprobación del cliente",
                size=40, translate=True),
            'aprobacion': fields.date(string="Fecha de aprobación"),
            'medio': fields.selection([("telefono", "LLamada telefónica"),
                ("mail", "Correo electrónico"),
                ("visita", "Presencial")], string="Medio de Confirmación"),
            'salario_ids': fields.one2many("ea.encuesta_salario",
                "encuesta", string="Salarios"),
            'odt_id': fields.many2one("ea.project_wizard", "Orden de Trabajo"),
            'adicionales': fields.boolean("Desbloquear el Cuestionario"),
            'ad_txt': fields.text("Cambios"),
            'ad_pers': fields.char("Quien autoriza cambios"),
            'bloquear': fields.boolean("Bloquear Cuestionario"),
            'criterio_ids': fields.one2many("ea.salario.concepto", "encuesta_id", string="Criterios Habilitados"),
            'usr_1': fields.many2one("res.users", string="Aprobó"),
            'usr_2': fields.many2one("res.users", string="Segundo Aprobador"),
            'usr_3': fields.many2one("res.users", string="Tercer Aprobador"),
            'usr_4': fields.many2one("res.users", string="Capturó Ok Cliente"),
        }


class jmdsalarioencuesta(osv.Model):
    _name = "ea.encuesta_salario"

    def get_idestudio(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.encuesta.proyecto.id
        return ret

    _columns = {
            'name': fields.many2one("ea.salario.concepto",
                string="Pago Entrevista"),
            'encuesta': fields.many2one("ea.encuesta", string="",
                ondelete="set null"),
            'puesto': fields.many2one("hr.job", "Puesto"),
            'descripcion': fields.char("Descripción"),
            'min': fields.integer("Mínimo"),
            'max': fields.integer("Máximo"),
            'monto': fields.float(digits=(9, 2), string="Monto Asignado"),
            'tipo': fields.selection([("propia", "Propia"),
                ("equipo", "Equipo Supervisado")], string="Tipo de Pago"),
            'plaza_id': fields.many2one("plaza", string="Plaza"),
            'idestudio': fields.function(get_idestudio,
                string="Id Estudio", type="char"),
        }


class jmdsalarioconcepto(osv.Model):
    _inherit = "mail.thread"
    _name = "ea.salario.concepto"

    def get_idestudio(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.encuesta_id and i.encuesta_id.proyecto:
                ret[i.id] = i.encuesta_id.proyecto.id
        return ret

    _columns = {
        'name': fields.char(string="Nombre", size=40),
        'encuesta_id': fields.many2one("ea.encuesta", string="Cuestionario"),
        'idestudio': fields.function(get_idestudio,
                string="Id Estudio", type="char", store=True),
        }