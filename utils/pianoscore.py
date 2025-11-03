from music21 import *

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

def piano_score(
    key_signature: str,
    time_signature: str,
    parts: list[str],
) -> stream.Score:
    """
    创建一个空的 Score，包含指定声部和基础设置。
    parts 是 ["Treble", "Bass", "Alto"] 的子集。
    """
    valid_parts = {"Treble", "Bass", "Alto"}
    if not set(parts).issubset(valid_parts):
        raise ValueError("parts must be subset of ['Treble', 'Bass', 'Alto']")
    if not parts:
        raise ValueError("parts must contain at least one of ['Treble', 'Bass', 'Alto']")
    
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
        elif part_name == "Bass":
            p.append(clef.BassClef())
        elif part_name == "Alto":
            p.append(clef.AltoClef())
        else:
            raise ValueError(f"Unknown part name: {part_name}")

        p.append(k)
        p.append(meter.TimeSignature(time_signature))
        sc._part_dict[part_name] = p
        sc.append(p)

    return sc

def add_notes(score: stream.Score, part: str, notes, bpm: int = None):
    """
    向指定 score 的某个声部 part 添加一个小节的音符序列。
    
    支持两种格式的音符输入：
    - 单个音符或休止符，格式为 (音高, 时值)，如 ("C4", 0.25) 或 ("rest", 0.5)
    - 连杆组，格式为一个列表，内部元素为 (音高, 时值) 的元组列表，表示需要连杆的音符组
    
    函数会自动为连杆组内的音符设置 beams，手动指定连杆开始、持续和结束。
    
    参数:
    - score: music21.stream.Score 对象，目标乐谱
    - part: str，目标声部名称（需已存在于 score._part_dict 中）
    - notes: list，音符或连杆组列表，示例：
        [
            ("rest", 0.5),#休止
            [("F#4", 0.25), ("A4", 0.25)],  # 连杆组
            ("C5", 1.0),#单音
            (["C5","E5","G5"], 1.0),#和弦
            ("C5", 1.0, ["staccato", "accent"]),#articulations
        ]
    """
    if not hasattr(score, "_part_dict"):
        raise ValueError("Score has no '_part_dict' attribute; use piano_score() to create score.")
    if part not in score._part_dict:
        raise ValueError(f"Part '{part}' not found in score.")

    m = stream.Measure()  # 创建一个新小节

    # 如果指定了 bpm，且是该 Part 的首个小节，就插入 BPM
    if bpm is not None and len(score._part_dict[part].getElementsByClass(stream.Measure)) == 0:
        m.insert(0, tempo.MetronomeMark(number=bpm))

    def create_note(pitch, dur, arts=None):
        """辅助函数，根据 pitch 和 dur 创建 Note、Chord 或 Rest 对象，附加 articulations。"""
        if pitch == "rest":
            n = note.Rest()
        elif isinstance(pitch, list):  # 和弦
            n = chord.Chord(pitch)
        else:
            n = note.Note(pitch)

        n.quarterLength = dur

        # 添加 articulations（如 staccato, accent 等）
        if arts:
            art_map = {
                "staccato": articulations.Staccato,
                "tenuto": articulations.Tenuto,
                "accent": articulations.Accent,
                "marcato": articulations.StrongAccent,
                "staccatissimo": articulations.Staccatissimo,
                #"fermata": articulations.Fermata,
                "spiccato": articulations.Spiccato,
                "breath": articulations.BreathMark,
                "caesura": articulations.Caesura,
                #"portato": articulations.Portato,
            }
            for art_name in arts:
                art_class = art_map.get(art_name.lower())
                if art_class:
                    n.articulations.append(art_class())

        return n

    for entry in notes:
        if isinstance(entry, tuple):
            # 格式: (pitch, dur) 或 (pitch, dur, [articulations])
            pitch = entry[0]
            dur = entry[1]
            arts = entry[2] if len(entry) > 2 else None
            n = create_note(pitch, dur, arts)
            m.append(n)

        elif isinstance(entry, list):
            # 连杆组：[(pitch, dur), ...] 或 [(pitch, dur, [articulations]), ...]
            for i, item in enumerate(entry):
                pitch = item[0]
                dur = item[1]
                arts = item[2] if len(item) > 2 else None
                n = create_note(pitch, dur, arts)
                if i == 0:
                    n.beams.append('start')
                elif i == len(entry) - 1:
                    n.beams.append('stop')
                else:
                    n.beams.append('continue')
                m.append(n)
        else:
            raise ValueError("Invalid entry in notes: must be tuple or list of tuples.")

    score._part_dict[part].append(m)
