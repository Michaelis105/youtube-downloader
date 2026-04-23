import argparse
from pytubefix import YouTube
from moviepy import VideoFileClip, AudioFileClip

def download_youtube_video(youtube_url, download_path, filename):
	print(f"Downloading video from {youtube_url} to {download_path} with filename {filename}.mp4")
	yt = YouTube(youtube_url)

	# YouTube uses DASH over HTTP for videos over 720p.
	# Use adaptive streams for higher resolutions (requires downloading video and audio separately and merging them later).
	video_stream = yt.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
	video_stream.download(output_path=download_path, filename=filename + ".mp4")

def download_youtube_audio(youtube_url, download_path, filename):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True, file_extension="m4a").first()
    if audio_stream:
        extension = ".m4a"
        print(f"Downloading M4A audio from {youtube_url} to {download_path} with filename {filename}{extension}")
    else:
        # Fallback to MP3 or best available audio
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp3").first()
        if audio_stream:
            extension = ".mp3"
            print(f"Downloading MP3 audio from {youtube_url} to {download_path} with filename {filename}{extension}")
        else:
            # If no MP3, get the best audio only stream
            audio_stream = yt.streams.get_audio_only()
            extension = ".mp3"  # Default to mp3 extension, even if it's m4a
            print(f"Downloading best audio from {youtube_url} to {download_path} with filename {filename}{extension}")
    
    if audio_stream:
        audio_stream.download(output_path=download_path, filename=filename + extension)
        print("Audio download completed.")
        return extension
    else:
        print("No audio stream found for this video.")
        exit(1)
	

def merge_video_and_audio(video_path, audio_path, output_path):
	video_clip = VideoFileClip(video_path)
	audio_clip = AudioFileClip(audio_path)
	video_clip = video_clip.with_audio(audio_clip)
	video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="YouTube Downloader", description="Download YouTube video and audio.")
	parser.add_argument("--url", type=str.strip, required=True, help="YouTube URL (e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
	parser.add_argument("--download_path", type=str.strip, required=True, help="Download directory path (e.g. C:\\Users\\Username\\Downloads\\)")
	parser.add_argument("--video_filename", type=str.strip, help="Video filename (without extension, default 'video')", default="video")
	parser.add_argument("--audio_filename", type=str.strip, help="Audio filename (without extension, default 'audio')", default="audio")
	args = parser.parse_args()
	youtube_url = args.url
	download_directory_path = args.download_path
	video_file_name = args.video_filename
	audio_file_name = args.audio_filename
	if not youtube_url:
		print("YouTube URL is required.")
		exit(1)
	if not download_directory_path:
		print("Download directory path is required.")
		exit(1)
	download_youtube_video(youtube_url, download_directory_path, video_file_name)
	audio_extension = download_youtube_audio(youtube_url, download_directory_path, audio_file_name)
	merge_video_and_audio(download_directory_path + video_file_name + ".mp4", download_directory_path + audio_file_name + audio_extension, download_directory_path + video_file_name + "_merged.mp4")
	