package com.internship.tool;

import com.internship.tool.entity.AuditReport;
import com.internship.tool.repository.AuditReportRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataLoader implements CommandLineRunner {

    private final AuditReportRepository auditReportRepository;

    @Override
    public void run(String... args) throws Exception {
        if (auditReportRepository.count() == 0) {
            log.info("Seeding 30 demo audit reports...");
            createReports();
            log.info("Seeding complete.");
        }
    }

    private void createReports() {
        String[][] data = {
                { "Q1 Financial Controls Review", "Review of financial controls for Q1", "OPEN", "Finance", "8",
                        "John Smith", "HIGH" },
                { "IT Security Assessment", "Annual IT security audit", "IN_PROGRESS", "IT", "9", "Sarah Johnson",
                        "CRITICAL" },
                { "Vendor Compliance Check", "Compliance review of top vendors", "CLOSED", "Compliance", "5",
                        "Mike Davis", "MEDIUM" },
                { "Payroll Audit Q2", "Payroll process audit for Q2", "OPEN", "Finance", "7", "Emily Brown", "HIGH" },
                { "Data Privacy Review", "GDPR compliance assessment", "IN_PROGRESS", "IT", "8", "Chris Wilson",
                        "HIGH" },
                { "Supply Chain Risk", "Supply chain risk assessment", "OPEN", "Operations", "6", "Anna Taylor",
                        "MEDIUM" },
                { "Internal Controls Test", "Testing internal controls effectiveness", "CLOSED", "Finance", "4",
                        "James Moore", "LOW" },
                { "Cybersecurity Audit", "Full cybersecurity infrastructure audit", "IN_PROGRESS", "IT", "10",
                        "Lisa Anderson", "CRITICAL" },
                { "HR Policy Compliance", "HR policies compliance review", "OPEN", "HR", "3", "Robert Thomas", "LOW" },
                { "Revenue Recognition", "Revenue recognition process audit", "CLOSED", "Finance", "7",
                        "Jennifer Jackson", "HIGH" },
                { "Access Control Review", "User access control audit", "OPEN", "IT", "8", "William White", "HIGH" },
                { "Expense Management Audit", "Employee expense management review", "IN_PROGRESS", "Finance", "5",
                        "Patricia Harris", "MEDIUM" },
                { "Regulatory Compliance", "Annual regulatory compliance check", "OPEN", "Compliance", "9",
                        "Charles Martin", "CRITICAL" },
                { "Asset Management Review", "Fixed asset management audit", "CLOSED", "Operations", "4",
                        "Linda Garcia", "LOW" },
                { "Contract Compliance", "Vendor contract compliance review", "OPEN", "Compliance", "6",
                        "Mark Martinez", "MEDIUM" },
                { "Financial Reporting Audit", "Quarterly financial reporting review", "IN_PROGRESS", "Finance", "7",
                        "Barbara Robinson", "HIGH" },
                { "Network Security Audit", "Network infrastructure security review", "OPEN", "IT", "9", "Paul Clark",
                        "CRITICAL" },
                { "Procurement Process Review", "Procurement process efficiency audit", "CLOSED", "Operations", "5",
                        "Sandra Rodriguez", "MEDIUM" },
                { "Anti-Fraud Assessment", "Anti-fraud controls assessment", "OPEN", "Finance", "8", "Kenneth Lewis",
                        "HIGH" },
                { "Business Continuity Audit", "Business continuity planning review", "IN_PROGRESS", "Operations", "7",
                        "Donna Lee", "HIGH" },
                { "Tax Compliance Review", "Corporate tax compliance audit", "OPEN", "Finance", "6", "Steven Walker",
                        "MEDIUM" },
                { "Cloud Security Audit", "Cloud infrastructure security review", "CLOSED", "IT", "9", "Karen Hall",
                        "CRITICAL" },
                { "Operational Risk Review", "Operational risk management audit", "OPEN", "Operations", "7",
                        "Edward Allen", "HIGH" },
                { "Budget Variance Analysis", "Budget vs actual variance audit", "IN_PROGRESS", "Finance", "5",
                        "Betty Young", "MEDIUM" },
                { "Third Party Risk", "Third party vendor risk assessment", "OPEN", "Compliance", "8",
                        "George Hernandez", "HIGH" },
                { "Data Quality Audit", "Data quality and integrity review", "CLOSED", "IT", "6", "Susan King",
                        "MEDIUM" },
                { "Insurance Compliance", "Insurance policy compliance review", "OPEN", "Compliance", "4",
                        "Donald Wright", "LOW" },
                { "Cash Management Audit", "Cash handling and management review", "IN_PROGRESS", "Finance", "7",
                        "Maria Lopez", "HIGH" },
                { "Environmental Compliance", "Environmental regulation compliance", "OPEN", "Compliance", "5",
                        "Joseph Hill", "MEDIUM" },
                { "Board Governance Review", "Board governance effectiveness audit", "CLOSED", "Governance", "8",
                        "Margaret Scott", "HIGH" }
        };

        for (String[] d : data) {
            AuditReport report = new AuditReport();
            report.setTitle(d[0]);
            report.setDescription(d[1]);
            report.setStatus(d[2]);
            report.setCategory(d[3]);
            report.setRiskScore(Integer.parseInt(d[4]));
            report.setAssignedTo(d[5]);
            report.setPriority(d[6]);
            report.setDeleted(false);
            auditReportRepository.save(report);
        }
    }
}