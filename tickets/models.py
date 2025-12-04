from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre

# --- NUEVO MODELO ---
class Area(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"
    
    def __str__(self):
        return self.nombre

class Ticket(models.Model):
    ESTADO_CHOICES = [
        ('new', 'Nuevo'),
        ('in-progress', 'En Progreso'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='medium')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='new')
    archivo = models.FileField(upload_to='tickets/', null=True, blank=True, verbose_name="Archivo Adjunto")
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_solicitados')
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    # --- NUEVO CAMPO ---
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Área Afectada")

    # --- NUEVOS CAMPOS DE CALIFICACIÓN ---
    calificacion = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    comentario_calificacion = models.TextField(null=True, blank=True)
    # -------------------------------------
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
    
    def __str__(self):
        return f"T-{self.id:04d} - {self.titulo}"

class HistorialTicket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = "Historial de Ticket"
        verbose_name_plural = "Historial de Tickets"

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('tech', 'Técnico'),
        ('admin', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    telefono = models.CharField(max_length=20, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class Comentario(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.ticket}"

# --- AGREGAR AL FINAL DE models.py ---
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Por defecto, creamos el perfil como 'user' (Usuario)
        # El admin luego puede cambiarlo a 'tech' si es necesario
        UserProfile.objects.create(user=instance, role='user')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Esto asegura que si guardas el usuario, se intente guardar el perfil
    # (aunque la creación la maneja la función de arriba)
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Si por alguna razón no existe (ej: usuarios viejos), lo crea
        UserProfile.objects.create(user=instance, role='user')

class FAQ(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Pregunta Frecuente"
        verbose_name_plural = "Preguntas Frecuentes"

    def __str__(self):
        return self.pregunta