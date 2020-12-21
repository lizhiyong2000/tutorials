#include "mainwindow.h"

#include <QApplication>

#include <cpprest/http_client.h>
#include <cpprest/filestream.h>
#include <cpprest/json.h>

using namespace std;

using namespace web;
using namespace web::http;
using namespace web::http::client;

// Retrieves a JSON value from an HTTP request.
pplx::task<std::string> RequestJSONValueAsync()
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
//            cout << "200 OK";
            return response.extract_json();
        }

        // Handle error cases, for now return empty json value...
        return pplx::task_from_result(json::value());
    })
        .then([](pplx::task<json::value> previousTask)
    {
        try
        {
            const json::value& v = previousTask.get();
            cout << v.as_string()<< endl;
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
            // Print error.
            ostringstream ss;
            ss << e.what() << endl;
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

// Demonstrates how to iterate over a JSON object.
void IterateJSONValue()
{
    // Create a JSON object.
    json::value obj;
    obj["key1"] = json::value::boolean(false);
    obj["key2"] = json::value::number(44);
    obj["key3"] = json::value::number(43.6);
    obj["key4"] = json::value::string(U("str"));

    // Loop over each element in the object.
    for(auto iter = obj.as_object().cbegin(); iter != obj.as_object().cend(); ++iter)
    {
        // Make sure to get the value as const reference otherwise you will end up copying
        // the whole JSON value recursively which can be expensive if it is a nested object.
        const std::string &str = iter->first;
        const json::value &v = iter->second;

        // Perform actions here to process each string and value in the JSON object...
        std::cout << "String: " << str << ", Value: " << v.as_string() << endl;
    }

    /* Output:
    String: key1, Value: false
    String: key2, Value: 44
    String: key3, Value: 43.6
    String: key4, Value: str
    */
}


int main(int argc, char *argv[])
{

//    cout << L"Calling RequestJSONValueAsync..." << endl;
//    RequestJSONValueAsync().wait();
//
//    cout << L"Calling IterateJSONValue..." << endl;
//    IterateJSONValue();
//    
    
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
