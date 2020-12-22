#include "mainwindow.h"


#include "VideoGrabber.hpp"
#include "VideoImageWidget.hpp"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    widget= new QWidget(this);
    QHBoxLayout *layout = new QHBoxLayout();
    QString url = "url:";
    QLabel *label = new QLabel(url);
    layout->addWidget(label);

//    std::string stream_url = "rtsp://admin:dm666666@192.168.30.224:554/h264/ch1/main/av_stream";
//    std::string stream_url = "rtsp://admin:dp666666@192.168.10.250:554/1/1";
    std::string stream_url = "64050200001327948149";
    
    QString qstr = QString::fromStdString(stream_url);
    urlEdit = new QLineEdit();
    
    urlEdit->setText(qstr);
    layout->addWidget(urlEdit);
    
    QPushButton *playButton = new QPushButton("play");
    layout->addWidget(playButton);


    QVBoxLayout *layout2 = new QVBoxLayout();

    layout2->addLayout(layout);
    
    videoWidget = new VideoImageWidget();
    videoWidget->setFixedSize(640, 360);
    
    layout2->addWidget(videoWidget);
    
    layout2->setSpacing(10);
    layout2->setMargin(10);
    
    connect(playButton, SIGNAL(clicked()), this, SLOT(playOrStop()));
    

//    run_button.clicked.connect(self.record_video.start_recording);
    widget->setLayout(layout2);
    this->setCentralWidget(widget);
    
    
    
}

MainWindow::~MainWindow()
{
    delete widget;
}


void MainWindow::playOrStop(){
    printf("play clicked\n");
    
    if(videoGrabber != NULL){
        videoGrabber->stop();
        delete videoGrabber;
    }
    
    QString url = urlEdit->text();
    
    videoGrabber = new VideoGrabber();
//    int ret = videoGrabber->initWithUrl(url.toStdString());
    int ret = videoGrabber->initWithDeviceId(url.toStdString());
    
    if(ret == 0){
        videoGrabber->start();
        videoWidget->setMediaState(videoGrabber->getMediaState());
    }
}


