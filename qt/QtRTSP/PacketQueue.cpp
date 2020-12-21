//
//  PacketQueue.cpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/21.
//

#include "PacketQueue.hpp"


PacketQueue::PacketQueue()
{
    nb_packets = 0;
    size       = 0;

    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cond, NULL);
}

bool PacketQueue::enQueue(const AVPacket *packet)
{
    AVPacket *pkt = av_packet_alloc();
    if (av_packet_ref(pkt, packet) < 0)
        return false;

    pthread_mutex_lock(&mutex);
    queue.push(*pkt);

    size += pkt->size;
    nb_packets++;

    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&mutex);
    return true;
}

bool PacketQueue::deQueue(AVPacket *packet, bool block)
{
    bool ret = false;

    pthread_mutex_lock(&mutex);
    while (true)
    {
//        if (quit)
//        {
//            ret = false;
//            break;
//        }

        if (!queue.empty())
        {
            if (av_packet_ref(packet, &queue.front()) < 0)
            {
                ret = false;
                break;
            }
            AVPacket pkt = queue.front();

            queue.pop();
            av_packet_unref(&pkt);
            nb_packets--;
            size -= packet->size;

            ret = true;
            break;
        }
        else if (!block)
        {
            ret = false;
            break;
        }
        else
        {
            pthread_cond_wait(&cond, &mutex);
        }
    }
    pthread_mutex_unlock(&mutex);
    return ret;
}
