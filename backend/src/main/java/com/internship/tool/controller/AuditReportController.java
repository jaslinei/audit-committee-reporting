package com.internship.tool.controller;

import com.internship.tool.dto.AuditReportDTO;
import com.internship.tool.entity.AuditReport;
import com.internship.tool.service.AuditReportService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
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
@Tag(name = "Audit Reports", description = "APIs for managing audit committee reports")
public class AuditReportController {

    private final AuditReportService auditReportService;

    @Operation(summary = "Get all reports", description = "Returns all non-deleted audit reports")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Successfully retrieved all reports"),
            @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
    @GetMapping("/all")
    public ResponseEntity<List<AuditReport>> getAllReports() {
        return ResponseEntity.ok(auditReportService.getAllReports());
    }

    @Operation(summary = "Get paginated reports", description = "Returns audit reports with pagination and sorting")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Successfully retrieved paginated reports"),
            @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
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

    @Operation(summary = "Get report by ID", description = "Returns a single audit report by its ID")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Report found"),
            @ApiResponse(responseCode = "404", description = "Report not found"),
            @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
    @GetMapping("/{id}")
    public ResponseEntity<AuditReport> getReportById(@PathVariable Long id) {
        return ResponseEntity.ok(auditReportService.getReportById(id));
    }

    @Operation(summary = "Create a new report", description = "Creates a new audit committee report")
    @ApiResponses({
            @ApiResponse(responseCode = "201", description = "Report created successfully"),
            @ApiResponse(responseCode = "400", description = "Validation failed"),
            @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
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

    @Operation(summary = "Update a report", description = "Updates an existing audit report by ID")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Report updated successfully"),
            @ApiResponse(responseCode = "400", description = "Validation failed"),
            @ApiResponse(responseCode = "404", description = "Report not found"),
            @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
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

    @Operation(summary = "Delete a report", description = "Soft deletes an audit report by ID")
    @ApiResponses({
            @ApiResponse(responseCode = "204", description = "Report deleted successfully"),
            @ApiResponse(responseCode = "404", description = "Report not found"),
            @ApiResponse(responseCode = "401", description = "Unauthorized")
    })
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReport(@PathVariable Long id) {
        auditReportService.deleteReport(id);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Search reports", description = "Search reports by title, category or status")
    @ApiResponse(responseCode = "200", description = "Search results returned")
    @GetMapping("/search")
    public ResponseEntity<List<AuditReport>> searchReports(@RequestParam String q) {
        return ResponseEntity.ok(auditReportService.searchReports(q));
    }

    @Operation(summary = "Get dashboard stats", description = "Returns KPI stats for dashboard")
    @ApiResponse(responseCode = "200", description = "Stats returned successfully")
    @GetMapping("/stats")
    public ResponseEntity<?> getStats() {
        return ResponseEntity.ok(auditReportService.getStats());
    }
}