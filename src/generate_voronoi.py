import os
import pandas as pd
import numpy as np
from scipy.spatial import Voronoi

def generate_voronoi(seeds_file, output_file, grid_size):
    """生成Voronoi图
    
    Args:
        seeds_file (str): 种子点数据文件路径
        output_file (str): 输出文件路径
        grid_size (int): 网格大小
    """
    # 读取种子点
    df = pd.read_csv(seeds_file)
    points = df[['x', 'y']].values  # shape (N, 2)
    
    # 生成 Voronoi
    vor = Voronoi(points)
    
    # 提取可用区域的顶点索引
    region_indices = []
    for region in vor.regions:
        # 排除空区域和无界区域（含 -1）
        if not region or -1 in region:
            continue
        region_indices.append(region)
    
    # 保存为 .npz
    # points           : (N,2) float64
    # vertices         : (M,2) float64
    # region_indices   : object array of lists of ints
    np.savez_compressed(
        output_file,
        points=points,
        vertices=vor.vertices,
        region_indices=np.array(region_indices, dtype=object)
    )

if __name__ == '__main__':
    # 默认参数
    base_dir = os.path.dirname(__file__)
    seeds_file = os.path.join(base_dir, '../data/seeds.csv')
    output_file = os.path.join(base_dir, '../data/voronoi_data.npz')
    grid_size = 5120
    
    generate_voronoi(seeds_file, output_file, grid_size)
