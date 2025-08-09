# Crop Image

Crops images using various methods including pixel coordinates, percentages, and smart cropping modes.

## Description

The Crop Image node provides flexible image cropping capabilities with multiple modes to suit different use cases. It supports precise pixel-based cropping, percentage-based cropping for responsive designs, and smart cropping modes for common patterns like centered squares and circles. Cropped images are automatically uploaded to S3 with project-based isolation.

## Inputs

### Basic Settings
- **Input Image**: Image to crop (URL or image object) (required)
- **Quality**: JPEG quality (1-100) (default: 85)

### Crop Mode
- **Crop Mode**: Method for defining crop area
  - **Pixels**: Use exact pixel coordinates [default]
  - **Percentage**: Use percentage values relative to image dimensions
  - **Center Square**: Center square crop (largest possible)
  - **Center Circle**: Center circle crop area

### Pixel Mode Settings
- **X Position**: Left position in pixels (0 = left edge) (default: 0)
- **Y Position**: Top position in pixels (0 = top edge) (default: 0)
- **Width**: Width of crop area in pixels (0 = use remaining width) (default: 0)
- **Height**: Height of crop area in pixels (0 = use remaining height) (default: 0)

### Percentage Mode Settings
- **X Percent**: Left position as percentage (0-100) (default: 0.0)
- **Y Percent**: Top position as percentage (0-100) (default: 0.0)
- **Width Percent**: Width as percentage (0-100) (default: 100.0)
- **Height Percent**: Height as percentage (0-100) (default: 100.0)

## Outputs

- **Cropped Image**: Complete image object with URL and metadata
  ```json
  {
    "url": "https://bucket.s3.region.amazonaws.com/path/to/cropped.jpg",
    "mime_type": "image/jpeg",
    "width": 400,
    "height": 300,
    "size": 38456,
    "metadata": {
      "original": {
        "width": 800,
        "height": 600,
        "url": "https://original-image-url.com/image.jpg"
      },
      "crop": {
        "x": 100,
        "y": 50,
        "width": 400,
        "height": 300,
        "mode": "pixels"
      },
      "quality": 85,
      "s3_key": "tenant/project/node/execution/crop_x100y50w400h300_timestamp.jpg",
      "bucket": "polysynergy-tenant-project-media"
    }
  }
  ```
- **Image URL**: Direct URL to the cropped image

## Paths

- **Success**: Image cropped successfully
- **Error**: Error during image cropping

## Crop Modes

### Pixels Mode
Uses exact pixel coordinates to define the crop area. Provides precise control over the crop region.

**Use Cases:**
- Precise cropping based on known coordinates
- Removing specific elements from images
- When exact pixel control is needed

**Parameters:**
- **X, Y**: Top-left corner position (0,0 = top-left of image)
- **Width, Height**: Dimensions of crop area (0 = use remaining space)

**Example:**
```
Original: 800x600 image
X: 100, Y: 50, Width: 400, Height: 300
Result: 400x300 crop starting at (100, 50)
```

### Percentage Mode  
Uses percentage values relative to the original image dimensions. Ideal for responsive cropping.

**Use Cases:**
- Responsive image cropping
- Maintaining crop ratios across different image sizes
- Dynamic cropping based on layout requirements

**Parameters:**
- **X%, Y%**: Position as percentage of image dimensions
- **Width%, Height%**: Size as percentage of image dimensions

**Example:**
```
Original: 800x600 image
X: 25%, Y: 20%, Width: 50%, Height: 60%
Calculated: X: 200px, Y: 120px, Width: 400px, Height: 360px
Result: 400x360 crop
```

### Center Square Mode
Automatically creates the largest possible square crop from the center of the image.

**Use Cases:**
- Profile pictures
- Avatar images
- Thumbnail generation
- Social media images requiring square format

**Behavior:**
- Uses the smaller dimension as the square size
- Centers the crop area automatically
- No additional parameters needed

**Example:**
```
Original: 800x600 image (landscape)
Square size: 600x600 (limited by height)
Position: X: 100, Y: 0 (centered horizontally)

Original: 600x800 image (portrait)  
Square size: 600x600 (limited by width)
Position: X: 0, Y: 100 (centered vertically)
```

### Center Circle Mode
Creates a square crop area centered on the image, suitable for circular content or avatars.

**Use Cases:**
- Circular avatar preparation
- Logo cropping
- Icon generation
- Round profile pictures

**Behavior:**
- Same as center square but intended for circular content
- Creates square crop that will contain the circle
- Centers automatically

**Note:** This mode creates a square crop area - the actual circular shape would be applied by subsequent processing or CSS styling.

## Dimension Calculations

### Automatic Bounds Checking
The node automatically ensures crop areas stay within image boundaries:

```javascript
// Pixel mode bounds checking
x = max(0, min(x, imageWidth - 1))
y = max(0, min(y, imageHeight - 1))
width = min(width, imageWidth - x)
height = min(height, imageHeight - y)
```

### Zero-Value Handling
- **Width = 0**: Uses remaining width from X position to right edge
- **Height = 0**: Uses remaining height from Y position to bottom edge
- **X or Y beyond bounds**: Automatically constrained to valid range

