package com.examle.oauth;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;


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


    @GetMapping(path = "/api/test")
    public String api1() {
        return "api test";
    }


    @GetMapping(value = "/logout_success")
    public String logout() {
        return "logged out";
    }
}
