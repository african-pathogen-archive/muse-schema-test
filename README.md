# Muse Schema Test

```
python check.py <tsv_file> <tsv_schema>
```

```
python fill.py <tsv_file> <template_file> <output_dir>
```

### The process should be:

**DONE**

- upload TSV, headers of TSV must match the tsv-schema.json, 
- values from rows get captured and used to fill in payload-template.json

**TODO**

- and the resulting JSON document must validate against cholgen_sequence.json