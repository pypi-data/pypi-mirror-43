# Django Admin relation links

An easy way to add links to relations in the Django Admin site.

### Install

    pip install django-admin-relation-links

### How to use

The links are placed on the *change page* of the model and go to the *change
list page* or the *change page* of the related model, depending on whether the
related model has a `ForeignKey` to this model or this model has a `ForeignKey`
to the related model, or if it's a `OneToOneField`.

So for example, if you have these models:


```python
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=200)


class Member(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(Group, related_name='members')
```


Then in the admin you can add links on the `Group` *change page* to the
`Member` *change list page* (all the members of that group) and on the `Member`
*change page* a link to the `Group` *change page* (the group of that member).

```python
from django.contrib import admin
from django_admin_relation_links import AdminChangeLinksMixin


@admin.register(Group)
class GroupAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ['name']
    changelist_links = ['members']  # Use the `related_name` of the `Member.group` field


@admin.register(Member)
class MemberAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ['name']
    change_links = ['group']  # Just specify the name of the `ForeignKey` field
```


### Extra options

You can also set extra options like `label`, `model` and `lookup_filter` like this:

```python
@admin.register(Group)
class GroupAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ['name']
    changelist_links = [
        ('members', {
            'label': 'All members',  # Used as label for the link
            'model': 'Member',  # Specify a different model, you can also specify an app using `app.Member`
            'lookup_filter': 'user_group'  # Specify the GET parameter used for filtering the queryset
        })
    ]
```