### Percentage Conversion
```javascript
pixelX = (percentX / 100) * imageWidth
pixelY = (percentY / 100) * imageHeight
pixelWidth = (percentWidth / 100) * imageWidth  
pixelHeight = (percentHeight / 100) * imageHeight
```

## Validation Rules

### Pixel Mode
- X, Y positions cannot be negative
- Width, Height cannot be negative
- Crop area must have positive dimensions
- Crop area cannot extend beyond image boundaries

### Percentage Mode
- All percentage values must be 0-100
- X% + Width% cannot exceed 100
- Y% + Height% cannot exceed 100
- Width% and Height% must be greater than 0

### General
- Quality must be between 1-100
- Input image must be valid URL or image object
- Crop area must result in non-empty region

## Error Handling

### Validation Errors
```javascript
// Example error messages
"X position cannot be negative"
"Width percent must be between 0 and 100"  
"X percent + Width percent cannot exceed 100"
"Quality must be between 1 and 100"
```

### Processing Errors
- **Invalid crop area**: Results in empty or invalid dimensions
- **Bounds exceeded**: Crop area extends beyond image boundaries
- **Download failed**: Invalid image URL or network issues
- **Upload failed**: S3 upload errors

### Automatic Recovery
- Out-of-bounds coordinates are automatically constrained
- Zero dimensions are replaced with calculated values
- Invalid URLs trigger clear error messages

## S3 Storage Structure

Images are organized with descriptive filenames indicating crop parameters:

```
bucket-name: polysynergy-{tenant_id}-{project_id}-media/
  └── {tenant_id}/
      └── {project_id}/
          └── {node_id}/
              └── {execution_id}/
                  └── crop_{params}_{timestamp}.jpg
```

**Filename Examples:**
- Pixels: `crop_x100y50w400h300_20240315_143022_123.jpg`
- Percentage: `crop_px25.0py20.0pw50.0ph60.0_20240315_143022_123.jpg`
- Center Square: `crop_center_square_20240315_143022_123.jpg`
- Center Circle: `crop_center_circle_20240315_143022_123.jpg`

## Performance Considerations

### Processing Speed
- **Crop operation**: Very fast (~10-50ms) - simple pixel manipulation
- **Download time**: Varies with image size and network
- **Upload time**: Varies with crop size and network
- **Total time**: Usually 200-800ms depending on image size

### Memory Usage
- Cropping reduces memory usage (smaller output image)
- Original image briefly loaded into memory
- More efficient than resize operations

### Optimization Tips
- Use percentage mode for responsive applications
- Prefer center square/circle for uniform outputs
- Consider image dimensions when choosing crop parameters
- Cache results for repeated operations

## Best Practices

### Mode Selection
- **Pixels**: When you know exact coordinates (e.g., from image analysis)
- **Percentage**: For responsive designs or proportional cropping
- **Center Square**: For profile pictures, avatars, thumbnails
- **Center Circle**: When preparing circular images

### Quality Guidelines
- **Thumbnails**: 70-80 quality
- **Display images**: 80-90 quality  
- **High-res crops**: 90-95 quality
- **Archive/print**: 95-100 quality

### Crop Planning
- Preview crop areas before processing
- Consider aspect ratios of target displays
- Leave margins for important content
- Test with various image sizes and orientations

### Responsive Cropping
```javascript
// Mobile: Focus on center
{ x_percent: 25, y_percent: 25, width_percent: 50, height_percent: 50 }

// Desktop: Show more context  
{ x_percent: 10, y_percent: 10, width_percent: 80, height_percent: 80 }
```

## Integration Examples

### With Other Image Nodes
1. **Upload Image** → **Crop Image** → **Resize Image** → **Apply Effects**
2. **Generate QR Code** → **Crop Image** (trim borders) → **Email**
3. **Camera Capture** → **Crop Image** (center square) → **Profile Update**

### Avatar Pipeline
```
Original Photo → Crop (center_square) → Resize (128x128) → Cache
```

### Responsive Thumbnails
```
Original → Crop (percentage) → Multiple Resize operations
```

### Focus Area Extraction
```
Full Image → Crop (pixels, face detection coords) → Display
```

## Advanced Use Cases

### Face-Centered Cropping
Combine with face detection to automatically center crops on faces:
```javascript
// After face detection provides coordinates
crop_mode: "pixels",
x: faceX - padding,
y: faceY - padding,  
width: faceWidth + (2 * padding),
height: faceHeight + (2 * padding)
```

### Smart Thumbnail Generation
```javascript
// For landscape images
crop_mode: "center_square"

// For portraits, crop to focus area
crop_mode: "percentage", 
x_percent: 10, y_percent: 0, 
width_percent: 80, height_percent: 70
```

### Batch Cropping
Process multiple crops from single image:
```
Original → [
  Crop (thumbnail),
  Crop (header), 
  Crop (detail view)
]
```

## Limitations

- Output format is always JPEG (PNG transparency not preserved)
- Crop area must be within original image boundaries
- Cannot add content outside original image bounds
- Minimum crop size limited by image format constraints
- S3 storage costs apply for each cropped image

## Security Considerations

- Validates all coordinate parameters before processing
- Ensures crop areas remain within safe boundaries
- Downloads images with timeout protection
- Generated images are publicly accessible via S3 URL
- No sensitive coordinate data should be embedded in metadata