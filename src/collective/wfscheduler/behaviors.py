# -*- coding: utf-8 -*-
from collective.wfscheduler import _
from plone.app.event.base import default_timezone
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.indexer.decorator import indexer
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import provider


def refs_to_objs(refs):
    ret = []
    for ref in refs:
        obj = ref.to_object
        ret.append(obj)
    return ret


@provider(IFormFieldProvider)
class IWFTask(model.Schema):
    """Behavior providing fields for the workflow tasks.
    """

    task_items = RelationList(
        title=_(
            u'label_task_items',
            default=u'Task items'
        ),
        description=_(
            u'description_task_items',
            default=u'Select one or more content objects to be processed.'
        ),
        default=[],
        value_type=RelationChoice(
            title=_(u'label_task_items', default=u'Task items'),
            vocabulary='plone.app.vocabularies.Catalog',
        ),
        required=True,
    )
    directives.widget(
        'task_items',
        RelatedItemsFieldWidget,
        orderable=True,
    )

    task_action = schema.Choice(
        title=_(
            u'label_task_action',
            default=u'Task action'),
        description=_(
            u'help_task_action',
            default=u'Select a workflow transition, which should be applied '
                    u'when the task is executed.',
        ),
        vocabulary='plone.app.vocabularies.WorkflowTransitions',
        required=True,
        missing_value='',
    )
    directives.widget('task_action', SelectFieldWidget)

    task_date = schema.Datetime(
        title=_(
            u'label_task_date',
            default=u'Task task date'
        ),
        description=_(
            u'help_task_date',
            default=u'Date and time, when the task action should be executed.'
        ),
        required=False,
        default=None
    )
    directives.widget(
        'task_date',
        DatetimeFieldWidget,
        default_timezone=default_timezone
    )

    task_active = schema.Bool(
        title=_(
            u'label_task_active',
            default=u'Active?'
        ),
        description=_(
            u'help_task_active',
            default=u'On, if the task is active. After successful run, this will be automatically set to off.'  # noqa
        ),
        required=False,
        default=True
    )


@indexer(IWFTask)
def date_indexer(obj):
    acc = IWFTask(obj, None)
    date = acc.task_date
    if not date:
        raise AttributeError
    return date


@indexer(IWFTask)
def title_indexer(obj):
    title = obj.Title()
    acc = IWFTask(obj, None)
    items = [it.Title() for it in refs_to_objs(acc.task_items)]
    action = acc.task_action
    date = acc.task_date

    ret = u'{0} - {1} ({2}){3}'.format(
        title,
        action,
        u', '.join(items),
        u', {0}'.format(date) if date else u''
    )

    return ret


@indexer(IWFTask)
def is_active_indexer(obj):
    acc = IWFTask(obj, None)
    return acc.task_active
