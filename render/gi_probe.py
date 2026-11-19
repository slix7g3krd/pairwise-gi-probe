"""第 53 批：室内外过渡时墙角漏光、动态物体发黑、探头更新时间..."""


def surface_offset(normal, bias):
    """沿探针表面法线返回采样偏移。"""
    return tuple(n * bias for n in normal)


def update_priority(distance, moved):
    """返回探针更新优先级：距离越近、相机移动过则优先级越高。"""
    return 1.0 / (1.0 + distance) + (1.0 if moved else 0.0)


def normal_bias(thickness, base):
    """按遮挡厚度返回自适应法线偏移。"""
    return base * (1.0 + thickness)


def ray_step(scene_scale, probes):
    """按场景尺度返回遮挡射线步长。"""
    return scene_scale / probes


def temporal_blend(previous, current, dt, rate):
    """按时间累积新旧辐射度。"""
    alpha = min(1.0, max(0.0, dt * rate))
    return previous + (current - previous) * alpha


def in_bounds(probe, minimum, maximum):
    """判断探针是否在有效边界内。"""
    return all(lo <= p <= hi for p, lo, hi in zip(probe, minimum, maximum))


def interpolate_weights(weights):
    """归一化探针插值权重；全零时退化为均匀权重。"""
    total = sum(weights)
    if total == 0:
        return [1.0 / len(weights)] * len(weights)
    return [w / total for w in weights]


def clear_history(scene_changed):
    """判断场景切换是否清空探针历史。"""
    return bool(scene_changed)
