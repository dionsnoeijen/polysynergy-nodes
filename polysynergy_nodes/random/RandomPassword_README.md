# 🔐 Random Password Node

The `Random Password` node is part of the **random** category and generates secure random passwords with customizable character sets and options.

---

## ✅ Functionality

This node creates cryptographically random passwords with full control over character types, length, and security features. Ideal for user registration systems, API key generation, or security testing.

---

## 🔌 Inputs

| Name                     | Type | Required | Description                                        |
|--------------------------|------|----------|----------------------------------------------------|
| length                   | int  | Yes      | Password length (minimum 1)                       |
| include_uppercase        | bool | Yes      | Include uppercase letters (A-Z)                   |
| include_lowercase        | bool | Yes      | Include lowercase letters (a-z)                   |
| include_numbers          | bool | Yes      | Include numbers (0-9)                             |
| include_symbols          | bool | Yes      | Include symbols (!@#$%^&*()_+-=[]{}|;:,.<>?)     |
| exclude_ambiguous        | bool | Yes      | Exclude ambiguous characters (l, o, I, O, 0, 1)  |

---

## 🔀 Outputs

| Name       | Type   | Description                                    |
|------------|--------|------------------------------------------------|
| true_path  | string | The generated random password                  |
| false_path | dict   | Error information if failure occurs           |

---

## 💡 Examples

### Basic Password:
```json
{
  "length": 12,
  "include_uppercase": true,
  "include_lowercase": true, 
  "include_numbers": true,
  "include_symbols": true,
  "exclude_ambiguous": false
}
```

### Output:
```json
{
  "true_path": "A7$kL9mP2@qX"
}
```

### High Security Password (no ambiguous chars):
```json
{
  "length": 16,
  "include_uppercase": true,
  "include_lowercase": true,
  "include_numbers": true, 
  "include_symbols": true,
  "exclude_ambiguous": true
}
```

### Simple Alphanumeric Password:
```json
{
  "length": 8,
  "include_uppercase": true,
  "include_lowercase": true,
  "include_numbers": true,
  "include_symbols": false,
  "exclude_ambiguous": false
}
```

---

## ⚠️ Notes

- **Minimum Requirements**: At least one character type must be selected
- **Length Validation**: Password length must be at least 1 character
- **Ambiguous Characters**: When excluded, removes l, o, I, O, 0, 1 to prevent confusion
- **Cryptographic Security**: Uses Python's `random` module for generation
- **Character Distribution**: All selected character types have equal probability

---

## 🔒 Security Features

- **Customizable Complexity**: Control exactly which character types to include
- **Ambiguity Reduction**: Option to exclude visually similar characters
- **Length Control**: Generate passwords of any required length
- **Validation**: Prevents generation with no character types selected

---

## 🎯 Use Cases

- **User Registration**: Generate temporary passwords for new accounts
- **API Keys**: Create random tokens for API authentication  
- **Security Testing**: Generate test passwords with specific requirements
- **System Administration**: Create secure passwords for system accounts
- **Development**: Generate random strings for testing authentication systems