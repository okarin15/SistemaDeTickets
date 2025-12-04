import os
import django
import random
from django.utils import timezone
from datetime import timedelta

# 1. Configurar el entorno de Django
# Asegúrate de que 'sistema_tickets.settings' sea el nombre correcto de tu carpeta de configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_tickets.settings')
django.setup()

from django.contrib.auth.models import User
from tickets.models import Ticket, Categoria, UserProfile, FAQ, Comentario, HistorialTicket, Area

def populate():
    print("🚀 Iniciando script de población de datos...")

    # --- 0. CREAR ÁREAS (NUEVO) ---
    print("   🏢 Creando áreas...")
    
    areas_data = [
        ('Administración', 'Gerencia y administrativos'),
        ('Finanzas', 'Contabilidad y pagos'),
        ('Recursos Humanos', 'Gestión de personas'),
        ('Ventas', 'Equipo comercial'),
        ('Operaciones', 'Terreno y logística'),
        ('Bodega', 'Almacenamiento'),
        ('Tecnología', 'Departamento TI'),
        ('Otro', 'Otras áreas')
    ]
    
    lista_areas = []
    for nombre, desc in areas_data:
        area_obj, created = Area.objects.get_or_create(
            nombre=nombre, 
            defaults={'descripcion': desc}
        )
        lista_areas.append(area_obj)

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
        # Intentar obtener usuario, si no existe lo crea
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        
        if created:
            user.set_password(password)
            user.first_name = nombre
            user.last_name = apellido
            user.is_staff = is_staff
            user.is_superuser = is_staff
            user.save()
            
            # Crear o actualizar perfil
            if hasattr(user, 'userprofile'):
                user.userprofile.role = rol
                user.userprofile.save()
            else:
                UserProfile.objects.create(user=user, role=rol)
                
            print(f"      + Usuario '{username}' creado.")
        else:
            # Si ya existe, aseguramos que tenga el rol y email correctos
            user.email = email
            user.first_name = nombre
            user.last_name = apellido
            if is_staff: user.is_staff = True
            user.save()
            
            if hasattr(user, 'userprofile'):
                user.userprofile.role = rol
                user.userprofile.save()
            print(f"      . Usuario '{username}' actualizado.")
                
        return user

    # Usuarios base (Usamos tu correo real para que funcionen las notificaciones)
    mi_correo = 'jackds15rv@gmail.com' 
    
    admin_user = crear_usuario('admin', 'admin@coyahue.cl', 'admin123', 'admin', 'Super', 'Admin', is_staff=True)
    tecnico = crear_usuario('tecnico', 'tecnico@coyahue.cl', 'tecnico123', 'tech', 'Roberto', 'Técnico')
    okatecnico = crear_usuario('okatecnico', 'okatecnico@coyahue.cl', 'tecnico123', 'tech', 'Diego', 'Sepúlveda')
    usuario = crear_usuario('user', mi_correo, 'user123', 'user', 'Juan', 'Usuario')
    okarin = crear_usuario('okarin', mi_correo, 'okarin123', 'user', 'Okarin', 'Demo')

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
    tecnicos_disponibles = [tecnico, okatecnico]

    for i in range(15): # Crear 15 tickets aleatorios
        titulo_base, cat_nombre, prioridad = random.choice(problemas)
        categoria = Categoria.objects.get(nombre=cat_nombre)
        area_azar = random.choice(lista_areas) # <--- Elige un área
        solicitante = random.choice([usuario, okarin])
        estado = random.choice(estados)
        
        # Fecha aleatoria en los últimos 7 días
        dias_atras = random.randint(0, 7)
        fecha_creacion = timezone.now() - timedelta(days=dias_atras)


        ticket = Ticket.objects.create(
            titulo=titulo_base,  # Solo el título limpio (ej: "Mouse roto")
            descripcion="Ticket generado automáticamente para pruebas de carga y visualización.",
            categoria=categoria,
            prioridad=prioridad,
            estado='new', # Nacen nuevos
            area=area_azar, # <--- Asigna el área aquí
            solicitante=solicitante,
            fecha_creacion=fecha_creacion
        )
        
        # Crear historial de creación
        HistorialTicket.objects.create(ticket=ticket, usuario=solicitante, accion="Creación del Ticket", fecha=fecha_creacion)

        # Simular flujo según el estado aleatorio
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
                fecha=fecha_creacion + timedelta(minutes=30)
            )

            # Agregar un comentario
            Comentario.objects.create(
                ticket=ticket,
                autor=tech_asignado,
                contenido="Hola, estoy revisando tu caso. Iré a tu puesto en breve.",
                fecha=fecha_creacion + timedelta(hours=1)
            )

            if estado in ['resolved', 'closed']:
                ticket.estado = estado
                fecha_cierre = fecha_creacion + timedelta(hours=random.randint(2, 48))
                
                if estado == 'closed':
                    ticket.fecha_cierre = fecha_cierre
                
                ticket.save()
                
                HistorialTicket.objects.create(
                    ticket=ticket, 
                    usuario=tech_asignado, 
                    accion=f"Cambio de estado a {ticket.get_estado_display()}",
                    fecha=fecha_cierre
                )
                
                # Calificación aleatoria (Satisfacción)
                if random.choice([True, False]):
                    ticket.calificacion = random.randint(3, 5)
                    ticket.comentario_calificacion = "Buen servicio, gracias."
                    ticket.save()
                    
                    HistorialTicket.objects.create(
                        ticket=ticket,
                        usuario=solicitante,
                        accion=f"Calificó el servicio con {ticket.calificacion} estrellas",
                        fecha=fecha_cierre + timedelta(minutes=15)
                    )

    print("\n✅ ¡Base de datos poblada con éxito!")
    print("========================================")
    print("Usuario Admin:   admin / admin123")
    print("Usuario Técnico: tecnico / tecnico123")
    print("Usuario Normal:  user / user123")
    print("Usuario Okarin:  okarin / okarin123")

if __name__ == '__main__':
    populate()