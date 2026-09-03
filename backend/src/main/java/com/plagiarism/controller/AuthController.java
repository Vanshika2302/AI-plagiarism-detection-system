package com.plagiarism.controller;

import com.plagiarism.config.JwtUtil;
import com.plagiarism.dto.AuthDtos.AuthRequest;
import com.plagiarism.dto.AuthDtos.AuthResponse;
import com.plagiarism.model.User;
import com.plagiarism.repository.UserRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "${frontend.origin}")
public class AuthController {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;

    public AuthController(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtUtil jwtUtil) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody AuthRequest request) {
        if (userRepository.findByUsername(request.username).isPresent()) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body("Username already taken");
        }
        User user = new User(request.username, passwordEncoder.encode(request.password));
        userRepository.save(user);
        String token = jwtUtil.generateToken(user.getUsername());
        return ResponseEntity.ok(new AuthResponse(token, user.getUsername()));
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody AuthRequest request) {
        var user = userRepository.findByUsername(request.username)
            .filter(u -> passwordEncoder.matches(request.password, u.getPasswordHash()));

        if (user.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body("Invalid username or password");
        }

        User authenticatedUser = user.get();
        return ResponseEntity.ok(
            new AuthResponse(
                jwtUtil.generateToken(authenticatedUser.getUsername()),
                authenticatedUser.getUsername()
            )
        );
    }
}
