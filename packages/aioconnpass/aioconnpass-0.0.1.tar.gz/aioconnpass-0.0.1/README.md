# Aioconnpass
aioconnpassは、connpass APIのラッパーです。
aiohttpを使用しています。

# Installing
`pip`でインストール可能です。
```commandline
pip install aiospotipy
```

# Quick Example
```python
from aioconnpass import Connpass

connpass = Connpass()

results = await connpass.search(keyword="長野")
```