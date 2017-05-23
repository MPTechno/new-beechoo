#######################################################################

from openerp import models, fields, api, _
from openerp.tools import amount_to_text_en

to_19 = ( 'Zero',  'One',   'Two',  'Three', 'Four',   'Five',   'Six',
		  'Seven', 'Eight', 'Nine', 'Ten',   'Eleven', 'Twelve', 'Thirteen',
		  'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen' )
tens  = ( 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety')
denom = ( '',
		  'Thousand',     'Million',         'Billion',       'Trillion',       'Quadrillion',
		  'Quintillion',  'Sextillion',      'Septillion',    'Octillion',      'Nonillion',
		  'Decillion',    'Undecillion',     'Duodecillion',  'Tredecillion',   'Quattuordecillion',
		  'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Novemdecillion', 'Vigintillion' )

def _convert_nn(val):
	"""convert a value < 100 to English.
	"""
	if val < 20:
		return to_19[val]
	for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens)):
		if dval + 10 > val:
			if val % 10:
				return dcap + '-' + to_19[val % 10]
			return dcap

def _convert_nnn(val):
	"""
		convert a value < 1000 to english, special cased because it is the level that kicks 
		off the < 100 special case.  The rest are more general.  This also allows you to
		get strings in the form of 'forty-five hundred' if called directly.
	"""
	word = ''
	(mod, rem) = (val % 100, val // 100)
	if rem > 0:
		word = to_19[rem] + ' Hundred'
		if mod > 0:
			word += ' '
	if mod > 0:
		word += _convert_nn(mod)
	return word

def english_number(val):
	if val < 100:
		return _convert_nn(val)
	if val < 1000:
		 return _convert_nnn(val)
	for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom))):
		if dval > val:
			mod = 1000 ** didx
			l = val // mod
			r = val - (l * mod)
			ret = _convert_nnn(l) + ' ' + denom[didx]
			if r > 0:
				ret = ret + ', ' + english_number(r)
			return ret

			
class account_voucher(models.Model):

	_inherit = 'account.voucher'

	@api.multi
	def amount_to_text_fixed(self,number, currency):
		number = '%.2f' % number
		units_name = currency
		list = str(number).split('.')
		start_word = english_number(int(list[0]))
		end_word = english_number(int(list[1]))
		cents_number = int(list[1])
		cents_name = (cents_number > 1) and 'Cents' or 'Cent'
		return ' '.join(filter(None, [units_name, start_word, (start_word or units_name) and (end_word or cents_name) and 'and', end_word, cents_name]))

	@api.multi
	def action_sales_receipt_sent(self):
		""" Open a window to compose an email, with the edi invoice template
			message loaded by default
		"""
		assert len(self) == 1, 'This option should only be used for a single id at a time.'
		template = self.env.ref('SalesReceipt_SendByEmail_and_Print_Button_Module.email_template_sales_receipt', False)
		compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)

		ctx = dict(
			default_model='account.voucher',
			default_res_id=self.id,
			default_use_template=bool(template),
			default_template_id=template and template.id or False,
		)
		return {
			'name': _('Compose Email'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'views': [(compose_form.id, 'form')],
			'view_id': compose_form.id,
			'target': 'new',
			'context': ctx,
		}


	@api.multi
	def sales_receipt_print(self):
		assert len(self) == 1, 'This option should only be used for a single id at a time.'
		self.sent = True
		return self.env['report'].get_action(self, 'SalesReceipt_SendByEmail_and_Print_Button_Module.report_sales_receipt')
