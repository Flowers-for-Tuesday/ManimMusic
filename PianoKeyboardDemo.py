"""
钢琴键盘演示：展示 MultiOctavePianoKeyboard 组件的使用
"""
from manim import *
from Mobjects import *
from utils import *
from music21 import *

class PianoKeyboardDemo(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # 创建两个键盘：基础版本和带标签版本
        piano1 = MultiOctavePianoKeyboard(octaves=3, start_octave=3).scale(0.8)
        piano2 = MultiOctavePianoKeyboard(octaves=3, start_octave=3, show_labels=True).scale(0.8).shift(DOWN*1)

        # 显示基础键盘
        self.play(Write(piano1))
        self.wait(2)

        # 依次高亮每个八度，展示键盘结构
        self.play(Circumscribe(piano1[0], color=TEAL), run_time=1)
        self.play(Circumscribe(piano1[1], color=TEAL), run_time=1)
        self.play(Circumscribe(piano1[2], color=TEAL), run_time=1)
        self.wait(1)
        
        # 指示特定键（白键和黑键）
        self.play(Indicate(piano1[1][0], color=BLUE_D))  # 白键
        self.play(Indicate(piano1[1][1], color=BLUE_A))  # 黑键
        self.wait(1)

        # 移动第一个键盘，显示带标签的键盘
        self.play(piano1.animate.shift(UP*1.5))
        self.play(Write(piano2))
        self.wait(2)
