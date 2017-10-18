# Easier Alembic exporting.

## Usage

This module extends the functionality of Maya's "AbcExport" command, to alleviate tedious string formatting and work easier with mayapy.

To install, download [alembic_export.py](https://raw.githubusercontent.com/tokejepsen/maya-alembic-export/master/alembic_export.py) and place it in a directory where Maya can find it.

## Examples

```python
import alembic_export

alembic_export.export("/output/path/for/alembicFile.abc")
```

Alembic export with Mayapy
```bash
$ "path/to/mayapy" "path/to/alembic_export.py" -mayaFile "path/to/mayaFile.mb" -alembicFile "/output/path/for/alembicFile.abc"
```
