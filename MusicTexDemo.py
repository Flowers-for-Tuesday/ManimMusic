"""
乐谱渲染演示：展示 MusicTex 组件的使用，演示不同调性乐谱的转换
"""
from manim import *
from Mobjects import *
from utils import *
from music21 import *

class MusicTexDemo(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # 创建两个不同调性的乐谱（C大调和D大调）
        sc1 = create_piano_score1()  # C大调
        sc2 = create_piano_score2()  # D大调
        
        # 将乐谱转换为 SVG 图像
        mtx1 = MusicTex(sc1)
        mtx2 = MusicTex(sc2)
        self.wait(2)

        # 显示第一个乐谱
        self.play(Write(mtx1))
        self.wait(2)
        
        # 平滑转换为第二个乐谱（展示调号变化）
        self.play(Transform(mtx1, mtx2))
        self.wait(2)
        
        # 淡出结束
        self.play(FadeOut(*self.mobjects))
        self.wait(2)

def create_piano_score1():
    """创建C大调钢琴乐谱"""
    score = piano_score("C", "2/4", parts=["Treble", "Bass"])

    # 第1小节
    add_notes(score, "Treble", [('D5', 1.0), ('D5', 1.0), ('A5', 1.0), ('A5', 1.0)])
    add_notes(score, "Bass", [('D3', 1.0), ('D4', 1.0), ('F#4', 1.0), ('D4', 1.0)])

    # 第2小节
    add_notes(score, "Treble", [('B5', 1.0), ('B5', 1.0), ('A5', 1.0), ('A5', 1.0)])
    add_notes(score, "Bass", [('G4', 1.0), ('D4', 1.0), ('F#4', 1.0), ('D4', 1.0)])

    # 第3小节
    add_notes(score, "Treble", [('G5', 1.0), ('G5', 1.0), ('F#5', 1.0), ('F#5', 1.0)])
    add_notes(score, "Bass", [('E4', 1.0), ('C#4', 1.0), ('D4', 1.0), ('B3', 1.0)])

    # 第4小节
    add_notes(score, "Treble", [('E5', 1.0), ('E5', 0.75), ('F#5', 0.25), ('D5', 2.0)])
    add_notes(score, "Bass", [('G3', 1.0), ('A3', 1.0), ('D3', 2.0)])

    return score

def create_piano_score2():
    """创建D大调钢琴乐谱（音符相同，但调性不同）"""
    score = piano_score("D", "2/4", parts=["Treble", "Bass"])

    # 第1小节
    add_notes(score, "Treble", [('D5', 1.0), ('D5', 1.0), ('A5', 1.0), ('A5', 1.0)])
    add_notes(score, "Bass", [('D3', 1.0), ('D4', 1.0), ('F#4', 1.0), ('D4', 1.0)])

    # 第2小节
    add_notes(score, "Treble", [('B5', 1.0), ('B5', 1.0), ('A5', 1.0), ('A5', 1.0)])
    add_notes(score, "Bass", [('G4', 1.0), ('D4', 1.0), ('F#4', 1.0), ('D4', 1.0)])

    # 第3小节
    add_notes(score, "Treble", [('G5', 1.0), ('G5', 1.0), ('F#5', 1.0), ('F#5', 1.0)])
    add_notes(score, "Bass", [('E4', 1.0), ('C#4', 1.0), ('D4', 1.0), ('B3', 1.0)])

    # 第4小节
    add_notes(score, "Treble", [('E5', 1.0), ('E5', 0.75), ('F#5', 0.25), ('D5', 2.0)])
    add_notes(score, "Bass", [('G3', 1.0), ('A3', 1.0), ('D3', 2.0)])

    return score

