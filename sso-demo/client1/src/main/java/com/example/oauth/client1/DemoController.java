package com.example.oauth.client1;


import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.security.Principal;


@RestController
public class DemoController {

    @GetMapping(path = "/")
    public String index() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String name = auth.getName();

        return "client1 index:" + name;
    }

    @GetMapping(path = "/test/hello")
    public String hello() {
        return "client1 hello";
    }


    @GetMapping(value = "/logout_success")
    public String logout() {
        return "logged out";
    }


}
