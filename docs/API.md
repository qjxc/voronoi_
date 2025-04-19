# API 文档

## C++ 模块

### generate_seeds.cpp

```cpp
void generateSeeds(int numSeeds, int gridSize, const char* outputFile)
```

生成随机种子点。

参数：
- `numSeeds`: 要生成的种子点数量
- `gridSize`: 网格大小（正方形网格的边长）
- `outputFile`: 输出文件路径（CSV格式）

输出格式：
- CSV文件，每行包含一个种子点的x,y坐标

## Python 模块

### generate_voronoi.py

```python
def generate_voronoi(seeds_file, output_file, grid_size)
```

生成Voronoi图。

参数：
- `seeds_file`: 种子点数据文件路径
- `output_file`: 输出文件路径（.npz格式）
- `grid_size`: 网格大小

### viz_voronoi.py

```python
def visualize_voronoi(data_file, output_image=None)
```

可视化Voronoi图。

参数：
- `data_file`: Voronoi数据文件路径
- `output_image`: 输出图像文件路径（可选，默认为None，将显示图像而不保存） 