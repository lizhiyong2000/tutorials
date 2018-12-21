package com.example.oauth.client2;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.provider.token.ConsumerTokenServices;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;


@RestController
public class DemoController {


//    @Autowired
//    private ConsumerTokenServices tokenServices;

    @Autowired
    HttpServletRequest request;


    @GetMapping(path = "/")
    public String index() {

        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String name = auth.getName();
        return "client2 index:" + name;
    }

    @GetMapping(path = "/test/hello")
    public String hello() {
        return "client2 hello";
    }

    @GetMapping(value = "/logout_success")
    public String logout() {

//        String authorization = request.getHeader("AUTH-TOKEN");
//        if (authorization != null && authorization.contains("Bearer")) {
//            String tokenId = authorization.substring("Bearer".length() + 1);
//            System.out.println("tokenId : " + tokenId);
//            tokenServices.revokeToken(tokenId);
//        }


        return "logged out";
    }

}
