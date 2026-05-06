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
public class AuditReportRepositoryTest {

    @Mock
    private AuditReportRepository auditReportRepository;

    @InjectMocks
    private AuditReportService auditReportService;

    private AuditReport sampleReport;

    @BeforeEach
    void setUp() {
        sampleReport = new AuditReport();
        sampleReport.setId(1L);
        sampleReport.setTitle("Repo Test Report");
        sampleReport.setStatus("OPEN");
        sampleReport.setCategory("Finance");
        sampleReport.setRiskScore(5);
        sampleReport.setDeleted(false);
    }

    @Test
    void testFindByDeletedFalse_ReturnsList() {
        when(auditReportRepository.findByDeletedFalse()).thenReturn(List.of(sampleReport));
        List<AuditReport> result = auditReportService.getAllReports();
        assertFalse(result.isEmpty());
    }

    @Test
    void testFindByIdAndDeletedFalse_Found() {
        when(auditReportRepository.findByIdAndDeletedFalse(1L)).thenReturn(Optional.of(sampleReport));
        AuditReport result = auditReportService.getReportById(1L);
        assertNotNull(result);
    }

    @Test
    void testFindByIdAndDeletedFalse_NotFound() {
        when(auditReportRepository.findByIdAndDeletedFalse(999L)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> auditReportService.getReportById(999L));
    }

    @Test
    void testCountByDeletedFalse() {
        when(auditReportRepository.countByDeletedFalse()).thenReturn(5L);
        long count = auditReportRepository.countByDeletedFalse();
        assertEquals(5L, count);
    }

    @Test
    void testCountByStatusAndDeletedFalse() {
        when(auditReportRepository.countByStatusAndDeletedFalse("OPEN")).thenReturn(3L);
        long count = auditReportRepository.countByStatusAndDeletedFalse("OPEN");
        assertEquals(3L, count);
    }

    @Test
    void testSearchReports_ReturnsList() {
        when(auditReportRepository.searchReports("Repo")).thenReturn(List.of(sampleReport));
        List<AuditReport> result = auditReportService.searchReports("Repo");
        assertFalse(result.isEmpty());
    }
}