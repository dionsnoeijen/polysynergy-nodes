# Text Extraction

Local OCR and text extraction node that works with images and PDFs.  
Uses EasyOCR for images and PyMuPDF for PDFs - no cloud dependencies required.

## **Category:** OCR

## **Description**
The **Text Extraction** node provides reliable text extraction from images and PDF documents. It automatically chooses the best extraction method based on file type and supports multiple input sources.

Key features:
- **EasyOCR Integration**: Deep learning OCR for images with excellent accuracy
- **PDF Text Extraction**: Fast extraction from text-based PDFs using PyMuPDF
- **Multiple Input Sources**: File paths, base64 data, URLs
- **Automatic Engine Selection**: Chooses the best method for each file type
- **Lambda Ready**: All dependencies included, no external system requirements
- **Fully Local**: No cloud dependencies, works completely offline

## **Variables**

### **Input Variables**

#### **Input Source Configuration**
| Name            | Type | Input | Required | Description |
|-----------------|------|-------|----------|-------------|
| `input_source`  | str  | ✅     | ✅        | How to provide the file (`file_path`, `base64`, `url`) |
| `file_path`     | str  | ✅     | *         | Local file path (when source is `file_path`) |
| `file_data`     | str  | ✅     | *         | Base64 encoded file data (when source is `base64`) |
| `file_url`      | str  | ✅     | *         | URL to download file from (when source is `url`) |

#### **Extraction Settings**
| Name            | Type | Input | Required | Description |
|-----------------|------|-------|----------|-------------|
| `engine`        | str  | ✅     | ❌        | OCR engine (`auto`, `easyocr`, `pymupdf`) |
| `language`      | str  | ✅     | ❌        | Language code for OCR (default: `en`) |

### **Output Variables**
| Name                | Type  | Output | Description |
|---------------------|-------|--------|-------------|
| `extracted_text`    | str   | ✅      | The extracted text content |
| `confidence_score`  | float | ✅      | OCR confidence score (0-1, when available) |
| `word_count`        | int   | ✅      | Number of words extracted |
| `detected_language` | str   | ✅      | Detected language code |
| `extraction_metadata` | dict | ✅      | Processing details and statistics |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when text extraction succeeds. Contains extracted text. |
| `false_path` | Triggered when extraction fails. Contains error details. |

## **How It Works**

### **Engine Selection (Auto Mode)**
1. **PDF Files** → PyMuPDF (fast text extraction from text-based PDFs)
2. **Image Files** → EasyOCR (deep learning OCR for images)
3. **Manual Override** → Use specified engine

### **Processing Pipeline**
1. **Input Handling**: Load file from specified source
2. **Engine Selection**: Choose optimal extraction method
3. **Text Extraction**: Process file with selected engine
4. **Post-Processing**: Clean text and calculate metrics
5. **Output**: Return extracted text and metadata

---

## **Example Usage**

### **Basic Image OCR**
```
Input:
- input_source: "file_path"
- file_path: "/uploads/receipt.jpg"
- engine: "auto"
- language: "en"

Output (Success):
- extracted_text: "RECEIPT\nStore Name: Example Store\nTotal: $45.99\nDate: 2024-01-15"
- confidence_score: 0.94
- word_count: 8
- extraction_metadata: {"engine_used": "easyocr", "processing_time": 2.1}
```

### **PDF Text Extraction**
```
Input:
- input_source: "file_path"
- file_path: "/documents/report.pdf"
- engine: "auto"

Output (Success):
- extracted_text: "Annual Report 2024\nExecutive Summary\nThis year showed..."
- confidence_score: 1.0
- word_count: 1247
- extraction_metadata: {"engine_used": "pymupdf", "page_count": 15}
```

### **Base64 Image Processing**
```
Input:
- input_source: "base64"
- file_data: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
- engine: "easyocr"
- language: "en"

Output (Success):
- extracted_text: "Welcome to our service!"
- confidence_score: 0.89
```

### **URL Image Download & OCR**
```
Input:
- input_source: "url"
- file_url: "https://example.com/images/document.png"
- engine: "auto"

Output (Success):
- extracted_text: "Invoice #12345\nDue Date: March 15, 2024"
```


---

## **Supported File Types**

### **Image Formats** (via EasyOCR)
✅ **JPEG/JPG** - Most common image format  
✅ **PNG** - High quality images  
✅ **GIF** - Animated and static images  
✅ **WEBP** - Modern web format  
✅ **TIFF** - High resolution scans  

### **Document Formats**
✅ **PDF** - Text-based and scanned PDFs  
✅ **Text Files** - Direct text extraction  

### **Input Sources**
✅ **Local Files** - Direct file system access  
✅ **Base64 Data** - Embedded file data  
✅ **URLs** - Download from web  

---

## **Engine Comparison**

| Engine | Best For | Speed | Accuracy | Cost |
|--------|----------|-------|----------|------|
| **EasyOCR** | Images, Handwriting | Medium | High | Free |
| **PyMuPDF** | Text PDFs | Very Fast | Perfect* | Free |

*Perfect accuracy for text-based PDFs, not applicable to scanned PDFs

---

## **Configuration**

### **Language Support**
EasyOCR supports 80+ languages. Common codes:
- `en` - English (default)
- `es` - Spanish
- `fr` - French
- `de` - German
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean


---

## **Error Handling**

### **Common Issues**
| Error | Cause | Solution |
|-------|-------|----------|
| File not found | Invalid file path | Check file exists and path is absolute |
| Invalid base64 | Malformed data | Verify base64 encoding is correct |
| Download failed | Network/URL issues | Check URL is accessible |
| Unsupported format | Unknown file type | Use supported image/PDF formats |

### **Error Response Format**
```json
{
  "error": "Descriptive error message",
  "type": "ErrorType",
  "details": "Additional context"
}
```

---

## **Performance Tips**

### **For Best Results**
✅ **High Resolution**: Use 300+ DPI for scanned documents  
✅ **Good Lighting**: Ensure images are well-lit and clear  
✅ **Correct Orientation**: Rotate images to proper reading orientation  
✅ **Clean Images**: Remove noise, shadows, and distortions  

### **File Size Optimization**
✅ **Compress Large Files**: Reduce file size for faster processing  
✅ **Use Appropriate Format**: PNG for text, JPEG for photos  
✅ **Consider Preprocessing**: Crop to relevant areas  

---

## **Integration Examples**

### **Document Processing Workflow**
```
File Upload → Text Extraction → Text Analysis → Data Storage
             ├─ OCR Success → Process Content
             └─ OCR Failure → Manual Review Queue
```

### **Receipt Processing**
```
Receipt Image → Text Extraction → Parse Amounts → Expense Tracking
              └─ confidence_score → Quality Assessment
```

### **Multi-Format Document Handler**
```
Document Input
├─ .pdf → PyMuPDF → Fast Text Extraction
├─ .jpg → EasyOCR → Image OCR
└─ Complex → Textract → Premium Processing
```

---

## **Use Cases**
✔ **Document Digitization**: Convert scanned documents to searchable text  
✔ **Receipt Processing**: Extract data from receipts and invoices  
✔ **Form Processing**: OCR form fields and data entry  
✔ **Content Moderation**: Extract text from user-uploaded images  
✔ **Legal Document Processing**: Convert legal documents to text  
✔ **Medical Records**: Digitize handwritten or printed medical forms  
✔ **Archive Digitization**: Convert physical archives to digital text  

---

📄 **Use this node for reliable text extraction from any image or PDF file, with no AWS dependencies required for basic functionality.**