package com.plagiarism.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import java.util.List;

public class CompareResponseDto {

    @JsonAlias("overall_score")
    private Double overallScore;

    @JsonAlias("semantic_score")
    private Double semanticScore;

    @JsonAlias("lexical_score")
    private Double lexicalScore;

    private List<SentenceMatchDto> matches;

    public static class SentenceMatchDto {
        @JsonAlias("source_sentence")
        public String sourceSentence;

        @JsonAlias("matched_sentence")
        public String matchedSentence;

        public Double similarity;

        @JsonAlias("match_type")
        public String matchType;
    }

    public Double getOverallScore() {
        return overallScore;
    }

    public void setOverallScore(Double overallScore) {
        this.overallScore = overallScore;
    }

    public Double getSemanticScore() {
        return semanticScore;
    }

    public void setSemanticScore(Double semanticScore) {
        this.semanticScore = semanticScore;
    }

    public Double getLexicalScore() {
        return lexicalScore;
    }

    public void setLexicalScore(Double lexicalScore) {
        this.lexicalScore = lexicalScore;
    }

    public List<SentenceMatchDto> getMatches() {
        return matches;
    }

    public void setMatches(List<SentenceMatchDto> matches) {
        this.matches = matches;
    }
}