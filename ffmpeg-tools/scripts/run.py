#!/usr/bin/env python3
"""
视频处理脚本入口
只负责参数解析和调度，业务逻辑在 utils 模块中
"""

import argparse
import json
import sys

from utils import (
    AudioExtractor,
    VideoTrimmer,
    VideoCropper,
    VideoResizer,
    validate_file_exists,
    validate_ffmpeg_installed,
    validate_python_version,
    get_output_path,
)


def handle_extract_audio(args) -> dict:
    """处理音频提取"""
    validate_file_exists(args.input, "输入视频")

    output_path = get_output_path(
        args.input,
        args.output_dir,
        args.output_name,
        "extract_audio",
        args.format or 'mp3'
    )

    extractor = AudioExtractor(args.input)
    return extractor.extract(
        output_path=output_path,
        audio_format=args.format or 'mp3',
        bitrate=args.bitrate,
        sample_rate=args.sample_rate,
        channels=args.channels,
    )


def handle_trim(args) -> dict:
    """处理时间裁切"""
    validate_file_exists(args.input, "输入视频")

    output_path = get_output_path(
        args.input,
        args.output_dir,
        args.output_name,
        "trim"
    )

    trimmer = VideoTrimmer(args.input)
    return trimmer.trim(
        output_path=output_path,
        start_time=args.start_time,
        end_time=args.end_time,
        duration=args.duration,
        re_encode=args.re_encode,
    )


def handle_crop(args) -> dict:
    """处理尺寸裁切"""
    validate_file_exists(args.input, "输入视频")

    if not args.width or not args.height:
        raise ValueError("crop 操作需要指定 --width 和 --height")

    output_path = get_output_path(
        args.input,
        args.output_dir,
        args.output_name,
        "crop"
    )

    cropper = VideoCropper(args.input)
    return cropper.crop(
        output_path=output_path,
        width=args.width,
        height=args.height,
        x=args.x,
        y=args.y,
        preset=args.preset or 'medium',
    )


def handle_resize(args) -> dict:
    """处理分辨率调整"""
    validate_file_exists(args.input, "输入视频")

    if not args.width:
        raise ValueError("resize 操作需要指定 --width")

    output_path = get_output_path(
        args.input,
        args.output_dir,
        args.output_name,
        "resize"
    )

    resizer = VideoResizer(args.input)
    return resizer.resize(
        output_path=output_path,
        width=args.width,
        height=args.height,
        keep_aspect_ratio=args.keep_aspect_ratio,
        preset=args.preset or 'medium',
        crf=args.crf or 23,
    )


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description='视频处理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 提取音频
  python run.py --input video.mp4 --operation extract_audio --format mp3 --bitrate 192k

  # 时间裁切
  python run.py --input video.mp4 --operation trim --start-time 10 --duration 60

  # 尺寸裁切
  python run.py --input video.mp4 --operation crop --width 1920 --height 1080

  # 调整分辨率
  python run.py --input video.mp4 --operation resize --width 1280 --height 720
        """
    )

    # 基础参数
    parser.add_argument('--input', required=True, help='输入视频文件路径')
    parser.add_argument(
        '--operation', required=True,
        choices=['trim', 'crop', 'extract_audio', 'resize'],
        help='操作类型'
    )
    parser.add_argument('--output-dir', default=None, help='输出目录（默认与源文件同目录）')
    parser.add_argument('--output-name', help='输出文件名（可选）')

    # 时间裁切参数
    trim_group = parser.add_argument_group('时间裁切参数 (trim)')
    trim_group.add_argument('--start-time', help='起始时间（HH:MM:SS 或秒数）')
    trim_group.add_argument('--end-time', help='结束时间（HH:MM:SS 或秒数）')
    trim_group.add_argument('--duration', help='持续时长（HH:MM:SS 或秒数）')
    trim_group.add_argument('--re-encode', action='store_true', help='重新编码（默认复制流）')

    # 尺寸裁切参数
    crop_group = parser.add_argument_group('尺寸裁切参数 (crop)')
    crop_group.add_argument('--width', type=int, help='宽度')
    crop_group.add_argument('--height', type=int, help='高度')
    crop_group.add_argument('--x', type=int, help='裁切起始 X 坐标（默认居中）')
    crop_group.add_argument('--y', type=int, help='裁切起始 Y 坐标（默认居中）')

    # 音频提取参数
    audio_group = parser.add_argument_group('音频提取参数 (extract_audio)')
    audio_group.add_argument(
        '--format',
        choices=['mp3', 'wav', 'aac', 'flac', 'ogg', 'm4a'],
        help='音频格式（默认 mp3）'
    )
    audio_group.add_argument('--bitrate', help='音频比特率（如 192k）')
    audio_group.add_argument('--sample-rate', type=int, help='采样率（如 44100）')
    audio_group.add_argument('--channels', type=int, choices=[1, 2], help='声道数（1/2）')

    # 分辨率调整参数
    resize_group = parser.add_argument_group('分辨率调整参数 (resize)')
    resize_group.add_argument('--keep-aspect-ratio', action='store_true', default=True,
                               help='保持宽高比（默认启用）')
    resize_group.add_argument('--crf', type=int, help='质量参数 (0-51, 默认 23)')

    # 通用编码参数
    encode_group = parser.add_argument_group('编码参数')
    encode_group.add_argument(
        '--preset',
        choices=['ultrafast', 'fast', 'medium', 'slow', 'veryslow'],
        help='编码预设（默认 medium）'
    )

    args = parser.parse_args()

    # 环境检查
    try:
        validate_python_version((3, 12))
        validate_ffmpeg_installed()
    except SystemExit as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    # 操作分发
    handlers = {
        'extract_audio': handle_extract_audio,
        'trim': handle_trim,
        'crop': handle_crop,
        'resize': handle_resize,
    }

    try:
        result = handlers[args.operation](args)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"未知错误: {str(e)}"
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
