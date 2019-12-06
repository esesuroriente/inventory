# -*- coding: utf-8 -*-

import datetime
from odoo import fields, models, api, _

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    alert = fields.Selection([  ('A',  'Alerta'),
                                ('W',  'Advertencia'),
                                ('NR', 'Sin Riesgo')],
        help=" 'Alert' -> the expiration date of the product is below 90 days. "+
        "'Warning' -> the expiration date of the product is between 91 and 180 days. " +
        "'No Risk' -> the expiration date of the product is above 181 days. "
        , store=True
        )
    num_days = fields.Integer(
        string='Number of Days',
        help='Number of days for product expiration')

    @api.onchange('life_date')
    def _onchange_life_date(self):
        if self.life_date:
            self.alert_date = self.life_date - datetime.timedelta(days=90)

    @api.onchange('life_date')
    def _calculate_dif_date(self):
        current_date = fields.Datetime.now()
        if self.life_date:
            self.num_days = (self.life_date - current_date).days
            self.alert = self._alert_calc(self.num_days)


    def _alert_calc(self, dif):
        if  dif <= 90:
            alert = 'A'
        if 90 < dif <= 180:
            alert = 'W'
        if dif > 180:
            alert = 'NR'
        return alert


    @api.model
    def _alert_date_validation(self):
        current_date = fields.Datetime.now()
        lots = self.env['stock.production.lot'].search([
            ('life_date', '!=', False)])

        for alert_lots in lots:
            dif = (alert_lots.life_date - current_date).days
            alert = self._alert_calc(dif)

            alert_lots.write({
            'alert': alert ,
            'num_days': dif
            })
