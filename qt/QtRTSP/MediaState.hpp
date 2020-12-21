//
//  MediaState.hpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/21.
//

#ifndef MediaState_hpp
#define MediaState_hpp

#include <stdio.h>

extern "C"{
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavfilter/avfilter.h>
#include <libswscale/swscale.h>

}

#include "PacketQueue.hpp"
#include "FrameQueue.hpp"


/**
 * 播放audio时所需要的数据封装
 */
struct AudioState
{
    const uint32_t BUFFER_SIZE;// 缓冲区的大小

    PacketQueue audioq;

    double audio_clock; // audio clock
    AVStream *stream; // audio stream

    uint8_t *audio_buff;       // 解码后数据的缓冲空间
    uint32_t audio_buff_size;  // buffer中的字节数
    uint32_t audio_buff_index; // buffer中未发送数据的index
    
    int stream_index;          // audio流index
    AVCodecContext *audio_ctx; // 已经调用avcodec_open2打开

    AudioState();              //默认构造函数
    AudioState(AVCodecContext *audio_ctx, int audio_stream);
    
    ~AudioState();

    /**
    * audio play
    */
    bool audio_play();

    // get audio clock
    double get_audio_clock();
};



/**
 * 播放音频所需的数据封装
 */
struct VideoState
{
    PacketQueue* videoq;        // 保存的video packet的队列缓存

    int stream_index;           // index of video stream
    AVCodecContext *video_ctx;  // have already be opened by avcodec_open2
    AVStream *stream;           // video stream

    FrameQueue frameq;          // 保存解码后的原始帧数据
    AVFrame *frame;
    AVFrame *displayFrame;

    double frame_timer;         // Sync fields
    double frame_last_pts;
    double frame_last_delay;
    double video_clock;

//    SDL_Window *window;
//    SDL_Renderer *renderer;
//    SDL_Texture *bmp;
//    SDL_Rect rect;

//    void video_play(MediaState *media);

    double synchronize(AVFrame *srcFrame, double pts);
    
    VideoState();

    ~VideoState();
};


//int decode(void *arg); // 将packet解码，并将解码后的Frame放入FrameQueue队列中


struct MediaState
{
    AudioState *audio;
    VideoState *video;
    AVFormatContext *pFormatCtx;

    char* filename;
    //bool quit;

    MediaState(char *filename);

    ~MediaState();

    bool openInput();
    
    void start_play();
    
    pthread_t packet_thread_id;
    pthread_t video_thread_id;
    pthread_t audio_thread_id;
};

//int decode_thread(void *data);

void* packet_decode_thread(void* data);

void* video_decode_thread(void* data);

void audio_decode_thread(void* data);

///**
// * 向设备发送audio数据的回调函数
// */
//void audio_callback(void* userdata, Uint8 *stream, int len);
//
///**
// * 解码Avpacket中的数据填充到缓冲空间
// */
//int audio_decode_frame(AudioState *audio_state, uint8_t *audio_buf, int buf_size);
//

#endif /* MediaState_hpp */
