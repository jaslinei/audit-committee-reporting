package com.internship.tool.service;

import com.internship.tool.entity.AuditReport;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.exception.ValidationException;
import com.internship.tool.repository.AuditReportRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class AuditReportService {

    private final AuditReportRepository auditReportRepository;

    @Cacheable(value = "reports")
    public List<AuditReport> getAllReports() {
        return auditReportRepository.findByDeletedFalse();
    }

    @Cacheable(value = "reports", key = "#pageable.pageNumber + '-' + #pageable.pageSize")
    public Page<AuditReport> getAllReportsPaged(Pageable pageable) {
        return auditReportRepository.findByDeletedFalse(pageable);
    }

    @Cacheable(value = "report", key = "#id")
    public AuditReport getReportById(Long id) {
        return auditReportRepository.findByIdAndDeletedFalse(id)
                .orElseThrow(() -> new ResourceNotFoundException("Audit report not found with id: " + id));
    }

    @CacheEvict(value = { "reports", "report" }, allEntries = true)
    public AuditReport createReport(AuditReport report) {
        validateReport(report);
        return auditReportRepository.save(report);
    }

    @CacheEvict(value = { "reports", "report" }, allEntries = true)
    public AuditReport updateReport(Long id, AuditReport updatedReport) {
        AuditReport existing = getReportById(id);
        validateReport(updatedReport);
        existing.setTitle(updatedReport.getTitle());
        existing.setDescription(updatedReport.getDescription());
        existing.setStatus(updatedReport.getStatus());
        existing.setCategory(updatedReport.getCategory());
        existing.setRiskScore(updatedReport.getRiskScore());
        existing.setAssignedTo(updatedReport.getAssignedTo());
        existing.setPriority(updatedReport.getPriority());
        return auditReportRepository.save(existing);
    }

    @CacheEvict(value = { "reports", "report" }, allEntries = true)
    public void deleteReport(Long id) {
        AuditReport report = getReportById(id);
        report.setDeleted(true);
        auditReportRepository.save(report);
    }

    public List<AuditReport> searchReports(String query) {
        return auditReportRepository.searchReports(query);
    }

    public Map<String, Object> getStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("total", auditReportRepository.countByDeletedFalse());
        stats.put("highRisk", auditReportRepository.countByRiskScoreGreaterThanEqualAndDeletedFalse(8));
        stats.put("open", auditReportRepository.countByStatusAndDeletedFalse("OPEN"));
        stats.put("closed", auditReportRepository.countByStatusAndDeletedFalse("CLOSED"));
        return stats;
    }

    private void validateReport(AuditReport report) {
        if (report.getTitle() == null || report.getTitle().trim().isEmpty()) {
            throw new ValidationException("Title cannot be empty");
        }
        if (report.getStatus() == null || report.getStatus().trim().isEmpty()) {
            throw new ValidationException("Status cannot be empty");
        }
        if (report.getCategory() == null || report.getCategory().trim().isEmpty()) {
            throw new ValidationException("Category cannot be empty");
        }
        if (report.getRiskScore() != null && (report.getRiskScore() < 1 || report.getRiskScore() > 10)) {
            throw new ValidationException("Risk score must be between 1 and 10");
        }
    }
}