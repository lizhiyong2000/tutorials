package com.example.oauth.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;


@Controller
public class AuthController
{

    @GetMapping(path = "/")
    public String index() {
        return "index";
    }


    @GetMapping(path = "/login")
    public String login() {
        return "login";
    }

}
