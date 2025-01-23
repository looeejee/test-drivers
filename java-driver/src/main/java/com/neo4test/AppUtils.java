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
                System.setProperty("NEO4J_URI", properties.getProperty("NEO4J_URI"));
                System.setProperty("NEO4J_USERNAME", properties.getProperty("NEO4J_USERNAME"));
                System.setProperty("NEO4J_PASSWORD", properties.getProperty("NEO4J_PASSWORD"));
            } else {
                throw new RuntimeException("application.properties file not found");
            }
        } catch (IOException e) {
            throw new RuntimeException("Error loading application.properties", e);
        }
    }

    static String getNeo4jUri() {
        return System.getProperty("NEO4J_URI");
    }

    static String getNeo4jUsername() {
        return System.getProperty("NEO4J_USERNAME");
    }

    static String getNeo4jPassword() {
        return System.getProperty("NEO4J_PASSWORD");
    }
}