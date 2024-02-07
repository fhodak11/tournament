from django.urls import path
from . import views

# add static url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("add_tournament/", views.add_tournament, name="add_tournament"),
    path("configure_tournament/<int:tournament_id>/", views.configure_tournament, name="configure_tournament"),
    path("add_team/", views.add_team, name="add_team"),
    path("start_tournament/<int:tournament_id>/", views.start_tournament, name="start_tournament"),
    path("delete_team/", views.delete_team, name="delete_team"),
    path('view_results/<int:tournament_id>/', views.view_results, name='view_results'), 
    path('record_scores/', views.record_scores, name='record_scores'),
    path('view_quarter_finals/<int:tournament_id>/', views.view_quarter_finals, name='view_quarters'),
    path('view_semi_finals/<int:tournament_id>', views.view_semi_finals, name='view_semi_finals'),
    path('view_pos_three/<int:tournament_id>', views.view_pos_three, name='view_pos_three'),
    path('final_results/<int:tournament_id>', views.final_results)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# print(urlpatterns)