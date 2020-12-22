//
//  VideoImageWidget.hpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/15.
//

#ifndef VideoImageWidget_hpp
#define VideoImageWidget_hpp

#include <stdio.h>

#include <QWidget>
#include <QTimer>

extern "C"{
#include <pthread.h>

}

class MediaState;
class QImage;

class VideoImageWidget : public QWidget
{
    Q_OBJECT
    
    

public:
    explicit VideoImageWidget(QWidget *parent = 0);
    ~VideoImageWidget();
    void paintEvent(QPaintEvent *);
    
    
    void setMediaState(MediaState * state);
    void schedule_refresh(int delay);
public slots:
    void timerEvent();
private:
    QTimer* video_timer;
    MediaState * mediaState;
    QImage *currentImage;
    pthread_mutex_t mutex;
};


#endif /* VideoImageWidget_hpp */
