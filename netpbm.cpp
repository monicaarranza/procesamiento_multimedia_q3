
#include "netpbm.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <vector> 


Image::Image(int w, int h, const std::string& mode) : width(w), height(h), max_val(255) {
    if (mode == "pbm") {
        magic_number = "P1";
        data.resize(width * height, 0); // PBM: 0=blanco
    } else if (mode == "pgm") {
        magic_number = "P2";
        data.resize(width * height, 255); // PGM: 255=blanco
    } else if (mode == "ppm") {
        magic_number = "P3";
        data.resize(width * height * 3, 255); // PPM: 255,255,255=blanco
    } else {
        throw std::runtime_error("Modo no soportado. Use 'pbm', 'pgm', o 'ppm'.");
    }
    std::cout << "DEBUG: Image created. Data size: " << data.size() << std::endl;
}


Image::Image(const std::string& filename) {
    load(filename);
}

void Image::load(const std::string& filename) {
    std::ifstream file(filename, std::ios::in | std::ios::binary);
    if (!file) throw std::runtime_error("No se pudo abrir el archivo: " + filename);

    file >> magic_number;

   
    while (file.peek() == '\n' || file.peek() == '\r' || file.peek() == ' ' || file.peek() == '\t') {
        file.get();
    }
    
    if (file.peek() == '#') {
        std::string comment;
        std::getline(file, comment);
    }
    

    file >> width >> height;

    if (magic_number != "P1" && magic_number != "P4") {
        file >> max_val;
    }

    
    file.get();

    if (magic_number == "P1") read_pbm_ascii(file);
    else if (magic_number == "P2") read_pgm_ascii(file);
    else if (magic_number == "P3") read_ppm_ascii(file);
    else if (magic_number == "P4") read_pbm_binary(file);
    else if (magic_number == "P5") read_pgm_binary(file);
    else if (magic_number == "P6") read_ppm_binary(file);
    else throw std::runtime_error("Formato Netpbm no soportado: " + magic_number);
    
    std::cout << "DEBUG: Image loaded. Data size: " << data.size() << std::endl;
}

void Image::read_pbm_ascii(std::ifstream& file) {
    data.resize(width * height);
    int pixel_val;
    for (int i = 0; i < width * height; ++i) {
        file >> pixel_val;
        data[i] = (pixel_val == 1) ? 0 : 255; 
    }
}

void Image::read_pbm_binary(std::ifstream& file) {
    data.resize(width * height);
    int bytes_per_row = (width + 7) / 8;
    std::vector<char> row_data(bytes_per_row);
    for (int r = 0; r < height; ++r) {
        file.read(row_data.data(), bytes_per_row);
        for (int c = 0; c < width; ++c) {
            int byte_idx = c / 8;
            int bit_idx = c % 8;
            data[r * width + c] = ((row_data[byte_idx] >> (7 - bit_idx)) & 1) ? 0 : 255;
        }
    }
}

void Image::read_pgm_ascii(std::ifstream& file) {
    data.resize(width * height);
    int pixel_val;
    for (int i = 0; i < width * height; ++i) {
        file >> pixel_val;
        data[i] = pixel_val;
    }
}

void Image::read_pgm_binary(std::ifstream& file) {
    data.resize(width * height);
    file.read(reinterpret_cast<char*>(data.data()), data.size());
}

void Image::read_ppm_ascii(std::ifstream& file) {
    data.resize(width * height * 3); 
    int pixel_val;
    for (int i = 0; i < width * height * 3; ++i) {
        file >> pixel_val;
        data[i] = pixel_val;
    }
}

void Image::read_ppm_binary(std::ifstream& file) {
    data.resize(width * height * 3);
    file.read(reinterpret_cast<char*>(data.data()), data.size());
}



