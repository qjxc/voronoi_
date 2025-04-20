import numpy as np
import math
from scipy.spatial import Voronoi
from PyQt5.QtCore import Qt, QPointF, QTimer
from PyQt5.QtGui import QPainter, QPen, QPainterPath
from PyQt5.QtWidgets import QWidget
from concurrent.futures import ThreadPoolExecutor
from ..core.worker import VoronoiWorker

class VoronoiWidget(QWidget):
    def __init__(self, n_initial=50, tile_size=400):
        super().__init__()
        self.setWindowTitle("稳定网格 Voronoi 图")
        self.resize(800, 600)

        # 固定瓦片尺寸
        self.tile_w = tile_size
        self.tile_h = tile_size

        # 每瓦片点密度
        self.density = n_initial / (self.tile_w * self.tile_h)

        # 瓦片管理
        self.tile_points = {}  # {(tx,ty): points}
        self.filled_tiles = set()  # {(tx,ty)}
        self.visible_tiles = set()  # 当前可见的瓦片
        self.workers = {}  # {(tx,ty): worker}
        self.thread_pool = ThreadPoolExecutor(max_workers=4)

        # 视图状态
        self.offset = np.array([0.0, 0.0])
        self.scale = 1.0
        self.min_scale = 0.1
        self.max_scale = 10.0
        self.target_scale = self.scale
        self.zoom_timer = QTimer(self)
        self.zoom_timer.timeout.connect(self._smooth_zoom)
        self.zoom_timer.setInterval(16)

        # 平移状态
        self.panning = False
        self.pan_start = None
        self.offset_start = None

        # 缓存绘制路径
        self.cached_path = None
        self.cached_points = None
        self.cached_edges = None
        self.last_visible_tiles = None
        self.last_scale = None
        self.last_offset = None

        # 预填初始瓦片
        for tx in (-1, 0, 1):
            for ty in (-1, 0, 1):
                self._fill_tile(tx, ty)

        self.setMouseTracking(True)

    def _get_neighbor_points(self, tx, ty):
        """获取邻域点"""
        neighbor_points = []
        for nx in (tx-1, tx, tx+1):
            for ny in (ty-1, ty, ty+1):
                if (nx, ny) in self.tile_points:
                    neighbor_points.extend(self.tile_points[(nx, ny)])
        return np.array(neighbor_points) if neighbor_points else None

    def _fill_tile(self, tx, ty):
        """生成瓦片的随机点并进行 Lloyd 放松"""
        if (tx, ty) in self.filled_tiles or (tx, ty) in self.workers:
            return

        # 获取邻域点
        neighbor_points = self._get_neighbor_points(tx, ty)

        # 创建并启动工作线程
        worker = VoronoiWorker(tx, ty, self.tile_w, self.tile_h, self.density, neighbor_points)
        worker.finished.connect(self._on_tile_finished)
        self.workers[(tx, ty)] = worker
        worker.start()

    def _on_tile_finished(self, coords, points):
        """处理瓦片生成完成事件"""
        tx, ty = coords
        self.tile_points[(tx, ty)] = points
        self.filled_tiles.add((tx, ty))
        del self.workers[(tx, ty)]
        self.update()

    def _get_visible_points(self):
        """获取当前可见区域内的所有点"""
        points = []
        for tile in self.visible_tiles:
            if tile in self.tile_points:
                points.extend(self.tile_points[tile])
        points_array = np.array(points)
        if len(points_array) == 0:
            return np.zeros((0, 2))
        return points_array.reshape(-1, 2)

    def _update_cached_path(self):
        """更新缓存的绘制路径"""
        if (self.visible_tiles == self.last_visible_tiles and 
            self.scale == self.last_scale and 
            np.array_equal(self.offset, self.last_offset)):
            return  # 不需要更新缓存

        pts = self._get_visible_points()
        if len(pts) >= 2:
            vor = Voronoi(pts)
            
            # 预计算所有边
            edges = []
            for ridge in vor.ridge_vertices:
                if -1 in ridge: continue
                v0, v1 = vor.vertices[ridge]
                edges.append((v0, v1))
            
            # 创建绘制路径
            path = QPainterPath()
            
            # 批量添加边
            for v0, v1 in edges:
                path.moveTo(*v0)
                path.lineTo(*v1)
            
            # 缓存结果
            self.cached_path = path
            self.cached_points = pts
            self.cached_edges = edges
            self.last_visible_tiles = self.visible_tiles.copy()
            self.last_scale = self.scale
            self.last_offset = self.offset.copy()

    def paintEvent(self, event):
        """优化绘制性能"""
        painter = QPainter(self)
        if not painter.isActive():
            return
            
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()
        painter.translate(self.offset[0], self.offset[1])
        painter.scale(self.scale, self.scale)

        # 更新缓存路径
        self._update_cached_path()

        if self.cached_path is not None:
            # 批量绘制边
            black_pen = QPen(Qt.black, 1)
            painter.setPen(black_pen)
            painter.drawPath(self.cached_path)

            # 批量绘制点
            red_pen = QPen(Qt.red, 3)
            painter.setPen(red_pen)
            for x, y in self.cached_points:
                painter.drawEllipse(QPointF(x, y), 4, 4)

        painter.restore()

    def _screen_to_world(self, screen_pos):
        """将屏幕坐标转换为世界坐标"""
        return (screen_pos - self.offset) / self.scale

    def _world_to_screen(self, world_pos):
        """将世界坐标转换为屏幕坐标"""
        return world_pos * self.scale + self.offset

    def _update_visible_tiles(self):
        """更新可见瓦片集合"""
        l = -self.offset[0] / self.scale
        t = -self.offset[1] / self.scale
        r = l + self.width() / self.scale
        b = t + self.height() / self.scale

        tx0 = math.floor(l / self.tile_w) - 1
        tx1 = math.floor(r / self.tile_w) + 1
        ty0 = math.floor(t / self.tile_h) - 1
        ty1 = math.floor(b / self.tile_h) + 1

        new_visible = set()
        for tx in range(tx0, tx1 + 1):
            for ty in range(ty0, ty1 + 1):
                new_visible.add((tx, ty))
                if (tx, ty) not in self.filled_tiles and (tx, ty) not in self.workers:
                    self._fill_tile(tx, ty)

        if new_visible != self.visible_tiles:
            self.visible_tiles = new_visible
            self.cached_path = None  # 清除缓存
            self.update()

    def _zoom_at_point(self, screen_pos, factor):
        """以指定屏幕坐标点为中心进行缩放"""
        # 直接设置目标缩放值
        if factor == 0.1:  # 最小缩放
            new_scale = self.min_scale
        elif factor == 10.0:  # 最大缩放
            new_scale = self.max_scale
        else:  # 正常缩放
            new_scale = self.scale * factor
            
        # 计算新的偏移量
        world_pos = self._screen_to_world(screen_pos)
        new_offset = screen_pos - world_pos * new_scale
        
        # 更新状态
        self.target_scale = new_scale
        self.offset = new_offset
        self.scale = new_scale  # 立即应用缩放，不等待动画
        
        # 更新可见瓦片
        self._update_visible_tiles()
        self.cached_path = None  # 清除缓存
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.panning = True
            self.pan_start = np.array([event.x(), event.y()])
            self.offset_start = self.offset.copy()

    def mouseMoveEvent(self, event):
        if self.panning and event.buttons() & Qt.LeftButton:
            curr = np.array([event.x(), event.y()])
            self.offset = self.offset_start + (curr - self.pan_start)
            self._update_visible_tiles()
            self.cached_path = None  # 清除缓存
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.panning = False

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Plus, Qt.Key_Equal):
            # 以窗口中心为缩放中心
            center = np.array([self.width()/2, self.height()/2])
            self._zoom_at_point(center, 1.1)
        elif event.key() == Qt.Key_Minus:
            # 以窗口中心为缩放中心
            center = np.array([self.width()/2, self.height()/2])
            self._zoom_at_point(center, 0.9)
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        """鼠标滚轮缩放，以鼠标位置为中心点"""
        # 获取鼠标位置
        mouse_pos = np.array([event.x(), event.y()])
        # 计算缩放因子
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        # 执行缩放
        self._zoom_at_point(mouse_pos, factor)

    def resizeEvent(self, event):
        """处理窗口大小变化"""
        # 计算窗口大小变化比例
        old_width = event.oldSize().width()
        old_height = event.oldSize().height()
        new_width = event.size().width()
        new_height = event.size().height()
        
        if old_width > 0 and old_height > 0:  # 确保不是首次创建窗口
            # 计算中心点偏移
            center_x = old_width / 2
            center_y = old_height / 2
            world_center = self._screen_to_world(np.array([center_x, center_y]))
            
            # 更新偏移量，保持中心点位置
            self.offset = np.array([new_width/2, new_height/2]) - world_center * self.scale
            
            # 更新可见瓦片
            self._update_visible_tiles()
            self.update()

    def _smooth_zoom(self):
        """平滑缩放动画"""
        if abs(self.scale - self.target_scale) < 0.001:
            self.zoom_timer.stop()
            self.scale = self.target_scale
        else:
            # 计算当前缩放比例
            self.scale = self.scale * 0.9 + self.target_scale * 0.1
            
            # 计算当前中心点在世界坐标系中的位置
            center = np.array([self.width()/2, self.height()/2])
            world_center = self._screen_to_world(center)
            
            # 更新偏移量，保持中心点位置
            self.offset = center - world_center * self.scale
            
            # 更新可见瓦片
            self._update_visible_tiles()
            self.cached_path = None  # 清除缓存
            self.update()

    def closeEvent(self, event):
        """清理资源"""
        for worker in self.workers.values():
            worker.quit()
            worker.wait()
        self.thread_pool.shutdown(wait=False)
        super().closeEvent(event) 