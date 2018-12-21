package com.example.oauth;


import org.springframework.web.bind.annotation.*;

import java.security.Principal;


@RestController
public class DemoController {


    @GetMapping(path = "/api/test")
    public String api1() {
        return "api test";
    }

//
//    @GetMapping(value = "/logout_success")
//    public String logout() {
//        return "logged out";
//    }


    @GetMapping("/user/me")
    public Principal user(Principal principal) {
        return principal;
    }
}
