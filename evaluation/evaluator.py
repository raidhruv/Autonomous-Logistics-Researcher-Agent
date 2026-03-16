import re
from typing import List, Dict
from utils.logger import logger


class Evaluator:
    def __init__(self):
        pass

    def evaluate(
        self,
        query: str,
        retrieved_chunks: List[Dict],
        report: str,
        citations: List[Dict]
    ) -> Dict:

        retrieval_relevance = self._retrieval_relevance(query, retrieved_chunks)
        evidence_coverage = self._evidence_coverage(retrieved_chunks, citations, report)
        citation_density = self._citation_density(report, citations)
        hallucination_risk = self._hallucination_risk(report, retrieved_chunks)

        quality_score = (
            0.35 * retrieval_relevance +
            0.25 * evidence_coverage +
            0.20 * citation_density +
            0.20 * hallucination_risk
        )
        logger.info(f"Evaluation score: {quality_score}")

        issues = self._detect_issues(
            retrieval_relevance,
            evidence_coverage,
            citation_density,
            hallucination_risk
        )

        return {
            "quality_score": round(quality_score, 3),
            "retrieval_relevance": round(retrieval_relevance, 3),
            "evidence_coverage": round(evidence_coverage, 3),
            "citation_density": round(citation_density, 3),
            "hallucination_risk": round(hallucination_risk, 3),
            "issues": issues
        }

    # Metrics
    def _retrieval_relevance(self, query, retrieved_chunks):

        if not retrieved_chunks:
            return 0.0

        query_terms = set(query.lower().split())
        scores = []

        for chunk in retrieved_chunks:

            if isinstance(chunk, dict):
                text = chunk.get("text", "").lower()
            else:
                text = str(chunk).lower()

            words = set(text.split())

            overlap = query_terms.intersection(words)
            score = len(overlap) / max(len(query_terms), 1)

            scores.append(score)

        return sum(scores) / len(scores)


    def _evidence_coverage(self, retrieved_chunks, citations, report):

        cited_numbers = set(map(int, re.findall(r"\[(\d+)\]", report)))

        if not cited_numbers:
            return 0.0

        retrieved_count = len(retrieved_chunks)

        return min(len(cited_numbers) / retrieved_count, 1.0)

    def _citation_density(self, report, citations):

        paragraphs = [p for p in report.split("\n") if p.strip()]
        if not paragraphs:
            return 0.0

        citation_matches = re.findall(r"\[\d+\]", report)

        citation_count = len(citation_matches)

        density = citation_count / len(paragraphs)

        return min(density, 1.0)

    def _hallucination_risk(self, report, retrieved_chunks):

        if not retrieved_chunks:
            return 0.0

        evidence_parts = []

        for c in retrieved_chunks:
            if isinstance(c, dict):
                evidence_parts.append(c.get("text", ""))
            else:
                evidence_parts.append(str(c))

        evidence_text = " ".join(evidence_parts).lower()

        report_words = set(report.lower().split())

        matches = sum(1 for w in report_words if w in evidence_text)

        score = matches / max(len(report_words), 1)

        return score

    # Issue detection
    def _detect_issues(
        self,
        relevance: float,
        coverage: float,
        density: float,
        hallucination: float
    ) -> List[str]:

        issues = []

        if relevance < 0.3:
            issues.append("Low retrieval relevance")

        if coverage < 0.3:
            issues.append("Low evidence coverage")

        if density < 0.2:
            issues.append("Low citation density")

        if hallucination < 0.4:
            issues.append("Possible unsupported claims")

        return issues
