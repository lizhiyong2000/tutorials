//
//  VideoDecoder.hpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/15.
//

#ifndef VideoDecoder_hpp
#define VideoDecoder_hpp

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

class VideoDecoder
{
public:
    VideoDecoder();
    int initWithCodec(AVCodecContext *pCodecCtx);
    int decodeData(AVPacket *packet);
    virtual ~VideoDecoder();
//    friend class Video;
private:

    AVCodec *pCodec;
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

#endif /* VideoDecoder_hpp */
