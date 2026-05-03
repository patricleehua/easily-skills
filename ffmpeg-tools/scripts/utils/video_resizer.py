"""
视频分辨率调整模块
"""

import ffmpeg
from typing import Dict, Any, Optional
from .video_processor import VideoProcessor


class VideoResizer(VideoProcessor):
    """
    视频分辨率调整器

    缩放视频分辨率
    """

    def resize(
        self,
        output_path: str,
        width: int,
        height: Optional[int] = None,
        keep_aspect_ratio: bool = True,
        preset: str = 'medium',
        crf: int = 23
    ) -> Dict[str, Any]:
        """
        调整分辨率

        Args:
            output_path: 输出文件路径
            width: 目标宽度
            height: 目标高度（None=保持宽高比）
            keep_aspect_ratio: 是否保持宽高比
            preset: 编码预设 (ultrafast/fast/medium/slow/veryslow)
            crf: 质量参数 (0-51, 越小质量越高，默认23)

        Returns:
            处理结果字典

        Raises:
            ValueError: 参数无效
        """
        # 验证参数
        if width <= 0:
            raise ValueError("宽度必须大于 0")

        if height is not None and height <= 0 and height != -1:
            raise ValueError("高度必须大于 0 或为 -1（保持宽高比）")

        if crf < 0 or crf > 51:
            raise ValueError("CRF 必须在 0-51 之间")

        # 获取原视频信息
        info = self.get_video_info()
        original_width = info['width']
        original_height = info['height']

        # 如果保持宽高比，计算高度
        if height is None or (keep_aspect_ratio and height == -1):
            height = -1  # ffmpeg 自动计算

        # 构建 ffmpeg 命令
        stream = ffmpeg.input(self.input_path)
        stream = ffmpeg.filter(stream, 'scale', width, height)
        stream = ffmpeg.output(
            stream,
            output_path,
            vcodec='libx264',
            acodec='aac',
            preset=preset,
            crf=crf
        )

        self.execute_ffmpeg(stream, output_path)

        # 获取输出文件信息
        output_info = VideoProcessor(output_path).get_video_info()

        return {
            "status": "success",
            "output_file": output_path,
            "operation": "resize",
            "original_resolution": f"{original_width}x{original_height}",
            "output_resolution": f"{output_info['width']}x{output_info['height']}",
            "size_mb": round(output_info['size_mb'], 2),
            "preset": preset,
            "crf": crf,
            "kept_aspect_ratio": keep_aspect_ratio,
        }
