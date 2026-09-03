package com.plagiarism.dto;
import com.fasterxml.jackson.annotation.JsonAlias;
import java.util.List;

public class AnalyzeResponseDto {
    @JsonAlias("document_id")
    private Long documentId;

    @JsonAlias("word_count")
    private Integer wordCount;

    @JsonAlias("highest_similarity_pct")
    private Double highestSimilarityPct;

    @JsonAlias("top_corpus_matches")
    private List<CorpusMatchDto> topCorpusMatches;

    public static class CorpusMatchDto {
        @JsonAlias("document_id")
        public Long documentId;

        @JsonAlias("chunk_text")
        public String chunkText;

        public Double similarity;
    }

    public Long getDocumentId() { return documentId; }
    public void setDocumentId(Long documentId) { this.documentId = documentId; }

    public Integer getWordCount() { return wordCount; }
    public void setWordCount(Integer wordCount) { this.wordCount = wordCount; }

    public Double getHighestSimilarityPct() { return highestSimilarityPct; }
    public void setHighestSimilarityPct(Double highestSimilarityPct) { this.highestSimilarityPct = highestSimilarityPct; }

    public List<CorpusMatchDto> getTopCorpusMatches() { return topCorpusMatches; }
    public void setTopCorpusMatches(List<CorpusMatchDto> topCorpusMatches) { this.topCorpusMatches = topCorpusMatches; }
}
