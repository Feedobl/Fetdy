import yt_dlp
import os
import threading

class DownloadManager:
    def __init__(self):
        self.progress_hooks = []
        self.current_download = None
        self.is_cancelled = False

    def register_progress_hook(self, hook):
        self.progress_hooks.append(hook)

    def download(self, url, output_path, media_type, quality, format_type, progress_callback=None, completion_callback=None):
        output_template = os.path.join(output_path, '%(title)s.%(ext)s')
        
        ydl_opts = {
            'outtmpl': output_template,
            'progress_hooks': [self._create_progress_hook(progress_callback)],
            'quiet': True,
            'no_warnings': True,
        }
        
        if media_type == 'audio':
            ydl_opts.update(self._get_audio_options(quality, format_type))
        else:
            ydl_opts.update(self._get_video_options(quality, format_type))
        
        self.is_cancelled = False
        thread = threading.Thread(
            target=self._download_thread,
            args=(url, ydl_opts, completion_callback)
        )
        thread.daemon = True
        thread.start()
        
        return thread
    
    def cancel_download(self):
        self.is_cancelled = True
        if self.current_download:
            self.current_download.cancel()
    
    def _download_thread(self, url, ydl_opts, completion_callback):
        result = {'success': False, 'error': None, 'filepath': None}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.current_download = ydl
                info = ydl.extract_info(url, download=True)
                if info:
                    result['success'] = True
                    result['filepath'] = os.path.join(
                        ydl_opts['outtmpl'] % {'title': info.get('title', 'download'), 'ext': info.get('ext', 'mp4')}
                    )
        except Exception as e:
            result['error'] = str(e)
        
        finally:
            self.current_download = None
            if completion_callback:
                completion_callback(result)
    
    def _create_progress_hook(self, progress_callback):
        def hook(d):
            if d['status'] == 'downloading':
                total_bytes = d.get('total_bytes')
                downloaded_bytes = d.get('downloaded_bytes', 0)
                
                if total_bytes:
                    percent = (downloaded_bytes / total_bytes) * 100
                else:
                    total_bytes_estimate = d.get('total_bytes_estimate', 0)
                    if total_bytes_estimate:
                        percent = (downloaded_bytes / total_bytes_estimate) * 100
                    else:
                        percent = 0
                
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                filename = os.path.basename(d.get('filename', ''))
                
                if progress_callback:
                    progress_callback({
                        'percent': percent,
                        'speed': self._format_speed(speed) if speed else "-- KB/s",
                        'eta': self._format_time(eta) if eta else "--:--",
                        'filename': filename,
                        'status': 'downloading'
                    })
                    
            elif d['status'] == 'finished':
                if progress_callback:
                    progress_callback({
                        'percent': 100,
                        'status': 'finished',
                        'filename': os.path.basename(d.get('filename', ''))
                    })
        
        return hook
    
    def _get_audio_options(self, quality, format_type):
        quality_map = {
            '64kbps': '64K',
            '128kbps': '128K',
            '192kbps': '192K',
            '256kbps': '256K',
            '320kbps': '320K'
        }
        
        format_map = {
            'MP3': 'mp3',
            'M4A': 'm4a',
            'WAV': 'wav',
            'FLAC': 'flac',
            'OGG': 'vorbis'
        }
        
        audio_bitrate = quality_map.get(quality, '192K')
        audio_format = format_map.get(format_type, 'mp3')
        
        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': audio_bitrate,
            }]
        }
    
    def _get_video_options(self, quality, format_type):
        quality_map = {
            '144p': '[height<=144]',
            '240p': '[height<=240]',
            '360p': '[height<=360]',
            '480p': '[height<=480]',
            '720p': '[height<=720]',
            '1080p': '[height<=1080]',
            '1440p': '[height<=1440]',
            '2160p': '[height<=2160]'
        }
        
        format_map = {
            'MP4': 'mp4',
            'MKV': 'mkv',
            'WEBM': 'webm',
            'AVI': 'avi',
            'MOV': 'mov'
        }
        
        format_selector = f'bestvideo{quality_map.get(quality, "")}+bestaudio/best{quality_map.get(quality, "")}'
        
        options = {
            'format': format_selector
        }
        
        if format_type in format_map:
            options['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': format_map[format_type]
            }]
        
        return options
    
    def _format_speed(self, speed):
        if speed < 1024:
            return f"{speed:.1f} B/s"
        elif speed < 1024 * 1024:
            return f"{speed/1024:.1f} KB/s"
        elif speed < 1024 * 1024 * 1024:
            return f"{speed/(1024*1024):.1f} MB/s"
        else:
            return f"{speed/(1024*1024*1024):.1f} GB/s"
    
    def _format_time(self, seconds):
        if seconds < 0:
            return "--:--"
        m, s = divmod(seconds, 60)
        return f"{int(m):02d}:{int(s):02d}"

download_manager = DownloadManager()