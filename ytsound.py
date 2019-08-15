# coding=utf-8
from pytube import YouTube
import sys
import os

class YTSound:
    def __init__(self, output_path):
        self.output_path = output_path
        self.decimals = 2 #the number of digits following the decimal point
        self.progressbar_length = 40 #number of characters

    # Prints something like "15.555% done..." 
    # credit: https://stackoverflow.com/a/34325723
    def progress_function(self, stream, chunk, file_handle, bytes_remaining):
        bytes_remaining = self.video_filesize - bytes_remaining
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (bytes_remaining / float(self.video_filesize)))
        filledLength = int(self.progressbar_length * bytes_remaining / float(self.video_filesize))
        bar = u'█' * filledLength + '-' * (self.progressbar_length - filledLength)
        print '%s |%s| %s%% %s' % ('  Downloading', bar, percent, 'completed'),
        # Print New Line on Complete
        if bytes_remaining == self.video_filesize: 
            print
        else: #return cursor to the beginning of line
            sys.stdout.write("\r")
            sys.stdout.flush()

    def download_mp4(self, link):
        yt=YouTube(link, on_progress_callback = self.progress_function)
        video=yt.streams.filter(only_audio = True).first()
        print 'Start downloading video "{title}"'.format(title = video.title)
        self.video_filesize = video.filesize
        return video.download(output_path = self.output_path)

    def convert_to_mp3(self, file):
        print "Converting to mp3: ", file
        #convert to mp3
        os.system('ffmpeg -y -i "{input}" -acodec libmp3lame -vn {output}'.format(input = file, output = 'tmp.mp3'))
        #fix mp3 file for errors
        os.system('ffmpeg -y -err_detect ignore_err -i {input} -c copy "{output}"'
            .format(input='tmp.mp3', output = file.replace('.mp4', '.mp3')))
        os.remove(file)  # Delete original file
        os.remove('tmp.mp3') # Delete temporary file

    def download_sound(self, link):
        self.convert_to_mp3(self.download_mp4(link))

#Syntax: ytsound.py [-o <output path>] link [link...]
def parse_arg():
    list_argv = sys.argv
    if len(list_argv) > 1:
        if list_argv[1] == '-o': 
            if len(list_argv) >= 4: #if output path is defined, at least 4 arguments required
                output_path = list_argv[2]
                links = list_argv[3::]
                return (output_path, links)
            else:
                raise ValueError("not enough argument")
        else: #no output path, default will be used
            return ('audio', list_argv[1::])
    else:
        raise ValueError("not enough argument")

def main():
    try:
        output_path, links = parse_arg()

        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        yts = YTSound(output_path)
        for link in links:
            try:
                yts.download_sound(link)
            except Exception as e: print(e)
    except ValueError:
        print "Usage: ytsound.py [-o <output path>] link [link...]"
                
if __name__ == '__main__':
    main()