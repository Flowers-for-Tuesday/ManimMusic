"""
五度圈演示：展示 CircleOfFifths 组件的使用
"""
from manim import *
from Mobjects import *
from utils import *
from music21 import *

class CircleOfFifthsDemo(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # 创建基础五度圈（不显示乐谱）
        c1 = CircleOfFifths("Major1").set_color(BLACK)
        self.wait(2)
        
        # 创建带乐谱显示的五度圈
        c2 = CircleOfFifths("Major1", show_scores=True).set_color(BLACK)
        
        # 显示基础五度圈
        self.play(Write(c1))
        self.wait(2)
        
        # 切换到带乐谱版本
        self.play(FadeOut(c1), FadeIn(c2))
        self.wait(1)
        
        # 演示旋转功能：依次旋转到G、D、A调
        self.play(c2.animate.rotate_to_key("G"))
        self.play(c2.animate.rotate_to_key("D"))
        self.play(c2.animate.rotate_to_key("A"))
        self.wait(2)
        
        # 淡出结束
        self.play(FadeOut(*self.mobjects))
        self.wait(2)