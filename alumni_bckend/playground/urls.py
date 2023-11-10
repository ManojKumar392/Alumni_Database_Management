from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('send_email/', views.send_email, name='send_email'),
    path('login/', views.login, name='login'),
    path('choose/',views.choose, name = 'choose'),
    path('alumni/', views.alumni_list, name='alumni_list'),
    path('alumni/create/', views.alumni_create, name='alumni_create'),
    path('alumni/update/', views.alumni_update, name='alumni_update'),
    path('alumni/delete-confirm/<str:first_name>/<str:last_name>', views.alumni_delete, name='alumni_delete'),
    path('alumni/delete/', views.delete_alumni, name='delete_alumni'),
    path('alumni/user_query/', views.query_form, name='query'),
    path('alumni/list_tables/', views.list_tables, name='list_tables'),
    path('alumni/view_table/<str:table_name>', views.view_table, name='view_table'),
    path('add_job_opening/', views.add_job_opening, name='add_job_opening'),
    path('delete_job_opening/<int:job_id>/', views.delete_job_opening, name='delete_job_opening'),
    path('job_openings/',views.job_openings,name='job_openings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)