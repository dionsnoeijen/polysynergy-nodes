# Contains In List Node

De **Contains In List** node controleert of een opgegeven waarde voorkomt in een lijst. Deze lijst kan bestaan uit simpele waardes of dictionaries. In het geval van dictionaries kan gezocht worden op een specifieke key.

## 🧩 Node-specificaties

- **Naam:** Contains In List
- **Categorie:** list
- **Type:** util
- **Icoon:** list.svg

## 🛠️ Invoervelden

| Naam         | Type   | Vereist | Omschrijving |
|--------------|--------|---------|---------------|
| `input_list`   | `list` | ✅       | De lijst waarin gezocht wordt. |
| `match_value`  | `any`  | ✅       | De waarde die gezocht wordt. |
| `key`          | `str`  | ❌       | Optioneel: de key waarop gezocht wordt wanneer de lijst uit dictionaries bestaat. |

## 📤 Uitgangen

| Naam         | Type         | Omschrijving |
|--------------|--------------|--------------|
| `true_path`  | `bool`       | `True` als een match is gevonden, `False` als niet. |
| `false_path` | `dict`       | Een foutmelding indien geen match gevonden is of input ongeldig is. |

## ✅ Voorbeelden

### Eenvoudige lijst

```json
{
  "input_list": ["apple", "banana", "cherry"],
  "match_value": "banana"
}
```

➡️ `true_path = True`

### Dictionary lijst met key

```json
{
  "input_list": [{"id": 1}, {"id": 2}, {"id": 3}],
  "match_value": 2,
  "key": "id"
}
```

➡️ `true_path = True`

### Geen match

```json
{
  "input_list": ["a", "b", "c"],
  "match_value": "x"
}
```

➡️ `false_path = { "error": "Value not found" }`

## ⚠️ Let op

- Vergelijking gebeurt als `str(value) == str(match_value)` om consistent gedrag te garanderen, ongeacht het type.
- Wanneer `key` is opgegeven maar een item in de lijst is geen dictionary, dan wordt dat item overgeslagen.
- Als `input_list` geen lijst is, wordt een foutmelding teruggegeven via `false_path`.

## 🧪 Testen

Deze node wordt gedekt door unit tests in:

```
nodes/nodes/list/tests/test_contains_list.py
```
