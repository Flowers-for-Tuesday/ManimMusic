from manim import *

def show_coordinate(
    scene: Scene,
    x_range=(-7, 7, 0.5),
    y_range=(-4, 4, 0.5),
    x_length=14,
    y_length=8,
    grid_opacity=0.6,
    axis_color=BLUE,
    grid_color=GREY,
    include_numbers=True,
):
    """
    在当前 scene 中叠加坐标系（坐标轴 + 网格）。
    可随时调用，不影响已有物体坐标。
    """
    axes = Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        axis_config={"color": axis_color},
    )

    # 坐标刻度数字
    if include_numbers:
        number_plane = NumberPlane(
            x_range=x_range,
            y_range=y_range,
            background_line_style={
                "stroke_color": grid_color,
                "stroke_opacity": grid_opacity,
            }
        )
    else:
        number_plane = NumberPlane(
            x_range=x_range,
            y_range=y_range,
            include_numbers=False,
            background_line_style={
                "stroke_color": grid_color,
                "stroke_opacity": grid_opacity,
            }
        )

    # 保证网格和坐标轴对齐
    number_plane.move_to(ORIGIN)
    axes.move_to(ORIGIN)

    # 显示
    scene.add(number_plane, axes)
    return number_plane, axes
