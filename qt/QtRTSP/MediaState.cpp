//
//  MediaState.cpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/21.
//

#include "MediaState.hpp"

extern "C"
{
//#include <pthread.h>
//#include <libavcodec/avcodec.h>
//#include <libavformat/avformat.h>
//#include <libavfilter/avfilter.h>
#include <libswscale/swscale.h>
#include <libswresample/swresample.h>
#include <libavutil/time.h>


}

#include <iostream>

using namespace std;


AudioState::AudioState()
    :BUFFER_SIZE(192000)
{
    audio_ctx = nullptr;
    stream_index = -1;
    stream = nullptr;
    audio_clock = 0;

    audio_buff = new uint8_t[BUFFER_SIZE];
    audio_buff_size = 0;
    audio_buff_index = 0;
}

AudioState::AudioState(AVCodecContext *audioCtx, int index)
    :BUFFER_SIZE(192000)
{
    audio_ctx = audioCtx;
    stream_index = index;
    

    audio_buff = new uint8_t[BUFFER_SIZE];
    audio_buff_size = 0;
    audio_buff_index = 0;
}

AudioState::~AudioState()
{
    if (audio_buff)
        delete[] audio_buff;
}

bool AudioState::audio_play()
{
//    SDL_AudioSpec desired;
//    desired.freq = audio_ctx->sample_rate;
//    desired.channels = audio_ctx->channels;
//    desired.format = AUDIO_S16SYS;
//    desired.samples = 1024;
//    desired.silence = 0;
//    desired.userdata = this;
//    desired.callback = audio_callback;
//
//    if (SDL_OpenAudio(&desired, nullptr) < 0)
//    {
//        return false;
//    }
//
//    SDL_PauseAudio(0); // playing

    return true;
}

double AudioState::get_audio_clock()
{
    int hw_buf_size = audio_buff_size - audio_buff_index;
    int bytes_per_sec = stream->codec->sample_rate * audio_ctx->channels * 2;

    double pts = audio_clock - static_cast<double>(hw_buf_size) / bytes_per_sec;

    
    return pts;
}

///**
//* 向设备发送audio数据的回调函数
//*/
//void audio_callback(void* userdata, uint8_t *stream, int len)
//{
//    AudioState *audio_state = (AudioState*)userdata;
//
//    SDL_memset(stream, 0, len);
//
//    int audio_size = 0;
//    int len1 = 0;
//    while (len > 0)// 向设备发送长度为len的数据
//    {
//        if (audio_state->audio_buff_index >= audio_state->audio_buff_size) // 缓冲区中无数据
//        {
//            // 从packet中解码数据
//            audio_size = audio_decode_frame(audio_state, audio_state->audio_buff, sizeof(audio_state->audio_buff));
//            if (audio_size < 0) // 没有解码到数据或出错，填充0
//            {
//                audio_state->audio_buff_size = 0;
//                memset(audio_state->audio_buff, 0, audio_state->audio_buff_size);
//            }
//            else
//                audio_state->audio_buff_size = audio_size;
//
//            audio_state->audio_buff_index = 0;
//        }
//        len1 = audio_state->audio_buff_size - audio_state->audio_buff_index; // 缓冲区中剩下的数据长度
//        if (len1 > len) // 向设备发送的数据长度为len
//            len1 = len;
//
//        SDL_MixAudio(stream, audio_state->audio_buff + audio_state->audio_buff_index, len, SDL_MIX_MAXVOLUME);
//
//        len -= len1;
//        stream += len1;
//        audio_state->audio_buff_index += len1;
//    }
//}





VideoState::VideoState()
{
    video_ctx        = nullptr;
    stream_index     = -1;
    stream           = nullptr;

//    window           = nullptr;
//    bmp              = nullptr;
//    renderer         = nullptr;

//    frame            = nullptr;
//    displayFrame     = nullptr;

    videoq           = new PacketQueue();

    frame_timer      = 0.0;
    frame_last_delay = 0.0;
    frame_last_pts   = 0.0;
    video_clock      = 0.0;
    
    frame = av_frame_alloc();
    displayFrame = av_frame_alloc();
    
//    displayFrame->format = AV_PIX_FMT_YUV420P;
    
    displayFrame->format = AV_PIX_FMT_RGB24;
    displayFrame->width = 640;
    displayFrame->height = 360;

    int numBytes = avpicture_get_size((AVPixelFormat)displayFrame->format,displayFrame->width, displayFrame->height);
    uint8_t *buffer = (uint8_t*)av_malloc(numBytes * sizeof(uint8_t));

    avpicture_fill((AVPicture*)displayFrame, buffer, (AVPixelFormat)displayFrame->format, displayFrame->width, displayFrame->height);
}

VideoState::~VideoState()
{
    delete videoq;

    av_frame_free(&frame);
    av_free(displayFrame->data[0]);
    av_frame_free(&displayFrame);
}

