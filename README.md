# Voronoi 地形生成器

这是一个用于生成和可视化 Voronoi 图的工具集，主要用于地形模拟和板块划分。项目使用 C++ 和 Python 混合开发，结合了高性能计算和可视化功能。

## 项目结构

```
Voronoi/
├── data/                # 数据目录
│   ├── seeds.csv       # 生成的种子点数据
│   └── voronoi_data.npz # 生成的 Voronoi 图数据
├── src/                # 源代码目录
│   ├── generate_seeds.cpp    # C++ 种子点生成器
│   ├── generate_voronoi.py   # Python Voronoi 图生成器
│   └── viz_voronoi.py       # Voronoi 图可视化工具
└── test/               # 测试目录
    ├── voronoi_test.py      # 测试脚本
    └── voronoi_test_time.py # 性能测试脚本
```

## 功能特点

- 使用 C++ 生成大量随机种子点，确保高性能
- 利用 Python 的 scipy.spatial 库生成 Voronoi 图
- 提供可视化工具，支持随机颜色渲染
- 支持大规模数据处理（默认 5120x5120 网格，100万种子点）

## 使用方法

1. 生成种子点：
   ```bash
   cd src
   g++ generate_seeds.cpp -o generate_seeds
   ./generate_seeds
   ```

2. 生成 Voronoi 图：
   ```bash
   cd src
   python generate_voronoi.py
   ```

3. 可视化结果：
   ```bash
   cd src
   python viz_voronoi.py
   ```

## 依赖项

- C++ 编译器（支持 C++11）
- Python 3.x
- Python 包：
  - numpy
  - pandas
  - scipy
  - matplotlib

## 注意事项

- 默认生成 5120x5120 的网格
- 默认生成 100 万个种子点
- 生成的数据文件将保存在 `data/` 目录下
- 请确保有足够的磁盘空间 