import numpy as np
from scipy.spatial import Voronoi
from PyQt5.QtCore import QThread, pyqtSignal

class VoronoiWorker(QThread):
    """用于后台生成Voronoi图的线程"""
    finished = pyqtSignal(tuple, np.ndarray)  # (tile_coords, points)
    
    def __init__(self, tx, ty, tile_w, tile_h, density, neighbor_points=None):
        super().__init__()
        self.tx = tx
        self.ty = ty
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.density = density
        self.neighbor_points = neighbor_points
        self.rng = np.random.default_rng()

    def run(self):
        # 生成随机点
        x0, y0 = self.tx * self.tile_w, self.ty * self.tile_h
        cnt = int(self.density * self.tile_w * self.tile_h)
        
        # 使用更高效的随机数生成方法
        pts = self.rng.random((cnt, 2)) * np.array([self.tile_w, self.tile_h]) + np.array([x0, y0])

        # 如果有邻域点，合并它们
        if self.neighbor_points is not None:
            pts = np.vstack((self.neighbor_points, pts))

        # Lloyd 放松
        for _ in range(2):
            vor = Voronoi(pts)
            new_pts = []
            for i, reg_idx in enumerate(vor.point_region):
                reg = vor.regions[reg_idx]
                if -1 in reg or not reg:
                    new_pts.append(pts[i])
                else:
                    new_pts.append(vor.vertices[reg].mean(axis=0))
            pts = np.array(new_pts)

        # 只保留本瓦片的点
        pts = pts[-cnt:]
        self.finished.emit((self.tx, self.ty), pts) 