from odoo.addons.portal.controllers import portal
from odoo.http import request
import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request

from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class CustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        RepairOrder = request.env['repair.order']
        if 'repair_order_count' in counters:
            values['repair_order_count'] = RepairOrder.search_count(self._prepare_repair_order_domain(partner)) \
                if RepairOrder.check_access_rights('read', raise_exception=False) else 0

        return values

    def _prepare_repair_order_domain(self, partner):
        return ['|',
                (
                    'oner_id', '=', partner.id
                ),
                ('public', '=', True)
        ]
    
    def _prepare_repair_order_rendering_values(
        self, page=1, registry_id=None, vin=None, mileage=None, partner_id=None, sale_order_id = None, product_id = None, **kwargs
    ):
        records = request.env['repair.order']

        partner = request.env.user.partner_id
        values = {}

        
        domain = [('partner_id', '=', partner.id)]

        userRecords = records.search(domain)

        values.update({
            "userRecords" : userRecords
        })

        return values
    

    @http.route(['/my/repair-order'], type='http', auth="user", website=True)
    def portal_my_repair_order(self, **kwargs):
        values = self._prepare_moto_portal_rendering_values( **kwargs)
        #request.session['my_orders_history'] = values['orders'].ids[:100]
        return request.render("ge6-3361950.repair_order_list", values)
    

    @http.route(['/my/repair-order/<int: id>'], type='http', auth="user", website=True)
    def portal_repair_order(self, id, access_token=None, **kw):
        print(id)
        try:
            repair_sudo = self._document_check_access('repair.order', id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._task_get_page_view_values(repair_sudo, access_token, **kw)
        return request.render("ge6-3361950.portal_my_repair", values)
    
    def _task_get_page_view_values(self, repair_sudo, access_token, **kwargs):
        values = {
            'page_name': 'Motorcycle Repair',
            'repair': repair_sudo,
            'user': request.env.user,
            'project_accessible': True,
            'task_link_section': [],
        }
        history = 'my_repair_history'

        values = self._get_page_view_values(repair_sudo, access_token, values, history, False, **kwargs)

        return values
    
    #TODO: make post req contorller
    


