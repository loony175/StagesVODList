SNH48 Group所有能获取到的公演录播

## Requirement
```
sudo apt update && sudo apt install -y parallel
parallel --bibtex
```

## Usage & Updating manually
```
usage: ./bash/stage48 [-j JOBS]

optional arguments:
  -j JOBS, --job JOBS  向*.???48.com发送GET请求时的并发数（并发
                       数越大，请求效率越高，默认值为CPU逻辑核心
                       总数的4倍）
```
工作原理：执行`./bash/stage48`后，首先向*.???48.com发送GET请求以获取原始HTML代码，过滤出单场公演录播的实际URL，并写入normal文件夹下的对应文件中。

本repository中的录播列表我会不定期更新，如需自行手动更新，也可通过执行上述脚本实现。
