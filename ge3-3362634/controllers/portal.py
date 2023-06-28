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

        MotorcycleRegistry = request.env['motorcycle.registry']
        if 'motorcycle_registry_count' in counters:
            values['motorcycle_registry_count'] = MotorcycleRegistry.search_count(self._prepare_motorcycle_registry_domain(partner)) \
                if MotorcycleRegistry.check_access_rights('read', raise_exception=False) else 0

        return values
    
    def _prepare_motorcycle_registry_domain(self, partner):
        return ['|',
            ('owner_id', '=', partner.id),
            ('public', '=', True)
        ]
    
    def _prepare_moto_portal_rendering_values(
        self, page=1, reg_number=None, vin=None, lot_id=None, brand=None,make = None,model = None,plate_number = None, owner = None, **kwargs
    ):
        records = request.env['motorcycle.registry']

        partner = request.env.user.partner_id
        values = {}

        
        domain = [('owner_id', '=', partner.id)]

        userRecords = records.search(domain)

        values.update({
            "userRecords" : userRecords
        })

        return values


    @http.route(['/my/registry'], type='http', auth="user", website=True)
    def portal_my_registry(self, **kwargs):
        values = self._prepare_moto_portal_rendering_values( **kwargs)
        #request.session['my_orders_history'] = values['orders'].ids[:100]
        return request.render("ge3-3362634.portal_moto_reg_list", values)
    
    @http.route(['/my/registry/<int:registry_number>'], type='http', auth="user", website=True)
    def portal_motorcycle_registry(self, registry_number, access_token=None, **kw):
        try:
            registry_sudo = self._document_check_access('motorcycle.registry', registry_number, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._task_get_page_view_values(registry_sudo, access_token, **kw)
        return request.render("ge3-3362634.portal_my_motorcycle", values)
    
    def _task_get_page_view_values(self, registry_sudo, access_token, **kwargs):
        values = {
            'page_name': 'Motorcycle Registry',
            'registry': registry_sudo,
            'user': request.env.user,
            'project_accessible': True,
            'task_link_section': [],
        }
        history = 'my_registry_history'

        values = self._get_page_view_values(registry_sudo, access_token, values, history, False, **kwargs)

        return values
    
    @http.route('/my/registry/form/motorcycle_registry', methods=['POST'], type='http', auth="user")
    def submit_form(self, id, access_token=None, **kwargs):
        try:
            registry_sudo = self._document_check_access('motorcycle.registry', int(id))
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        registry_sudo.update({
            "vin": kwargs.get('vin'),
            "brand": kwargs.get('brand', None),
            "make": kwargs.get('make', None),
            "model": kwargs.get('model', None),
            "current_mileage": kwargs.get('current_mileage', None),
            "license_plate": kwargs.get('license_plate', None),
            "registry_date": kwargs.get('registry_date', None)
        })

        values = self._task_get_page_view_values(registry_sudo, access_token=access_token, **kwargs)
        return request.render("ge3-3362634.portal_my_motorcycle", values)
