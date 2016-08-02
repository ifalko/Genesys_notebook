from django.conf.urls import include, url


from .views import (
        add_record,
        list_record,
        update_record,
        delete_record,
    )

urlpatterns = [
    url(r'^add_record/', add_record, name="add_record"),
    url(r'^update_record/(?P<id>\d+)/$', update_record, name="update_record"),
    url(r'^delete_record/(?P<id>\d+)/$', delete_record, name="delete_record"),
    url(r'^', list_record, name="list_record"),
]
