# 🎨 Random Color Node

The `Random Color` node is part of the **random** category and generates random colors in various formats.

---

## ✅ Functionality

This node generates random colors in different formats including hex, RGB, HSL, and color names. Perfect for generating design assets, testing UI components, or creating visual variety in applications.

---

## 🔌 Inputs

| Name   | Type   | Required | Description                                           |
|--------|--------|----------|-------------------------------------------------------|
| format | string | Yes      | Color format: `hex` (#FFFFFF), `rgb` (255, 255, 255), `hsl` (360, 100%, 50%), `name` (red, blue, etc.) |

---

## 🔀 Outputs

| Name       | Type   | Description                                    |
|------------|--------|------------------------------------------------|
| true_path  | string | The generated random color in the selected format |
| false_path | dict   | Error information if failure occurs           |

---

## 💡 Example

### Input:
```json
{
  "format": "hex"
}
```

### Output via `true_path`:
```json
{
  "true_path": "#3a7bd5"
}
```

### RGB Format Example:
```json
{
  "format": "rgb",
  "true_path": "rgb(58, 123, 213)"
}
```

### HSL Format Example:
```json
{
  "format": "hsl", 
  "true_path": "hsl(220, 68%, 53%)"
}
```

### Color Name Example:
```json
{
  "format": "name",
  "true_path": "turquoise"
}
```

---

## ⚠️ Notes

- **Hex format**: Generates 6-digit hexadecimal colors with # prefix
- **RGB format**: Values range from 0-255 for each color channel
- **HSL format**: Hue (0-360°), Saturation (0-100%), Lightness (0-100%)
- **Name format**: Returns common color names from a predefined list
- Colors are generated randomly on each execution
- All formats produce valid CSS color values

---

## 🎯 Use Cases

- **UI Testing**: Generate random colors for component testing
- **Design Systems**: Create color palettes programmatically  
- **Data Visualization**: Assign random colors to chart elements
- **Game Development**: Random color generation for game assets
- **Art Generation**: Create random color schemes for digital art