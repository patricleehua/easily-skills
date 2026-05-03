"""
音频提取模块
"""

import os
import ffmpeg
from typing import Dict, Any, Optional
from .video_processor import VideoProcessor


class AudioExtractor(VideoProcessor):
    """
    音频提取器

    从视频中提取音频并转换为指定格式
    """

    # 音频格式对应的编码器
    CODEC_MAP = {
        'mp3': 'libmp3lame',
        'aac': 'aac',
        'wav': 'pcm_s16le',
        'flac': 'flac',
        'ogg': 'libvorbis',
        'm4a': 'aac',
    }

    def extract(
        self,
        output_path: str,
        audio_format: str = 'mp3',
        bitrate: Optional[str] = None,
        sample_rate: Optional[int] = None,
        channels: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        提取音频

        Args:
            output_path: 输出文件路径
            audio_format: 音频格式 (mp3/wav/aac/flac/ogg/m4a)
            bitrate: 音频比特率（如 "192k"）
            sample_rate: 采样率（如 44100, 48000）
            channels: 声道数（1=单声道, 2=立体声）

        Returns:
            处理结果字典

        Raises:
            ValueError: 不支持的音频格式
            RuntimeError: 提取失败
        """
        # 验证格式
        if audio_format not in self.CODEC_MAP:
            supported = ', '.join(self.CODEC_MAP.keys())
            raise ValueError(f"不支持的音频格式: {audio_format}。支持的格式: {supported}")

        # 检查视频是否包含音频
        info = self.get_video_info()
        if not info['has_audio']:
            raise RuntimeError("输入视频不包含音频流")

        # 修改输出文件扩展名
        from pathlib import Path
        output_path = str(Path(output_path).with_suffix(f'.{audio_format}'))

        # 构建 ffmpeg 命令
        stream = ffmpeg.input(self.input_path)

        # 设置音频编码器
        audio_codec = self.CODEC_MAP[audio_format]

        # 构建输出参数
        output_kwargs = {
            'acodec': audio_codec,
            'vn': None,  # 不包含视频
        }

        # 可选参数
        if bitrate:
            output_kwargs['audio_bitrate'] = bitrate

        if sample_rate:
            output_kwargs['ar'] = sample_rate

        if channels:
            output_kwargs['ac'] = channels

        # 执行转换
        stream = ffmpeg.output(stream, output_path, **output_kwargs)
        self.execute_ffmpeg(stream, output_path)

        # 返回结果
        file_size = self.get_file_size_mb(output_path)

        return {
            "status": "success",
            "output_file": output_path,
            "operation": "extract_audio",
            "format": audio_format,
            "size_mb": round(file_size, 2),
            "bitrate": bitrate,
            "sample_rate": sample_rate,
            "channels": channels,
        }
