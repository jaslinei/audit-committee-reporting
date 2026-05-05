package com.internship.tool.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class AuditReportDTO {

    @NotBlank(message = "Title cannot be empty")
    private String title;

    private String description;

    @NotBlank(message = "Status cannot be empty")
    private String status;

    @NotBlank(message = "Category cannot be empty")
    private String category;

    @Min(value = 1, message = "Risk score must be at least 1")
    @Max(value = 10, message = "Risk score must be at most 10")
    private Integer riskScore;

    private String assignedTo;

    private String priority;
}