//
//  FrameQueue.hpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/21.
//

#ifndef FrameQueue_hpp
#define FrameQueue_hpp

#include <stdio.h>
#include <queue>


extern "C"{
#include <pthread.h>
#include <libavcodec/avcodec.h>

}


struct FrameQueue
{
    static const int capacity = 30;

    std::queue<AVFrame*> queue;

    uint32_t nb_frames;

    pthread_mutex_t mutex;
    pthread_cond_t cond;

    FrameQueue();
    bool enQueue(const AVFrame* frame);
    bool deQueue(AVFrame **frame);
};

#endif /* FrameQueue_hpp */
