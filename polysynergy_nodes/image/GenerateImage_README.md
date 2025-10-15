# 🎨 Generate Image Node

The `Generate Image` node creates AI-generated images using OpenAI's DALL-E models from text prompts. Supports both DALL-E 2 and DALL-E 3 with automatic S3 storage and optional caching.

---

## 📂 Category

**image**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| prompt     | str    | ✅        | Text description of image to generate    |
| model      | str    | ❌        | AI model (dall-e-2, dall-e-3)            |
| size       | str    | ❌        | Image dimensions (default: 1024x1024)    |
| quality    | str    | ❌        | Quality: standard, hd (DALL-E 3 only)    |
| style      | str    | ❌        | Style: vivid, natural (DALL-E 3 only)    |
| rerender   | bool   | ❌        | Generate new image each time (default: true) |
| save_path  | str    | ❌        | Custom S3 path (default: generated/images/) |

---

## 🔌 Outputs

| Name             | Type   | Description                              |
|------------------|--------|------------------------------------------|
| generated_image  | Image  | Image object with URL and metadata       |
| image_url        | str    | Direct URL to the image                  |
| file_path        | str    | S3 key/path of the image file            |

---

## 🔀 Flow Control

| Path        | Description                                 |
|-------------|---------------------------------------------|
| true_path   | Image generated successfully                |
| false_path  | Error during generation                     |

---

## ✅ Examples

### Basic Image Generation (DALL-E 2):
```json
{
  "prompt": "A serene landscape with mountains and a lake at sunset"
}
```

### High Quality Image (DALL-E 3):
```json
{
  "prompt": "A futuristic city with flying cars and neon lights",
  "model": "dall-e-3",
  "size": "1792x1024",
  "quality": "hd",
  "style": "vivid"
}
```

### Cached Image (No Rerender):
```json
{
  "prompt": "A professional headshot photo",
  "model": "dall-e-3",
  "rerender": false
}
```
Subsequent executions with same prompt reuse the cached image.

### Custom S3 Path:
```json
{
  "prompt": "Company logo concept",
  "save_path": "assets/logos/"
}
```

---

## 🎨 Model Comparison

| Feature | DALL-E 2 | DALL-E 3 |
|---------|----------|----------|
| **Quality** | Good | Excellent |
| **Speed** | Faster | Slower |
| **Cost** | Lower | Higher |
| **Sizes** | 256x256, 512x512, 1024x1024 | 1024x1024, 1792x1024, 1024x1792 |
| **Quality Options** | ❌ | standard, hd |
| **Style Options** | ❌ | vivid, natural |

---

## 📐 Supported Sizes

### DALL-E 2:
- `256x256` - Small, fast
- `512x512` - Medium
- `1024x1024` - Large (square)

### DALL-E 3:
- `1024x1024` - Square
- `1792x1024` - Landscape
- `1024x1792` - Portrait

---

## 🔄 Caching Behavior

### With Rerender (Default):
```
Generate → New Image Every Time → Unique Filename with Timestamp
```

### Without Rerender (Cached):
```
First Run: Generate → Cache in S3 → Return URL
Next Runs: Check Cache → Reuse Existing → Return Same URL
```

Cache key based on: prompt + model + size + quality + style

---

## 📁 File Storage

**Path Structure:**
```
{save_path}/{unique_id}_{model}_{size}_{timestamp}.png
```

**Examples:**
- `generated/images/a1b2c3d4_dalle3_1024x1024_20250115_123045.png` (rerender=true)
- `generated/images/cached_dalle3_1024x1024_f8a3b2c1.png` (rerender=false)

---

## 🔒 Security & Validation

- **Path Sanitization**: Removes dangerous characters
- **No Traversal**: Blocks `..` in paths
- **Relative Paths**: Must be relative to bucket root
- **Character Limits**: Max 800 characters for path
- **Auto-cleanup**: Invalid paths default to `generated/images/`

---

## 💡 Use Cases

- **Content Creation**: Generate illustrations for articles
- **Product Mockups**: Create product concept images
- **Marketing Assets**: Generate promotional imagery
- **Prototyping**: Quick visual concept generation
- **Avatar Generation**: Create user profile images

---

## ⚠️ Notes

- **API Key Required**: Needs `OPENAI_API_KEY` environment variable
- **S3 Storage**: Automatically uploads to tenant S3 bucket
- **PNG Format**: All images saved as PNG
- **Cost Consideration**: DALL-E 3 HD is most expensive option
- **Prompt Length**: Prompts truncated to 200 chars in metadata
- **Model Restrictions**: Size options vary by model
