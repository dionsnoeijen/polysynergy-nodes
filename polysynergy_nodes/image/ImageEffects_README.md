# Image Effects

Applies various visual effects and enhancements to images including color adjustments, filters, and blur effects.

## Description

The Image Effects node provides comprehensive image enhancement capabilities with color adjustments (brightness, contrast, saturation, sharpness) and artistic filters. It intelligently skips processing when no effects are applied and generates descriptive filenames based on the effects used. All processed images are uploaded to S3 with project-based isolation.

## Inputs

### Source Image
- **Input Image**: Image to apply effects to (URL or image object) (required)

### Color Adjustments
- **Brightness**: Brightness adjustment (0.0 = black, 1.0 = original, 2.0 = double brightness) (default: 1.0)
- **Contrast**: Contrast adjustment (0.0 = gray, 1.0 = original, 2.0 = double contrast) (default: 1.0)
- **Saturation**: Color saturation (0.0 = grayscale, 1.0 = original, 2.0 = double saturation) (default: 1.0)
- **Sharpness**: Sharpness adjustment (0.0 = blurred, 1.0 = original, 2.0 = sharp) (default: 1.0)

### Filters
- **Blur Radius**: Gaussian blur radius (0.0 = no blur) (default: 0.0)
- **Filter Effect**: Additional filter to apply (default: "none")
  - **None**: No filter
  - **Emboss**: Emboss effect
  - **Edge Enhancement**: Edge enhancement
  - **Strong Edge Enhancement**: Strong edge enhancement
  - **Find Edges**: Find edges
  - **Smooth**: Smooth filter
  - **Strong Smooth**: Strong smooth filter
  - **Sharpen**: Sharpen filter

### Output Settings
- **Quality**: JPEG quality (1-100) (default: 85)

## Outputs

- **Processed Image**: Complete image object with URL and metadata
  ```json
  {
    "url": "https://bucket.s3.region.amazonaws.com/path/to/effects.jpg",
    "mime_type": "image/jpeg",
    "width": 800,
    "height": 600,
    "size": 156789,
    "metadata": {
      "original": {
        "width": 800,
        "height": 600,
        "url": "https://original-image-url.com/image.jpg"
      },
      "effects": {
        "brightness": 1.2,
        "contrast": 1.1,
        "saturation": 0.9,
        "sharpness": 1.3,
        "blur_radius": 0.5,
        "filter_effect": "emboss"
      },
      "quality": 85,
      "s3_key": "tenant/project/node/execution/effects_br1.2_co1.1_sa0.9_sh1.3_bl0.5_femboss_timestamp.jpg",
      "bucket": "polysynergy-tenant-project-media"
    }
  }
  ```
- **Image URL**: Direct URL to the processed image

## Paths

- **Success**: Effects applied successfully  
- **Error**: Error during image processing

## Color Adjustments

### Brightness
Controls the overall lightness or darkness of the image.

**Values:**
- **0.0**: Completely black image
- **0.5**: Very dark image
- **1.0**: Original brightness [default]
- **1.5**: Brighter image
- **2.0**: Very bright image
- **3.0**: Maximum brightness

**Use Cases:**
- Correcting underexposed photos
- Creating mood effects
- Enhancing visibility of dark images
- Preparing images for different display environments

**Example Effects:**
```javascript
brightness: 0.7  // Darken for dramatic effect
brightness: 1.3  // Brighten for outdoor visibility  
brightness: 0.3  // Very dark for night mode
```

### Contrast
Controls the difference between light and dark areas.

**Values:**
- **0.0**: Completely gray image (no contrast)
- **0.5**: Low contrast, washed out
- **1.0**: Original contrast [default]  
- **1.5**: High contrast, more dramatic
- **2.0**: Very high contrast
- **3.0**: Maximum contrast

**Use Cases:**
- Enhancing flat, dull images
- Creating dramatic effects
- Improving text readability
- Correcting overexposed photos

**Example Effects:**
```javascript
contrast: 1.4    // Enhance drama in landscapes
contrast: 0.8    // Soften harsh lighting
contrast: 1.8    // High contrast black & white effect
```

### Saturation
Controls the intensity of colors.

**Values:**
- **0.0**: Grayscale image (no color)
- **0.5**: Desaturated, muted colors
- **1.0**: Original color saturation [default]
- **1.5**: Vivid, enhanced colors
- **2.0**: Very saturated colors
- **3.0**: Maximum saturation

