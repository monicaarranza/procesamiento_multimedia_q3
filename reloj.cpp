#include <opencv2/opencv.hpp>
#include <iostream>
#include <iomanip>
#include <sstream>

int main() {
    const std::string filename = "reloj_timer.avi";
    const int fps = 30;                    
    const int duration_seconds = 30;        
    const int total_frames = fps * duration_seconds; 
    const cv::Size frame_size(640, 480);
    const bool isColor = true;

    int fourcc = cv::VideoWriter::fourcc('X', 'V', 'I', 'D');
    cv::VideoWriter writer(filename, fourcc, fps, frame_size, isColor);

    if (!writer.isOpened()) {
        std::cerr << "no se pudo abrir el archivo";
        return -1;
    }

    int font = cv::FONT_HERSHEY_SIMPLEX;
    const std::string windowName = "temporizador";
    cv::namedWindow(windowName, cv::WINDOW_AUTOSIZE);

    for (int frame_idx = 0; frame_idx < total_frames; ++frame_idx) {
        
        int seconds = frame_idx / fps;
        int milliseconds = ((frame_idx % fps) * 30) / fps;  
        cv::Mat frame(frame_size, CV_8UC3, cv::Scalar(0, 0, 0));

        std::ostringstream text;
        text << seconds << " s " 
             << std::setw(2) << std::setfill('0') << milliseconds;

        int baseline = 0;
        cv::Size text_size = cv::getTextSize(text.str(), font, 2.5, 3, &baseline);
        cv::Point text_org((frame.cols - text_size.width) / 2, (frame.rows + text_size.height) / 2);

        cv::putText(frame, text.str(), text_org, font, 2.5, cv::Scalar(255, 255, 255), 5);

        cv::imshow(windowName, frame);

        writer.write(frame);

        int key = cv::waitKey(1000 / fps);
        if (key == 27) {  
            break;
        }
    }

    writer.release();
    cv::destroyAllWindows();

    return 0;
}
