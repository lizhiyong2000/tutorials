package com.example.oauth.client2.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.security.oauth2.client.EnableOAuth2Sso;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.NoOpPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@Configuration
@EnableWebSecurity(debug = true)
@EnableOAuth2Sso
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    private static Logger logger = LoggerFactory.getLogger(SecurityConfig.class);
    @Override
    protected void configure(HttpSecurity http) throws Exception {

        http.rememberMe()
            .and()
                .authorizeRequests()
                    .anyRequest().authenticated()
                    .antMatchers("/login**").permitAll()
                    .antMatchers("/logout**").permitAll()
                    .antMatchers("/**").hasAnyRole("ROLE_ADMIN", "ROLE_USER")
                    .antMatchers("/auth/**", "/oauth2/**").permitAll()
            .and()
                .formLogin().permitAll()
            .and()
                .logout()
                    .logoutSuccessUrl("/logout_success")
                    .invalidateHttpSession(true)
                    .deleteCookies("JSESSIONID")
                    .permitAll()
            .and()
                .csrf()
                    .disable();
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.inMemoryAuthentication() // creating user in memory
                .withUser("user")
                .password(passwordEncoder().encode("password")).roles("USER")
                .and().withUser("admin")
                .password(passwordEncoder().encode("password")).authorities("ADMIN");
    }


    @Override
    @Bean
    public AuthenticationManager authenticationManagerBean() throws Exception {
        // provides the default AuthenticationManager as a Bean
        return super.authenticationManagerBean();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}