**Use Cases:**
- Creating black and white effects
- Enhancing dull colors
- Creating vintage/retro looks
- Preparing images for different color schemes

**Example Effects:**
```javascript
saturation: 0.0  // Black and white conversion
saturation: 1.6  // Vivid social media look
saturation: 0.4  // Muted, professional tone
```

### Sharpness
Controls the clarity and edge definition.

**Values:**
- **0.0**: Completely blurred
- **0.5**: Soft, slightly blurred
- **1.0**: Original sharpness [default]
- **1.5**: Enhanced sharpness
- **2.0**: Very sharp
- **3.0**: Maximum sharpness

**Use Cases:**
- Correcting soft/blurry photos
- Enhancing text readability
- Creating artistic soft effects
- Preparing images for print

**Example Effects:**
```javascript
sharpness: 1.8   // Enhance details for print
sharpness: 0.6   // Soft portrait effect
sharpness: 2.2   // Sharp product photography
```

## Filter Effects

### Blur Effects
**Gaussian Blur**: Applies smooth blurring effect.

**Radius Values:**
- **0.0**: No blur [default]
- **0.5-2.0**: Subtle blur
- **2.0-5.0**: Moderate blur
- **5.0-10.0**: Strong blur
- **10.0-20.0**: Very strong blur

**Use Cases:**
- Background blur effects
- Creating depth of field
- Softening harsh details
- Privacy protection (faces, text)

### Artistic Filters

#### Emboss
Creates a raised, 3D-like effect by highlighting edges.
- **Use Cases**: Logo effects, artistic styling, texture enhancement
- **Best With**: High contrast images, text, geometric shapes

#### Edge Enhancement / Strong Edge Enhancement
Sharpens edges and boundaries in the image.
- **Use Cases**: Technical illustrations, architectural photos, detail enhancement
- **Best With**: Images with clear boundaries, line art

#### Find Edges
Highlights edges and converts the image to show only edge information.
- **Use Cases**: Technical analysis, artistic effects, outline creation
- **Best With**: High contrast images, objects with clear boundaries

#### Smooth / Strong Smooth
Reduces noise and creates a smoother appearance.
- **Use Cases**: Noise reduction, skin smoothing, artistic softening
- **Best With**: Noisy images, portraits, textured surfaces

#### Sharpen
Enhances image sharpness and detail definition.
- **Use Cases**: Correcting soft images, enhancing details, print preparation
- **Best With**: Slightly blurry images, photos needing detail enhancement

## Effect Combinations

### Popular Combinations

#### Vintage Effect
```javascript
brightness: 1.1,
contrast: 0.9,
saturation: 0.7,
filter_effect: "smooth"
```

#### High Contrast B&W
```javascript
brightness: 1.0,
contrast: 1.6,
saturation: 0.0,
sharpness: 1.2
```

#### Soft Portrait
```javascript
brightness: 1.1,
contrast: 0.9,
saturation: 1.1,
blur_radius: 0.3,
filter_effect: "smooth"
```

#### Dramatic Landscape
```javascript
brightness: 1.0,
contrast: 1.4,
saturation: 1.3,
sharpness: 1.3,
filter_effect: "edge_enhance"
```

#### Product Photo Enhancement
```javascript
brightness: 1.05,
contrast: 1.15,
saturation: 1.1,
sharpness: 1.4
```

## Smart Processing

### No Effects Detection
The node automatically detects when no effects are applied (all values at defaults) and skips processing:

```javascript
// These settings trigger bypass
brightness: 1.0,
contrast: 1.0, 
saturation: 1.0,
sharpness: 1.0,
blur_radius: 0.0,
filter_effect: "none"

// Result: Original image returned with message
"No effects applied - all settings at default values"
```

### Processing Order
Effects are applied in optimal order for best results:

1. **Color Adjustments** (brightness → contrast → saturation → sharpness)
2. **Blur Effects** (Gaussian blur)
3. **Artistic Filters** (emboss, edge enhance, etc.)

## Validation Rules

### Value Ranges
- **Brightness**: 0.0 - 3.0
- **Contrast**: 0.0 - 3.0  
- **Saturation**: 0.0 - 3.0
- **Sharpness**: 0.0 - 3.0
- **Blur Radius**: 0.0 - 20.0
- **Quality**: 1 - 100

