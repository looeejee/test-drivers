package com.neo4test;

import java.util.concurrent.TimeUnit; // Import Level
import java.util.logging.Level;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Config;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Logging;

public class App {

    public static void main(String... args) {

        AppUtils.loadProperties(); // Load properties

        final String dbUri = AppUtils.getNeo4jUri();
        final String dbUser = AppUtils.getNeo4jUsername();
        final String dbPassword = AppUtils.getNeo4jPassword();

        Config config = Config.builder()
                .withConnectionTimeout(30, TimeUnit.SECONDS)
                .withMaxConnectionLifetime(30, TimeUnit.MINUTES)
                .withMaxConnectionPoolSize(10)
                .withConnectionAcquisitionTimeout(20, TimeUnit.SECONDS)
                .withFetchSize(1000)
                .withDriverMetrics()
                .withLogging(Logging.console(Level.INFO))
                .build();

        try (var driver = GraphDatabase.driver(dbUri, AuthTokens.basic(dbUser, dbPassword), config)) {
            driver.verifyConnectivity();
             System.out.println("Connection established.");
        }
    }
}