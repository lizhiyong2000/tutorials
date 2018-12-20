package com.example.oauth.client1;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.security.Principal;


@RestController
public class DemoController {

    @GetMapping(path = "/")
    public String index() {
        return "index";
    }


}
