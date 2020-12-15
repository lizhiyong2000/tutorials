//
//  VideoDecoder.cpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/15.
//

#include "VideoDecoder.hpp"


VideoDecoder::VideoDecoder()
{
    pCodec = NULL;
    videoStream=-1;
    pthread_mutex_init(&mutex, 0);

}

VideoDecoder::~VideoDecoder()
{
    sws_freeContext(pSwsCtx);
    pthread_mutex_destroy(&mutex);
}

int VideoDecoder::initWithCodec(AVCodecContext *pCodecCtx)
{

//    pCodecCtx = pCodec;

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

//int VideoDecoder::h264Decodec()
//{
//    int frameFinished=0;
//    while (av_read_frame(pFormatCtx, &packet) >= 0)
//    {
//        if(packet.stream_index==videoStream)
//        {
//            avcodec_decode_video2(pCodecCtx, pFrame, &frameFinished, &packet);
//            if (frameFinished)
//            {
//                printf("***************ffmpeg decodec*******************\n");
//                pthread_mutex_lock(&mutex);
//                int rs = sws_scale(pSwsCtx, (const uint8_t* const *) pFrame->data,
//                                   pFrame->linesize, 0,
//                                   height, picture.data, picture.linesize);
//                pthread_mutex_unlock(&mutex);
//                if (rs == -1)
//                {
//                    printf("__________Can open to change to des imag_____________e\n");
//                    return -1;
//                }
//            }
//        }
//    }
//    return 1;
//
//}
