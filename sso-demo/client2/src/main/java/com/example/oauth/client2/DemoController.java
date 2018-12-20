package com.example.oauth.client2;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class DemoController {

    @GetMapping(path = "/")
    public String index() {
        return "index";
    }


    @GetMapping(path = "/hello")
    public String hello() {
        return "hello";
    }

}
