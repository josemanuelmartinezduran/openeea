from osv import osv, fields

class location (osv.Model):
	_inherit='stock.location'
	_columns = {
		'chained_delay':fields.integer('Plazo en esta ubicacion', traslate=True),
		'es_persona':fields.boolean('Es persona'),
		'empleado':fields.many2one('hr.employee', ondelete="set null")
		}
