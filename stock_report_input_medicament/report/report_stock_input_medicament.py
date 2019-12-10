# -*- coding: utf-8 -*-

import xlsxwriter
import datetime
import unicodedata
import base64
import io

from PIL import Image
from io import StringIO
from datetime import datetime

from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource


class ReportStockInputMedicament(models.Model):
    _name = 'report.stock.input.medicament'
    _description = 'report stock input medicament'

    report_data = fields.Char('Name', size=256)
    file_name = fields.Binary('Input Medicament Excel Report', readonly=True)


class WizardReportInputMedicaments(models.Model):
    _name = 'wizard.report.input.medicament'
    _description = 'stock wizard input medicament report'


    def _get_sequence(self, warehouse_id):

        wh = ((self.env['stock.warehouse']
                .browse(warehouse_id)).name).upper()

        if 'ALMAGUER' in wh:
            return self.env['ir.sequence'].next_by_code('report.stock.input.medicament.alm')
        if 'VEGA' in wh:
            return self.env['ir.sequence'].next_by_code('report.stock.input.medicament.lveg')
        if 'SEBASTIAN' in wh:
            return self.env['ir.sequence'].next_by_code('report.stock.input.medicament.sseb')
        if 'ROSA' in wh:
            return self.env['ir.sequence'].next_by_code('report.stock.input.medicament.srosa')
        if 'VILLALOBOS' in wh:
            return self.env['ir.sequence'].next_by_code('report.stock.input.medicament.sjvl')
        else:
            return ''


    def action_stock_input_medicament_report(self):

        custom_value = {}

        #XLS report
        #filename = ('Report'+ '.xlsx')
        filename = ('/opt/odoo/Report'+ '.xlsx')
        workbook = xlsxwriter.Workbook(filename)
        sheet = workbook.add_worksheet()

        # FORMATOS DE CELDAS
        style_title_1 = workbook.add_format({'font_name':'Arial'
                , 'font_size':'12'
                , 'bold': True
                , 'align': 'center'})

        style_num = workbook.add_format({'num_format': '#,##0'
                , 'font_name':'Arial'
                , 'font_size':'12'})
        style_title = workbook.add_format({'font_name':'Arial'
                , 'font_size':'12'
                , 'bold': True})
        style_text = workbook.add_format({'font_name':'Arial'
                , 'font_size':'12'})
        style_money = workbook.add_format({'num_format': '[$$-240A]#,##0.00'
                , 'font_name':'Arial'
                , 'font_size':'12'})
        style_date = workbook.add_format({'num_format': 'mm/dd/yyyy'
                , 'font_name':'Arial'
                , 'font_size':'12'})

        picking = (self.env['stock.picking']
                .browse(self._context.get('active_ids', list())))

        row_num = 0
        for rec in picking:
            inputs = []
            for sm in rec.move_lines:
                for sml in sm._get_move_lines():
                    for line in sml:
                        product = {}

                        if line.product_id.default_code:
                            product ['product_code'] = line.product_id.default_code
                        else:
                            product ['product_code'] = ''

                        if line.product_id.name:
                            product ['product_id'] = line.product_id.name
                        else:
                            product ['product_id'] = ''

                        if line.product_id.is_medicament and line.product_id.product_tmpl_id.commercial_presentation:
                            product ['product_presentation'] = line.product_id.product_tmpl_id.commercial_presentation
                        else:
                            product ['product_presentation'] = ''

                        if line.product_id.is_medicament and line.product_id.product_tmpl_id.concentration:
                            product ['product_concent'] = line.product_id.product_tmpl_id.concentration
                        else:
                            product ['product_concent'] = ''

                        # grname = ""
                        # for group in line.product_id.product_tmpl_id.med_group_id:
                        #     grname += group.name + ', '
                        # if line.product_id.is_medicament:
                        #     product ['product_group'] = grname
                        # else:
                        #      product ['product_group'] = ''

                        if line.product_id.is_medicament and line.product_id.product_tmpl_id.med_group_id:
                            if line.product_id.product_tmpl_id.med_group_id.parent_id.name:
                                product ['product_group'] = line.product_id.product_tmpl_id.med_group_id.parent_id.name
                            else:
                                product ['product_group'] = line.product_id.product_tmpl_id.med_group_id.name
                        else:
                             product ['product_group'] = ''

                        if line.product_id.is_medicament and line.product_id.product_tmpl_id.storage:
                            if line.product_id.product_tmpl_id.storage == 'norm':
                                product ['product_storage'] = 'Normal de 15ºC a 30ºC. Humedad entre 25% a 70%'
                            else:
                                product ['product_storage'] = 'Cadena de frío de 2ºC a 8ºC'
                        else:
                            product ['product_storage'] = ''

                        if line.product_id.is_medicament and line.product_id.product_tmpl_id.individual_presentation:
                            product ['product_prest_ind'] = line.product_id.product_tmpl_id.individual_presentation
                        else:
                            product ['product_prest_ind'] = ''

                        product ['product_qty'] = line.qty_done # sm.product_qty
                        product ['product_price'] = sm.price_unit

                        if line.product_id.is_medicament and sml.lot_id.name:
                            product ['prod_lot'] = sml.lot_id.name
                        else:
                            product ['prod_lot'] = ''

                        if line.product_id.is_medicament and sml.lot_id.cums_consecutive:
                            product ['prod_cums_cons'] = sml.lot_id.cums_consecutive
                        else:
                            product ['prod_cums_cons'] = ''

                        if line.product_id.is_medicament and sml.lot_id.cums:
                            product ['prod_cums_cod'] = sml.lot_id.cums
                        else:
                            product ['prod_cums_cod'] = ''

                        if line.product_id.is_medicament and sml.lot_id.laboratory:
                            product ['prod_laboratory'] = sml.lot_id.laboratory
                        else:
                            product ['prod_laboratory'] = ''

                        if line.product_id.is_medicament and sml.lot_id.register_invima:
                            product ['prod_invima'] = sml.lot_id.register_invima
                        else:
                            product ['prod_invima'] = ''

                        if line.product_id.is_medicament and sml.lot_id.life_date:
                            product ['prod_date_end_life'] = sml.lot_id.life_date
                        else:
                            product ['prod_date_end_life'] = ''

                        inputs.append(product)

                    custom_value ['products'] = inputs
                    custom_value ['partner_id'] = sm.picking_id.partner_id.name
                    custom_value ['date_done'] = sm.picking_id.date_done
                    custom_value ['partner_no'] = sm.picking_id.name
                    custom_value ['order'] = sm.origin

                    if sm.picking_id.vendor_remission_date:
                        custom_value ['vender_invo_date'] = sm.picking_id.vendor_remission_date
                    else:
                        custom_value ['vender_invo_date'] = ''

                    if sm.picking_id.vendor_remission_number:
                        custom_value ['vender_invo_num'] = sm.picking_id.vendor_remission_number
                    else:
                        custom_value ['vender_invo_num'] = ''

                # if picking.picking_type_id.warehouse_id.company_id.logo:
                #     custom_value ['logo'] = (
                #             io.BytesIO(base64.b64decode(picking.picking_type_id.warehouse_id.company_id.logo))
                #         )
                # else:
                #     custom_value ['logo'] = ''

                path = get_module_resource('stock_report_input_medicament', 'src/img/escudo-de-colombia.png')
                if path:
                    with tools.file_open(path, 'rb') as image_file:
                        custom_value ['logo'] = (
                                     io.BytesIO((image_file.read()))
                                 )

                # path = './src/img/escudo-de-colombia.png'
                #
                # custom_value ['logo'] = path

                if picking.picking_type_id.warehouse_id.partner_id.city:
                    custom_value ['address'] = picking.picking_type_id.warehouse_id.partner_id.city
                else:
                    custom_value ['address'] = ''


            # OBTENER SECUENCIA
            seq = self._get_sequence( (rec.location_id.get_warehouse().id) )

            # ENCABEZADO DEL REPORTE
            img_tmp = custom_value ['logo']
            title = ('FORMATO DE RECEPCION TECNICA SF  HOSPITAL NIVEL I  '
                + custom_value ['address'] ).upper()

            sheet.insert_image(row_num, 9
                , 'logo.png'
                , {'image_data': img_tmp
                    , 'x_scale': 0.2
                    , 'y_scale': 0.2} )
            sheet.merge_range(row_num + 5, 5
                , row_num + 5, 14
                , title
                , style_title_1 )
            sheet.merge_range(row_num + 7, 0
                , row_num + 7, 4
                , 'Acta de Recepción Técnica de medicamentos'
                , style_title)

            sheet.write(row_num + 7, 6, 'No', style_title)
            sheet.write(row_num + 7, 7, seq, style_title)
            sheet.merge_range(row_num + 7, 12
                , row_num + 7, 13
                , 'Fecha de generación'
                , style_title)
            sheet.write(row_num + 7, 14, (fields.Datetime.now()).strftime('%d/%m/%Y'), style_date)

            sheet.write(row_num + 8, 0, 'Proveedor', style_title)
            sheet.write(row_num + 8, 1,  custom_value['partner_id'], style_text)
            sheet.write(row_num + 8, 6, 'Fecha', style_text)
            sheet.write(row_num + 8, 7,  custom_value['date_done'], style_date)

            sheet.write(row_num + 10,  0, 'Fecha de llegada', style_title)
            sheet.write(row_num + 10,  1,  custom_value['date_done'], style_date)
            sheet.write(row_num + 10,  6, 'Fecha de inspección', style_title)
            sheet.write(row_num + 10, 12, 'No Cajas', style_title)


            # ENCABEZADOS DE  COLUMNAS
            sheet.write(row_num + 12,  0, 'Código Interno', style_title)
            sheet.write(row_num + 12,  1, 'Nombre del medicamento', style_title)
            sheet.write(row_num + 12,  2, 'Presentación comercial', style_title)
            sheet.write(row_num + 12,  3, 'Valor unitario ', style_title)
            sheet.write(row_num + 12,  4, 'Proveedor', style_title)
            sheet.write(row_num + 12,  5, 'Número de factura de Proveedor'
                , style_title)
            sheet.write(row_num + 12,  6, 'Fecha de la factura de Proveedor'
                , style_title)
            sheet.write(row_num + 12,  7, 'Cantidad', style_title)
            sheet.write(row_num + 12,  8
                , 'Fecha de ingreso a farmacia', style_title)
            sheet.write(row_num + 12,  9, 'Laboratorio', style_title)
            sheet.write(row_num + 12, 10, 'Presentación', style_title) # presentación individual
            sheet.write(row_num + 12, 11, 'Concentración', style_title)
            sheet.write(row_num + 12, 12, 'Lote', style_title)
            sheet.write(row_num + 12, 13, 'Registro Invima', style_title)
            sheet.write(row_num + 12, 14, 'CUMS', style_title)
            sheet.write(row_num + 12, 15, 'Consecutivo CUMS', style_title)
            sheet.write(row_num + 12, 16, 'Grupo', style_title)
            sheet.write(row_num + 12, 17, 'Almacenaje', style_title)
            sheet.write(row_num + 12, 18, 'Fecha de vencimiento', style_title)
            sheet.write(row_num + 12, 19, 'Semáforo', style_title)
            sheet.write(row_num + 12, 20, 'Se acepta', style_title)

            # DATOS
            n = row_num + 13
            if rec.state == 'done':
                for product in custom_value ['products']:
                    sheet.write(n,  0, product ['product_code'], style_text)
                    sheet.write(n,  1, product ['product_id'], style_text)
                    sheet.write(n,  2, product ['product_presentation'], style_text)
                    sheet.write(n,  3, product ['product_price'] , style_money)

                    sheet.write(n,  7, product ['product_qty'], style_num)

                    sheet.write(n,  9, product ['prod_laboratory'], style_text)
                    sheet.write(n, 10, product ['product_prest_ind'], style_text)
                    sheet.write(n, 11, product ['product_concent'], style_text)
                    sheet.write(n, 12, product ['prod_lot'], style_text)
                    sheet.write(n, 13, product ['prod_invima'], style_text)
                    sheet.write(n, 14, product ['prod_cums_cod'], style_text)
                    sheet.write(n, 15, product ['prod_cums_cons'], style_text)
                    sheet.write(n, 16, product ['product_group'], style_text)
                    sheet.write(n, 17, product ['product_storage'], style_text)
                    sheet.write(n, 18, product ['prod_date_end_life'], style_date)

                    sheet.write(n,  4, custom_value['partner_id'], style_text)
                    sheet.write(n,  5, custom_value ['vender_invo_num'], style_text)
                    sheet.write(n,  6, custom_value ['vender_invo_date'], style_date)
                    sheet.write(n,  8, custom_value ['date_done'], style_date)

                    sheet.write(n, 19, ' ', style_text)
                    sheet.write(n, 20, ' ', style_text)
                    n += 1

                # OBSERVACION
                sheet.write(n + 2, 0, 'Observaciones ', style_title)
                note = ''
                if rec.note:
                    note = rec.note
                else:
                    note = ''
                sheet.write(n + 2, 1, note, style_title)

                # FIRMAS
                sheet.write(n + 5, 0, 'Responsable de la Recepción Técnica ', style_title)
                sheet.write(n + 6, 5, 'Firma ', style_title)
                sheet.write(n + 6, 9, 'Verificado por ', style_title)

                row_num = n + 1


        workbook.close()
        fp = open(filename, "rb")
        file_data = fp.read()
        out = base64.encodestring(file_data)
        mes = ((fields.Datetime.now()).strftime('%B %Y')).upper()

        # Files actions
        attach_vals = {
                'report_data': 'ACTA DE RECEPCION DE MEDICAMENTOS '+ mes +'.xlsx',
                'file_name': out,
            }
        act_id = self.env['report.stock.input.medicament'].create(attach_vals)
        fp.close()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'report.stock.input.medicament',
            'res_id': act_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'context': self.env.context,
            'target': 'new',
        }
