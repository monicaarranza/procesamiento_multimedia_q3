import numpy as np
import matplotlib.pyplot as plt
import netpbm_cpp as netpbm
import os
import time
import random

class Colors:
    
    DEEP_BLUE = (10, 25, 80)
    LIGHT_BLUE = (100, 150, 255)
    SEAWEED_GREEN = (20, 140, 60)
    BUBBLE_BLUE = (180, 220, 255)
    FISH_YELLOW = (255, 200, 0)
    BLACK = (0, 0, 0)

def visualize_image(image_obj, title, ax=None):
    
    show_plot = (ax is None)
    if show_plot:
        fig, ax = plt.subplots(figsize=(8, 8))

    img_data = np.array(image_obj, copy=False)

    if len(img_data.shape) == 1:
        expected_size = image_obj.get_height() * image_obj.get_width()
        channels = len(img_data) // expected_size if expected_size > 0 else 0
        if channels == 3:
            img_data = img_data.reshape((image_obj.get_height(), image_obj.get_width(), 3))
        else:
            img_data = img_data.reshape((image_obj.get_height(), image_obj.get_width()))

    cmap = 'gray' if len(img_data.shape) == 2 else None
    ax.imshow(img_data, cmap=cmap, vmin=0, vmax=255)
    ax.set_title(title, fontsize=12)
    ax.axis('off')

    if show_plot:
        plt.show()

def create_underwater_scene(width, height):
 
    print("Creando una nueva escena submarina...")
    img = netpbm.Image(width, height, 'ppm')

 
    for y in range(height):
        ratio = y / height
        r = int((1 - ratio) * Colors.LIGHT_BLUE[0] + ratio * Colors.DEEP_BLUE[0])
        g = int((1 - ratio) * Colors.LIGHT_BLUE[1] + ratio * Colors.DEEP_BLUE[1])
        b = int((1 - ratio) * Colors.LIGHT_BLUE[2] + ratio * Colors.DEEP_BLUE[2])
        water_color = netpbm.Color(r, g, b)
        img.draw_line(0, y, width - 1, y, water_color)

    # Algas
    algas_color = netpbm.Color(*Colors.SEAWEED_GREEN)
    for i in range(5):
        start_x = int(width * (0.1 + i * 0.2))
        end_x1 = start_x + random.randint(-20, 20)
        end_y1 = int(height * 0.7)
        end_x2 = end_x1 + random.randint(-15, 15)
        end_y2 = int(height * 0.5)
        img.draw_line(start_x, height - 1, end_x1, end_y1, algas_color)
        img.draw_line(end_x1, end_y1, end_x2, end_y2, algas_color)

    # Pez 
    fish_color = netpbm.Color(*Colors.FISH_YELLOW)
    eye_color = netpbm.Color(*Colors.BLACK)
    fish_x, fish_y, fish_r = int(width * 0.7), int(height * 0.4), int(width * 0.08)
    img.draw_circle(fish_x, fish_y, fish_r, fish_color, fill=True)
    img.draw_circle(fish_x + 10, fish_y - 5, 3, eye_color, fill=True) # Ojo

    # Burbujas a
    bubble_color = netpbm.Color(*Colors.BUBBLE_BLUE)
    for _ in range(25):
        x = random.randint(0, width)
        y = random.randint(int(height * 0.2), height)
        radius = random.randint(1, 5)
        img.draw_circle(x, y, radius, bubble_color, fill=True)

    print("Escena generada exitosamente.")
    return img

def save_and_verify(image_obj):
    print("\nGuardando la imagen en formatos P6 (binario) y P3 (ASCII)...")
    ruta_binaria = 'escena3_binaria.ppm'
    ruta_ascii = 'escena3_ascii.ppm'

    image_obj.save(ruta_binaria, binary=True)
    print(f"   Guardado en '{ruta_binaria}'")

    image_obj.save(ruta_ascii, binary=False)
    print(f"   Guardado en '{ruta_ascii}'")

    print("\nCargando imágenes desde el disco para verificación...")
    time.sleep(1)

    try:
        img_cargada_bin = netpbm.Image(ruta_binaria)
        print(f"   '{ruta_binaria}' cargada.")
        img_cargada_ascii = netpbm.Image(ruta_ascii)
        print(f"   '{ruta_ascii}' cargada.")
    except Exception as e:
        print(f"Error al cargar las imágenes: {e}")
        return

    print("\nMostrando ambas imagenes para comparacion visual...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("Verificación de Guardado y Carga", fontsize=16)

    visualize_image(img_cargada_bin, f"Cargada desde Binario (P6)\n{os.path.getsize(ruta_binaria)} bytes", ax=ax1)
    visualize_image(img_cargada_ascii, f"Cargada desde ASCII (P3)\n{os.path.getsize(ruta_ascii)} bytes", ax=ax2)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    # Limpiar los archivos generados
    #os.remove(ruta_binaria)
    #os.remove(ruta_ascii)

def run_scene():
    
    
    img_generada = create_underwater_scene(width=400, height=300)

    visualize_image(img_generada, "Escena Submarina Original generada en C++")

    save_and_verify(img_generada)

    print("\nDemostración completada.")


if __name__ == "__main__":
    run_scene()