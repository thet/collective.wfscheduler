# -*- coding: utf-8 -*-
from collective.wfscheduler.behaviors import IWFTask
from plone.api.exc import InvalidParameterError
from plone.app.uuid.utils import uuidToObject
from Products.Five.browser import BrowserView
from Products.ZCatalog.interfaces import ICatalogBrain

import logging
import plone.api
import plone.app.event


logger = logging.getLogger(__name__)


class WFTaskRunnerView(BrowserView):

    warnings = []

    def __call__(self, *args, **kwargs):
        """Run a task with a specified id or all upcoming tasks.
        """
        tasks = []

        infos = []
        warnings = []

        now = plone.app.event.base.localized_now(self.context)

        infos.append(
            u'Starting workflow task runner on {:%Y-%m-%d %H:%M}'.format(now)
        )
        logger.info(infos[-1])

        task_id = self.request.form.get('task_id', None)
        if task_id:
            tasks = [uuidToObject(task_id)]
        else:
            # Get all upcoming tasks
            query = {}
            query['portal_type'] = 'WFTask'
            query['start'] = {'query': now, 'range': 'max'}
            query['is_active'] = True
            tasks = plone.api.content.find(**query)

        if not tasks:
            warnings.append(u'No tasks found')
            logger.warn(warnings[-1])

        for task in tasks:

            if ICatalogBrain.providedBy(task):
                task = task.getObject()

            if not (task.task_action and task.task_items):
                warnings.append(
                    u'Task <a href="{0}">{1}</a> (action: {2}, items: {3}) incomplete.'.format(  # noqa
                        task.absolute_url(),
                        task.title,
                        task.task_action,
                        task.task_items
                    )
                )
                logger.warn(warnings[-1])
                continue

            for ref in task.task_items:
                ob = ref.to_object
                if not ob:
                    continue
                try:
                    plone.api.content.transition(
                        obj=ob,
                        transition=task.task_action
                    )
                    infos.append(u'Task <a href="{0}">{1}</a> successfully run for object <a href="{2}">{3}</a>.'.format(  # noqa
                        task.absolute_url(),
                        task.title,
                        ob.absolute_url(),
                        ob.title
                    ))
                    logger.info(infos[-1])
                except InvalidParameterError:
                    warnings.append(u'Could not apply task <a href="{0}">{1}</a> with transform {2} for object <a href="{3}">{4}</a>.'.format(  # noqa
                        task.absolute_url(),
                        task.title,
                        task.task_action,
                        ob.absolute_url(),
                        ob.title
                    ))
                    logger.warn(warnings[-1])
                    continue

            IWFTask(task).task_active = False
            task.reindexObject(idxs=['is_active'])

        # Final summary
        self.infos = infos
        self.warnings = warnings
        return super(WFTaskRunnerView, self).__call__(*args, **kwargs)
