//
//  VideoImageWidget.cpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/15.
//

#include "VideoImageWidget.hpp"


#include <QPainter>
#include <QTimerEvent>
#include <QImage>

#include <iostream>

#include "MediaState.hpp"

extern "C"{

#include <libswscale/swscale.h>
#include <libavutil/time.h>

}

using namespace std;

static const double SYNC_THRESHOLD = 0.01;
static const double NOSYNC_THRESHOLD = 10.0;

VideoImageWidget::VideoImageWidget(QWidget *parent) :
    QWidget(parent)
{
    mediaState = NULL;
    video_timer = new QTimer();
    connect(video_timer, SIGNAL(timeout()), this, SLOT(timerEvent()));
    
    
    
    pthread_mutex_init(&mutex, NULL);
    pthread_mutex_lock(&mutex);
    currentImage = NULL;
    pthread_mutex_unlock(&mutex);
    
    schedule_refresh(1000);
}

VideoImageWidget::~VideoImageWidget()
{
   
}
void VideoImageWidget::setMediaState(MediaState * state){
    this->mediaState = state;
}

void VideoImageWidget::paintEvent(QPaintEvent *)
{
//    cout<<"VideoImageWidget::paintEvent"<<endl;
    pthread_mutex_lock(&mutex);
    
    if(currentImage != NULL){
        QPainter pp(this);
        QRect Temp(0,0,this->width(),this->height());
    //    QImage currentImage;
        pp.drawImage(Temp, *currentImage);
        
//        cout<<"VideoImageWidget::display"<<endl;
    }

    pthread_mutex_unlock(&mutex);
    
    
//    if(ffmpeg->picture.data!=NULL)
//    {
//     QPainter painter(this);
//    if(ffmpeg->mutex.tryLock(1000))
//    {
//
//        QImage image=QImage(ffmpeg->picture.data[0],ffmpeg->width,ffmpeg->height,QImage::Format_RGB888);
//        QPixmap  pix =  QPixmap::fromImage(image);
//        painter.drawPixmap(0, 0, 640, 480, pix);
//        update();
//        ffmpeg->mutex.unlock();
//    }
//    }
}


// 延迟delay ms后刷新video帧
void VideoImageWidget::schedule_refresh(int delay)
{
//    SDL_AddTimer(delay, sdl_refresh_timer_cb, media);
    video_timer->stop();
    video_timer->start(delay);
}


void VideoImageWidget::timerEvent()
{
//    cout<<"VideoImageWidget::timerEvent"<<endl;
    
//    if(event->timerId() != video_timer->timerId()){
//        return;
//    }
    
    
    if(mediaState == NULL){
        return;
    }
    
//    cout<<"mediaState not null"<<endl;
    VideoState *video = mediaState->video;

    if (video->stream_index >= 0)
    {
        if (video->videoq->queue.empty()){
            schedule_refresh(10);
        }

        else
        {
            video->frameq.deQueue(&video->frame);

            // 将视频同步到音频上，计算下一帧的延迟时间
            double current_pts = *(double*)video->frame->opaque;
            double delay = current_pts - video->frame_last_pts;
            if (delay <= 0 || delay >= 1.0)
                delay = video->frame_last_delay;

            video->frame_last_delay = delay;
            video->frame_last_pts = current_pts;

            // 当前显示帧的PTS来计算显示下一帧的延迟
            double ref_clock = mediaState->audio->get_audio_clock();

            double diff = current_pts - ref_clock;// diff < 0 => video slow,diff > 0 => video quick

            double threshold = (delay > SYNC_THRESHOLD) ? delay : SYNC_THRESHOLD;

            if (fabs(diff) < NOSYNC_THRESHOLD) // 不同步
            {
                if (diff <= -threshold) // 慢了，delay设为0
                    delay = 0;
                else if (diff >= threshold) // 快了，加倍delay
                    delay *= 2;
            }
            video->frame_timer += delay;
            double actual_delay = video->frame_timer - static_cast<double>(av_gettime()) / 1000000.0;
            if (actual_delay <= 0.010)
                actual_delay = 0.010;

            schedule_refresh(static_cast<int>(actual_delay * 1000 + 0.5));
            
//            cout<<"video->width:"<<video->video_ctx->width<<",video->height:"<<video->video_ctx->height<<endl;
            
            AVPixelFormat pixFormat;
            switch (video->video_ctx->pix_fmt)
              {
                case AV_PIX_FMT_YUVJ420P:
                  pixFormat = AV_PIX_FMT_YUV420P;
                  break;
                case AV_PIX_FMT_YUVJ422P:
                  pixFormat = AV_PIX_FMT_YUV422P;
                  break;
                case AV_PIX_FMT_YUVJ444P:
                  pixFormat = AV_PIX_FMT_YUV444P;
                  break;
                case AV_PIX_FMT_YUVJ440P:
                  pixFormat = AV_PIX_FMT_YUV440P;
                  break;
                default:
                  pixFormat = video->video_ctx->pix_fmt;
              }
//            cout<<"display->width:"<<video->displayFrame->width<<",display->height:"<<video->displayFrame->height<<endl;

            SwsContext *sws_ctx = sws_getContext(video->video_ctx->width, video->video_ctx->height, pixFormat,
            video->displayFrame->width,video->displayFrame->height,(AVPixelFormat)video->displayFrame->format, SWS_BILINEAR, nullptr, nullptr, nullptr);
            
//            cout<<"frame->linesize:"<<video->frame->linesize<<",displayFrame->linesize:"<<video->displayFrame->linesize<<endl;

            sws_scale(sws_ctx, (uint8_t const * const *)video->frame->data, video->frame->linesize, 0,
                video->video_ctx->height, video->displayFrame->data, video->displayFrame->linesize);
            
            pthread_mutex_lock(&mutex);
            if (currentImage != NULL){
                delete currentImage;
            }

            currentImage = new QImage ((uchar*)video->displayFrame->data[0], 640, 360, QImage::Format_RGB888);
            pthread_mutex_unlock(&mutex);
            
            update();
            
            // Display the image to screen
//            SDL_UpdateTexture(video->bmp, &(video->rect), video->displayFrame->data[0], video->displayFrame->linesize[0]);
//            SDL_RenderClear(video->renderer);
//            SDL_RenderCopy(video->renderer, video->bmp, &video->rect, &video->rect);
//            SDL_RenderPresent(video->renderer);

            sws_freeContext(sws_ctx);
            av_frame_unref(video->frame);
        }
    }
    else
    {
        schedule_refresh(100);
    }
}


