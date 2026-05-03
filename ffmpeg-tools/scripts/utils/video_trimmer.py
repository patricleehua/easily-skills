"""
视频裁切模块（时间维度）
"""

import ffmpeg
from typing import Dict, Any, Optional
from .video_processor import VideoProcessor
from .helpers import parse_time, format_duration


class VideoTrimmer(VideoProcessor):
    """
    视频时间裁切器

    按时间段裁切视频
    """

    def trim(
        self,
        output_path: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        duration: Optional[str] = None,
        re_encode: bool = False
    ) -> Dict[str, Any]:
        """
        时间裁切

        Args:
            output_path: 输出文件路径
            start_time: 起始时间（HH:MM:SS 或秒数）
            end_time: 结束时间（HH:MM:SS 或秒数）
            duration: 持续时长（HH:MM:SS 或秒数）
            re_encode: 是否重新编码（False=复制流，更快但精度较低）

        Returns:
            处理结果字典

        Raises:
            ValueError: 参数无效
        """
        # 解析时间参数
        start_seconds = parse_time(start_time) if start_time else 0

        # 验证参数
        if end_time and duration:
            raise ValueError("end_time 和 duration 不能同时指定")

        # 构建 ffmpeg 命令
        stream = ffmpeg.input(self.input_path, ss=start_seconds)

        output_kwargs = {}

        if end_time:
            end_seconds = parse_time(end_time)
            duration_seconds = end_seconds - start_seconds
            if duration_seconds <= 0:
                raise ValueError("结束时间必须大于起始时间")
            output_kwargs['t'] = duration_seconds
        elif duration:
            duration_seconds = parse_time(duration)
            if duration_seconds <= 0:
                raise ValueError("持续时长必须大于 0")
            output_kwargs['t'] = duration_seconds

        # 是否重新编码
        if not re_encode:
            output_kwargs['c'] = 'copy'  # 复制流，速度快
        else:
            output_kwargs['vcodec'] = 'libx264'
            output_kwargs['acodec'] = 'aac'

        stream = ffmpeg.output(stream, output_path, **output_kwargs)
        self.execute_ffmpeg(stream, output_path)

        # 获取输出文件信息
        output_info = VideoProcessor(output_path).get_video_info()

        return {
            "status": "success",
            "output_file": output_path,
            "operation": "trim",
            "start_time": start_time or "0",
            "duration": format_duration(output_info['duration']),
            "size_mb": round(output_info['size_mb'], 2),
            "re_encoded": re_encode,
        }
