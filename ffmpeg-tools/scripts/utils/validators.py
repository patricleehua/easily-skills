"""
环境和参数验证工具
"""

import os
import sys
import shutil
from typing import Optional


def validate_python_version(min_version: tuple = (3, 12)) -> None:
    """
    验证 Python 版本

    Args:
        min_version: 最低版本要求元组，如 (3, 12)

    Raises:
        SystemExit: Python 版本不满足要求
    """
    if sys.version_info < min_version:
        version_str = '.'.join(map(str, min_version))
        raise SystemExit(f"需要 Python {version_str}+，当前版本: {sys.version}")


def validate_ffmpeg_installed() -> None:
    """
    验证 ffmpeg 是否已安装

    Raises:
        SystemExit: ffmpeg 未找到
    """
    if shutil.which('ffmpeg') is None:
        raise SystemExit(
            "缺少外部依赖: ffmpeg\n"
            "请安装 ffmpeg:\n"
            "  Windows: choco install ffmpeg 或 scoop install ffmpeg\n"
            "  macOS: brew install ffmpeg\n"
            "  Linux: sudo apt install ffmpeg"
        )


def validate_file_exists(file_path: str, param_name: str = "文件") -> None:
    """
    验证文件是否存在

    Args:
        file_path: 文件路径
        param_name: 参数名称（用于错误消息）

    Raises:
        FileNotFoundError: 文件不存在
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{param_name}不存在: {file_path}")


def validate_positive_int(value: Optional[int], param_name: str) -> None:
    """
    验证正整数

    Args:
        value: 待验证的值
        param_name: 参数名称

    Raises:
        ValueError: 值不是正整数
    """
    if value is not None and value <= 0:
        raise ValueError(f"{param_name} 必须是正整数，当前值: {value}")


def validate_required_params(params: dict, required_keys: list) -> None:
    """
    验证必需参数是否提供

    Args:
        params: 参数字典
        required_keys: 必需的键列表

    Raises:
        ValueError: 缺少必需参数
    """
    missing = [key for key in required_keys if not params.get(key)]
    if missing:
        raise ValueError(f"缺少必需参数: {', '.join(missing)}")
