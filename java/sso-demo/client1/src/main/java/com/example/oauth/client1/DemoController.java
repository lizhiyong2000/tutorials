package com.example.oauth.client1;



import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;



@Controller
public class DemoController {

    @GetMapping(path = "/")
    public String index() {
        return "index";
    }


    @GetMapping(path = "/securedPage")
    public String login() {
        return "securedPage";
    }
}
