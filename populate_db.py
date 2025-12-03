import os
import django
import random
from django.utils import timezone
from datetime import timedelta

# 1. Configurar el entorno de Django
# Cambia 'sistema_tickets.settings' por el nombre real de tu carpeta de configuración si es distinto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_tickets.settings')
django.setup()

from django.contrib.auth.models import User
from tickets.models import Ticket, Categoria, UserProfile, FAQ, Comentario, HistorialTicket

def populate():
    print("🚀 Iniciando script de población de datos...")

    # --- 1. CREAR CATEGORÍAS ---
    print("   📂 Creando categorías...")
    categorias_data = [
        ('Hardware', 'Fallas en equipos físicos, impresoras, monitores.'),
        ('Software', 'Errores de sistema operativo, Office, antivirus.'),
        ('Redes', 'Problemas de internet, wifi, cableado.'),
        ('Cuentas y Accesos', 'Recuperación de claves, permisos de carpetas.'),
        ('Mobiliario', 'Sillas, escritorios, iluminación.')
    ]
    
    lista_categorias = []
    for nombre, desc in categorias_data:
        cat, created = Categoria.objects.get_or_create(
            nombre=nombre, 
            defaults={'descripcion': desc, 'activo': True}
        )
        lista_categorias.append(cat)
        if created: print(f"      + Categoría '{nombre}' creada.")

    # --- 2. CREAR USUARIOS Y PERFILES ---
    print("   👥 Creando usuarios...")
    
    def crear_usuario(username, email, password, rol, nombre, apellido, is_staff=False):
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        
        if created:
            user.set_password(password)
            user.first_name = nombre
            user.last_name = apellido
            user.is_staff = is_staff
            user.is_superuser = is_staff
            user.save()
            
            # El perfil se crea por Signal, pero aseguramos el rol aquí
            if hasattr(user, 'userprofile'):
                user.userprofile.role = rol
                user.userprofile.save()
            else:
                UserProfile.objects.create(user=user, role=rol)
                
            print(f"      + Usuario '{username}' creado (Pass: {password})")
        else:
            # Si ya existe, aseguramos que tenga el rol correcto
            if hasattr(user, 'userprofile'):
                user.userprofile.role = rol
                user.userprofile.save()
                
        return user

    admin_user = crear_usuario('admin', 'admin@coyahue.cl', 'admin123', 'admin', 'Super', 'Admin', is_staff=True)
    tecnico = crear_usuario('tecnico', 'tecnico@coyahue.cl', 'tecnico123', 'tech', 'Roberto', 'Técnico')
    tecnico2 = crear_usuario('okatecnico', 'okatecnico@coyahue.cl', 'tecnico123', 'tech', 'Diego', 'Sepúlveda')
    usuario = crear_usuario('user', 'user@coyahue.cl', 'user123', 'user', 'Juan', 'Usuario')
    usuario2 = crear_usuario('okarin', 'okarin@coyahue.cl', 'user123', 'user', 'Okarin', 'Demo')

    # --- 3. CREAR FAQs ---
    print("   ❓ Creando FAQs...")
    faqs = [
        ("¿Cómo cambio mi contraseña?", "Ingresa a tu perfil en la esquina superior derecha."),
        ("No tengo internet", "Verifica que el cable de red esté conectado y la luz parpadeando."),
        ("La impresora no imprime", "Revisa si tiene papel y si no hay luces rojas."),
        ("Error 404 en el ERP", "Intenta borrar las cookies del navegador y recargar.")
    ]
    
    for preg, resp in faqs:
        FAQ.objects.get_or_create(pregunta=preg, defaults={'respuesta': resp, 'creado_por': tecnico})

    # --- 4. CREAR TICKETS Y MOVIMIENTOS ---
    print("   🎫 Generando tickets e historial...")
    
    problemas = [
        ("El mouse no funciona", "Hardware", "high"),
        ("Pantalla azul", "Hardware", "critical"),
        ("No puedo entrar al ERP", "Software", "medium"),
        ("Internet lento", "Redes", "low"),
        ("Necesito instalar Python", "Software", "low"),
        ("La impresora atasca papel", "Hardware", "medium"),
        ("No me llegan correos", "Cuentas y Accesos", "high"),
        ("Silla rota", "Mobiliario", "low")
    ]

    estados = ['new', 'in-progress', 'resolved', 'closed']
    tecnicos_disponibles = [tecnico, tecnico2]

    for i in range(15): # Crear 15 tickets aleatorios
        titulo, cat_nombre, prioridad = random.choice(problemas)
        categoria = Categoria.objects.get(nombre=cat_nombre)
        solicitante = random.choice([usuario, usuario2])
        estado = random.choice(estados)
        
        # Fecha aleatoria en los últimos 7 días
        dias_atras = random.randint(0, 7)
        fecha_creacion = timezone.now() - timedelta(days=dias_atras)

        ticket = Ticket.objects.create(
            titulo=f"{titulo} (Caso {i+1})",
            descripcion="Ticket generado automáticamente. Se requiere asistencia en el área de operaciones.",
            categoria=categoria,
            prioridad=prioridad,
            estado='new', # Nacen nuevos
            solicitante=solicitante,
            fecha_creacion=fecha_creacion
        )
        
        # Crear historial de creación
        HistorialTicket.objects.create(ticket=ticket, usuario=solicitante, accion="Ticket Creado", fecha=fecha_creacion)

        # Simular flujo según el estado que le tocó
        if estado != 'new':
            # Asignar técnico
            tech_asignado = random.choice(tecnicos_disponibles)
            ticket.asignado_a = tech_asignado
            ticket.estado = 'in-progress'
            ticket.save()
            
            HistorialTicket.objects.create(
                ticket=ticket, 
                usuario=tech_asignado, 
                accion=f"Ticket asignado a {tech_asignado.username}",
                fecha=fecha_creacion + timedelta(hours=1)
            )

            # Agregar un comentario
            Comentario.objects.create(
                ticket=ticket,
                autor=tech_asignado,
                contenido="Hola, estoy revisando tu caso. Iré a tu puesto en breve.",
                fecha=fecha_creacion + timedelta(hours=1, minutes=10)
            )

            if estado in ['resolved', 'closed']:
                ticket.estado = estado
                if estado == 'closed':
                    ticket.fecha_cierre = fecha_creacion + timedelta(hours=4)
                ticket.save()
                
                HistorialTicket.objects.create(
                    ticket=ticket, 
                    usuario=tech_asignado, 
                    accion="Cambio de estado a Resuelto/Cerrado",
                    fecha=fecha_creacion + timedelta(hours=4)
                )
                
                # Calificación aleatoria
                if random.choice([True, False]):
                    ticket.calificacion = random.randint(3, 5)
                    ticket.comentario_calificacion = "Buen servicio, gracias."
                    ticket.save()

    print("\n✅ ¡Base de datos poblada con éxito!")
    print("========================================")
    print("Usuario Admin:   admin / admin123")
    print("Usuario Técnico: tecnico / tecnico123")
    print("Usuario Normal:  user / user123")