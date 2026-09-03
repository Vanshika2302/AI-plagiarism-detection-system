package com.plagiarism.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class AuthDtos {

    public static class AuthRequest {
        @NotBlank
        public String username;

        @NotBlank
        @Size(min = 6, message = "Password must be at least 6 characters")
        public String password;
    }

    public static class AuthResponse {
        public String token;
        public String username;

        public AuthResponse(String token, String username) {
            this.token = token;
            this.username = username;
        }
    }
}
