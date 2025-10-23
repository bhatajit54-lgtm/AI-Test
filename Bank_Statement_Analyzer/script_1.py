
# Create Page 2: File Upload (upload.html)
upload_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Statement - Bank Statement Analyzer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            background: white;
            padding: 20px 40px;
            border-radius: 15px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 { color: #667eea; font-size: 24px; }
        .welcome { color: #666; font-size: 14px; }
        .logout-btn {
            background: #ef4444;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
        }
        .logout-btn:hover { background: #dc2626; }
        .container {
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            max-width: 700px;
            margin: 0 auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 40px;
            font-size: 16px;
        }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 60px 20px;
            margin-bottom: 30px;
            cursor: pointer;
            transition: all 0.3s;
            background: #f8f9ff;
        }
        .upload-area:hover {
            background: #f0f2ff;
            border-color: #764ba2;
        }
        .upload-area.dragover {
            background: #e8ebff;
            border-color: #764ba2;
        }
        .upload-icon {
            font-size: 60px;
            color: #667eea;
            margin-bottom: 20px;
        }
        .file-info {
            margin: 20px 0;
            padding: 15px;
            background: #d4edda;
            border-radius: 8px;
            color: #155724;
            display: none;
        }
        input[type="file"] { display: none; }
        .btn-process {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 16px 50px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            margin-top: 20px;
            display: none;
        }
        .btn-process:hover { transform: translateY(-2px); }
        .btn-process:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .loading {
            display: none;
            margin-top: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Bank Statement Analyzer</h1>
            <p class="welcome">Welcome, <span id="username"></span>!</p>
        </div>
        <button class="logout-btn" onclick="logout()">Logout</button>
    </div>

    <div class="container">
        <h2>Upload Your Bank Statement</h2>
        <p class="subtitle">Select a PDF file of your Axis Bank statement to analyze</p>
        
        <div class="upload-area" onclick="document.getElementById('file-input').click()" 
             ondrop="handleDrop(event)" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)">
            <div class="upload-icon">📄</div>
            <p style="font-size: 18px; color: #333; margin-bottom: 10px;">
                <strong>Drop your PDF file here</strong>
            </p>
            <p style="color: #666; font-size: 14px;">or click to browse</p>
        </div>

        <input type="file" id="file-input" accept=".pdf" onchange="handleFileSelect(event)">
        
        <div id="file-info" class="file-info"></div>
        
        <button id="btn-process" class="btn-process" onclick="processStatement()">
            Process Statement
        </button>

        <div id="loading" class="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px; color: #666;">Preparing to process...</p>
        </div>
    </div>

    <script>
        // Check if user is logged in
        const session = JSON.parse(localStorage.getItem('bank_session') || '{}');
        if (!session.username) {
            window.location.href = 'index.html';
        }

        // Display username
        const urlParams = new URLSearchParams(window.location.search);
        const username = urlParams.get('user') || session.username;
        document.getElementById('username').textContent = username;

        let selectedFile = null;

        function logout() {
            localStorage.removeItem('bank_session');
            localStorage.removeItem('bank_pdffile');
            localStorage.removeItem('bank_transactions');
            localStorage.removeItem('bank_accountinfo');
            localStorage.removeItem('bank_summary');
            window.location.href = 'index.html';
        }

        function handleDragOver(e) {
            e.preventDefault();
            e.stopPropagation();
            document.querySelector('.upload-area').classList.add('dragover');
        }

        function handleDragLeave(e) {
            e.preventDefault();
            e.stopPropagation();
            document.querySelector('.upload-area').classList.remove('dragover');
        }

        function handleDrop(e) {
            e.preventDefault();
            e.stopPropagation();
            document.querySelector('.upload-area').classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        }

        function handleFileSelect(e) {
            const file = e.target.files[0];
            if (file) {
                handleFile(file);
            }
        }

        function handleFile(file) {
            if (file.type !== 'application/pdf') {
                alert('Please select a PDF file');
                return;
            }

            selectedFile = file;
            
            const fileInfo = document.getElementById('file-info');
            fileInfo.innerHTML = `<strong>Selected:</strong> ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
            fileInfo.style.display = 'block';
            
            document.getElementById('btn-process').style.display = 'inline-block';
        }

        function processStatement() {
            if (!selectedFile) {
                alert('Please select a file first');
                return;
            }

            document.getElementById('btn-process').style.display = 'none';
            document.getElementById('loading').style.display = 'block';

            // Convert file to base64 and store in localStorage
            const reader = new FileReader();
            reader.onload = function(e) {
                const base64 = e.target.result;
                localStorage.setItem('bank_pdffile', base64);
                localStorage.setItem('bank_filename', selectedFile.name);
                
                // Redirect to processing page after short delay
                setTimeout(() => {
                    window.location.href = 'processing.html';
                }, 1500);
            };
            reader.readAsDataURL(selectedFile);
        }
    </script>
</body>
</html>"""

with open('upload.html', 'w', encoding='utf-8') as f:
    f.write(upload_html)

print("Created: upload.html (File Upload page)")
print("File size:", len(upload_html), "bytes")
