from django import template

from menu.models import MenuItem


register = template.Library()


@register.inclusion_tag('tags/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name='Main'):
    # if page not related with this menu we render only root item
    # else we render all branch and one of children layer
    path = context.get("path")
    obj = context.get("object")
    if obj and obj.menu_id == menu_name:
        menu_items = obj.get_branch()
        close_uls = "</ul>"*len(set(i.parent_id for i in menu_items))
    else:
        menu_items = [MenuItem.objects.filter(menu_id=menu_name).first()]
        close_uls = "</ul>"
    context = {'path': path, 'menu_items': menu_items, 'object': obj, 'close_uls': close_uls,}
    return context
