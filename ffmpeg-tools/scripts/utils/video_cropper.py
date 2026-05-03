"""
视频裁切模块（空间维度）
"""

import ffmpeg
from typing import Dict, Any, Optional
from .video_processor import VideoProcessor


class VideoCropper(VideoProcessor):
    """
    视频尺寸裁切器

    按画面区域裁切视频
    """

    def crop(
        self,
        output_path: str,
        width: int,
        height: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
        preset: str = 'medium'
    ) -> Dict[str, Any]:
        """
        尺寸裁切

        Args:
            output_path: 输出文件路径
            width: 裁切宽度
            height: 裁切高度
            x: 起始 X 坐标（None=居中）
            y: 起始 Y 坐标（None=居中）
            preset: 编码预设 (ultrafast/fast/medium/slow/veryslow)

        Returns:
            处理结果字典

        Raises:
            ValueError: 参数无效
        """
        # 验证参数
        if width <= 0 or height <= 0:
            raise ValueError("宽度和高度必须大于 0")

        # 获取原视频尺寸
        info = self.get_video_info()
        original_width = info['width']
        original_height = info['height']

        if width > original_width or height > original_height:
            raise ValueError(
                f"裁切尺寸 ({width}x{height}) 不能超过原视频尺寸 ({original_width}x{original_height})"
            )

        # 计算裁切起点（默认居中）
        if x is None:
            x = (original_width - width) // 2
        if y is None:
            y = (original_height - height) // 2

        # 验证裁切区域在视频范围内
        if x < 0 or y < 0 or x + width > original_width or y + height > original_height:
            raise ValueError(
                f"裁切区域超出视频范围。"
                f"原视频: {original_width}x{original_height}, "
                f"裁切区域: ({x}, {y}) -> ({x + width}, {y + height})"
            )

        # 构建 ffmpeg 命令
        stream = ffmpeg.input(self.input_path)
        stream = ffmpeg.crop(stream, x, y, width, height)
        stream = ffmpeg.output(
            stream,
            output_path,
            vcodec='libx264',
            acodec='aac',
            preset=preset
        )

        self.execute_ffmpeg(stream, output_path)

        # 获取输出文件信息
        output_info = VideoProcessor(output_path).get_video_info()

        return {
            "status": "success",
            "output_file": output_path,
            "operation": "crop",
            "original_resolution": f"{original_width}x{original_height}",
            "crop_resolution": f"{width}x{height}",
            "crop_position": f"({x}, {y})",
            "size_mb": round(output_info['size_mb'], 2),
            "preset": preset,
        }
