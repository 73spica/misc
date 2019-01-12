# pypingがpython3で使えない時の対処
## TL;DR
ここにある`__init__.py` と`core.py` が修正済みのものなのでそれをパッケージ内のものと交換すれば動くはず．

## 現象
pip3でインストールしたpypingが動作しない．

## 環境
- MacBook Pro macOS Mojave
- pip18.1
- python3.6.5

## 調査&原因
どうやらpip3でインストールできるが，それがpython3用に作られたpypingであるわけでは無いらしい．
他にもいろいろ出てくる．

- `https://stackoverflow.com/questions/35330964/unable-to-import-pyping-for-python3`


## 対処
原因はいくつかあるが，致命的なものはなくほぼ全てsyntaxの問題なのでpython2 to python3の変換でうまくいく．
探せばpython3に対応したものが転がっていそうだけど今回はコードを修正する形で対処した．

### \_\_init\_\_.pyのfrom core import \* をfrom .core import \* に変える
```
$ python3 ping.py
Traceback (most recent call last):
  File "ping.py", line 1, in <module>
    import pyping
  File "/usr/local/lib/python3.6/site-packages/pyping/__init__.py", line 3, in <module>
    from core import *
ModuleNotFoundError: No module named 'core'
```
python3では同一ディレクトリのモジュールを指す時にピリオドが必要．

### インデントをよしなに変える
```
$ python3 ping.py
Traceback (most recent call last):
  File "ping.py", line 1, in <module>
    import pyping
  File "/usr/local/lib/python3.6/site-packages/pyping/__init__.py", line 3, in <module>
    from .core import *
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 179
    msg = "%d bytes from %s: icmp_seq=%d ttl=%d time=%.1f ms" % (packet_size, from_info, icmp_header["seq_number"], ip_header["ttl"], delay)
                                                                                                                                           ^
```
これは僕の環境だけかもしれないけどインデントがおかしいところがあるのでよしなに変える．

### 例外処理，例外送出の記述のpython3化
```
$ python3 ping.py
Traceback (most recent call last):
  File "ping.py", line 1, in <module>
    import pyping
  File "/usr/local/lib/python3.6/site-packages/pyping/__init__.py", line 3, in <module>
    from .core import *
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 170
    raise Exception, "unknown_host"
                   ^
SyntaxError: invalid syntax
```
これは以下のように変える．
```
raise Exception, "unknown_host"
↓
raise Exception("unknown_host")
```
---
```
$ python3 ping.py
Traceback (most recent call last):
  File "ping.py", line 1, in <module>
    import pyping
  File "/usr/local/lib/python3.6/site-packages/pyping/__init__.py", line 3, in <module>
    from .core import *
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 304
    except socket.error, (errno, msg):
                       ^
SyntaxError: invalid syntax
```
これは以下のように変える．

```
except socket.error, (errno, msg):
↓
except socket.error as e:
    errno, msg = e.args
```
---
```
$ python3 ping.py
Traceback (most recent call last):
  File "ping.py", line 1, in <module>
    import pyping
  File "/usr/local/lib/python3.6/site-packages/pyping/__init__.py", line 3, in <module>
    from .core import *
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 311
    raise etype, evalue, etb
               ^
SyntaxError: invalid syntax
```
これは以下のように変える．
```
raise etype, evalue, etb
↓
raise etype(evalue).with_traceback(etb)
```
---

これらの変更は以下を参考にした．
- https://stackoverflow.com/questions/7775062/porting-python-2-program-to-python-3-random-line-generator
- http://docs.python.org/library/2to3.html


### ord()がいらないので外す
ここからsudoがいることを思い出してsudoがつくけど修正とは一切関係ない．
```
$ sudo python3 ping.py
Traceback (most recent call last):
  File "ping.py", line 5, in <module>
    RPing = pyping.ping(host)
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 425, in ping
    return p.run(count)
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 271, in run
    delay = self.do()
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 315, in do
    send_time = self.send_one_ping(current_socket)
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 356, in send_one_ping
    checksum = calculate_checksum(header + data) # Checksum is in network order
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 64, in calculate_checksum
    sum = sum + (ord(hiByte) * 256 + ord(loByte))
TypeError: ord() expected string of length 1, but int found
```

```
$ sudo python3 ping.py
Traceback (most recent call last):
  File "ping.py", line 5, in <module>
    RPing = pyping.ping(host)
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 426, in ping
    return p.run(count)
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 272, in run
    delay = self.do()
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 316, in do
    send_time = self.send_one_ping(current_socket)
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 357, in send_one_ping
    checksum = calculate_checksum(header + data) # Checksum is in network order
  File "/usr/local/lib/python3.6/site-packages/pyping/core.py", line 72, in calculate_checksum
    sum += ord(loByte)
TypeError: ord() expected string of length 1, but int found
```

## 結果
できた．
```
$ sudo python3 ping.py
ADD:ftp.tsukuba.wide.ad.jp
AIP:203.178.132.80
MAX:8.362ms
MIN:7.455ms
AVG:7.940ms
```
