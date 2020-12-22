//
//  FrameQueue.cpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/21.
//

#include "FrameQueue.hpp"

FrameQueue::FrameQueue()
{
    nb_frames = 0;

    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cond, NULL);
}

bool FrameQueue::enQueue(const AVFrame* frame)
{
    AVFrame* p = av_frame_alloc();

    int ret = av_frame_ref(p, frame);
    if (ret < 0)
        return false;

    p->opaque = (void *)new double(*(double*)p->opaque); //上一个指向的是一个局部的变量，这里重新分配pts空间

    pthread_mutex_lock(&mutex);
    queue.push(p);

    nb_frames++;
//    printf("frame queue size:%d\n", nb_frames);
    
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&mutex);
    
    return true;
}

bool FrameQueue::deQueue(AVFrame **frame)
{
    bool ret = true;

    pthread_mutex_lock(&mutex);
    while (true)
    {
        if (!queue.empty())
        {
            if (av_frame_ref(*frame, queue.front()) < 0)
            {
                ret = false;
                break;
            }

            auto tmp = queue.front();
            queue.pop();

            av_frame_free(&tmp);

            nb_frames--;

            ret = true;
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
