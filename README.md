SNH48 Group所有能获取到的公演录播

## Requirement
```
pip install -U -r requirements.txt
```

## Usage & Updating manually
```
usage: ./stage48.py [-j JOBS]

optional arguments:
  -j JOBS, --jobs JOBS  向*.???48.com发送GET请求时的并发执行数（并发执行数越大，请求效率越高，默认值为32）
```
工作原理：执行`./stage48.py`后，首先向*.???48.com发送GET请求以获取原始HTML代码，过滤出单场公演录播的实际URL，并写入normal文件夹下的对应文件中。

本repository中的录播列表我会不定期更新，如需自行手动更新，也可通过执行上述脚本实现。
