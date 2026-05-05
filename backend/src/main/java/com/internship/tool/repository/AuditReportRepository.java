package com.internship.tool.repository;

import com.internship.tool.entity.AuditReport;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface AuditReportRepository extends JpaRepository<AuditReport, Long> {

    List<AuditReport> findByDeletedFalse();

    Page<AuditReport> findByDeletedFalse(Pageable pageable);

    Optional<AuditReport> findByIdAndDeletedFalse(Long id);

    List<AuditReport> findByStatusAndDeletedFalse(String status);

    List<AuditReport> findByCategoryAndDeletedFalse(String category);

    long countByDeletedFalse();

    long countByStatusAndDeletedFalse(String status);

    long countByRiskScoreGreaterThanEqualAndDeletedFalse(int riskScore);

    @Query("SELECT r FROM AuditReport r WHERE r.deleted = false AND " +
            "(LOWER(r.title) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
            "LOWER(r.category) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
            "LOWER(r.status) LIKE LOWER(CONCAT('%', :query, '%')))")
    List<AuditReport> searchReports(@Param("query") String query);
}