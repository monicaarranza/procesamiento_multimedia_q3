
#ifndef NETPBM_H
#define NETPBM_H

#include <string>
#include <vector>
#include <stdexcept>

// Estructura simple para representar un color RGB
struct Color {
    unsigned char r, g, b;
};

class Image {
public:
    // Constructores
    Image(int width, int height, const std::string& mode);
    Image(const std::string& filename);

    // Métodos para cargar y guardar
    void load(const std::string& filename);
    void save(const std::string& filename, bool binary = false);

    // Métodos de dibujo
    void draw_line(int x0, int y0, int x1, int y1, const Color& color);
    void draw_rectangle(int x0, int y0, int x1, int y1, const Color& color, bool fill = false);
    void draw_circle(int xc, int yc, int r, const Color& color, bool fill = false);

    // Getters
    int get_width() const { return width; }
    int get_height() const { return height; }
    const std::vector<unsigned char>& get_data() const { return data; }

private:
    int width, height, max_val;
    std::string magic_number;
    std::vector<unsigned char> data;

    void set_pixel(int x, int y, const Color& color);
    void read_pbm_ascii(std::ifstream& file);
    void read_pbm_binary(std::ifstream& file);
    void read_pgm_ascii(std::ifstream& file);
    void read_pgm_binary(std::ifstream& file);
    void read_ppm_ascii(std::ifstream& file);
    void read_ppm_binary(std::ifstream& file);
};

#endif // NETPBM_H
