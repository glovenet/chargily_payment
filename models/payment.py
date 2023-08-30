from odoo import models, fields, api
from chargily_lib.constant import EDAHABIA
from chargily_lib.invoice import Invoice
from chargily_lib.utils import extract_redirect_url
from chargily_lib.sync_lib.webhook import make_payment

class PaymentChargily(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('chargily', 'Chargily')])

    @api.model
    def _get_chargily_api_key(self):
        # Retrieve the Chargily API key from the configuration or any other source
        return 'YOUR-API-KEY'

    def chargily_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        chargily_invoice = Invoice()
        chargily_invoice.client = values['partner_name']
        chargily_invoice.client_email = values['partner_email']
        chargily_invoice.invoice_number = values['reference']
        chargily_invoice.mode = EDAHABIA
        chargily_invoice.amount = values['amount']
        chargily_invoice.discount = 0
        chargily_invoice.comment = 'Payment for Order: %s' % values['reference']
        chargily_invoice.back_url = base_url
        chargily_invoice.webhook_url = base_url + '/payment/chargily/callback'

        response = make_payment(chargily_invoice, self._get_chargily_api_key())

        if response.status_code == 201:
            redirect_url = extract_redirect_url(response.content)
            return {
                'redirect_url': redirect_url,
            }
        else:
            return {}

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _chargily_form_get_tx_from_data(self, data):
        reference = data.get('reference')
        if not reference:
            return False
        return self.search([('reference', '=', reference)])

    def _chargily_form_validate(self, data):
        status = data.get('status')
        if status == 'success':
            self._set_transaction_done()
        elif status == 'failure':
            self._set_transaction_cancel()
        else:
            self._set_transaction_pending()
        return True
