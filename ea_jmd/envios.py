from osv import osv, fields


class paqueteria(osv.Model):
    _name = "hd.paqueteria"
    _columns = {
        'name': fields.char('Nombre', size=64, required=True),
        'paqueteria': fields.char('Empresa de Paqueteria', size=64),
        'guia': fields.char('No. de Guia', size=64, required=False),
        'entrega': fields.date('Fecha de entrega'),
        'envio': fields.date('Fecha de envio'),
        'status': fields.selection([('Enviado', 'enviado'),
            ('Recibido', 'recibido')], string='Estado'),
    }
