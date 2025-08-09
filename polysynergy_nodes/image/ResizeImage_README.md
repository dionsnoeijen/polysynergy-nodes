# Resize Image

Resizes images using various methods while maintaining quality and uploading results to S3 storage.

## Description

The Resize Image node provides flexible image resizing capabilities with multiple resize methods to suit different use cases. It supports both exact dimensions and aspect-ratio preserving resizes, with constraints for maximum dimensions. The resized images are automatically uploaded to S3 with project-based isolation.

## Inputs

- **Input Image**: Image to resize (URL or image object) (required)
- **Width**: Target width in pixels (0 = maintain aspect ratio) (default: 0)
- **Height**: Target height in pixels (0 = maintain aspect ratio) (default: 0)  
- **Max Width**: Maximum width constraint (0 = no limit) (default: 0)
- **Max Height**: Maximum height constraint (0 = no limit) (default: 0)
- **Resize Method**: How to resize the image
  - **Fit**: Fit within dimensions (maintain aspect ratio) [default]
  - **Fill**: Fill dimensions exactly (may stretch)
  - **Crop**: Crop to fill dimensions
  - **Pad**: Pad to fill dimensions
- **Quality**: JPEG quality (1-100) (default: 85)

## Outputs

- **Resized Image**: Complete image object with URL and metadata
  ```json
  {
    "url": "https://bucket.s3.region.amazonaws.com/path/to/resized.jpg",
    "mime_type": "image/jpeg",
    "width": 400,
    "height": 300,
    "size": 45123,
    "metadata": {
      "original": {
        "width": 800,
        "height": 600,
        "url": "https://original-image-url.com/image.jpg"
      },
      "resize_method": "fit",
      "quality": 85,
      "s3_key": "tenant/project/node/execution/resized_w400h300_fit_timestamp.jpg",
      "bucket": "polysynergy-tenant-project-media"
    }
  }
  ```
- **Image URL**: Direct URL to the resized image

## Paths

- **Success**: Image resized successfully
- **Error**: Error during image resizing

## Resize Methods

### Fit (Default)
Resizes the image to fit within the specified dimensions while preserving aspect ratio. The image will be smaller than or equal to the target dimensions.

**Use Cases:**
- Thumbnails that must fit within specific bounds
- Responsive image display
- When aspect ratio preservation is critical

**Example:**
```
Original: 800x600 → Target: 400x300
Result: 400x300 (fits exactly)

Original: 800x400 → Target: 400x300  
Result: 400x200 (preserves wide aspect ratio)
```

### Fill
Resizes the image to exactly match the target dimensions. May stretch or compress the image, potentially distorting the aspect ratio.

**Use Cases:**
- When exact dimensions are required
- Placeholder images
- Graphics that can tolerate distortion

**Example:**
```
Original: 800x600 → Target: 400x300
Result: 400x300 (exact match, may stretch)

Original: 800x400 → Target: 400x300
Result: 400x300 (stretched vertically)
```

### Crop
Resizes and crops the image to exactly fill the target dimensions while preserving aspect ratio. Parts of the image may be cropped off.

**Use Cases:**
- Profile pictures
- Hero images
- When exact dimensions and aspect ratio are both important

**Example:**
```
Original: 800x600 → Target: 400x400
Process: Resize to 533x400, then crop to 400x400 (center crop)

Original: 600x800 → Target: 400x400
Process: Resize to 400x533, then crop to 400x400 (center crop)
```

### Pad
Resizes the image to fit within the target dimensions, then pads with white background to achieve exact dimensions.

**Use Cases:**
- Product images with consistent sizing
- Gallery displays
- When both aspect ratio and exact dimensions are needed

**Example:**
```
Original: 800x400 → Target: 400x400
Process: Resize to 400x200, then pad to 400x400 with white borders

Original: 400x800 → Target: 400x400
Process: Resize to 200x400, then pad to 400x400 with white borders
```

## Dimension Logic

