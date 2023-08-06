<!--
https://pypi.org/project/readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install gitmsg
```

#### CLI
```bash
usage: gitmsg
```

#### Examples
```bash
$ cd /path/to/repo/
$ touch new_file
$ rm deleted_file
$ echo "new" > modified_file
$ git add -A
$ gitmsg
'+new_file; -deleted_file; ^modified_file'
```

<p align="center">
    <a href="https://pypi.org/project/readme-generator/">readme-generator</a>
</p>