# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms import TreeNodeForm
from .utils import split_pks


class TreeNodeModelAdmin(admin.ModelAdmin):

    """
    Usage:

    from django.contrib import admin
    from treenode.admin import TreeNodeModelAdmin
    from treenode.forms import TreeNodeForm
    from .models import MyModel


    class MyModelAdmin(TreeNodeModelAdmin):

        treenode_accordion = True
        form = TreeNodeForm

    admin.site.register(MyModel, MyModelAdmin)
    """

    form = TreeNodeForm
    treenode_accordion = False
    list_per_page = 1000

    def get_list_display(self, request):
        base_list_display = super(TreeNodeModelAdmin, self).get_list_display(request)
        base_list_display = list(base_list_display)
        def treenode_field_display(obj):
            return self.__get_treenode_field_display(
                obj, accordion=self.treenode_accordion, style='')
        treenode_field_display.short_description = self.model._meta.verbose_name
        treenode_field_display.allow_tags = True
        if len(base_list_display) == 1 and base_list_display[0] == '__str__':
            return (treenode_field_display, )
        else:
            treenode_display_field = getattr(self.model, 'treenode_display_field')
            if len(base_list_display) >= 1 and base_list_display[0] == treenode_display_field:
                base_list_display.pop(0)
            return (treenode_field_display, ) + tuple(base_list_display)
        return base_list_display

    def get_list_filter(self, request):
        return ()

    def __get_treenode_field_display(self, obj, accordion=True, style=''):
        ancestors_count = obj.tn_ancestors_count
        parent_pk = ''
        if ancestors_count:
            ancestors_pks = split_pks(obj.tn_ancestors_pks)
            parent_pk = ancestors_pks[-1]
        tabs = ('&mdash; ' * ancestors_count)
        tabs_class = 'treenode-tabs' if tabs else ''
        model_package = '%s.%s' % (obj.__module__, obj.__class__.__name__, )
        return mark_safe(''\
            '<span class="treenode" style="%s"'\
                    ' data-treenode-type="%s"'\
                    ' data-treenode-pk="%s"'\
                    ' data-treenode-accordion="%s"'\
                    ' data-treenode-depth="%s"'\
                    ' data-treenode-level="%s"'\
                    ' data-treenode-parent="%s">'\
                '<span class="%s">%s</span> %s'\
            '</span>' % (style,
                model_package.lower().replace('.', '_'),
                str(obj.pk),
                str(int(accordion)),
                str(obj.tn_depth),
                str(obj.tn_level),
                str(parent_pk),
                tabs_class, tabs, obj.get_display(indent=False), ))

    class Media:
        css = {'all':('treenode/css/treenode.css',)}
        js = ['treenode/js/treenode.js']
