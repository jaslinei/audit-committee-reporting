package com.internship.tool.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
@Schema(description = "Request body for creating or updating an audit report")
public class AuditReportDTO {

    @Schema(description = "Title of the audit report", example = "Q1 Financial Audit")
    @NotBlank(message = "Title cannot be empty")
    private String title;

    @Schema(description = "Detailed description", example = "This report covers Q1 financial controls")
    private String description;

    @Schema(description = "Status of the report", example = "OPEN")
    @NotBlank(message = "Status cannot be empty")
    private String status;

    @Schema(description = "Category of the report", example = "Finance")
    @NotBlank(message = "Category cannot be empty")
    private String category;

    @Schema(description = "Risk score from 1 to 10", example = "7")
    @Min(value = 1, message = "Risk score must be at least 1")
    @Max(value = 10, message = "Risk score must be at most 10")
    private Integer riskScore;

    @Schema(description = "Person assigned to this report", example = "John Smith")
    private String assignedTo;

    @Schema(description = "Priority level", example = "HIGH")
    private String priority;
}