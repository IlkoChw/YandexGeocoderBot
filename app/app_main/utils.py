from django.contrib.auth.models import Group, Permission


def create_groups_and_permissions():
    """
    Создаем группы пользователей и разрешения если отсутствуют
    """
    group1 = Group.objects.get_or_create(name='Group 1')[0]
    group2 = Group.objects.get_or_create(name='Group 2')[0]

    content_types = ['searcharea', 'searchresult']
    group2_codenames = [
        'add_searcharea',
        'change_searcharea',
        'delete_searcharea',
        'view_searcharea',
        'delete_searchresult',
        'view_searchresult']
    group1_codenames = group2_codenames[-2:]

    group2_permissions = Permission.objects.filter(
        content_type__app_label='app_main', content_type__model__in=content_types, codename__in=group2_codenames)
    group1_permissions = group2_permissions.filter(codename__in=group1_codenames)

    for p in group2_permissions:
        group2.permissions.add(p)
    for p in group1_permissions:
        group1.permissions.add(p)



