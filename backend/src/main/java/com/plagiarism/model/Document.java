package com.plagiarism.model;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "documents")
public class Document {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String filename;

    @Column(nullable = false)
    private String ownerUsername;

    @Column(name = "word_count")
    private Integer wordCount;

    @Column(name = "highest_similarity_pct")
    private Double highestSimilarityPct;

    @Column(name = "uploaded_at", nullable = false)
    private Instant uploadedAt = Instant.now();

    public Document() {}

    public Document(String filename, String ownerUsername) {
        this.filename = filename;
        this.ownerUsername = ownerUsername;
    }

    // --- getters / setters ---
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getFilename() { return filename; }
    public void setFilename(String filename) { this.filename = filename; }

    public String getOwnerUsername() { return ownerUsername; }
    public void setOwnerUsername(String ownerUsername) { this.ownerUsername = ownerUsername; }

    public Integer getWordCount() { return wordCount; }
    public void setWordCount(Integer wordCount) { this.wordCount = wordCount; }

    public Double getHighestSimilarityPct() { return highestSimilarityPct; }
    public void setHighestSimilarityPct(Double highestSimilarityPct) { this.highestSimilarityPct = highestSimilarityPct; }

    public Instant getUploadedAt() { return uploadedAt; }
    public void setUploadedAt(Instant uploadedAt) { this.uploadedAt = uploadedAt; }
}
