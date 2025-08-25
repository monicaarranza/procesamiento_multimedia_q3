import numpy as np
import matplotlib.pyplot as plt
import netpbm_cpp as netpbm
import os
import time


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (220, 40, 40)
    GREEN = (40, 180, 99)
    BLUE = (52, 152, 219)
    YELLOW_SUN = (241, 196, 15)
    PURPLE_SKY = (135, 78, 169)
    ORANGE_SKY = (230, 126, 34)

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


def create_artistic_scene(width, height):
   
    print("Creando una nueva escena...")
    img = netpbm.Image(width, height, 'ppm')

    
    for y in range(int(height * 0.6)):
      
        ratio = y / (height * 0.6)
        
        r = int((1 - ratio) * Colors.PURPLE_SKY[0] + ratio * Colors.ORANGE_SKY[0])
        g = int((1 - ratio) * Colors.PURPLE_SKY[1] + ratio * Colors.ORANGE_SKY[1])
        b = int((1 - ratio) * Colors.PURPLE_SKY[2] + ratio * Colors.ORANGE_SKY[2])
       
        sky_color = netpbm.Color(r, g, b)
        img.draw_line(0, y, width - 1, y, sky_color)

   
    sun_color_obj = netpbm.Color(*Colors.YELLOW_SUN)
    img.draw_circle(int(width * 0.75), int(height * 0.3), int(width * 0.1), sun_color_obj, fill=True)

    mountain_color_obj = netpbm.Color(*Colors.BLACK)
    img.draw_rectangle(0, int(height * 0.55), width, height, mountain_color_obj, fill=True)

    print("Escena generada exitosamente.")
    return img

def save_and_verify(image_obj):

    print("\n💾 Guardando la imagen en formatos P6 (binario) y P3 (ASCII)...")
    ruta_binaria = 'escena_binaria.ppm'
    ruta_ascii = 'escena_ascii.ppm'
    
    image_obj.save(ruta_binaria, binary=True)
    print(f"Guardado en '{ruta_binaria}'")
    
    image_obj.save(ruta_ascii, binary=False)
    print(f"Guardado en '{ruta_ascii}'")

    print("\Cargando imágenes desde el disco para verificación...")
    time.sleep(1) 
    
    try:
        img_cargada_bin = netpbm.Image(ruta_binaria)
        print(f" '{ruta_binaria}' cargada.")
        img_cargada_ascii = netpbm.Image(ruta_ascii)
        print(f"  '{ruta_ascii}' cargada.")
    except Exception as e:
        print(f"Error al cargar las imágenes: {e}")
        return


    print("\n Mostrando ambas imagenes para comparacion visual...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("Verificación de Guardado y Carga", fontsize=16)

    visualize_image(img_cargada_bin, f"Cargada desde Binario (P6)\n{os.path.getsize(ruta_binaria)} bytes", ax=ax1)
    visualize_image(img_cargada_ascii, f"Cargada desde ASCII (P3)\n{os.path.getsize(ruta_ascii)} bytes", ax=ax2)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
    os.remove(ruta_binaria)
    os.remove(ruta_ascii)

def main():
    print("=" * 50)
    print(" DEMOSTRACIÓN DE LA LIBRERÍA NetPBM C++")
    print("=" * 50)
    
    img_generada = create_artistic_scene(width=400, height=300)
    
    visualize_image(img_generada, "Escena Original Generada en C++")
    
    save_and_verify(img_generada)
    
    print("\n Demostracion completada")
    print("=" * 50)


if __name__ == "__main__":
    main()