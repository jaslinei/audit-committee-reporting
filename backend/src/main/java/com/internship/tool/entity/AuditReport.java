package com.internship.tool.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import java.time.LocalDateTime;

@Entity
@Table(name = "audit_reports")
@EntityListeners(AuditingEntityListener.class)
@Data
public class AuditReport {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(nullable = false)
    private String status;

    @Column(nullable = false)
    private String category;

    @Column
    private Integer riskScore;

    @Column
    private String assignedTo;

    @Column
    private String priority;

    @Column(columnDefinition = "TEXT")
    private String aiDescription;

    @Column(columnDefinition = "TEXT")
    private String aiRecommendation;

    @Column
    private String attachmentPath;

    @Column(nullable = false, updatable = false)
    @CreatedDate
    private LocalDateTime createdAt;

    @Column(nullable = false)
    @LastModifiedDate
    private LocalDateTime updatedAt;

    @Column
    private boolean deleted = false;
}