# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.folder import FolderView
from collective.wfscheduler.behaviors import refs_to_objs
from Products.CMFPlone.utils import safe_callable


class WFTaskFolderView(FolderView):

    @property
    def tabular_fields(self):
        return [
            'title',
            'task_action',
            'task_items',
            'task_date'
        ]

    def tabular_fielddata(self, item, fieldname):
        value = getattr(item, fieldname, '')
        if safe_callable(value):
            value = value()

        if fieldname == 'task_date' and value:
            value = self.toLocalizedTime(value, long_format=1)

        if fieldname == 'task_items':
            value = u', '.join([it.Title() for it in refs_to_objs(value)])

        return {
            # 'title': _(fieldname, default=fieldname),
            'value': value
        }
