package com.example.oauth.client1;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;

@SpringBootApplication
public class OauthDemoClient1Application {

    BasicAuthenticationFilter filter;

    public static void main(String[] args) {
        SpringApplication.run(OauthDemoClient1Application.class, args);
    }
}
