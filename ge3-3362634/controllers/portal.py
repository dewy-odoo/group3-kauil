from odoo.addons.portal.controllers import portal
from odoo.http import request

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