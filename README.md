# Muse Schema Test

```
python test_prep.py <tsv_file> <tsv_scheme_file> <template_file> <output_dir>
```

Only `tsv_file` is required. Script uses schemas in directory by default.

### The process should be:

**DONE**

- upload TSV, headers of TSV must match the tsv-schema.json, 
- values from rows get captured and used to fill in payload-template.json
- payload file is generated IF all required fields are present.
- hardcoded `"files"` array gets added payload file.

**TODO**

- and the resulting JSON document must validate against cholgen_sequence.json