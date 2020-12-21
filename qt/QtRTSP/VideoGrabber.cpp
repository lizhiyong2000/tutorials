//
//  VideoGrabber.cpp
//  QtRTSP
//
//  Created by lizhiyong on 2020/12/15.
//

#include "VideoGrabber.hpp"

#include <string>
#include <cstdio>
#include <cstdarg>

#include <cpprest/http_client.h>
#include <cpprest/filestream.h>
#include <cpprest/json.h>

//#include <boost/stacktrace.hpp>

using namespace utility;                    // Common utilities like string conversions
using namespace web;                        // Common features like URIs.
using namespace web::http;                  // Common HTTP functionality
using namespace web::http::client;          // HTTP client features
using namespace concurrency::streams;
using namespace std;// Asynchronous streams


VideoGrabber::VideoGrabber()
{
    pCodecCtx = NULL;
    videoStream=-1;
    pthread_mutex_init(&mutex, 0);

}

VideoGrabber::~VideoGrabber()
{
    sws_freeContext(pSwsCtx);
    pthread_mutex_destroy(&mutex);
}

int VideoGrabber::initWithDeviceId(const std::string &device_id){
    deviceId = device_id;
    
    pplx::task<std::string> url_task = this->getVideoUrl();
    
    try{
        std::string url = url_task.get();
        
        std::cout<<"url for device:"<<deviceId <<":"<<url<<std::endl;
        
        if(url.length() > 0){
            return this->initWithUrl(url);
        }
    }
    catch (const std::exception &e)
    {
        printf("Error exception:%s\n", e.what());
    }
    
    
    
    return -1;
    
    
    
}

int VideoGrabber::initWithUrl(const std::string & url){
    rtspURL=url;
    return init();
}

int VideoGrabber::init(){
    
    const char* url = rtspURL.c_str();
    
    mediaState = new MediaState((char *)url);
    if (mediaState->openInput()){
        cout<<"open stream success"<<endl;
        mediaState->start_play();
    }
//    int err;
//
//    AVCodec *pCodec;
//    av_register_all();
//    avformat_network_init();
//    pFormatCtx = avformat_alloc_context();
//    pFrame=av_frame_alloc();
//
//    AVDictionary *opts = 0;
//    av_dict_set(&opts, "rtsp_transport", "tcp", 0);
//
//    err = avformat_open_input(&pFormatCtx, rtspURL.c_str(), NULL,
//                              &opts);
//    if (err < 0)
//    {
//        printf("Can not open this file");
//        return -1;
//    }
//    if (avformat_find_stream_info(pFormatCtx,NULL) < 0)
//    {
//        printf("Unable to get stream info");
//        return -1;
//    }
//    int i = 0;
//    videoStream = -1;
//    for (i = 0; i < pFormatCtx->nb_streams; i++)
//    {
//        if (pFormatCtx->streams[i]->codec->codec_type == AVMEDIA_TYPE_VIDEO)
//        {
//            videoStream = i;
//            break;
//        }
//    }
//    if (videoStream == -1)
//    {
//        printf("Unable to find video stream");
//        return -1;
//    }
//    pCodecCtx = pFormatCtx->streams[videoStream]->codec;
//
//    width=pCodecCtx->width;
//    height=pCodecCtx->height;
//    avpicture_alloc(&picture,AV_PIX_FMT_RGB24,pCodecCtx->width,pCodecCtx->height);
//    pCodec = avcodec_find_decoder(pCodecCtx->codec_id);
//    pSwsCtx = sws_getContext(width, height, AV_PIX_FMT_YUV420P, width,
//            height, AV_PIX_FMT_RGB24,
//            SWS_BICUBIC, 0, 0, 0);
//
//    if (pCodec == NULL)
//    {
//        printf("Unsupported codec");
//        return -1;
//    }
//    printf("video size : width=%d height=%d \n", pCodecCtx->width,
//           pCodecCtx->height);
//    if (avcodec_open2(pCodecCtx, pCodec, NULL) < 0)
//    {
//        printf("Unable to open codec");
//        return -1;
//    }
//    printf("initial successfully");
//    return 0;
}


