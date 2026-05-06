package com.internship.tool.service;

import com.internship.tool.entity.FileAttachment;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.exception.ValidationException;
import com.internship.tool.repository.FileAttachmentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.nio.file.*;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class FileAttachmentService {

    private final FileAttachmentRepository fileAttachmentRepository;
    private static final long MAX_SIZE = 10 * 1024 * 1024;
    private static final List<String> ALLOWED_TYPES = List.of(
            "application/pdf", "image/jpeg", "image/png",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document");
    private static final String UPLOAD_DIR = "uploads/";

    public FileAttachment uploadFile(MultipartFile file, Long reportId) throws IOException {
        if (file.getSize() > MAX_SIZE) {
            throw new ValidationException("File size exceeds 10MB limit");
        }
        if (!ALLOWED_TYPES.contains(file.getContentType())) {
            throw new ValidationException("File type not allowed. Allowed: PDF, JPEG, PNG, DOC, DOCX");
        }
        Files.createDirectories(Paths.get(UPLOAD_DIR));
        String uuid = UUID.randomUUID().toString();
        String extension = getExtension(file.getOriginalFilename());
        String storedName = uuid + "." + extension;
        Path path = Paths.get(UPLOAD_DIR + storedName);
        Files.copy(file.getInputStream(), path, StandardCopyOption.REPLACE_EXISTING);
        FileAttachment attachment = new FileAttachment();
        attachment.setOriginalFilename(file.getOriginalFilename());
        attachment.setStoredFilename(storedName);
        attachment.setFileType(file.getContentType());
        attachment.setFileSize(file.getSize());
        attachment.setFilePath(path.toString());
        return fileAttachmentRepository.save(attachment);
    }

    public FileAttachment getFileById(Long id) {
        return fileAttachmentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("File not found with id: " + id));
    }

    public List<FileAttachment> getFilesByReportId(Long reportId) {
        return fileAttachmentRepository.findByReportId(reportId);
    }

    private String getExtension(String filename) {
        if (filename == null || !filename.contains("."))
            return "bin";
        return filename.substring(filename.lastIndexOf(".") + 1);
    }
}