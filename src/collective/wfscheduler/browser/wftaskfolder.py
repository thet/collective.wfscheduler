# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.folder import FolderView
from collective.wfscheduler.behaviors import refs_to_objs
from Products.CMFPlone.utils import safe_callable

import plone.api


class WFTaskFolderView(FolderView):

    def results(self, **kwargs):
        # Default is to show all.
        kwargs['portal_type'] = 'WFTask'
        filter_ = self.request.form.get('filter')
        if filter_ == 'active':
            kwargs['is_active'] = True
        elif filter_ == 'inactive':
            kwargs['is_active'] = False
        return super(WFTaskFolderView, self).results(**kwargs)

    @property
    def filter_selected(self):
        filter_ = self.request.form.get('filter')
        return {
            'active': ' selected' if filter_ == 'active' else '',
            'inactive': ' selected' if filter_ == 'inactive' else '',
            'all': ' selected' if filter_ not in ('active', 'inactive') else ''
        }

    @property
    def tabular_fields(self):
        return [
            'title',
            'task_action',
            'task_items',
            'task_date',
            'task_active'
        ]

    def tabular_fielddata(self, item, fieldname):
        value = getattr(item, fieldname, '')
        if safe_callable(value):
            value = value()

        if fieldname == 'task_date' and value:
            value = self.toLocalizedTime(value, long_format=1)

        if fieldname == 'task_items':

            value = u', '.join([
                u'<a class="pat-plone-modal" href="{1}">{0} ({2})</a>'.format(
                    it.Title(),
                    it.absolute_url(),
                    plone.api.content.get_state(it)
                ) for it in refs_to_objs(value)
            ])

        return {
            # 'title': _(fieldname, default=fieldname),
            'value': value
        }
