import numpy as np
import matplotlib.pyplot as plt
import netpbm_cpp as netpbm
import os
import random
import time

class Colors:
    BLACK_SILHOUETTE = (10, 10, 20)
    DEEP_SPACE_BLUE = (20, 30, 70)
    MOON_GLOW = (240, 240, 220)
    STAR_YELLOW = (255, 255, 180)
    STAR_BLUE = (200, 220, 255)


def visualize_image(image_obj, title, ax=None):

    show_plot = (ax is None)
    if show_plot:
        fig, ax = plt.subplots(figsize=(8, 8))

    img_data = np.array(image_obj, copy=False)

    if len(img_data.shape) == 1:
        expected_size = image_obj.get_height() * image_obj.get_width()
        channels = len(img_data) // expected_size if expected_size > 0 else 0
        if channels == 3: # PPM
            img_data = img_data.reshape((image_obj.get_height(), image_obj.get_width(), 3))
        else: # PBM/PGM
            img_data = img_data.reshape((image_obj.get_height(), image_obj.get_width()))

    cmap = 'gray' if len(img_data.shape) == 2 else None
    ax.imshow(img_data, cmap=cmap, vmin=0, vmax=255)
    ax.set_title(title, fontsize=12)
    ax.axis('off')

    if show_plot:
        plt.show()



def create_night_sky_scene(width, height):
    
    print("Creando una nueva escena de cielo nocturno...")
    img = netpbm.Image(width, height, 'ppm')


    background_color = netpbm.Color(*Colors.DEEP_SPACE_BLUE)
    img.draw_rectangle(0, 0, width, height, background_color, fill=True)

  
    star_colors = [netpbm.Color(*Colors.STAR_YELLOW), netpbm.Color(*Colors.STAR_BLUE)]
    for _ in range(200):
        x = random.randint(0, width - 1)
        y = random.randint(0, int(height * 0.8)) 
        
        img.draw_line(x, y, x, y, random.choice(star_colors))

    moon_color = netpbm.Color(*Colors.MOON_GLOW)
    moon_x, moon_y, moon_r = int(width * 0.7), int(height * 0.3), int(width * 0.15)
    img.draw_circle(moon_x, moon_y, moon_r, moon_color, fill=True)
    
    
    shadow_offset = int(width * 0.03)
    img.draw_circle(moon_x - shadow_offset, moon_y + shadow_offset, moon_r, background_color, fill=True)
    

    silhouette_color = netpbm.Color(*Colors.BLACK_SILHOUETTE)
    img.draw_rectangle(0, int(height * 0.75), width, height, silhouette_color, fill=True)

    print("Escena nocturna generada exitosamente.")
    return img

def save_and_verify(image_obj, scene_name="escena2"):

    print(f"\nGuardando la '{scene_name}' en formatos P6 (binario) y P3 (ASCII)...")
    ruta_binaria = f'{scene_name}_binaria.ppm'
    ruta_ascii = f'{scene_name}_ascii.ppm'
    
    image_obj.save(ruta_binaria, binary=True)
    print(f" Guardado en '{ruta_binaria}'")
    image_obj.save(ruta_ascii, binary=False)
    print(f"Guardado en '{ruta_ascii}'")

    print("\nCargando imágenes desde el disco para verificación...")
    try:
        img_bin = netpbm.Image(ruta_binaria)
        print(f"'{ruta_binaria}' cargada.")
        img_ascii = netpbm.Image(ruta_ascii)
        print(f"'{ruta_ascii}' cargada.")
    except Exception as e:
        print(f"Error al cargar las imágenes: {e}")
        return 

    print("\nMostrando ambas imágenes para comparación visual...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("Verificación de Guardado y Carga", fontsize=16)

    visualize_image(img_bin, f"Cargada desde Binario (P6)\n{os.path.getsize(ruta_binaria)} bytes", ax=ax1)
    visualize_image(img_ascii, f"Cargada desde ASCII (P3)\n{os.path.getsize(ruta_ascii)} bytes", ax=ax2)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    #os.remove(ruta_binaria)
    #os.remove(ruta_ascii)

def run_scene():
  
    img_generada = create_night_sky_scene(width=500, height=350)
 
    visualize_image(img_generada, "Escena Nocturna Original Generada en C++")
    
  
    save_and_verify(img_generada, scene_name="cielo_nocturno")
    
    print("\nDemostración completada")
   

if __name__ == "__main__":
    run_scene()