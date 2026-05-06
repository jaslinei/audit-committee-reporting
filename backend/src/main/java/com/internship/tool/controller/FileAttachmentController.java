package com.internship.tool.controller;

import com.internship.tool.entity.FileAttachment;
import com.internship.tool.service.FileAttachmentService;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

@RestController
@RequestMapping("/api/files")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class FileAttachmentController {

    private final FileAttachmentService fileAttachmentService;

    @PostMapping("/upload")
    public ResponseEntity<FileAttachment> uploadFile(
            @RequestParam("file") MultipartFile file,
            @RequestParam(value = "reportId", required = false) Long reportId) throws IOException {
        return ResponseEntity.ok(fileAttachmentService.uploadFile(file, reportId));
    }

    @GetMapping("/{id}")
    public ResponseEntity<Resource> downloadFile(@PathVariable Long id) throws MalformedURLException {
        FileAttachment attachment = fileAttachmentService.getFileById(id);
        Path path = Paths.get(attachment.getFilePath());
        Resource resource = new UrlResource(path.toUri());
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(attachment.getFileType()))
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"" + attachment.getOriginalFilename() + "\"")
                .body(resource);
    }

    @GetMapping("/report/{reportId}")
    public ResponseEntity<List<FileAttachment>> getFilesByReport(@PathVariable Long reportId) {
        return ResponseEntity.ok(fileAttachmentService.getFilesByReportId(reportId));
    }
}