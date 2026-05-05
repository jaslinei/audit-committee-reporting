package com.internship.tool.controller;

import com.internship.tool.dto.AuditReportDTO;
import com.internship.tool.entity.AuditReport;
import com.internship.tool.service.AuditReportService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/audit-reports")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class AuditReportController {

    private final AuditReportService auditReportService;

    @GetMapping("/all")
    public ResponseEntity<List<AuditReport>> getAllReports() {
        return ResponseEntity.ok(auditReportService.getAllReports());
    }

    @GetMapping("/paged")
    public ResponseEntity<Page<AuditReport>> getAllReportsPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "createdAt") String sortBy,
            @RequestParam(defaultValue = "desc") String sortDir) {
        Sort sort = sortDir.equalsIgnoreCase("asc")
                ? Sort.by(sortBy).ascending()
                : Sort.by(sortBy).descending();
        Pageable pageable = PageRequest.of(page, size, sort);
        return ResponseEntity.ok(auditReportService.getAllReportsPaged(pageable));
    }

    @GetMapping("/{id}")
    public ResponseEntity<AuditReport> getReportById(@PathVariable Long id) {
        return ResponseEntity.ok(auditReportService.getReportById(id));
    }

    @PostMapping("/create")
    public ResponseEntity<AuditReport> createReport(@Valid @RequestBody AuditReportDTO dto) {
        AuditReport report = new AuditReport();
        report.setTitle(dto.getTitle());
        report.setDescription(dto.getDescription());
        report.setStatus(dto.getStatus());
        report.setCategory(dto.getCategory());
        report.setRiskScore(dto.getRiskScore());
        report.setAssignedTo(dto.getAssignedTo());
        report.setPriority(dto.getPriority());
        return ResponseEntity.status(HttpStatus.CREATED).body(auditReportService.createReport(report));
    }

    @PutMapping("/{id}")
    public ResponseEntity<AuditReport> updateReport(@PathVariable Long id,
            @Valid @RequestBody AuditReportDTO dto) {
        AuditReport report = new AuditReport();
        report.setTitle(dto.getTitle());
        report.setDescription(dto.getDescription());
        report.setStatus(dto.getStatus());
        report.setCategory(dto.getCategory());
        report.setRiskScore(dto.getRiskScore());
        report.setAssignedTo(dto.getAssignedTo());
        report.setPriority(dto.getPriority());
        return ResponseEntity.ok(auditReportService.updateReport(id, report));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReport(@PathVariable Long id) {
        auditReportService.deleteReport(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/search")
    public ResponseEntity<List<AuditReport>> searchReports(@RequestParam String q) {
        return ResponseEntity.ok(auditReportService.searchReports(q));
    }

    @GetMapping("/stats")
    public ResponseEntity<?> getStats() {
        return ResponseEntity.ok(auditReportService.getStats());
    }
}