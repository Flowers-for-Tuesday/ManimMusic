from manim import *
from music21 import *
from .MusicTex import *
from typing import Literal
import re

__all__ = [
    "CircleOfFifths",
    "blank_score"
]

KEY_DICT = {
    "C": key.Key("C"),
    "G": key.Key("G"),
    "D": key.Key("D"),
    "A": key.Key("A"),
    "E": key.Key("E"),
    "B": key.Key("B"),
    "F#": key.Key("F#"),
    "C#": key.Key("C#"),
    "F": key.Key("F"),
    "Bb": key.Key("Bb"),
    "Eb": key.Key("Eb"),
    "Ab": key.Key("Ab"),
    "Db": key.Key("Db"),
    "Gb": key.Key("Gb"),
    "Cb": key.Key("Cb"),

    "Am": key.Key("A", "minor"),
    "Em": key.Key("E", "minor"),
    "Bm": key.Key("B", "minor"),
    "F#m": key.Key("F#", "minor"),
    "C#m": key.Key("C#", "minor"),
    "G#m": key.Key("G#", "minor"),
    "D#m": key.Key("D#", "minor"),
    "A#m": key.Key("A#", "minor"),
    "Dm": key.Key("D", "minor"),
    "Gm": key.Key("G", "minor"),
    "Cm": key.Key("C", "minor"),
    "Fm": key.Key("F", "minor"),
    "Bbm": key.Key("Bb", "minor"),
    "Ebm": key.Key("Eb", "minor"),
    "Abm": key.Key("Ab", "minor"),
}

CHORD_DICT = {
    "major": [0,4,1],
    "minor": [0,8,11],
    "diminished":[0,9,6,3],
    "augmented":[0,4,8],
    "sus2":[0,2,1],
    "dominant7":[0,8,6]
}

MajorLabels1 = [
            ("C", "C"), ("G", "G"), ("D", "D"), ("A", "A"), ("E", "E"), ("B", "B"),
            ("F♯", "F#"), ("C♯", "C#"), ("A♭", "Ab"), ("E♭", "Eb"), ("B♭", "Bb"), ("F", "F")
        ]
MajorLabels2 = [
            ("C", "C"), ("G", "G"), ("D", "D"), ("A", "A"), ("E", "E"), ("C♭", "Cb"),
            ("G♭", "Gb"), ("D♭", "Db"), ("A♭", "Ab"), ("E♭", "Eb"), ("B♭", "Bb"), ("F", "F")
        ]
MinorLabels1 = [
            ("a", "Am"), ("e", "Em"), ("b", "Bm"), ("f♯", "F#m"), ("c♯", "C#m"), ("g♯", "G#m"),
            ("d♯", "D#m"), ("a♯", "Abm"), ("f", "Fm"), ("c", "Cm"), ("g", "Gm"), ("d", "Dm")
        ]
MinorLabels2 = [
            ("a", "Am"), ("e", "Em"), ("b", "Bm"), ("f♯", "F#m"), ("c♯", "C#m"), ("a♭", "Abm"),
            ("e♭", "Ebm"), ("b♭", "Bbm"), ("f", "Fm"), ("c", "Cm"), ("g", "Gm"), ("d", "Dm")
        ]
typedict = {"Major1":MajorLabels1,"Major2":MajorLabels2,"Minor1":MinorLabels1,"Minor2":MinorLabels2}

