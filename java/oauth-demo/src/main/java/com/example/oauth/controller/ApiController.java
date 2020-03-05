package com.example.oauth.controller;


import org.springframework.web.bind.annotation.*;


@RestController
public class ApiController {


    @GetMapping(path = "/api/test")
    public String api1() {
        return "api test";
    }

}