### Error Messages
```javascript
"Brightness must be between 0 and 3"
"Blur radius must be between 0 and 20"  
"Quality must be between 1 and 100"
```

## S3 Storage Structure

Filenames include effect signatures for easy identification:

```
bucket-name: polysynergy-{tenant_id}-{project_id}-media/
  └── {tenant_id}/
      └── {project_id}/
          └── {node_id}/
              └── {execution_id}/
                  └── effects_{signature}_{timestamp}.jpg
```

**Filename Examples:**
- `effects_br1.2_co1.1_sa0.9_sh1.3_bl0.5_femboss_20240315_143022_123.jpg`
- `effects_br0.8_co1.4_sa0.0_20240315_143022_123.jpg` (B&W effect)
- `effects_noeffects_20240315_143022_123.jpg` (bypass case)

**Signature Components:**
- `br` = brightness
- `co` = contrast  
- `sa` = saturation
- `sh` = sharpness
- `bl` = blur radius
- `f` = filter effect

## Performance Considerations

### Processing Speed
- **Color adjustments**: Fast (~50-200ms)
- **Blur effects**: Moderate (~100-400ms, depends on radius)
- **Artistic filters**: Fast (~50-150ms)
- **Combined effects**: Sum of individual effects
- **Bypass (no effects)**: Instant (~5ms)

### Memory Usage
- Loads full image into memory during processing
- Peak usage: ~3x original image size (original + working + output)
- Larger images require more memory and processing time

### Optimization Tips
- Use bypass detection to avoid unnecessary processing
- Apply effects in batch rather than sequential nodes
- Consider image size when applying heavy blur effects
- Cache results for repeated access to same effects

## Best Practices

### Effect Moderation
- **Subtle adjustments** often look more professional than extreme effects
- **Test effects** on various image types before production use
- **Consider viewing environment** (mobile, print, web) when choosing intensity

### Quality Settings
- **Web display**: 80-85 quality
- **Social media**: 75-85 quality
- **Print materials**: 90-95 quality
- **Archival**: 95-100 quality

### Workflow Integration
```javascript
// Typical workflow
Original → Color Correction → Artistic Effect → Output

// Example pipeline
Upload → Effects (brightness: 1.1, contrast: 1.2) → Resize → Display
```

## Common Use Cases

### Photo Correction
- Fix underexposed photos: `brightness: 1.3, contrast: 1.1`
- Enhance dull photos: `saturation: 1.2, contrast: 1.2`
- Sharpen soft photos: `sharpness: 1.4`

### Artistic Effects
- Black & white: `saturation: 0.0, contrast: 1.3`
- Vintage look: `brightness: 1.1, contrast: 0.9, saturation: 0.7`
- Dramatic: `contrast: 1.5, saturation: 1.3, sharpness: 1.2`

### Technical Processing
- Edge detection: `filter_effect: "find_edges"`
- Noise reduction: `filter_effect: "smooth"`
- Detail enhancement: `sharpness: 1.5, filter_effect: "edge_enhance"`

## Integration Examples

### With Other Image Nodes
1. **Upload** → **Crop** → **Effects** → **Resize** → **Display**
2. **Generate QR** → **Effects** (contrast enhancement) → **Email**  
3. **Camera Capture** → **Effects** (auto-enhance) → **Save**

### Batch Processing
```javascript
// Apply same effects to multiple images
const effects = {
  brightness: 1.1,
  contrast: 1.2,
  saturation: 1.1
};
// Apply to image array
```

### Conditional Effects
```javascript
// Different effects based on image type
if (imageType === 'portrait') {
  effects = { brightness: 1.1, blur_radius: 0.3 };
} else if (imageType === 'landscape') {
  effects = { contrast: 1.3, saturation: 1.2 };
}
```

## Limitations

- Output format is always JPEG (PNG transparency not preserved)
- Some extreme effect combinations may produce unexpected results
- Very large images may consume significant memory
- Processing time increases with image size and effect complexity
- S3 storage costs apply for processed images

## Security Considerations

- Validates all effect parameters before processing
- Ensures safe value ranges to prevent system overload
- Downloads images with timeout protection
- Generated images are publicly accessible via S3 URL
- No sensitive effect data embedded in metadata