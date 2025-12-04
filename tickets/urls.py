from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/tecnico/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('dashboard/user/', views.dashboard_user, name='dashboard_user'),

    # Tickets
    path('tickets/crear/', views.crear_ticket, name='crear_ticket'),
    path('tickets/mis-tickets/', views.mis_tickets, name='mis_tickets'),
    path('admin/tickets/<int:ticket_id>/actualizar/', views.actualizar_ticket, name='actualizar_ticket'),
    path('ticket/<int:ticket_id>/tomar/', views.tomar_ticket, name='tomar_ticket'),
    path('ticket/<int:ticket_id>/cambiar-estado/', views.cambiar_estado_ticket, name='cambiar_estado_ticket'),
    path('ticket/<int:ticket_id>/cambiar-prioridad/', views.cambiar_prioridad_ticket, name='cambiar_prioridad_ticket'),
    path('ticket/<int:ticket_id>/imprimir/', views.imprimir_ticket, name='imprimir_ticket'),
    path('ticket/<int:ticket_id>/calificar/', views.calificar_ticket, name='calificar_ticket'),
    path('ticket/<int:ticket_id>/comentar/', views.agregar_comentario, name='agregar_comentario'),

    # Categorías
    path('guardar-categoria/', views.guardar_categoria, name='guardar_categoria'),
    path('categoria/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # Usuarios
    path('guardar-usuario/', views.guardar_usuario, name='guardar_usuario'),

    # FAQs
    path('faq/guardar/', views.guardar_faq, name='guardar_faq'),
    path('faq/eliminar/<int:faq_id>/', views.eliminar_faq, name='eliminar_faq'),

    # --- ÁREAS (ESTAS SON LAS QUE FALTAN) ---
    path('guardar_area/', views.guardar_area, name='guardar_area'),
    path('area/eliminar/<int:area_id>/', views.eliminar_area, name='eliminar_area'),
]