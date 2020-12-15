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


class VideoImageWidget : public QWidget
{
    Q_OBJECT

public:
    explicit VideoImageWidget(QWidget *parent = 0);
    ~VideoImageWidget();
    void paintEvent(QPaintEvent *);

private:

};


#endif /* VideoImageWidget_hpp */
