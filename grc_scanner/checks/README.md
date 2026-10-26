# Check inventory

`observed_check_catalog.json` inventories check IDs referenced by scanner code and
the control mappings in `frameworks/frameworks.json`. It is not a set of complete
check definitions: descriptions, validation logic, fixtures, and verified control
crosswalks still need to be authored and reviewed.

`scanner_coverage_matrix.json` records the prompt's expected counts, the observed
scanner references, and whether each scanner category currently has active,
partial, or unavailable implementation coverage. Some source references belong
to legacy methods and do not imply that a check runs in the current scan path.

Regenerate both JSON files after scanner or mapping changes:

```powershell
python scripts/build_check_catalog.py
```

Current inventory: 234 IDs in the union of code references and mapping keys,
229 code-referenced IDs, 112 mapped IDs, and 122 code-referenced IDs without
mappings. Five mapping entries are not referenced in scanner source.
The prompt's category table sums to 625, while its detailed SSL/header/network
file ranges sum to 605. The matrix preserves both counts so they can be resolved
before checks are authored.
