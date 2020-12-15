//
//  VideoGrabber.hpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/15.
//

#ifndef VideoGrabber_hpp
#define VideoGrabber_hpp

#include <stdio.h>

extern "C"
{
#include <pthread.h>
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavfilter/avfilter.h>
#include <libswscale/swscale.h>

}

#include <string>

class VideoGrabber
{
public:
    VideoGrabber();
    int initWithUrl(const std::string & url);
    virtual ~VideoGrabber();
    void stop();
    void start();
//    friend class Video;
private:
    AVFormatContext *pFormatCtx;
    AVCodecContext *pCodecCtx;
    AVFrame *pFrame;
    AVPacket packet;
    AVPicture picture;
    SwsContext *pSwsCtx;
    int videoStream;
    int width;
    int height;
    pthread_mutex_t mutex;
    std::string rtspURL;

};

#endif /* VideoGrabber_hpp */
