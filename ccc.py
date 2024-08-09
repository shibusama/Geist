import math

def is_curve_movement(positions):
    # 计算相邻两个位置的位移向量
    displacements = [(positions[i + 1][0] - positions[i][0], positions[i + 1][1] - positions[i][1]) for i in range(len(positions) - 1)]
    # 计算第一个位移向量与其他位移向量的夹角
    first_displacement = displacements[0]
    angles = [math.acos((first_displacement[0] * displacement[0] + first_displacement[1] * displacement[1]) / (math.sqrt(first_displacement[0] ** 2 + first_displacement[1] ** 2) * math.sqrt(displacement[0] ** 2 + displacement[1] ** 2))) for displacement in displacements[1:]]
    # 如果存在夹角不为 0 的情况，即为曲线运动
    for angle in angles:
        if not math.isclose(angle, 0, abs_tol=0.0001):
            return True
    return False

# 测试
positions = [(0, 0), (1, 0), (2, 0), (3, 0)]  # 直线运动的位置示例
print(is_curve_movement(positions))  # 输出: False

positions = [(0, 0), (1, 1), (2, 0), (3, 1)]  # 曲线运动的位置示例
print(is_curve_movement(positions))  # 输出: True