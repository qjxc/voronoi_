#include <iostream>
#include <vector>
#include <random>
#include <fstream>
#include <filesystem>
#include <string>

struct Point {
    int x, y;
};

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "用法: " << argv[0] << " <种子点数量> <网格大小> <输出文件路径>" << std::endl;
        return 1;
    }

    // 解析命令行参数
    const int P = std::stoi(argv[1]);  // 种子点数量
    const int W = std::stoi(argv[2]);  // 网格大小
    const int L = W;  // 正方形网格
    const std::string output_path = argv[3];  // 输出文件路径

    // 生成随机种子点
    std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<int> distX(0, W-1);
    std::uniform_int_distribution<int> distY(0, L-1);

    std::vector<Point> seeds;
    seeds.reserve(P);
    for (int i = 0; i < P; ++i) {
        seeds.push_back({distX(rng), distY(rng)});
    }

    // 确保输出目录存在
    std::filesystem::path output_file(output_path);
    std::filesystem::create_directories(output_file.parent_path());
    
    // 写入CSV文件
    std::ofstream out(output_path);
    if (!out) {
        std::cerr << "无法打开输出文件: " << output_path << std::endl;
        return 1;
    }

    out << "plate_id,x,y\n";
    for (int id = 0; id < (int)seeds.size(); ++id) {
        out << id << ',' << seeds[id].x << ',' << seeds[id].y << '\n';
    }
    std::cout << "种子点已写入 " << output_path << std::endl;
    return 0;
}
