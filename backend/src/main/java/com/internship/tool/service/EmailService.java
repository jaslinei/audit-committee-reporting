package com.internship.tool.service;

import com.internship.tool.entity.AuditReport;
import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;

@Service
@RequiredArgsConstructor
@Slf4j
public class EmailService {

    private final JavaMailSender mailSender;
    private final TemplateEngine templateEngine;

    @Async
    public void sendReportCreatedEmail(AuditReport report, String toEmail) {
        try {
            Context context = new Context();
            context.setVariable("title", report.getTitle());
            context.setVariable("category", report.getCategory());
            context.setVariable("status", report.getStatus());
            context.setVariable("riskScore", report.getRiskScore());
            context.setVariable("assignedTo", report.getAssignedTo());
            String html = templateEngine.process("report-created", context);
            sendEmail(toEmail, "New Audit Report Created: " + report.getTitle(), html);
        } catch (Exception e) {
            log.error("Failed to send report created email", e);
        }
    }

    @Async
    public void sendOverdueEmail(AuditReport report, String toEmail) {
        try {
            Context context = new Context();
            context.setVariable("title", report.getTitle());
            context.setVariable("category", report.getCategory());
            context.setVariable("assignedTo", report.getAssignedTo());
            String html = templateEngine.process("report-overdue", context);
            sendEmail(toEmail, "OVERDUE: Audit Report Requires Attention - " + report.getTitle(), html);
        } catch (Exception e) {
            log.error("Failed to send overdue email", e);
        }
    }

    private void sendEmail(String to, String subject, String html) throws MessagingException {
        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true);
        helper.setTo(to);
        helper.setSubject(subject);
        helper.setText(html, true);
        mailSender.send(message);
    }
}