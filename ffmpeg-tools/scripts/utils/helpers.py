"""
辅助工具函数
"""

import os
from pathlib import Path
from typing import Optional


def parse_time(time_str: str) -> float:
    """
    将时间字符串转换为秒数

    支持格式：
    - "HH:MM:SS" 或 "MM:SS"
    - 纯秒数 "90"

    Args:
        time_str: 时间字符串

    Returns:
        秒数（float）

    Raises:
        ValueError: 时间格式无效

    Examples:
        >>> parse_time("01:30:00")
        5400.0
        >>> parse_time("90")
        90.0
        >>> parse_time("1:30")
        90.0
    """
    if not time_str:
        return 0.0

    if ':' in time_str:
        parts = time_str.split(':')
        try:
            if len(parts) == 3:
                h, m, s = map(float, parts)
                return h * 3600 + m * 60 + s
            elif len(parts) == 2:
                m, s = map(float, parts)
                return m * 60 + s
            else:
                raise ValueError(f"无效的时间格式: {time_str}")
        except ValueError as e:
            raise ValueError(f"无法解析时间 '{time_str}': {e}")

    try:
        return float(time_str)
    except ValueError:
        raise ValueError(f"无效的时间格式: {time_str}")


def format_duration(seconds: float) -> str:
    """
    将秒数格式化为可读的时间字符串

    Args:
        seconds: 秒数

    Returns:
        格式化的时间字符串 (MM:SS 或 HH:MM:SS)

    Examples:
        >>> format_duration(90)
        "1:30"
        >>> format_duration(3661)
        "1:01:01"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def get_output_path(
    input_path: str,
    output_dir: Optional[str],
    output_name: Optional[str],
    operation: str,
    extension: Optional[str] = None
) -> str:
    """
    生成输出文件路径

    兜底策略：output_dir > 源文件所在目录 > 当前工作目录

    Args:
        input_path: 输入文件路径
        output_dir: 输出目录（None 时使用源文件所在目录）
        output_name: 自定义输出文件名（可选）
        operation: 操作类型（用于自动命名）
        extension: 文件扩展名（可选，不含点号）

    Returns:
        完整的输出文件路径

    Examples:
        >>> get_output_path("/videos/video.mp4", None, None, "trim")
        "/videos/video_trim.mp4"
        >>> get_output_path("video.mp4", "./out", None, "trim")
        "./out/video_trim.mp4"
        >>> get_output_path("video.mp4", "./out", "result.mp4", "trim")
        "./out/result.mp4"
    """
    input_path_obj = Path(input_path).resolve()

    # 兜底策略：优先用 output_dir，否则用源文件所在目录，最后用 cwd
    if output_dir:
        target_dir = output_dir
    elif input_path_obj.parent.exists():
        target_dir = str(input_path_obj.parent)
    else:
        target_dir = os.getcwd()

    os.makedirs(target_dir, exist_ok=True)

    if output_name:
        return os.path.join(target_dir, output_name)

    input_stem = input_path_obj.stem

    if extension:
        output_filename = f"{input_stem}_{operation}.{extension}"
    else:
        input_ext = input_path_obj.suffix
        output_filename = f"{input_stem}_{operation}{input_ext}"

    return os.path.join(target_dir, output_filename)


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小为可读字符串

    Args:
        size_bytes: 字节数

    Returns:
        格式化的文件大小字符串

    Examples:
        >>> format_file_size(1024)
        "1.00 KB"
        >>> format_file_size(1048576)
        "1.00 MB"
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"
