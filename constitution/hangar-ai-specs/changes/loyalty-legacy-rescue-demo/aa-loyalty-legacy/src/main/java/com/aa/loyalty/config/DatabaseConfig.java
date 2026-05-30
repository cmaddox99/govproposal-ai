package com.aa.loyalty.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import javax.sql.DataSource;

/**
 * ENG-6.7 REMEDIATED (Phase 4): Database credentials now read from environment
 * variables / Spring externalized config. No credentials in source code.
 * Set LOYALTY_DB_URL, LOYALTY_DB_USER, LOYALTY_DB_PASS in the deployment environment.
 */
@Configuration
public class DatabaseConfig {

    @Value("${spring.datasource.url}")
    private String dbUrl;

    @Value("${spring.datasource.username}")
    private String dbUser;

    @Value("${spring.datasource.password}")
    private String dbPass;

    @Bean
    public DataSource dataSource() {
        DriverManagerDataSource ds = new DriverManagerDataSource();
        ds.setDriverClassName("oracle.jdbc.OracleDriver");
        ds.setUrl(dbUrl);
        ds.setUsername(dbUser);
        ds.setPassword(dbPass);
        return ds;
    }
}
