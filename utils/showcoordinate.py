import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from manim import *

def show_coordinate(scene: Scene):
    """
    导出当前 scene 的 PNG，并用 matplotlib 打开。
    鼠标移动时显示坐标；鼠标点击时在终端输出对应 Manim 坐标。
    """

    # === 1. 导出当前 frame 到 png ===
    frame = scene.camera.get_image()
    frame = np.array(frame)   # 转 numpy
    fname = "_manim_frame.png"
    plt.imsave(fname, frame)

    # === 2. 使用 matplotlib 显示图像 ===
    img = mpimg.imread(fname)
    H, W = img.shape[:2]

    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_title("Move mouse to see coords; Click to print coords to terminal")
    ax.axis("off")

    # 文本显示
    text = ax.text(
        10, 20, "", color="yellow", fontsize=12,
        bbox=dict(boxstyle="round", facecolor="black", alpha=0.5)
    )

    # === 3. 坐标转换函数 ===
    def pixel_to_manim(px, py):
        """像素坐标 → Manim 坐标"""
        manim_x = (px / W) * 14 - 7
        manim_y = 4 - (py / H) * 8
        return manim_x, manim_y

    # === 4. 鼠标移动事件（更新坐标显示） ===
    def on_move(event):
        if event.xdata is None or event.ydata is None:
            text.set_text("")
            fig.canvas.draw_idle()
            return

        mx, my = pixel_to_manim(event.xdata, event.ydata)
        text.set_text(f"({mx:.2f}, {my:.2f})")
        fig.canvas.draw_idle()

    # === 5. 鼠标点击事件（打印坐标） ===
    def on_click(event):
        if event.xdata is None or event.ydata is None:
            return

        mx, my = pixel_to_manim(event.xdata, event.ydata)
        print(f"[CLICK] Manim coordinate: [{mx:.2f}, {my:.2f},0]")

    # 绑定事件
    fig.canvas.mpl_connect("motion_notify_event", on_move)
    fig.canvas.mpl_connect("button_press_event", on_click)

    plt.show()
