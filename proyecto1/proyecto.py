import numpy as np
import matplotlib.pyplot as plt
import netpbm_cpp as netpbm

# --- Función auxiliar para visualizar imágenes ---
def visualize_image(image_obj, title):
    """Usa matplotlib para mostrar un objeto de nuestra clase Image."""
    # Convertimos el buffer de la imagen C++ a un array de NumPy
    # ¡Gracias al buffer protocol, esto no copia los datos!
    img_data = np.array(image_obj, copy=False)

    # Matplotlib necesita que los datos de 3 canales tengan la forma (alto, ancho, 3)
    # PBM/PGM son 2D (alto, ancho), PPM es 3D (alto, ancho, 3)
    if len(img_data.shape) == 1 and image_obj.get_width() > 0 and image_obj.get_height() > 0:
        channels = len(img_data) // (image_obj.get_width() * image_obj.get_height())
        if channels == 3: # PPM
            img_data = img_data.reshape((image_obj.get_height(), image_obj.get_width(), 3))
        else: # PBM/PGM
             img_data = img_data.reshape((image_obj.get_height(), image_obj.get_width()))

    plt.figure(figsize=(6, 6))
    # Use gray colormap for 2D data (PBM/PGM) and default for 3D (PPM)
    plt.imshow(img_data, cmap='gray' if len(img_data.shape) == 2 else None, vmin=0, vmax=255)
    plt.title(title)
    plt.axis('off')
    plt.show()

# --- DEMOSTRACIÓN DE FUNCIONALIDADES ---

# 1. GENERAR UNA IMAGEN CON FORMAS
print("\n--- 1. Generando una imagen de 300x300 con formas... ---")
# Crear una imagen PPM (RGB) de 300x300. El fondo es blanco por defecto.
img_generada = netpbm.Image(width=300, height=300, mode='ppm')

# Definir algunos colores
rojo = netpbm.Color(255, 0, 0)
verde = netpbm.Color(0, 255, 0)
azul = netpbm.Color(0, 0, 255)
amarillo = netpbm.Color(255, 255, 0)

# Dibujar formas en la imagen
img_generada.draw_line(10, 10, 290, 10, rojo)  # Línea superior
img_generada.draw_rectangle(20, 30, 120, 100, azul, fill=False) # Rectángulo sin relleno
img_generada.draw_rectangle(150, 120, 280, 280, verde, fill=True) # Rectángulo con relleno
img_generada.draw_circle(150, 150, 80, amarillo, fill=False) # Círculo sin relleno
img_generada.draw_circle(70, 220, 40, netpbm.Color(255,0,255), fill=True) # Círculo con relleno

print("Imagen generada. Mostrando con Matplotlib...")
visualize_image(img_generada, "Imagen Generada en C++, Visualizada con Python")


# 2. GUARDAR Y CONVERTIR FORMATOS
print("\n--- 2. Guardando la imagen en PPM binario (P6) y ASCII (P3)... ---")

# Guardar en formato binario (más eficiente)
ruta_binaria = 'generada_binaria.ppm'
img_generada.save(ruta_binaria, binary=True)
print(f"Imagen guardada como '{ruta_binaria}' (Formato P6).")

# Guardar en formato ASCII (legible por humanos)
ruta_ascii = 'generada_ascii.ppm'
img_generada.save(ruta_ascii, binary=False)
print(f"Imagen guardada como '{ruta_ascii}' (Formato P3).")


# 3. CARGAR IMÁGENES Y VERIFICAR LA CONVERSIÓN
print("\n--- 3. Cargando las imágenes guardadas para verificar... ---")

# Cargar la imagen binaria que acabamos de guardar
img_cargada_bin = netpbm.Image(ruta_binaria)
print(f"'{ruta_binaria}' cargada exitosamente.")
visualize_image(img_cargada_bin, f"Visualización de '{ruta_binaria}' (Cargada desde P6)")

# Cargar la imagen ASCII para demostrar que la conversión funciona
img_cargada_ascii = netpbm.Image(ruta_ascii)
print(f"'{ruta_ascii}' cargada exitosamente.")
visualize_image(img_cargada_ascii, f"Visualización de '{ruta_ascii}' (Cargada desde P3)")

print("\n¡Proyecto completado! Todas las funcionalidades han sido demostradas.")