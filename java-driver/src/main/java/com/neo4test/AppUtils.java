package com.neo4test;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class AppUtils {
    public static void loadProperties() {
        Properties properties = new Properties();
        try (InputStream input = AppUtils.class.getResourceAsStream("/application.properties")) {
            if (input != null) {
                properties.load(input);
                
                // Load values from properties or environment variables
                String neo4jUri = System.getenv("NEO4J_URL") != null ? System.getenv("NEO4J_URL") : properties.getProperty("NEO4J_URL");
                String neo4jUsername = System.getenv("NEO4J_USERNAME") != null ? System.getenv("NEO4J_USERNAME") : properties.getProperty("NEO4J_USERNAME");
                String neo4jPassword = System.getenv("NEO4J_PASSWORD") != null ? System.getenv("NEO4J_PASSWORD") : properties.getProperty("NEO4J_PASSWORD");

                // Set system properties
                System.setProperty("NEO4J_URL", neo4jUri);
                System.setProperty("NEO4J_USERNAME", neo4jUsername);
                System.setProperty("NEO4J_PASSWORD", neo4jPassword);
            } else {
                throw new RuntimeException("application.properties file not found");
            }
        } catch (IOException e) {
            throw new RuntimeException("Error loading application.properties", e);
        }
    }

    static String getNeo4jUri() {
        return System.getProperty("NEO4J_URL");
    }

    static String getNeo4jUsername() {
        return System.getProperty("NEO4J_USERNAME");
    }

    static String getNeo4jPassword() {
        return System.getProperty("NEO4J_PASSWORD");
   
    }
}