#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>
#include <QString>



QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class VideoImageWidget;
class VideoGrabber;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
public slots:
    void playOrStop();

private:
    QWidget *widget;
    QLineEdit *urlEdit;
    
    VideoImageWidget *videoWidget;
    
    VideoGrabber *videoGrabber;
    
    
};
#endif // MAINWINDOW_H
