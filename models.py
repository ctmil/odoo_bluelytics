# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from openerp.exceptions import UserError,ValidationError
from openerp.tools.safe_eval import safe_eval
from datetime import datetime

import urllib2
import simplejson

class ResCurrency(models.Model):
	_inherit = 'res.currency'

	@api.model
	def update_bluelytics(self):
		bluelytics_parm = self.env['ir.config_parameter'].search([('key','=','bluelytics_url')])
		if not bluelytics_parm:
			raise UserError('No esta presente URL de Bluelytics')
		bluelytics_url = bluelytics_parm.value
		try:
			response = urllib2.urlopen(bluelytics_url)
		except:
			raise UserError('No se pudo obtener tipo de cambio de Banco Cordoba')
		data = simplejson.load(response)
		try:
			value = data['oficial']['value_sell']
		except:
			raise UserError('No es posible determinar el valor del dolar')
		#import pdb;pdb.set_trace()
		currency_id = self.search([('name','=','USD')])
		if currency_id:
			vals = {
				'name': str(datetime.now()),
				'currency_id': currency_id.id,
				'rate': 1 / value
				}
			return_id = self.env['res.currency.rate'].create(vals)	



