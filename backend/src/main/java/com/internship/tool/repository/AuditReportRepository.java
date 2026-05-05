package com.internship.tool.repository;

import com.internship.tool.entity.AuditReport;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface AuditReportRepository extends JpaRepository<AuditReport, Long> {

    List<AuditReport> findByDeletedFalse();

    Optional<AuditReport> findByIdAndDeletedFalse(Long id);

    List<AuditReport> findByStatusAndDeletedFalse(String status);

    List<AuditReport> findByCategoryAndDeletedFalse(String category);
}