#
# Copyright 2015, Martin Owens <doctormo@gmail.com>
#
# This file is part of the software inkscape-web, consisting of custom 
# code for the Inkscape project's django-based website.
#
# inkscape-web is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# inkscape-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with inkscape-web.  If not, see <http://www.gnu.org/licenses/>.
#

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

@toolbar_pool.register
class SubscribeToolbar(CMSToolbar):
    """Displace a Subscribe to this page link."""
    def populate(self):
        from .alert import PagePublishedAlert
        alert = PagePublishedAlert.get_alert_type()
        menu = self.toolbar.get_or_create_menu('subscribe', _('Alerts'))
        subs = self.request.user.alert_subscriptions.filter(alert=alert)

        if hasattr(self.request.current_page, '_wrapped'):
            page = self.request.current_page._wrapped
        else:
            page = self.request.current_page

        if not subs.is_subscribed():
            if page and subs.is_subscribed(page, True):
                menu.add_link_item(_('Unsubscribe from this page'), url=alert.unsubscribe_url(page))
            elif page:
                menu.add_link_item(_('Subscribe to this page'), url=alert.subscribe_url(page))
            menu.add_link_item(_('Subscribe to all pages'), url=alert.subscribe_url())
        else:
            menu.add_link_item(_('Unsubscribe from all pages'), url=alert.unsubscribe_url())
