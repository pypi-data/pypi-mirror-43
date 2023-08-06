import six

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.reverse import reverse

from waldur_mastermind.marketplace import processors
from waldur_mastermind.support import models as support_models
from waldur_mastermind.support import views as support_views

from .views import IssueViewSet


class CreateRequestProcessor(processors.BaseCreateResourceProcessor):
    viewset = support_views.OfferingViewSet

    def get_post_data(self):
        order_item = self.order_item
        try:
            template = order_item.offering.scope
        except ObjectDoesNotExist:
            template = None

        if not isinstance(template, support_models.OfferingTemplate):
            raise serializers.ValidationError('Offering has invalid scope. Support template is expected.')

        project = order_item.order.project
        project_url = reverse('project-detail', kwargs={'uuid': project.uuid})
        template_url = reverse('support-offering-template-detail', kwargs={'uuid': template.uuid})
        attributes = order_item.attributes.copy()

        post_data = dict(
            project=project_url,
            template=template_url,
            name=attributes.pop('name', ''),
        )

        description = attributes.pop('description', '')
        link_template = settings.WALDUR_MARKETPLACE['ORDER_ITEM_LINK_TEMPLATE']
        order_item_url = link_template.format(order_item_uuid=order_item.uuid,
                                              project_uuid=order_item.order.project.uuid)
        description += "\n[Order item|%s]." % order_item_url

        if order_item.plan and order_item.plan.scope:
            post_data['plan'] = reverse('support-offering-plan-detail', kwargs={
                'uuid': order_item.plan.scope.uuid
            })

        if order_item.limits:
            components_map = order_item.offering.get_usage_components()
            for key, value in order_item.limits.items():
                component = components_map[key]
                description += "\n%s (%s): %s %s" % \
                               (component.name, component.type, value, component.measured_unit)

        if description:
            post_data['description'] = description
        if attributes:
            post_data['attributes'] = attributes
        return post_data


class DeleteRequestProcessor(processors.DeleteResourceProcessor):
    def get_viewset(self):
        return IssueViewSet

    def get_resource(self):
        return self.order_item


class UpdateRequestProcessor(processors.UpdateResourceProcessor):
    def get_view(self):
        return IssueViewSet.as_view({'post': 'update'})

    def get_post_data(self):
        return {'uuid': six.text_type(self.order_item.uuid)}
