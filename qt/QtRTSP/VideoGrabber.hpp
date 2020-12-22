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

#include <cpprest/http_client.h>
#include <cpprest/filestream.h>
#include <cpprest/json.h>

#include "MediaState.hpp"

using namespace utility;                    // Common utilities like string conversions
using namespace web;                        // Common features like URIs.
using namespace web::http;                  // Common HTTP functionality
using namespace web::http::client;          // HTTP client features
using namespace concurrency::streams;       // Asynchronous streams


class VideoGrabber
{
public:
    VideoGrabber();
    int initWithUrl(const std::string & url);
    virtual ~VideoGrabber();
    void stop();
    void start();
    int initWithDeviceId(const std::string & deviceId);
    
    MediaState* getMediaState();
    
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
    std::string deviceId;
    
    int init();
    pplx::task<std::string> getVideoUrl();
    
    MediaState *mediaState;

};

#endif /* VideoGrabber_hpp */
