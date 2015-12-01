# rjamVidEncode
Script to encode the Preston Raspberry Jam video.

Takes a text file that describes the cuts to make and a large video file. It then cuts up the large video file
and places introduction overlays at the beginning of the edited files. Produces a number of mp4 video files that can be uploaded to youtube.

It isn't efficient in the way it produces the videos (it could be made faster), it does require minimal input from me in order to make it work.

Hard coded to use /media/scratch/ as a scratch directory for the creation of the videos.

Usage
=====

Create a text file which describes the cuts you need, e.g.

Name 1,100,200
Name 2,300,400
Name 3,400,500

This means that there were 3 speakers called Name 1, Name 2 and Name 3. Name 1 talked from 100 seconds to 200 seconds in the source video. This is the part that will be extracted to a seperate mp4 and Name 1 will be put in an overlay.
