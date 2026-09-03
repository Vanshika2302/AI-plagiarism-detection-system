package com.plagiarism.repository;

import com.plagiarism.model.Document;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface DocumentRepository extends JpaRepository<Document, Long> {
    List<Document> findByOwnerUsernameOrderByUploadedAtDesc(String ownerUsername);
}
