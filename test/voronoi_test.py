import sys
import subprocess
from pathlib import Path

# 添加src目录到Python路径
src_path = str(Path(__file__).parent.parent / 'src')
sys.path.append(src_path)

from generate_voronoi import generate_voronoi
from viz_voronoi import load_data, build_regions, visualize

def run_voronoi_test():
    """运行Voronoi图生成测试"""
    print("开始Voronoi图生成测试...")
    
    # 设置测试参数
    test_seeds = 1000
    test_grid_size = 512
    
    # 生成测试数据路径
    base_dir = Path(__file__).parent
    data_dir = base_dir.parent / 'data'
    seeds_file = data_dir / 'test_seeds.csv'
    voronoi_file = data_dir / 'test_voronoi.npz'
    output_image = data_dir / 'test_output.png'
    
    try:
        # 确保数据目录存在
        data_dir.mkdir(exist_ok=True)
        
        # 生成种子点（使用C++模块）
        cpp_exe = base_dir.parent / 'src' / 'generate_seeds.exe'
        if not cpp_exe.exists():
            raise FileNotFoundError(f"C++可执行文件不存在: {cpp_exe}")
            
        cmd = [str(cpp_exe), str(test_seeds), str(test_grid_size), str(seeds_file)]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # 生成Voronoi图
        generate_voronoi(str(seeds_file), str(voronoi_file), test_grid_size)
        
        # 加载并可视化结果
        points, vertices, region_indices = load_data(str(voronoi_file))
        regions = build_regions(vertices, region_indices)
        visualize(points, regions, str(output_image))
        
        print(f"\n测试成功完成！输出图像: {output_image}")
        return True
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        return False
    
    finally:
        # 清理测试文件
        for file in [seeds_file, voronoi_file]:
            if file.exists():
                file.unlink()

if __name__ == '__main__':
    success = run_voronoi_test()
    sys.exit(0 if success else 1)
