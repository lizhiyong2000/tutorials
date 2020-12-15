//
//  VideoImageWidget.cpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/15.
//

#include "VideoImageWidget.hpp"


#include <QPainter>
VideoImageWidget::VideoImageWidget(QWidget *parent) :
    QWidget(parent)
{

}

VideoImageWidget::~VideoImageWidget()
{
   
}


void VideoImageWidget::paintEvent(QPaintEvent *)
{
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
