# 使用示例

## 基本用法

### 1. 生成小规模Voronoi图
```bash
# 生成1000个种子点
./generate_seeds 1000 512 seeds.csv

# 生成Voronoi图
python generate_voronoi.py seeds.csv voronoi.npz 512

# 可视化
python viz_voronoi.py voronoi.npz output.png
```

### 2. 生成大规模Voronoi图
```bash
# 生成100万个种子点
./generate_seeds 1000000 5120 seeds.csv

# 生成Voronoi图
python generate_voronoi.py seeds.csv voronoi.npz 5120

# 可视化
python viz_voronoi.py voronoi.npz output.png
```

## 参数调整

### 种子点数量影响
- 少量种子点（如1000个）：生成较大的Voronoi区域
- 大量种子点（如100万个）：生成细密的Voronoi区域

### 网格大小影响
- 小网格（如512x512）：适合快速测试
- 大网格（如5120x5120）：适合生成高分辨率图像

## 可视化效果

### 1. 基础Voronoi图
![基础Voronoi图](examples/basic.png)

### 2. 高密度Voronoi图
![高密度Voronoi图](examples/dense.png)

### 3. 自定义颜色方案
可以通过修改`viz_voronoi.py`中的颜色生成函数来实现不同的视觉效果。

## 性能测试

### 不同规模下的生成时间
| 种子点数量 | 网格大小 | 生成时间 |
|------------|----------|----------|
| 1,000      | 512      | ~1s      |
| 10,000     | 1024     | ~5s      |
| 100,000    | 2048     | ~30s     |
| 1,000,000  | 5120     | ~5min    |

注意：以上时间仅供参考，实际运行时间取决于硬件配置。 