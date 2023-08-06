# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .constants import FILTER_TYPE, FILTER_ID, EXCLUDE_ID
from .settings import DEFAULT

logger = logging.getLogger(__name__)


class ObjectFilter(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=False,
        related_name='%(app_label)s_%(class)s_users',
        verbose_name=_('User'))
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=False, blank=False,
        related_name='%(app_label)s_%(class)s_content_type', verbose_name=_('Class'))
    filter_type = models.SmallIntegerField(
        choices=FILTER_TYPE, null=False, blank=False, verbose_name=_('Filter Type'))
    filter_values = models.CharField(
        max_length=250, null=True, blank=True, verbose_name=_('Values'))

    class Meta:
        verbose_name = _('Data filter')
        verbose_name_plural = _('Data filter')

    def __str__(self):
        return "%s - %s" % (', '.join([str(i) for i in self.users.all()]), self.content_type)

    @classmethod
    def _check_filter_values(cls, record=None):
        cls.filter_values = eval(record.filter_values)

        if not isinstance(cls.filter_values, list):
            raise ValueError(_('Filter Values is not a List: %s' % record.filter_values))

    @classmethod
    def _update_filter_dict(cls, model=None, field_name='id', filter_type=FILTER_ID, values=[]):
        if model and model._meta.label_lower not in cls._filter_dict:
            cls._filter_dict[model._meta.label_lower] = {FILTER_ID: {}, EXCLUDE_ID: {}}
        if values:
            if '%s__in' % field_name in cls._filter_dict[model._meta.label_lower][filter_type]:
                cls._filter_dict[model._meta.label_lower][filter_type]['%s__in' % field_name].extend(values)
                cls._filter_dict[model._meta.label_lower][filter_type]['%s__in' % field_name] = list(set(cls._filter_dict[model._meta.label_lower][filter_type]['%s__in' % field_name]))
            else:
                cls._filter_dict[model._meta.label_lower][filter_type]['%s__in' % field_name] = values
        else:
            cls._filter_dict[model._meta.label_lower][filter_type]['%s__isnull' % field_name] = True

    @classmethod
    def _create_filter_dict(cls, user=None, session=None):
        DJ_AUTH = getattr(settings, 'DJ_AUTH', DEFAULT)

        cls._filter_dict = {}

        for record in ObjectFilter.objects.filter(users=user):
            cls._check_filter_values(record)

            content_type = ContentType.objects.get(pk=record.content_type_id)
            model_class = content_type.model_class()

            # Create filter for the own class
            cls._update_filter_dict(model_class, field_name='id', filter_type=record.filter_type,
                                    values=eval(record.filter_values))

            # Create filter for the related classes
            related_models = []
            for field in model_class._meta.get_fields():
                if field.is_relation and field.related_model:
                    if field.related_model not in related_models:
                        related_models.append(field.related_model)

            for related_model in related_models:
                for field in related_model._meta.get_fields():
                    if field.is_relation and field.related_model and not field.auto_created and \
                       field.related_model == model_class:
                        if 'global_fields_exclude' in DJ_AUTH and DJ_AUTH['global_fields_exclude'] and \
                           field.name in DJ_AUTH['global_fields_exclude']:
                            continue

                        if 'global_related_fields_exclude' in DJ_AUTH and DJ_AUTH['global_related_fields_exclude'] and \
                           field.name in DJ_AUTH['global_related_fields_exclude']:
                            continue

                        if 'related_filter_fields_exclude' in DJ_AUTH and DJ_AUTH['related_filter_fields_exclude'] and \
                           related_model._meta.label_lower in DJ_AUTH['related_filter_fields_exclude'] and \
                           field.name in DJ_AUTH['related_filter_fields_exclude'][related_model._meta.label_lower]:
                            continue

                        cls._update_filter_dict(related_model, field_name=field.name, filter_type=record.filter_type,
                                                values=eval(record.filter_values))

        if 'django.contrib.sessions' in settings.INSTALLED_APPS and session:
            session['dj_auth_filter_dict'] = str(cls._filter_dict)

    @classmethod
    def build_filter(cls, user=None, content_type=None, session=None):
        DJ_AUTH = getattr(settings, 'DJ_AUTH', DEFAULT)

        if 'django.contrib.sessions' in settings.INSTALLED_APPS and session and 'dj_auth_filter_dict' in session:
            cls._filter_dict = eval(session['dj_auth_filter_dict'])
        else:
            cls._create_filter_dict(user=user, session=session)

        filter_query = ''
        exclude_query = ''

        model_class = content_type.model_class()
        # filter for the own class
        if model_class._meta.label_lower in cls._filter_dict:
            if 'id__in' in cls._filter_dict[model_class._meta.label_lower][FILTER_ID]:
                pk = cls._filter_dict[model_class._meta.label_lower][FILTER_ID]['id__in']
                filter_query += "Q(**{'id__in': %s}) | " % pk
            else:
                for k, v in cls._filter_dict[model_class._meta.label_lower][FILTER_ID].items():
                    filter_query += "Q(**{'%s': %s}) | " % (k, v)

            if filter_query.endswith('| '):
                filter_query = filter_query[:-2]

            if 'id__in' in cls._filter_dict[model_class._meta.label_lower][EXCLUDE_ID]:
                pk = cls._filter_dict[model_class._meta.label_lower][EXCLUDE_ID]['id__in']
                exclude_query += "Q(**{'id__in': %s}) | " % pk
            else:
                for k, v in cls._filter_dict[model_class._meta.label_lower][EXCLUDE_ID].items():
                    exclude_query += "Q(**{'%s': %s}) | " % (k, v)

            if exclude_query.endswith('| '):
                exclude_query = exclude_query[:-2]
        else:
            # if the class is not set as filter, check FK an M2M of the class
            related_models = {}
            for field in model_class._meta.get_fields():
                if field.is_relation and field.related_model and not field.auto_created:
                    if field.related_model._meta.label_lower in cls._filter_dict:
                        if 'global_fields_exclude' in DJ_AUTH and DJ_AUTH['global_fields_exclude'] and \
                           field.name in DJ_AUTH['global_fields_exclude']:
                            continue

                        if 'related_filter_fields_exclude' in DJ_AUTH and DJ_AUTH['related_filter_fields_exclude'] and \
                           model_class._meta.label_lower in DJ_AUTH['related_filter_fields_exclude'] and \
                           field.name in DJ_AUTH['related_filter_fields_exclude'][model_class._meta.label_lower]:
                            continue

                        if field.related_model not in related_models:
                            related_models[field.related_model] = []
                        related_models[field.related_model].append(field.name)

            for related_model, field_name_list in related_models.items():
                for filter_text, filter_value in cls._filter_dict[related_model._meta.label_lower][FILTER_ID].items():
                    for field_name in field_name_list:
                        filter_query += "Q(**{'%s__%s': %s}) | " % (field_name, filter_text, filter_value)
                        filter_query += "Q(**{'%s__isnull': True}) | " % (field_name)

                for filter_text, filter_value in cls._filter_dict[related_model._meta.label_lower][EXCLUDE_ID].items():
                    for field_name in field_name_list:
                        exclude_query += "Q(**{'%s__%s': %s}) | " % (field_name, filter_text, filter_value)

            if filter_query.endswith('| '):
                filter_query = filter_query[:-2]

            if exclude_query.endswith('| '):
                exclude_query = exclude_query[:-2]

        if filter_query:
            filter_query = eval(filter_query)

        if exclude_query:
            exclude_query = eval(exclude_query)

        logger.debug("%s filter %s" % (model_class._meta.label_lower, filter_query))
        logger.debug("%s exclude %s" % (model_class._meta.label_lower, exclude_query))

        return filter_query, exclude_query