//void VideoState::video_play(MediaState *media)
//{
//    int width = 800;
//    int height = 600;
//    // ´´½¨sdl´°¿Ú
//    window = SDL_CreateWindow("FFmpeg Decode", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
//        width, height, SDL_WINDOW_OPENGL);
//    renderer = SDL_CreateRenderer(window, -1, 0);
//    bmp = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_YV12, SDL_TEXTUREACCESS_STREAMING,
//        width, height);
//
//    rect.x = 0;
//    rect.y = 0;
//    rect.w = width;
//    rect.h = height;
//
//    frame = av_frame_alloc();
//    displayFrame = av_frame_alloc();
//
//    displayFrame->format = AV_PIX_FMT_YUV420P;
//    displayFrame->width = width;
//    displayFrame->height = height;
//
//    int numBytes = avpicture_get_size((AVPixelFormat)displayFrame->format,displayFrame->width, displayFrame->height);
//    uint8_t *buffer = (uint8_t*)av_malloc(numBytes * sizeof(uint8_t));
//
//    avpicture_fill((AVPicture*)displayFrame, buffer, (AVPixelFormat)displayFrame->format, displayFrame->width, displayFrame->height);
//
//    SDL_CreateThread(decode, "", this);
//
//    schedule_refresh(media, 40); // start display
//}

double VideoState::synchronize(AVFrame *srcFrame, double pts)
{
    double frame_delay;

    if (pts != 0)
        video_clock = pts; // Get pts,then set video clock to it
    else
        pts = video_clock; // Don't get pts,set it to video clock

    frame_delay = av_q2d(stream->codec->time_base);
    frame_delay += srcFrame->repeat_pict * (frame_delay * 0.5);

    video_clock += frame_delay;

    return pts;
}




MediaState::MediaState(char* input_file)
    :filename(input_file)
{
    pFormatCtx = nullptr;
    audio = new AudioState();

    video = new VideoState();
    //quit = false;
}

MediaState::~MediaState()
{
    if(audio)
        delete audio;

    if (video)
        delete video;
}

bool MediaState::openInput()
{
    // Open input file
    AVDictionary *opts = 0;
    av_dict_set(&opts, "rtsp_transport", "tcp", 0);
    
    if (avformat_open_input(&pFormatCtx, filename, nullptr, &opts) < 0)
        return false;

    if (avformat_find_stream_info(pFormatCtx, nullptr) < 0)
        return false;

    // Output the stream info to standard
    av_dump_format(pFormatCtx, 0, filename, 0);

    for (uint32_t i = 0; i < pFormatCtx->nb_streams; i++)
    {
        if (pFormatCtx->streams[i]->codec->codec_type == AVMEDIA_TYPE_AUDIO && audio->stream_index < 0)
            audio->stream_index = i;

        if (pFormatCtx->streams[i]->codec->codec_type == AVMEDIA_TYPE_VIDEO && video->stream_index < 0)
            video->stream_index = i;
    }

    if (audio->stream_index < 0 || video->stream_index < 0)
        return false;

    // Fill audio state
    AVCodec *pCodec = avcodec_find_decoder(pFormatCtx->streams[audio->stream_index]->codec->codec_id);
    if (!pCodec)
        return false;

    audio->stream = pFormatCtx->streams[audio->stream_index];

    audio->audio_ctx = avcodec_alloc_context3(pCodec);
    if (avcodec_copy_context(audio->audio_ctx, pFormatCtx->streams[audio->stream_index]->codec) != 0)
        return false;

    avcodec_open2(audio->audio_ctx, pCodec, nullptr);

    // Fill video state
    AVCodec *pVCodec = avcodec_find_decoder(pFormatCtx->streams[video->stream_index]->codec->codec_id);
    if (!pVCodec)
        return false;

    video->stream = pFormatCtx->streams[video->stream_index];

    video->video_ctx = avcodec_alloc_context3(pVCodec);
    if (avcodec_copy_context(video->video_ctx, pFormatCtx->streams[video->stream_index]->codec) != 0)
        return false;

    avcodec_open2(video->video_ctx, pVCodec, nullptr);

    video->frame_timer = static_cast<double>(av_gettime()) / 1000000.0;
    video->frame_last_delay = 40e-3;

    return true;
}


void MediaState::start_play(){
    
    int ret = pthread_create(&packet_thread_id, NULL, &packet_decode_thread, this);
    
    if(ret != 0){
        std::cout<<"packet_decode_thread fail"<<std::endl;
        return;
    }
    
    ret = pthread_create(&video_thread_id, NULL, &video_decode_thread, this->video);
    
    if(ret != 0){
        std::cout<<"video_decode_thread fail"<<std::endl;
        return;
    }
    
}

