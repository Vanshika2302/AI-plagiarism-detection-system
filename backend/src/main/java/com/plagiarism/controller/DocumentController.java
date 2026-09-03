package com.plagiarism.controller;

import com.plagiarism.dto.AnalyzeResponseDto;
import com.plagiarism.dto.CompareResponseDto;
import com.plagiarism.model.Document;
import com.plagiarism.repository.DocumentRepository;
import com.plagiarism.service.AiServiceClient;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/documents")
@CrossOrigin(origins = "${frontend.origin}")
public class DocumentController {

    private final AiServiceClient aiServiceClient;
    private final DocumentRepository documentRepository;

    public DocumentController(AiServiceClient aiServiceClient, DocumentRepository documentRepository) {
        this.aiServiceClient = aiServiceClient;
        this.documentRepository = documentRepository;
    }

    /**
     * Direct pairwise comparison between two uploaded documents.
     * Does not persist anything — used for quick one-off A/B checks.
     */
    @PostMapping(value = "/compare", consumes = "multipart/form-data")
    public CompareResponseDto compare(
            @RequestParam("fileA") MultipartFile fileA,
            @RequestParam("fileB") MultipartFile fileB
    ) throws IOException {
        return aiServiceClient.compare(fileA, fileB);
    }

    /**
     * Full plagiarism check: persists the document, sends it to the AI
     * service to be embedded + checked against the whole corpus, then
     * stores the resulting similarity score back onto the Document row.
     */
    @PostMapping(value = "/analyze", consumes = "multipart/form-data")
    public AnalyzeResponseDto analyze(
            @RequestParam("file") MultipartFile file,
            Authentication authentication
    ) throws IOException {
        String username = authentication != null ? authentication.getName() : "anonymous";

        Document document = new Document(file.getOriginalFilename(), username);
        document = documentRepository.save(document);

        AnalyzeResponseDto result = aiServiceClient.analyze(document.getId(), file);

        document.setWordCount(result.getWordCount());
        document.setHighestSimilarityPct(result.getHighestSimilarityPct());
        documentRepository.save(document);

        result.setDocumentId(document.getId());
        return result;
    }

    /** Upload history for the current user. */
    @GetMapping("/history")
    public List<Document> history(Authentication authentication) {
        String username = authentication != null ? authentication.getName() : "anonymous";
        return documentRepository.findByOwnerUsernameOrderByUploadedAtDesc(username);
    }
}
