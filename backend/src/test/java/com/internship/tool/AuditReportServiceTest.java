package com.internship.tool;

import com.internship.tool.entity.AuditReport;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.exception.ValidationException;
import com.internship.tool.repository.AuditReportRepository;
import com.internship.tool.service.AuditReportService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.List;
import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class AuditReportServiceTest {

    @Mock
    private AuditReportRepository auditReportRepository;

    @InjectMocks
    private AuditReportService auditReportService;

    private AuditReport sampleReport;

    @BeforeEach
    void setUp() {
        sampleReport = new AuditReport();
        sampleReport.setId(1L);
        sampleReport.setTitle("Test Report");
        sampleReport.setStatus("OPEN");
        sampleReport.setCategory("Finance");
        sampleReport.setRiskScore(5);
        sampleReport.setDeleted(false);
    }

    @Test
    void testGetAllReports_Success() {
        when(auditReportRepository.findByDeletedFalse()).thenReturn(List.of(sampleReport));
        List<AuditReport> result = auditReportService.getAllReports();
        assertEquals(1, result.size());
        verify(auditReportRepository, times(1)).findByDeletedFalse();
    }

    @Test
    void testGetAllReports_EmptyList() {
        when(auditReportRepository.findByDeletedFalse()).thenReturn(List.of());
        List<AuditReport> result = auditReportService.getAllReports();
        assertTrue(result.isEmpty());
    }

    @Test
    void testGetReportById_Success() {
        when(auditReportRepository.findByIdAndDeletedFalse(1L)).thenReturn(Optional.of(sampleReport));
        AuditReport result = auditReportService.getReportById(1L);
        assertEquals("Test Report", result.getTitle());
    }

    @Test
    void testGetReportById_NotFound() {
        when(auditReportRepository.findByIdAndDeletedFalse(99L)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> auditReportService.getReportById(99L));
    }

    @Test
    void testCreateReport_Success() {
        when(auditReportRepository.save(sampleReport)).thenReturn(sampleReport);
        AuditReport result = auditReportService.createReport(sampleReport);
        assertEquals("Test Report", result.getTitle());
        verify(auditReportRepository, times(1)).save(sampleReport);
    }

    @Test
    void testCreateReport_EmptyTitle_ThrowsValidationException() {
        sampleReport.setTitle("");
        assertThrows(ValidationException.class, () -> auditReportService.createReport(sampleReport));
    }

    @Test
    void testCreateReport_EmptyStatus_ThrowsValidationException() {
        sampleReport.setStatus("");
        assertThrows(ValidationException.class, () -> auditReportService.createReport(sampleReport));
    }

    @Test
    void testCreateReport_InvalidRiskScore_ThrowsValidationException() {
        sampleReport.setRiskScore(15);
        assertThrows(ValidationException.class, () -> auditReportService.createReport(sampleReport));
    }

    @Test
    void testDeleteReport_Success() {
        when(auditReportRepository.findByIdAndDeletedFalse(1L)).thenReturn(Optional.of(sampleReport));
        when(auditReportRepository.save(any(AuditReport.class))).thenReturn(sampleReport);
        auditReportService.deleteReport(1L);
        assertTrue(sampleReport.isDeleted());
        verify(auditReportRepository, times(1)).save(sampleReport);
    }

    @Test
    void testUpdateReport_NotFound_ThrowsResourceNotFoundException() {
        when(auditReportRepository.findByIdAndDeletedFalse(99L)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> auditReportService.updateReport(99L, sampleReport));
    }
}