class ObjectFilterQuerySetMixin(object):

    def apply_user_object_filter(self, user=None, session=None):
        if hasattr(self, 'queryset'):
            queryset = self.queryset
        else:
            queryset = self
        if user and user.is_authenticated:
            filter_query, exclude_query = ObjectFilter.build_filter(
                user, ContentType.objects.get_for_model(self.model), session=session)
            if exclude_query:
                queryset = queryset.exclude(exclude_query).distinct()
            if filter_query:
                queryset = queryset.filter(filter_query).distinct()

        return queryset

    def apply_user_generic_objects_filter(self, user=None, session=None, content_type_ids=[]):
        DJ_AUTH = getattr(settings, 'DJ_AUTH', DEFAULT)
        if hasattr(self, 'queryset'):
            queryset = self.queryset
        else:
            queryset = self
        self.classes_to_check = []
        classes_to_check_cnt_type_ids = []
        content_type_ids = list(set(content_type_ids))

        for record in ObjectFilter.objects.filter(users=user):
            cnt_type = ContentType.objects.get(pk=record.content_type_id)
            model_class = cnt_type.model_class()

            related_models = []
            for field in model_class._meta.get_fields():
                if field.is_relation and field.related_model:
                    if field.related_model not in related_models:
                        related_models.append(field.related_model)

            for related_model in related_models:
                for field in related_model._meta.get_fields():
                    if field.is_relation and field.related_model and not field.auto_created and \
                       field.related_model == model_class:
                        try:
                            field_name = field.name.split('_')[2]
                        except Exception:
                            field_name = field.name

                        if 'global_fields_exclude' in DJ_AUTH and DJ_AUTH['global_fields_exclude'] and \
                           field_name in DJ_AUTH['global_fields_exclude']:
                            continue

                        if 'global_related_fields_exclude' in DJ_AUTH and DJ_AUTH['global_related_fields_exclude'] and \
                           field_name in DJ_AUTH['global_related_fields_exclude']:
                            continue

                        if 'related_filter_fields_exclude' in DJ_AUTH and DJ_AUTH['related_filter_fields_exclude'] and \
                           related_model._meta.label_lower in DJ_AUTH['related_filter_fields_exclude'] and \
                           field_name in DJ_AUTH['related_filter_fields_exclude'][related_model._meta.label_lower]:
                            continue

                        self.classes_to_check.append(related_model)

        f_query = ''
        e_query = ''
        self.classes_to_check = list(set(self.classes_to_check))
        for model_class in self.classes_to_check:
            cnt_type = ContentType.objects.get(app_label=model_class._meta.app_label,
                                               model=model_class._meta.model_name)
            classes_to_check_cnt_type_ids.append(cnt_type.id)
            if cnt_type.id in content_type_ids:
                content_type_ids.remove(cnt_type.id)

            filter_query, exclude_query = ObjectFilter.build_filter(
                user, content_type=cnt_type, session=session)
            if exclude_query:
                ids = model_class.objects.filter(exclude_query).values_list('id', flat=True)
                e_query += "Q(**{'content_type_id': %s, 'object_id__in': %s}) | " % (cnt_type.id, list(set(ids)))
            if filter_query:
                ids = model_class.objects.filter(filter_query).values_list('id', flat=True)
                f_query += "Q(**{'content_type_id': %s, 'object_id__in': %s}) | " % (cnt_type.id, list(set(ids)))

        # Include all objects where the datafilter could not be applied
        if not e_query:
            other_cnt_types_to_include = ContentType.objects.exclude(
                id__in=classes_to_check_cnt_type_ids).values_list('id', flat=True)
            f_query += "Q(**{'content_type_id__in': %s}) | Q(**{'content_type_id__isnull': True}) | " % (list(other_cnt_types_to_include))

        for cnt_type_id in content_type_ids:
            query = self._check_if_class_allowed_to_filter(cnt_type_id, user, session)
            if query:
                if e_query:
                    e_query += query

                if f_query:
                    f_query += query

        if e_query:
            if e_query.endswith('| '):
                e_query = e_query[:-2]
            e_query = eval(e_query)
            queryset = queryset.exclude(e_query)

        if f_query:
            if f_query.endswith('| '):
                f_query = f_query[:-2]
            f_query = eval(f_query)
            queryset = queryset.filter(f_query)

        # Apply Filters on the filtered generic objects
        queryset = queryset.apply_user_object_filter(user=user, session=session)

        return queryset

    def _check_if_class_allowed_to_filter(self, cnt_type_id=None, user=None, session=None):
        """
        Include all classes which doesn't belong to the filter, with filtering only to the content_type
        """
        query = ""
        add = True
        if cnt_type_id:
            cnt_type = ContentType.objects.get(id=cnt_type_id)
            model_class = cnt_type.model_class()
            for field in model_class._meta.get_fields():
                if field.is_relation and field.related_model:
                    if field.related_model in self.classes_to_check:
                        add = False
                        filter_query, exclude_query = ObjectFilter.build_filter(user, content_type=cnt_type, session=session)

                        if exclude_query:
                            ids = model_class.objects.filter(exclude_query).values_list('id', flat=True)
                            query += "Q(**{'content_type_id': %s, 'object_id__in': %s}) | " % (cnt_type_id, list(set(ids)))

                        if filter_query:
                            ids = model_class.objects.filter(filter_query).values_list('id', flat=True)
                            query += "Q(**{'content_type_id': %s, 'object_id__in': %s}) | " % (cnt_type_id, list(set(ids)))

                        break
            if add:
                query = "Q(**{'content_type_id': %s}) | " % cnt_type_id

        return query
