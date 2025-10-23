# Chunk/Batch List Node

The **Chunk/Batch List** node divides a list into smaller chunks (batches) of a specified size. Useful for processing large lists in smaller groups.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  The list to divide into chunks.

- **chunk_size** (`int`, required):
  Number of items per chunk. Default: `10`.

---

### Outputs

- **chunked_list** (`list`):
  A list of chunks (list of lists).

- **chunk_count** (`int`):
  Number of chunks created.

- **original_length** (`int`):
  Length of the original list.

- **true_path** (path):
  Triggered on success. Returns the list of chunks.

- **false_path** (path):
  Triggered if chunking fails. Returns error info.

---

## 🧠 Example Use

### Divide into Chunks of 3

```json
{
  "input_list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "chunk_size": 3
}
```

**Output (`true_path`):**
```json
[
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
  [10]
]
```

---

### Batch Processing Use Case

```json
{
  "input_list": ["user1", "user2", "user3", "user4", "user5"],
  "chunk_size": 2
}
```

**Output (`true_path`):**
```json
[
  ["user1", "user2"],
  ["user3", "user4"],
  ["user5"]
]
```

This allows processing users in batches of 2, with the last batch containing the remainder.

---

## ⚠️ Notes

- The last chunk may contain fewer items than `chunk_size` if the list length is not evenly divisible.
- Empty lists return an empty list of chunks.
- `chunk_size` must be greater than 0.

---

## 🧩 Category

- `list`
