
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h> 
#include "netpbm.h"

namespace py = pybind11;

PYBIND11_MODULE(netpbm_cpp, m) {
    m.doc() = "Biblioteca para crear, convertir y manipular imagenes Netpbm";

    
    py::class_<Color>(m, "Color")
        .def(py::init<unsigned char, unsigned char, unsigned char>(), py::arg("r"), py::arg("g"), py::arg("b"));

    
    py::class_<Image>(m, "Image", py::buffer_protocol())
        .def(py::init<int, int, const std::string&>(), py::arg("width"), py::arg("height"), py::arg("mode"))
        .def(py::init<const std::string&>(), py::arg("filename"))

        .def("load", &Image::load, "Carga una imagen desde un archivo")
        .def("save", &Image::save, "Guarda la imagen en un archivo", py::arg("filename"), py::arg("binary") = false)

        .def("draw_line", &Image::draw_line, "Dibuja una línea (Bresenham)",
             py::arg("x0"), py::arg("y0"), py::arg("x1"), py::arg("y1"), py::arg("color"))

        .def("draw_rectangle", &Image::draw_rectangle, "Dibuja un rectángulo",
             py::arg("x0"), py::arg("y0"), py::arg("x1"), py::arg("y1"), py::arg("color"), py::arg("fill") = false)

        .def("draw_circle", &Image::draw_circle, "Dibuja un círculo (Midpoint)",
             py::arg("xc"), py::arg("yc"), py::arg("r"), py::arg("color"), py::arg("fill") = false)

        .def("get_width", &Image::get_width, "Obtiene el ancho de la imagen")
        .def("get_height", &Image::get_height, "Obtiene la altura de la imagen")

        
        .def_buffer([](Image &img) -> py::buffer_info {
            size_t channels = img.get_data().size() / ((size_t)img.get_width() * img.get_height());
            std::string format = py::format_descriptor<unsigned char>::format();
            size_t itemsize = sizeof(unsigned char);

            if (channels == 3) { // PPM (3D: height, width, channels)
                return py::buffer_info(
                    (void*)img.get_data().data(), // Puntero a los datos
                    itemsize,                    // (byte)
                    format,                     
                    3,                           
                    { (size_t)img.get_height(), (size_t)img.get_width(), channels }, 
                    { itemsize * img.get_width() * channels, itemsize * channels, itemsize } 
                );
            } else { // PBM/PGM (2D: height, width)
                 return py::buffer_info(
                    (void*)img.get_data().data(), // Puntero a los datos
                    itemsize,                    // (byte)
                    format,                      // Formato (unsigned char)
                    2,                          
                    { (size_t)img.get_height(), (size_t)img.get_width() }, 
                    { itemsize * img.get_width(), itemsize } 
                );
            }
        });
}
