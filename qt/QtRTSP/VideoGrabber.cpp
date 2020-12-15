//
//  VideoGrabber.cpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/15.
//

#include "VideoGrabber.hpp"


VideoGrabber::VideoGrabber()
{
    pCodecCtx = NULL;
    videoStream=-1;
    pthread_mutex_init(&mutex, 0);

}

VideoGrabber::~VideoGrabber()
{
    sws_freeContext(pSwsCtx);
    pthread_mutex_destroy(&mutex);
}

int VideoGrabber::initWithUrl(const std::string & url)
{
    int err;
    rtspURL=url;
    AVCodec *pCodec;
    av_register_all();
    avformat_network_init();
    pFormatCtx = avformat_alloc_context();
    pFrame=av_frame_alloc();
    err = avformat_open_input(&pFormatCtx, rtspURL.c_str(), NULL,
                              NULL);
    if (err < 0)
    {
        printf("Can not open this file");
        return -1;
    }
    if (avformat_find_stream_info(pFormatCtx,NULL) < 0)
    {
        printf("Unable to get stream info");
        return -1;
    }
    int i = 0;
    videoStream = -1;
    for (i = 0; i < pFormatCtx->nb_streams; i++)
    {
        if (pFormatCtx->streams[i]->codec->codec_type == AVMEDIA_TYPE_VIDEO)
        {
            videoStream = i;
            break;
        }
    }
    if (videoStream == -1)
    {
        printf("Unable to find video stream");
        return -1;
    }
    pCodecCtx = pFormatCtx->streams[videoStream]->codec;

    width=pCodecCtx->width;
    height=pCodecCtx->height;
    avpicture_alloc(&picture,AV_PIX_FMT_RGB24,pCodecCtx->width,pCodecCtx->height);
    pCodec = avcodec_find_decoder(pCodecCtx->codec_id);
    pSwsCtx = sws_getContext(width, height, AV_PIX_FMT_YUV420P, width,
            height, AV_PIX_FMT_RGB24,
            SWS_BICUBIC, 0, 0, 0);

    if (pCodec == NULL)
    {
        printf("Unsupported codec");
        return -1;
    }
    printf("video size : width=%d height=%d \n", pCodecCtx->width,
           pCodecCtx->height);
    if (avcodec_open2(pCodecCtx, pCodec, NULL) < 0)
    {
        printf("Unable to open codec");
        return -1;
    }
    printf("initial successfully");
    return 0;
}


void VideoGrabber::stop(){
    
}
void VideoGrabber::start(){
    int frameFinished=0;
    while (av_read_frame(pFormatCtx, &packet) >= 0)
    {
        if(packet.stream_index==videoStream)
        {
            avcodec_decode_video2(pCodecCtx, pFrame, &frameFinished, &packet);
            if (frameFinished)
            {
                printf("***************ffmpeg decodec*******************\n");
                pthread_mutex_lock(&mutex);
                int rs = sws_scale(pSwsCtx, (const uint8_t* const *) pFrame->data,
                                   pFrame->linesize, 0,
                                   height, picture.data, picture.linesize);
                pthread_mutex_unlock(&mutex);
                if (rs == -1)
                {
                    printf("__________Can open to change to des imag_____________e\n");
                    return -1;
                }
            }
        }
    }
    return 1;
}


