# 囲みマス Python Core

リアルタイム陣地取りゲーム「[囲みマス](https://kakomimasu.com)」に使用されているコアライブラリ「[Kakomimasu](https://github.com/codeforkosen/Kakomimasu)」をPython版に移植したものです。

## インストール方法

```console
pip install kakomimasu-py
```

## 使用方法

```console
$ python main.py
```

## for Developers

```
# build
$ python -m build

# upload(testpypi)
$ python -m twine upload --repository testpypi dist/*
## username: __token__
## password: {API Token}

# upload(pypi)
$ python -m twine upload --repository pypi dist/*
## username: __token__
## password: {API Token}
```