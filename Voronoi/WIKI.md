# Voronoi 地形生成器技术文档

## 1. 系统架构

本项目采用 C++ 和 Python 混合架构，充分发挥两种语言的优势：
- C++ 负责高性能的种子点生成
- Python 负责 Voronoi 图生成和可视化

### 1.1 项目结构
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

### 1.2 数据流
```
src/generate_seeds.cpp -> data/seeds.csv -> src/generate_voronoi.py -> data/voronoi_data.npz -> src/viz_voronoi.py
```

## 2. 核心组件详解

### 2.1 种子点生成器 (src/generate_seeds.cpp)

- **实现语言**: C++
- **主要功能**: 生成随机分布的种子点
- **关键参数**:
  - 网格大小: 5120x5120
  - 种子点数量: 1,000,000
- **输出格式**: CSV 文件，保存在 `data/seeds.csv`，包含 plate_id, x, y 三列

### 2.2 Voronoi 图生成器 (src/generate_voronoi.py)

- **实现语言**: Python
- **主要功能**: 基于种子点生成 Voronoi 图
- **核心库**: scipy.spatial.Voronoi
- **数据处理**:
  - 过滤无效区域
  - 处理无界区域
- **输入文件**: `data/seeds.csv`
- **输出格式**: NPZ 文件，保存在 `data/voronoi_data.npz`，包含：
  - points: 种子点坐标
  - vertices: Voronoi 顶点
  - region_indices: 区域顶点索引

### 2.3 可视化工具 (src/viz_voronoi.py)

- **实现语言**: Python
- **主要功能**: 渲染 Voronoi 图
- **核心库**: matplotlib
- **输入文件**: `data/voronoi_data.npz`
- **特性**:
  - 随机颜色渲染
  - 自适应缩放
  - 支持保存图片
- **可视化元素**:
  - 多边形区域
  - 种子点标记
  - 边界线

## 3. 性能优化

### 3.1 C++ 部分
- 使用 Mersenne Twister 随机数生成器
- 批量生成种子点
- 高效的文件 I/O 操作

### 3.2 Python 部分
- 使用 numpy 进行向量化操作
- 使用 scipy.spatial 进行高效计算
- 数据压缩存储

## 4. 数据格式说明

### 4.1 data/seeds.csv
```csv
plate_id,x,y
0,1234,5678
1,2345,6789
...
```

### 4.2 data/voronoi_data.npz
- points: (N,2) float64 数组
- vertices: (M,2) float64 数组
- region_indices: 对象数组，每个元素是顶点索引列表

## 5. 扩展性说明

### 5.1 参数调整
- 可通过修改 `src/generate_seeds.cpp` 中的常量调整网格大小和种子点数量
- 可视化参数可在 `src/viz_voronoi.py` 中调整

### 5.2 功能扩展
- 可添加地形高度计算
- 可增加区域属性（如板块类型）
- 可添加交互式可视化功能

## 6. 注意事项

### 6.1 内存使用
- 处理大量数据时注意内存占用
- 建议在 8GB 以上内存的机器上运行

### 6.2 文件大小
- data/seeds.csv: ~17MB
- data/voronoi_data.npz: ~27MB

### 6.3 性能考虑
- 种子点生成时间：约 1-2 秒
- Voronoi 图生成时间：约 10-20 秒
- 可视化时间：约 5-10 秒

### 6.4 目录结构
- 源代码文件应放在 `src/` 目录下
- 生成的数据文件将保存在 `data/` 目录下
- 测试脚本应放在 `test/` 目录下 