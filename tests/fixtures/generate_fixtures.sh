#!/usr/bin/env bash
# Create sample files for all music formats
ffmpeg -f lavfi -i "sine=frequency=1000:duration=5" -t 5 -q:a 9 -acodec libmp3lame sine.mp3
ffmpeg -f lavfi -i "sine=frequency=1000:duration=5" -t 5 -q:a 9 -acodec flac sine.flac
ffmpeg -f lavfi -i "sine=frequency=1000:duration=5" -t 5 -q:a 9 -acodec libvorbis sine.oga
ffmpeg -f lavfi -i "sine=frequency=1000:duration=5" -t 5 -q:a 9 -acodec aac sine.m4a
