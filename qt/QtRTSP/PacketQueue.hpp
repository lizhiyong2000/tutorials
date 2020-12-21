//
//  PacketQueue.hpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/21.
//

#ifndef PacketQueue_hpp
#define PacketQueue_hpp

#include <stdio.h>

#include <queue>


extern "C"{
#include <pthread.h>
#include <libavcodec/avcodec.h>

}

struct PacketQueue
{
    std::queue<AVPacket> queue;

    uint32_t    nb_packets;
    uint64_t    size;
    
    pthread_mutex_t mutex;
    pthread_cond_t cond;

    PacketQueue();
    bool enQueue(const AVPacket *packet);
    bool deQueue(AVPacket *packet, bool block);
};

#endif /* PacketQueue_hpp */
