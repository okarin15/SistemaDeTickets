from django.contrib import admin
from .models import Categoria, Ticket, HistorialTicket, UserProfile

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'categoria', 'prioridad', 'estado', 'solicitante', 'fecha_creacion']
    list_filter = ['estado', 'prioridad', 'categoria', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'solicitante__username']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

@admin.register(HistorialTicket)
class HistorialTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'usuario', 'accion', 'fecha']
    list_filter = ['fecha']
    readonly_fields = ['fecha']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'departamento']
    list_filter = ['role']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']