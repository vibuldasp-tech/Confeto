// Document Gap Analysis Tool - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const userDocInput = document.getElementById('userDocument');
    const refDocsInput = document.getElementById('referenceDocuments');
    const userFileName = document.getElementById('userFileName');
    const refFileNames = document.getElementById('refFileNames');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const progress = document.getElementById('progress');
    const errorMessage = document.getElementById('errorMessage');
    const results = document.getElementById('results');
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');

    // File input handlers
    userDocInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            userFileName.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
            userFileName.classList.add('show');
        }
    });

    refDocsInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const files = Array.from(e.target.files);
            const fileList = files.map(f => `${f.name} (${formatFileSize(f.size)})`).join('\n');
            refFileNames.textContent = `Selected ${files.length} files:\n${fileList}`;
            refFileNames.classList.add('show');
        }
    });

    // Form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate files
        if (!userDocInput.files.length) {
            showError('Please select a user document');
            return;
        }
        
        if (!refDocsInput.files.length) {
            showError('Please select at least one reference document');
            return;
        }
        
        // Hide previous results/errors
        hideError();
        results.style.display = 'none';
        uploadForm.style.display = 'none';
        
        // Show progress
        progress.style.display = 'block';
        
        // Prepare form data
        const formData = new FormData();
        formData.append('user_document', userDocInput.files[0]);
        
        for (let i = 0; i < refDocsInput.files.length; i++) {
            formData.append('reference_documents', refDocsInput.files[i]);
        }
        
        try {
            // Send request
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Analysis failed');
            }
            
            // Hide progress
            progress.style.display = 'none';
            
            // Display results
            displayResults(data);
            
        } catch (error) {
            progress.style.display = 'none';
            uploadForm.style.display = 'block';
            showError(error.message);
        }
    });

    // New analysis button
    newAnalysisBtn.addEventListener('click', function() {
        results.style.display = 'none';
        uploadForm.style.display = 'block';
        uploadForm.reset();
        userFileName.classList.remove('show');
        refFileNames.classList.remove('show');
        hideError();
    });

    // Display results function
    function displayResults(data) {
        const report = data.report;
        
        // Coverage score
        document.getElementById('coverageScore').textContent = 
            report.coverage_score.toFixed(1) + '%';
        
        // Count gaps by status
        const present = report.gaps.filter(g => g.status === 'present');
        const partial = report.gaps.filter(g => g.status === 'partial');
        const absent = report.gaps.filter(g => g.status === 'absent');
        
        // Update stats
        document.getElementById('presentCount').textContent = present.length;
        document.getElementById('partialCount').textContent = partial.length;
        document.getElementById('absentCount').textContent = absent.length;
        
        document.getElementById('presentBadge').textContent = present.length;
        document.getElementById('partialBadge').textContent = partial.length;
        document.getElementById('absentBadge').textContent = absent.length;
        
        // Summary text
        document.getElementById('summaryText').textContent = report.summary;
        
        // Display gap items
        displayGapItems('presentItems', present, 'present');
        displayGapItems('partialItems', partial, 'partial');
        displayGapItems('absentItems', absent, 'absent');
        
        // Download links
        document.getElementById('downloadMarkdown').href = data.download_links.markdown;
        document.getElementById('downloadHtml').href = data.download_links.html;
        document.getElementById('downloadJson').href = data.download_links.json;
        
        // Show results
        results.style.display = 'block';
        
        // Scroll to results
        results.scrollIntoView({ behavior: 'smooth' });
    }

    // Display gap items
    function displayGapItems(containerId, items, status) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        
        if (items.length === 0) {
            container.innerHTML = '<p style="padding: 20px; color: #999; text-align: center;">No items in this category</p>';
            return;
        }
        
        items.forEach(item => {
            const div = document.createElement('div');
            div.className = `gap-item ${status}`;
            
            div.innerHTML = `
                <div class="gap-requirement">${escapeHtml(item.requirement)}</div>
                <div class="gap-source"><strong>Source:</strong> ${escapeHtml(item.requirement_source)}</div>
                <div class="gap-details">${escapeHtml(item.details)}</div>
                <span class="gap-confidence">Confidence: ${(item.confidence * 100).toFixed(0)}%</span>
            `;
            
            container.appendChild(div);
        });
    }

    // Helper functions
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    function showError(message) {
        errorMessage.textContent = '⚠️ Error: ' + message;
        errorMessage.style.display = 'block';
        errorMessage.scrollIntoView({ behavior: 'smooth' });
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
