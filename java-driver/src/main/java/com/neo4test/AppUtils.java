package com.neo4test;

import java.io.IOException;

public class AppUtils {
    public static void loadProperties() {
        try {
            var file = AppUtils.class.getResourceAsStream("/application.properties");
            if (file!=null) System.getProperties().load(file);
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
