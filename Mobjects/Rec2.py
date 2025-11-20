from manim import *

class Rec2(Rectangle):
    def __init__(self, p1, p2, **kwargs):
        """
        p1: 左下角坐标 [x1, y1, z1]
        p2: 右上角坐标 [x2, y2, z2]
        其他参数传给 Rectangle，例如 color, fill_opacity...
        """

        p1 = np.array(p1)
        p2 = np.array(p2)

        # 宽度与高度
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]

        # 中心 (左下 + 右上)/2
        center = (p1 + p2) / 2

        super().__init__(width=width, height=height, **kwargs)

        # 移动到正确位置
        self.move_to(center)