void* packet_decode_thread(void *data)
{
    printf("packet_thread start.....\n");
    MediaState *media = (MediaState*)data;
    AVPacket *packet = av_packet_alloc();

    while (true)
    {
        int ret = av_read_frame(media->pFormatCtx, packet);
        if (ret < 0)
        {
            if (ret == AVERROR_EOF){
                printf("packet_thread AVERROR_EOF\n");
                break;
            }
            if (media->pFormatCtx->pb->error == 0) // No error,wait for user input
            {
//                SDL_Delay(100);
                av_usleep(10000);
                continue;
            }
            else{
                break;
                printf("packet_thread break\n");
            }
               
        }
        
        if (packet->stream_index == media->video->stream_index) // video stream
        {
//            printf("packet_thread video\n");
            media->video->videoq->enQueue(packet);
            av_packet_unref(packet);
        }

//        else if (packet->stream_index == media->audio->stream_index) // audio stream
//        {
//            printf("packet_thread audio\n");
//            media->audio->audioq.enQueue(packet);
//            av_packet_unref(packet);
//        }
        else
            av_packet_unref(packet);
    }

    av_packet_free(&packet);

    return 0;
}


void* video_decode_thread(void *arg)
{
    
    std::cout<<"video_decode_thread start...."<<std::endl;
    VideoState *video = (VideoState*)arg;

    AVFrame *frame = av_frame_alloc();

    AVPacket packet;
    double pts;

    while (true)
    {
        video->videoq->deQueue(&packet, true);

        int ret = avcodec_send_packet(video->video_ctx, &packet);
        if (ret < 0 && ret != AVERROR(EAGAIN) && ret != AVERROR_EOF)
            continue;

        ret = avcodec_receive_frame(video->video_ctx, frame);
        if (ret < 0 && ret != AVERROR_EOF)
            continue;

        if ((pts = av_frame_get_best_effort_timestamp(frame)) == AV_NOPTS_VALUE)
            pts = 0;

        pts *= av_q2d(video->stream->time_base);

        pts = video->synchronize(frame, pts);

        frame->opaque = &pts;

        if (video->frameq.nb_frames >= FrameQueue::capacity){
            av_usleep(1000000);
        }
            

        video->frameq.enQueue(frame);

        av_frame_unref(frame);
    }


    av_frame_free(&frame);
    
    std::cout<<"video_decode_thread end...."<<std::endl;

    return 0;
}


void audio_decode_frame(AudioState *audio_state, uint8_t *audio_buf, int buf_size)
{
//    AVFrame *frame = av_frame_alloc();
//    int data_size = 0;
//    AVPacket pkt;
//    SwrContext *swr_ctx = nullptr;
//    static double clock = 0;
//
////    if (quit)
////        return -1;
//    if (!audio_state->audioq.deQueue(&pkt, true))
//        return -1;
//
//    if (pkt.pts != AV_NOPTS_VALUE)
//    {
//        audio_state->audio_clock = av_q2d(audio_state->stream->time_base) * pkt.pts;
//    }
//    int ret = avcodec_send_packet(audio_state->audio_ctx, &pkt);
//    if (ret < 0 && ret != AVERROR(EAGAIN) && ret != AVERROR_EOF)
//        return -1;
//
//    ret = avcodec_receive_frame(audio_state->audio_ctx, frame);
//    if (ret < 0 && ret != AVERROR_EOF)
//        return -1;
//
//    // 设置通道数或channel_layout
//    if (frame->channels > 0 && frame->channel_layout == 0)
//        frame->channel_layout = av_get_default_channel_layout(frame->channels);
//    else if (frame->channels == 0 && frame->channel_layout > 0)
//        frame->channels = av_get_channel_layout_nb_channels(frame->channel_layout);
//
//    AVSampleFormat dst_format = AV_SAMPLE_FMT_S16;//av_get_packed_sample_fmt((AVSampleFormat)frame->format);
//    uint64_t dst_layout = av_get_default_channel_layout(frame->channels);
//    // 设置转换参数
//    swr_ctx = swr_alloc_set_opts(nullptr, dst_layout, dst_format, frame->sample_rate,
//        frame->channel_layout, (AVSampleFormat)frame->format, frame->sample_rate, 0, nullptr);
//    if (!swr_ctx || swr_init(swr_ctx) < 0)
//        return -1;
//
//    // 计算转换后的sample个数 a * b / c
//    uint64_t dst_nb_samples = av_rescale_rnd(swr_get_delay(swr_ctx, frame->sample_rate) + frame->nb_samples, frame->sample_rate, frame->sample_rate, AVRounding(1));
//    // 转换，返回值为转换后的sample个数
//    int nb = swr_convert(swr_ctx, &audio_buf, static_cast<int>(dst_nb_samples), (const uint8_t**)frame->data, frame->nb_samples);
//    data_size = frame->channels * nb * av_get_bytes_per_sample(dst_format);
//
//    // 每秒钟音频播放的字节数 sample_rate * channels * sample_format(一个sample占用的字节数)
//    audio_state->audio_clock += static_cast<double>(data_size) / (2 * audio_state->stream->codec->channels * audio_state->stream->codec->sample_rate);
//
//
//    av_frame_free(&frame);
//    swr_free(&swr_ctx);
//
//    return data_size;
}
