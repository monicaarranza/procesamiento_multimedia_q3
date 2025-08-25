import numpy as np
import matplotlib.pyplot as plt
import netpbm_cpp as netpbm
import os
import time


def visualize_image(image_obj, title, ax=None):

    show_plot = (ax is None)
    if show_plot:
        fig, ax = plt.subplots(figsize=(6, 6))

 
    img_data = np.array(image_obj, copy=False)


    if len(img_data.shape) == 1 and image_obj.get_width() > 0 and image_obj.get_height() > 0:
        channels = len(img_data) // (image_obj.get_width() * image_obj.get_height())
        if channels == 3: # PPM
            img_data = img_data.reshape((image_obj.get_height(), image_obj.get_width(), 3))
        else: # PBM/PGM
            img_data = img_data.reshape((image_obj.get_height(), image_obj.get_width()))


    cmap = 'gray' if len(img_data.shape) == 2 else None
    ax.imshow(img_data, cmap=cmap, vmin=0, vmax=255)
    ax.set_title(title, fontsize=10)
    ax.axis('off')

    if show_plot:
        plt.tight_layout()
        plt.show()


def create_test_shapes(width, height):
 
    print("1. Generando una imagen de 300x300 con formas...")
    img = netpbm.Image(width, height, 'ppm')

    # Definir colores
    rojo = netpbm.Color(255, 0, 0)
    verde = netpbm.Color(0, 255, 0)
    azul = netpbm.Color(0, 0, 255)
    amarillo = netpbm.Color(255, 255, 0)
    magenta = netpbm.Color(255, 0, 255)

    # Dibujar formas
    img.draw_line(10, 10, 290, 10, rojo)
    img.draw_rectangle(20, 30, 120, 100, azul, fill=False)
    img.draw_rectangle(150, 120, 280, 280, verde, fill=True)
    img.draw_circle(150, 150, 80, amarillo, fill=False)
    img.draw_circle(70, 220, 40, magenta, fill=True)

    print("Imagen con formas generada exitosamente.")
    return img


def save_and_verify(image_obj):
  
    print("\n2. Guardando la imagen en formatos P6 (binario) y P3 (ASCII)...")
    ruta_binaria = 'generada_binaria.ppm'
    ruta_ascii = 'generada_ascii.ppm'


    image_obj.save(ruta_binaria, binary=True)
    print(f"   Guardado en '{ruta_binaria}'")
    image_obj.save(ruta_ascii, binary=False)
    print(f"   Guardado en '{ruta_ascii}'")

    print("\n3. Cargando imágenes desde el disco para verificación...")
    time.sleep(1)

    try:
        img_cargada_bin = netpbm.Image(ruta_binaria)
        print(f"   '{ruta_binaria}' cargada.")
        img_cargada_ascii = netpbm.Image(ruta_ascii)
        print(f"   '{ruta_ascii}' cargada.")
    except Exception as e:
        print(f"Error fatal al cargar las imágenes: {e}")
        return

   
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("Verificación de Guardado y Carga", fontsize=16)


    visualize_image(img_cargada_bin, f"Cargada desde Binario (P6)\n{os.path.getsize(ruta_binaria)} bytes", ax=ax1)
    visualize_image(img_cargada_ascii, f"Cargada desde ASCII (P3)\n{os.path.getsize(ruta_ascii)} bytes", ax=ax2)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    # Limpiar los archivos generados
    #print("\nLimpiando archivos de prueba...")
    #os.remove(ruta_binaria)
    #os.remove(ruta_ascii)
    #print("Archivos eliminados.")

def run_scene():

 
    img_generada = create_test_shapes(width=300, height=300)

    visualize_image(img_generada, "Imagen Original Generada en C++")

   
    save_and_verify(img_generada)

    print("\nDemostracion completada exitosamente")
   


if __name__ == "__main__":
    run_scene()