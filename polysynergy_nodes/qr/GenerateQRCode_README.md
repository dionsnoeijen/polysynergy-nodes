# Generate QR Code

Generates QR codes from text or URLs and stores them as images in S3 with project-based isolation.

## Description

The Generate QR Code node creates QR codes from any text data or URL and automatically uploads them to S3 storage. The generated images are stored in project-specific buckets with a hierarchical structure for organization. This node introduces the concept of image variables in the workflow system, providing both the image URL and rich metadata.

## Inputs

- **Data**: Text or URL to encode in the QR code (required)
- **Size**: Size of the QR code image in pixels (default: 400, range: 100-2000)
- **Border**: Border size in modules (default: 4, range: 0-20)
- **Error Correction**: Error correction level
  - L: Low (~7% correction)
  - M: Medium (~15% correction) [default]
  - Q: Quartile (~25% correction)
  - H: High (~30% correction)
- **Fill Color**: QR code color in hex format (default: #000000)
- **Background Color**: Background color in hex format (default: #FFFFFF)

## Outputs

- **QR Code Image**: Complete image object with URL and metadata
  ```json
  {
    "url": "https://bucket.s3.region.amazonaws.com/path/to/image.png",
    "mime_type": "image/png",
    "width": 400,
    "height": 400,
    "size": 12345,
    "metadata": {
      "data": "encoded data",
      "error_correction": "M",
      "border": 4,
      "qr_version": 1,
      "modules": 21,
      "s3_key": "tenant/project/node/execution/qr_timestamp.png",
      "bucket": "polysynergy-tenant-project-media"
    }
  }
  ```
- **Image URL**: Direct URL to the QR code image for simple use cases

## Paths

- **Success**: QR code generated and uploaded successfully
- **Error**: Error during generation or upload

## S3 Storage Structure

The node automatically organizes images in S3 with the following structure:
```
bucket-name: polysynergy-{tenant_id}-{project_id}-media/
  └── {tenant_id}/
      └── {project_id}/
          └── {node_id}/
              └── {execution_id}/
                  └── qr_{timestamp}.png
```

This ensures:
- **Project isolation**: Each project has its own bucket
- **Organization**: Clear hierarchy for managing images
- **Uniqueness**: Timestamps prevent naming conflicts
- **Traceability**: Execution IDs link images to specific workflow runs

## Error Correction Levels

### Low (L) - ~7% correction
- Best for: Clean environments, maximum data capacity
- Use when: QR code won't be damaged or partially obscured

### Medium (M) - ~15% correction [Default]
- Best for: General use, balanced capacity and resilience
- Use when: Standard applications, moderate wear expected

### Quartile (Q) - ~25% correction
- Best for: Industrial use, moderate damage expected
- Use when: QR codes may get dirty or partially damaged

### High (H) - ~30% correction
- Best for: Harsh environments, logos overlay
- Use when: Maximum durability needed or adding logos/images

## Example Use Cases

### URL Shortening & Tracking
```
Input: "https://example.com/very/long/url/with/parameters"
Output: QR code linking to the URL
Use: Marketing materials, event tracking
```

### WiFi Credentials
```
Input: "WIFI:T:WPA;S:NetworkName;P:Password;;"
Output: QR code for automatic WiFi connection
Use: Guest networks, offices, cafes
```

### Contact Information (vCard)
```
Input: "BEGIN:VCARD\nFN:John Doe\nTEL:555-1234\nEND:VCARD"
Output: QR code with contact details
Use: Business cards, networking events
```

### Product Information
```
Input: JSON.stringify({product_id: "12345", batch: "2024-01"})
Output: QR code with product data
Use: Inventory tracking, authentication
```

### Event Tickets
```
Input: "TICKET:EVENT2024:SEAT15A:USER123"
Output: QR code for event entry
Use: Digital ticketing, access control
```

## Color Customization

### Brand Colors
- Set fill_color to match brand colors
- Keep sufficient contrast for scanning reliability
- Test with various QR code readers

### Inverted Codes
```
Fill Color: #FFFFFF (white)
Background Color: #000000 (black)
Result: Inverted QR code for dark backgrounds
```

### Creative Designs
- Use colors that maintain 40%+ contrast
- Avoid similar hues for fill and background
- Test scanning at various distances

## Size Considerations

### Small (100-200px)
- Digital use only
- Email signatures
- Small web graphics

### Medium (300-500px) [Recommended]
- Print materials
- Standard marketing materials
- Mobile displays

### Large (600-2000px)
- High-quality print
- Posters and banners
- Detailed applications

## Image Variable Concept

This node introduces the **image variable type** to the workflow system:

### Structure
- **URL**: Direct link for display or download
- **Metadata**: Rich information about the image
- **Mime Type**: Enables proper handling by other nodes
- **Dimensions**: Width and height for layout calculations

### Benefits
- **Chainable**: Pass images between nodes
- **Trackable**: Metadata preserves generation context
- **Displayable**: Frontend can show inline previews
- **Persistent**: S3 storage ensures availability

## Performance

- **Generation Speed**: ~50-200ms depending on data complexity
- **Upload Speed**: ~100-500ms depending on image size and network
- **Caching**: Images are cached by CDN when configured
- **Parallel Processing**: Multiple QR codes can be generated simultaneously

## Best Practices

### Data Encoding
- Keep data concise for smaller, faster-scanning codes
- Use URL shorteners for long URLs
- Consider data compression for complex information
- Test with target scanning devices

### Error Correction
- Use higher levels for printed materials
- Use lower levels for digital-only applications
- Consider environmental factors (outdoor use, handling)

### Storage Management
- Implement cleanup policies for old execution images
- Monitor bucket storage costs
- Use lifecycle rules for automatic archival
- Consider CDN for frequently accessed images

## Security Considerations

- **Public Access**: Generated images are publicly accessible via URL
- **Data Privacy**: Don't encode sensitive information directly
- **URL Guessing**: Use complex paths to prevent enumeration
- **Bucket Policies**: Configure appropriate S3 bucket policies
- **Encryption**: Enable S3 encryption for sensitive projects

## Integration Examples

### With Other Nodes
1. **Generate Data** → **Generate QR Code** → **Send Email**
2. **Fetch URL** → **Generate QR Code** → **Add to PDF**
3. **Create vCard** → **Generate QR Code** → **Upload to CRM**

### Frontend Display
```javascript
// Display QR code in frontend
const qrImage = nodeOutput.qr_image;
<img src={qrImage.url} 
     alt="QR Code" 
     width={qrImage.width} 
     height={qrImage.height} />
```

## Limitations

- Maximum data capacity depends on error correction level
- Very long data may result in dense, hard-to-scan codes
- Color combinations must maintain sufficient contrast
- S3 storage costs apply for image storage
- Public bucket access required for image URLs