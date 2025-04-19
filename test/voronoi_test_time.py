import os
import sys
import time
import datetime
import subprocess
import pandas as pd
from pathlib import Path

# 添加src目录到Python路径
src_path = str(Path(__file__).parent.parent / 'src')
sys.path.append(src_path)

from generate_voronoi import generate_voronoi
from viz_voronoi import load_data, build_regions, visualize

# 记录每个步骤的时间戳和耗时（秒），输出字段为中文
def log_step(step_name, start_time, end_time, records):
    duration = end_time - start_time
    timestamp = datetime.datetime.now().strftime('%Y年%m月%d日 %H时%M分%S秒')
    records.append({
        '步骤': step_name,
        '时间戳': timestamp,
        '耗时(秒)': round(duration, 6)
    })

def test_performance():
    """测试不同规模下的性能"""
    # 测试参数
    test_cases = [
        (1000, 512),
        (10000, 1024),
        (100000, 2048),
        (1000000, 5120)
    ]
    
    # 准备测试环境
    base_dir = Path(__file__).parent
    data_dir = base_dir.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    all_records = []
    
    for num_seeds, grid_size in test_cases:
        print(f"\n测试用例: {num_seeds}个种子点, {grid_size}x{grid_size}网格")
        timing_records = []
        
        # 生成文件路径
        seeds_file = data_dir / f'test_seeds_{num_seeds}.csv'
        voronoi_file = data_dir / f'test_voronoi_{num_seeds}.npz'
        output_image = data_dir / f'test_output_{num_seeds}.png'
        
        # 1. 总计时开始
        total_start = time.perf_counter()
        
        # 2. 生成种子点
        step = '生成种子点'
        start = time.perf_counter()
        cpp_exe = base_dir.parent / 'src' / 'generate_seeds.exe'
        cmd = [str(cpp_exe), str(num_seeds), str(grid_size), str(seeds_file)]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e.stderr}")
            raise
        end = time.perf_counter()
        log_step(step, start, end, timing_records)
        
        # 3. 生成Voronoi图
        step = '生成Voronoi图'
        start = time.perf_counter()
        generate_voronoi(str(seeds_file), str(voronoi_file), grid_size)
        end = time.perf_counter()
        log_step(step, start, end, timing_records)
        
        # 4. 可视化
        step = '可视化'
        start = time.perf_counter()
        points, vertices, region_indices = load_data(str(voronoi_file))
        regions = build_regions(vertices, region_indices)
        visualize(points, regions, str(output_image))
        end = time.perf_counter()
        log_step(step, start, end, timing_records)
        
        # 5. 总计时结束
        total_end = time.perf_counter()
        log_step('总计时', total_start, total_end, timing_records)
        
        # 添加测试用例信息
        for record in timing_records:
            record['种子点数量'] = num_seeds
            record['网格大小'] = grid_size
            all_records.append(record)
        
        # 清理测试文件
        seeds_file.unlink()
        voronoi_file.unlink()
        output_image.unlink()
    
    # 保存所有测试结果
    log_df = pd.DataFrame(all_records)
    log_path = data_dir / 'performance_test_results.csv'
    log_df.to_csv(log_path, index=False, encoding='utf-8-sig')
    print(f"\n性能测试结果已保存到：{log_path}")

if __name__ == '__main__':
    test_performance()
