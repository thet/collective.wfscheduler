# -*- coding: utf-8 -*-
from plone.api.exc import InvalidParameterError
from plone.app.uuid.utils import uuidToObject
from Products.Five.browser import BrowserView

import plone.api

import logging

logger = logging.getLogger(__file__)


class WFTaskRunnerView(BrowserView):

    @property
    def run(self, task_id=None):
        """Run a task with a specified id.
        """
        task_id = str(task_id or self.request.form.get('task_id', None))
        if not task_id:
            logger.warn('No task given specified')
            return

        import pdb
        pdb.set_trace()

        task = uuidToObject(task_id)
        if not task:
            logger.warn('Task ({0}) not found.'.format(task_id))
            return
        if not (task.task_action and task.task_items):
            logger.warn(
                'Task ({0}, action: {1}, items: {2}) incomplete.'.format(
                    task_id,
                    task.task_action,
                    task.task_items
                )
            )
            return

        for ref in task.task_items:
            ob = ref.to_object()
            if not ob:
                return
            try:
                plone.api.content.transition(
                    ob=ob,
                    transition=task.task_action
                )
            except InvalidParameterError:
                logger.warn(
                    'Could not apply transform action to object {0}'.format(
                        task_id
                    )
                )

    def __call__(self, *args, **kwargs):
        pass