class CircleOfFifths(VGroup):
    def __init__(
            self, 
            type: Literal["Major1","Major2", "Minor1","Minor2"] = "Major1",
            radius=1.5, 
            dot_radius=0.06,
            show_scores = False,# 是否显示乐谱
            **kwargs
            ):
        super().__init__(**kwargs)
        self.radius = radius
        self.type = type
        self.labels = typedict[type]
        self.root_key = self.labels[0][1]
        self.arrows = {}  # 存储箭头，键为 (from_idx, to_idx)

        # 标签内容（从C开始，顺时针，每隔纯五度）

        # 背景圆
        circle = Circle(radius=radius, color=GREY_B, stroke_width=3)
        self.add(circle)

        # 添加12个点与标签
        for i, (label, key_signature) in enumerate(self.labels):
            angle = PI / 2 - i * TAU / 12  # C 在顶部，逆时针增加角度
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            point_pos = radius * direction

            # Dot
            dot = Dot(point_pos, radius=dot_radius, color=WHITE)
            self.add(dot)

            # Label
            text = Text(label, font_size=32,weight=BOLD).scale(0.6)
            text.move_to(point_pos + 0.4 * direction)  # 标签稍微偏离圆心方向
            self.add(text)

            if show_scores:
                score = blank_score(key_signature,"4/4",["Treble","Bass"])
                musictex = MusicTex(score,line_width=1,barline_on=False,timesignature_on=False,metronomemark_on=False)
                musictex.scale(0.4)
                musictex.move_to(point_pos + 1.3 * direction)
                musictex.set_color(WHITE)
                self.add(musictex)

    def rotate_to_key(self, target_key: str):
        """
        旋转整个Circle，使得指定的 key 出现在正上方（12点方向）。
        """
        index = next((i for i, (label, key_sig) in enumerate(self.labels) if key_sig == target_key), None)
        if index is None:
            raise ValueError(f"Invalid key: {target_key}")

        current_index = next((i for i, (label, key_sig) in enumerate(self.labels) if key_sig == self.root_key), 0)
        delta_index = index-current_index
        angle = delta_index * TAU / 12  # 每个step为 30°
        self.rotate(angle, about_point=self[0].get_center())
        self.root_key = target_key
        # 文字逆向旋转保持不变
        for mob in self.submobjects:
            if isinstance(mob, Text) or isinstance(mob, MusicTex):
                mob.rotate(-angle, about_point=mob.get_center())

    def markarrow(self, i: int, j: int, color=RED_A, radius_ratio = 0.8 ,stroke_width=3, tip_length=0.2):
        """
        在五度圈上从索引 i 指向 j 添加一条 CurvedArrow，自动弯曲角度。
        """
        if not hasattr(self, "arrows"):
            self.arrows = {}

        angle_i = i * TAU / 12
        angle_j = j * TAU / 12
        p1 = self[0].get_center()+radius_ratio*self.radius * np.array([np.sin(angle_i), np.cos(angle_i), 0])
        p2 = self[0].get_center()+radius_ratio*self.radius * np.array([np.sin(angle_j), np.cos(angle_j), 0])

        # 角度差用于控制弯曲方向与幅度
        curve_angle  = angle_i - angle_j

        arrow = CurvedArrow(p1, p2, angle=curve_angle, color=color, stroke_width=stroke_width, tip_length=tip_length)
        self.add(arrow)
        self.arrows[(i, j)] = arrow
        return Create(arrow)

    def unmarkarrow(self, i: int, j: int):
        """
        移除之前添加的从 i 到 j 的 CurvedArrow。
        """
        if hasattr(self, "arrows") and (i, j) in self.arrows:
            arrow = self.arrows.pop((i, j))
            return FadeOut(arrow)

    def show_chord(
            self,
            chord_type: str, 
            root_index: int = 0,
            color:ManimColor = BLUE_D,
            bpm:int=100
            ) -> Succession:
        """
        在当前五度圈位置下，以 root_index 为根音（0~11），根据 chord_type（如 "dim"）显示和弦动画。
        和弦结构从 CHORD_DICT 中读取，返回一个 Succession 。
        """
        if chord_type not in CHORD_DICT:
            raise ValueError(f"Unknown chord type: {chord_type}")
        if not (0 <= root_index < 12):
            raise ValueError("root_index must be between 0 and 11")

        intervals = CHORD_DICT[chord_type]
        radius = 1.5
        dots = []
        lines = []

        for i in intervals:
            idx = (root_index + i) % 12
            angle = PI / 2 - idx * TAU / 12
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            dot = Dot(pos, radius=0.08, color=color)
            dots.append(dot)

        for i in range(len(dots)):
            start = dots[i].get_center()
            end = dots[(i + 1) % len(dots)].get_center()
            line = Line(start, end, color=color, stroke_width=2)
            lines.append(line)

        chord_fig = VGroup()
        for i in range(len(dots)):
            dot = dots[i]
            line = lines[i]
            chord_fig.add(dot)   # 先放进VGroup，方便管理
            chord_fig.add(line)

        return Succession(Create(chord_fig).set_run_time(60/bpm*len(intervals)),Wait(1),FadeOut(chord_fig))

def blank_score(
    key_signature: str,
    time_signature: str,
    parts: list[str],
    bpm: int = 100
) -> stream.Score:
    """
    创建一个空的 Score，包含指定声部和基础设置。
    parts 是 ["Treble", "Bass"] 的子集。
    """
    valid_parts = {"Treble", "Bass"}
    if not set(parts).issubset(valid_parts):
        raise ValueError("parts must be subset of ['Treble', 'Bass']")
    if not parts:
        raise ValueError("parts must contain at least one of ['Treble', 'Bass']")
    
    k = KEY_DICT.get(key_signature)
    if k is None:
        raise ValueError(f"Unknown key signature: {key_signature}")

    sc = stream.Score()
    sc._part_dict = {}  # 自定义属性，方便后续访问

    for part_name in parts:
        p = stream.Part()
        p.id = part_name
        p.append(instrument.Piano())
        if part_name == "Treble":
            p.append(clef.TrebleClef())
        else:
            p.append(clef.BassClef())
        p.append(k)
        p.append(meter.TimeSignature(time_signature))
        p.append(tempo.MetronomeMark(number=bpm))

        # 添加一个全休符（空白音符）
        m = stream.Measure(number=0)
        r = note.Rest(quarterLength=2)
        m.append(r)
        p.append(m)

        sc._part_dict[part_name] = p
        sc.append(p)
    
    return sc