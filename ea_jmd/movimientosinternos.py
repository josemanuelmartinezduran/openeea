from openerp.osv import fields, osv


class InternalMove(osv.Model):

    _inherit = 'stock.picking'

    _columns = {
        'devolucion': fields.date('Fecha de devolucion'),
        'empleado': fields.many2one('hr.employee',
            string='Nombre del empleado'),
        'es_consigna': fields.boolean('Es Consigna'),
        'justificacion': fields.char('Justificacion', size=40),
        'elaboro': fields.char('Persona que elaboro', size=40),
        'estudio': fields.many2one('project.project'),
        'observaciones': fields.text('Observaciones'),
        'origen': fields.char("Origen", size=40)
        }


class Empleado(osv.Model):

    _inherit = 'hr.employee'

    _columns = {
        'nip': fields.char("NIP", size=15)
        }