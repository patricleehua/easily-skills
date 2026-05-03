"""
视频处理基础类
"""

import os
import ffmpeg
from typing import Dict, Any, Optional


class VideoProcessor:
    """
    视频处理基础类

    提供通用的视频信息获取和处理方法
    """

    def __init__(self, input_path: str):
        """
        初始化视频处理器

        Args:
            input_path: 输入视频文件路径

        Raises:
            FileNotFoundError: 文件不存在
        """
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"输入文件不存在: {input_path}")

        self.input_path = input_path
        self._info_cache: Optional[Dict[str, Any]] = None

    def get_video_info(self) -> Dict[str, Any]:
        """
        获取视频信息（带缓存）

        Returns:
            包含视频信息的字典:
            - duration: 时长（秒）
            - size_mb: 文件大小（MB）
            - width: 宽度
            - height: 高度
            - has_audio: 是否有音频
            - video_codec: 视频编码
            - audio_codec: 音频编码
            - fps: 帧率

        Raises:
            RuntimeError: 无法读取视频信息
        """
        if self._info_cache is not None:
            return self._info_cache

        try:
            probe = ffmpeg.probe(self.input_path)

            # 查找视频流和音频流
            video_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'video'),
                None
            )
            audio_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'audio'),
                None
            )

            # 提取帧率
            fps = None
            if video_stream and 'r_frame_rate' in video_stream:
                fps_parts = video_stream['r_frame_rate'].split('/')
                if len(fps_parts) == 2 and int(fps_parts[1]) != 0:
                    fps = int(fps_parts[0]) / int(fps_parts[1])

            self._info_cache = {
                "duration": float(probe['format'].get('duration', 0)),
                "size_mb": float(probe['format'].get('size', 0)) / (1024 * 1024),
                "width": video_stream.get('width', 0) if video_stream else 0,
                "height": video_stream.get('height', 0) if video_stream else 0,
                "has_audio": audio_stream is not None,
                "video_codec": video_stream.get('codec_name', 'unknown') if video_stream else None,
                "audio_codec": audio_stream.get('codec_name', 'unknown') if audio_stream else None,
                "fps": fps,
                "bitrate": int(probe['format'].get('bit_rate', 0)) // 1000,  # kbps
            }

            return self._info_cache

        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise RuntimeError(f"无法读取视频信息: {error_msg}")

    def get_file_size_mb(self, file_path: str) -> float:
        """
        获取文件大小（MB）

        Args:
            file_path: 文件路径

        Returns:
            文件大小（MB）
        """
        return os.path.getsize(file_path) / (1024 * 1024)

    def execute_ffmpeg(self, stream, output_path: str) -> None:
        """
        执行 ffmpeg 命令

        Args:
            stream: ffmpeg 流对象
            output_path: 输出文件路径

        Raises:
            RuntimeError: ffmpeg 执行失败
        """
        try:
            stream.overwrite_output().run(capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise RuntimeError(f"ffmpeg 执行失败: {error_msg}")