void VideoGrabber::stop(){
    
}
void VideoGrabber::start(){
//    int frameFinished=0;
//    while (av_read_frame(pFormatCtx, &packet) >= 0)
//    {
//        if(packet.stream_index==videoStream)
//        {
//            
//            int res = avcodec_send_packet(pCodecCtx, &packet);
//            if (res < 0){
//                printf("__________avcodec_send_packet exception_____________e\n");
//                continue;
//            }
//
//            res = avcodec_receive_frame(pCodecCtx, pFrame);
//            if (res < 0){
//                printf("__________avcodec_receive_frame exception_____________e\n");
//                continue;
//            }
//            
//            
//            printf("***************ffmpeg decodec*******************\n");
//            pthread_mutex_lock(&mutex);
//            int rs = sws_scale(pSwsCtx, (const uint8_t* const *) pFrame->data,
//                               pFrame->linesize, 0,
//                               height, picture.data, picture.linesize);
//            pthread_mutex_unlock(&mutex);
//            if (rs == -1)
//            {
//                printf("__________Can open to change to des imag_____________e\n");
////                    return -1;
//            }
//            
////            avcodec_decode_video2(pCodecCtx, pFrame, &frameFinished, &packet);
////            if (frameFinished)
////            {
////                printf("***************ffmpeg decodec*******************\n");
////                pthread_mutex_lock(&mutex);
////                int rs = sws_scale(pSwsCtx, (const uint8_t* const *) pFrame->data,
////                                   pFrame->linesize, 0,
////                                   height, picture.data, picture.linesize);
////                pthread_mutex_unlock(&mutex);
////                if (rs == -1)
////                {
////                    printf("__________Can open to change to des imag_____________e\n");
//////                    return -1;
////                }
////            }
//        }
//    }
//    return 1;
}



pplx::task<std::string> VideoGrabber::getVideoUrl()
{
    // TODO: To successfully use this example, you must perform the request
    // against a server that provides JSON data.
    // This example fails because the returned Content-Type is text/html and not application/json.
    http_client client("http://61.185.80.26:8660/stream/stable/61010010001320096418");
    http_request req(methods::POST);
    req.headers().set_content_type("application/json");
    
    
    json::value json_v ;
    json_v["supplier"] = json::value::string("ffcs3");
    json_v["userKey"] = json::value::string("qAWsNoN98SnbUnhmKAa2");
    
    req.set_body(json_v);
    
    return client.request(req).then([](http_response response) -> pplx::task<json::value>
    {
//        cout << response.status_code();
        if(response.status_code() == status_codes::OK)
        {
            cout << "200 OK" <<endl;
            return response.extract_json();
        }

        // Handle error cases, for now return empty json value...
        return pplx::task_from_result(json::value());
    })
        .then([](pplx::task<json::value> previousTask)
    {
        try
        {
            cout << "1111" <<endl;
            const json::value& v = previousTask.get();
            cout << "2222" <<endl;
            cout << v.to_string()<< endl;
            cout << "3333" <<endl;
            // Perform actions here to process the JSON value...
            json::value code = v.at("code");
            
            if(code.as_integer() == 0){
                json::value data = v.at("data");
                
                cout << data.as_string()<< endl;
                
                return data.as_string();
                
            }
            
            

        }
        catch (const std::exception& e)
        {
//            std::cout<<boost::stacktrace::stacktrace();
            // Print error.
            ostringstream ss;
            ss << "Exception Type: " << typeid(e).name() << e.what() <<endl;
            cout << "Exception:" << ss.str();
            
            
            
        }
//        catch (const web::json::json_exception& e)
//        {
//            ostringstream ss;
//            ss << e.what() << endl;
//            cout << "Exception:" << ss.str();
//        }
        
        return std::string();
    });

    /* Output:
    Content-Type must be application/json to extract (is: text/html)
    */
}