void Image::save(const std::string& filename, bool binary) {
    std::string current_type = (magic_number == "P1" || magic_number == "P4") ? "pbm" :
                               (magic_number == "P2" || magic_number == "P5") ? "pgm" : "ppm";

    std::string out_magic_number;
    if (current_type == "pbm") out_magic_number = binary ? "P4" : "P1";
    if (current_type == "pgm") out_magic_number = binary ? "P5" : "P2";
    if (current_type == "ppm") out_magic_number = binary ? "P6" : "P3";

    std::ofstream file(filename, std::ios::out | std::ios::binary);
    if (!file) throw std::runtime_error("No se pudo crear el archivo: " + filename);

    file << out_magic_number << "\n";
    file << width << " " << height << "\n";
    if (current_type != "pbm") file << max_val << "\n";

    if (!binary) {
        for (size_t i = 0; i < data.size(); ++i) {
             if (current_type == "pbm") {
                file << (data[i] < 128 ? 1 : 0) << ( (i + 1) % width == 0 ? "\n" : " ");
            } else {
                file << static_cast<int>(data[i]) << ( (i + 1) % (current_type == "ppm" ? width*3 : width) == 0 ? "\n" : " ");
            }
        }
    } else { 
        if (current_type == "pbm") {
            std::vector<unsigned char> binary_data((width + 7) / 8 * height, 0);
            for(int i=0; i < width*height; ++i) {
                if (data[i] < 128) { 
                    int byte_idx = i / 8;
                    int bit_idx = i % 8;
                    binary_data[byte_idx] |= (1 << (7 - bit_idx));
                }
            }
            file.write(reinterpret_cast<char*>(binary_data.data()), binary_data.size());
        } else {
            file.write(reinterpret_cast<const char*>(data.data()), data.size());
        }
    }
}

void Image::set_pixel(int x, int y, const Color& color) {
    if (x < 0 || x >= width || y < 0 || y >= height) return;

    if (magic_number[1] == '1' || magic_number[1] == '4') { // PBM
        data[y * width + x] = (color.r + color.g + color.b) / 3 < 128 ? 0 : 255;
    } else if (magic_number[1] == '2' || magic_number[1] == '5') { // PGM
        data[y * width + x] = (color.r + color.g + color.b) / 3;
    } else { // PPM
        size_t index = (y * width + x) * 3;
        data[index] = color.r;
        data[index + 1] = color.g;
        data[index + 2] = color.b;
    }
}

// Algoritmo de Bresenham para lineas
void Image::draw_line(int x0, int y0, int x1, int y1, const Color& color) {
    int dx = std::abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
    int dy = -std::abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
    int err = dx + dy, e2;

    while (true) {
        set_pixel(x0, y0, color);
        if (x0 == x1 && y0 == y1) break;
        e2 = 2 * err;
        if (e2 >= dy) { err += dy; x0 += sx; }
        if (e2 <= dx) { err += dx; y0 += sy; }
    }
    std::cout << "DEBUG: draw_line completed. Data size: " << data.size() << std::endl;
}

// Dibujo de rectangulos
void Image::draw_rectangle(int x0, int y0, int x1, int y1, const Color& color, bool fill) {
    if (fill) {
        for (int y = std::min(y0, y1); y <= std::max(y0, y1); ++y) {
            for (int x = std::min(x0, x1); x <= std::max(x0, x1); ++x) {
                set_pixel(x, y, color);
            }
        }
    } else {
        draw_line(x0, y0, x1, y0, color);
        draw_line(x0, y1, x1, y1, color);
        draw_line(x0, y0, x0, y1, color);
        draw_line(x1, y0, x1, y1, color);
    }
    std::cout << "DEBUG: draw_rectangle completed. Data size: " << data.size() << std::endl;
}

// Algoritmo de Midpoint/Bresenham para circulos
void Image::draw_circle(int xc, int yc, int r, const Color& color, bool fill) {
    if (fill) {
        
        int r_sq = r * r;
        for (int y = -r; y <= r; ++y) {
            for (int x = -r; x <= r; ++x) {
                if (x * x + y * y <= r_sq) {
                    set_pixel(xc + x, yc + y, color);
                }
            }
        }
    } else {
        
        int x = r, y = 0;
        int err = 0;
        while (x >= y) {
            set_pixel(xc + x, yc + y, color); set_pixel(xc - x, yc + y, color);
            set_pixel(xc + x, yc - y, color); set_pixel(xc - y, yc - y, color);
            set_pixel(xc + y, yc + x, color); set_pixel(xc - y, yc + x, color);
            set_pixel(xc + y, yc - x, color); set_pixel(xc - y, yc - x, color);

            y++;
            if (err <= 0) {
                err += 2 * y + 1;
            }
            if (err > 0) {
                x--;
                err -= 2 * x + 1;
            }
        }
    }
    std::cout << "DEBUG: draw_circle completed. Data size: " << data.size() << std::endl;
}
