from django.conf.urls import url
from crudapp import crudcontroller

urlpatterns = [
url(r'^sidebar/',crudcontroller.fn_sidebar),
url(r'^insert/(?P<ins>[a-z]*)/$',crudcontroller.fn_selectdata, name='insertdata'),
url(r'^retrieve/(?P<ret>[a-z]*)/',crudcontroller.fn_selectdata),
url(r'^insertTable/(?P<up_id>[0-9]*)/$',crudcontroller.fn_insertTable, name='insert'),
url(r'^retrieveTable/$',crudcontroller.fn_retrieveTable, name='retrieve'),
url(r'^deleteTable/(?P<del_id>[0-9]+)/$',crudcontroller.fn_deleteTable),
]