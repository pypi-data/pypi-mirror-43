# pyyaml-include

[![CircleCI](https://img.shields.io/circleci/project/github/tanbro/pyyaml-include.svg)](https://circleci.com/gh/tanbro/workflows/pyyaml-include)
[![Documentation Status](https://readthedocs.org/projects/pyyaml-include/badge/?version=stable)](https://pyyaml-include.readthedocs.io/en/stable/?badge=stable)
[![GitHub tag](https://img.shields.io/github/tag/tanbro/pyyaml-include.svg)](https://github.com/tanbro/pyyaml-include)
[![PyPI](https://img.shields.io/pypi/v/pyyaml-include.svg)](https://pypi.org/project/pyyaml-include/)
[![PyPI - License](https://img.shields.io/pypi/l/pyyaml-include.svg)](https://pypi.org/project/pyyaml-include/)
[![PyPI - Format](https://img.shields.io/pypi/format/pyyaml-include.svg)](https://pypi.org/project/pyyaml-include/)
[![PyPI - Status](https://img.shields.io/pypi/status/pyyaml-include.svg)](https://pypi.org/project/pyyaml-include/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyyaml-include.svg)](https://pypi.org/project/pyyaml-include/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pyyaml-include.svg)](https://pypi.org/project/pyyaml-include/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c6c77ccafa6f4f9096a713480902ab34)](https://www.codacy.com/app/tanbro/pyyaml-include?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tanbro/pyyaml-include&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c6c77ccafa6f4f9096a713480902ab34)](https://www.codacy.com/app/tanbro/pyyaml-include?utm_source=github.com&utm_medium=referral&utm_content=tanbro/pyyaml-include&utm_campaign=Badge_Coverage)

An extending constructor of [PyYAML][], which including [YAML][] files within [YAML][] files.

## Install

```sh
pip install pyyaml-include
```

## Usage

Consider we have such [YAML] files:

    ├── 0.yaml
    └── include.d
        ├── 1.yaml
        └── 2.yaml

- `1.yaml` 's content:

  ```yaml
  name: "1"
  ```

- `2.yaml` 's content:

  ```yaml
  name: "2"
  ```

To include `1.yaml`, `2.yaml` in `0.yaml`, we shall first add `YamlIncludeConstructor` to [PyYAML]'s loader, then write `!include` tag in `0.yaml` and load it:

```python
import yaml
from yamlinclude import YamlIncludeConstructor

YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir='/your/conf/dir')

with open('0.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

print(data)
```

### Include files by name

- On top level:

  If `0.yaml` was:

  ```yaml
  !include include.d/1.yaml
  ```

  We'll get:

  ```json
  {"name": "1"}
  ```

- In mapping:
  
  If `0.yaml` was:

  ```yaml
  file1: !include include.d/1.yaml
  file2: !include include.d/2.yaml
  ```

  We'll get:

  ```yaml
    file1:
      name: "1"
    file2:
      name: "2"
  ```

- In sequence:
  
  If `0.yaml` was:

  ```yaml
  files:
    - !include include.d/1.yaml
    - !include include.d/2.yaml
  ```

  We'll get:

  ```yaml
  files:
    - name: "1"
    - name: "2"
  ```

> ℹ **Note**:
>
> File name can be either absolute (like `/usr/conf/1.5/Make.yml`) or relative (like `../../cfg/img.yml`).

### Include files by wildcards

File name can contain shell-style wildcards. Data loaded from the file(s) found by wildcards will be set in a sequence.

If `0.yaml` was:

```yaml
files: !include include.d/*.yaml
```

We'll get:

```yaml
files:
  - name: "1"
  - name: "2"
```

> ℹ **Note**:
>
> - For `Python>=3.5`, if `recursive` argument of `!include` [YAML] tag is `true`, the pattern `“**”` will match any files and zero or more directories and subdirectories.
> - Using the `“**”` pattern in large directory trees may consume an inordinate amount of time because of recursive search.

In order to enable `recursive` argument, we shall write the `!include` tag in `Mapping` or `Sequence` mode:

- Arguments in `Sequence` mode:

  ```yaml
  !include [tests/data/include.d/**/*.yaml, true]
  ```

- Arguments in `Mapping` mode:

  ```yaml
  !include {pathname: tests/data/include.d/**/*.yaml, recursive: true}
  ```

[YAML]: http://yaml.org/
[PyYaml]: https://pypi.org/project/PyYAML/