### Single Dimension
When only width or height is specified:
- **Width only**: Height calculated to preserve aspect ratio
- **Height only**: Width calculated to preserve aspect ratio

### Maximum Constraints
Max width/height values override target dimensions if they would be exceeded:
```
Target: 1000x800, Max: 500x400
Result: Constrained to 500x400
```

### No Resize Needed
If calculated dimensions match the original image size, the node will skip processing and return the original image with a success message.

## Quality Settings

### High Quality (90-100)
- Best image quality
- Larger file sizes
- Use for: Final output, print materials

### Standard Quality (70-89) [Default: 85]
- Good balance of quality and file size
- Use for: Web display, general purposes

### Compressed (50-69)
- Smaller file sizes
- Noticeable quality reduction
- Use for: Thumbnails, bandwidth-limited scenarios

### Low Quality (1-49)
- Very small file sizes
- Significant quality loss
- Use for: Placeholder images only

## S3 Storage Structure

Images are organized in S3 with hierarchical structure:
```
bucket-name: polysynergy-{tenant_id}-{project_id}-media/
  └── {tenant_id}/
      └── {project_id}/
          └── {node_id}/
              └── {execution_id}/
                  └── resized_{params}_{timestamp}.jpg
```

**Filename Example:**
`resized_w400h300_fit_20240315_143022_123.jpg`

## Error Handling

### Validation Errors
- **Quality**: Must be between 1 and 100
- **Dimensions**: Width and height must be non-negative
- **Constraints**: At least one dimension constraint must be specified

### Processing Errors
- **Download Failed**: Invalid URL or network issues
- **Image Format**: Unsupported image formats
- **Upload Failed**: S3 upload errors
- **Memory**: Very large images may cause memory issues

### Automatic Handling
- **Transparency**: RGBA/LA images converted to RGB with white background
- **Color Modes**: Non-RGB modes automatically converted
- **Bounds Checking**: Prevents invalid crop areas

## Performance Considerations

### Image Size Impact
- **Small images** (< 1MB): ~100-300ms processing
- **Medium images** (1-5MB): ~300-800ms processing  
- **Large images** (> 5MB): ~800ms+ processing

### Optimization Tips
- Use appropriate quality settings
- Consider max dimension constraints for very large images
- Batch multiple resizes when possible
- Cache results when repeatedly accessing same images

## Best Practices

### Method Selection
- **Fit**: When aspect ratio is most important
- **Fill**: When exact dimensions matter more than distortion
- **Crop**: For uniform layouts (cards, grids)
- **Pad**: For consistent sizing with preserved content

### Quality Guidelines
- **Thumbnails**: 70-80 quality
- **Display images**: 80-90 quality
- **Print materials**: 90-100 quality
- **Background images**: 60-80 quality

### Dimension Planning
- Define standard sizes for your application
- Use max constraints to prevent excessive memory usage
- Consider responsive breakpoints when choosing sizes
- Test resize results with various aspect ratios

## Integration Examples

### With Other Image Nodes
1. **Generate QR Code** → **Resize Image** → **Add to PDF**
2. **Upload Image** → **Resize Image** → **Apply Effects**
3. **Crop Image** → **Resize Image** → **Email Attachment**

### Responsive Image Pipeline
```
Original Image
  ├── Resize (400x300) - Mobile
  ├── Resize (800x600) - Tablet  
  └── Resize (1200x900) - Desktop
```

### Thumbnail Generation
```
Upload → Resize (fit, 150x150) → Cache → Display
```

## Limitations

- Output format is always JPEG (PNG transparency not preserved)
- Very large images may consume significant memory
- S3 storage costs apply
- Maximum practical size depends on available memory
- Processing time increases with image size

## Security Considerations

- Validates image URLs before downloading
- Converts potentially unsafe image modes to RGB
- Generated images are publicly accessible via S3 URL
- No sensitive data should be embedded in images
- Consider implementing rate limiting for large images