package com.plagiarism.service;

import com.plagiarism.dto.AnalyzeResponseDto;
import com.plagiarism.dto.CompareResponseDto;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.util.UriComponentsBuilder;

import java.io.IOException;

/**
 * Thin client that forwards uploaded files to the FastAPI AI microservice
 * and maps its JSON responses onto backend DTOs. Keeping this isolated
 * means the AI service can be swapped/scaled independently of the backend.
 */
@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;

    @Value("${ai.service.base-url}")
    private String aiServiceBaseUrl;

    public AiServiceClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public CompareResponseDto compare(MultipartFile fileA, MultipartFile fileB) throws IOException {
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file_a", toResource(fileA));
        body.add("file_b", toResource(fileB));

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        String url = aiServiceBaseUrl + "/compare";
        return restTemplate.postForObject(url, requestEntity, CompareResponseDto.class);
    }

    public AnalyzeResponseDto analyze(Long documentId, MultipartFile file) throws IOException {
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", toResource(file));

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        String url = UriComponentsBuilder.fromHttpUrl(aiServiceBaseUrl + "/analyze")
                .queryParam("document_id", documentId)
                .toUriString();

        return restTemplate.postForObject(url, requestEntity, AnalyzeResponseDto.class);
    }

    private ByteArrayResource toResource(MultipartFile file) throws IOException {
        return new ByteArrayResource(file.getBytes()) {
            @Override
            public String getFilename() {
                return file.getOriginalFilename();
            }
        };
    }
}
