<!--
https://pypi.org/project/readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/github-description.svg?longCache=True)](https://pypi.org/project/github-description/)

#### Installation
```bash
$ [sudo] pip install github-description
```

#### Config
bash|python
-|-
`export GITHUB_TOKEN="your_github_token"`|`os.environ["GITHUB_TOKEN"]="your_github_token"`

#### Functions
function|`__doc__`
-|-
`github_description.get(fullname)` |return repo description
`github_description.update(fullname, description)` |update repo description

#### CLI
usage|`__doc__`
-|-
`python -m github_description fullname [description]` |get/set repo description

#### Examples
```bash
$ python -m github_description repo "new desc"
$ python -m github_description repo
new desc
```

<p align="center">
    <a href="https://pypi.org/project/readme-generator/">readme-generator</a>
</p>