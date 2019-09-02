# Dependencies

```sh
$ sudo pip install lxml
```

# Source

```py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import subprocess

def location(ip):
    cmd = 'curl -s ip.chinaz.com/' + ip
    html = subprocess.check_output(cmd, shell = True)
    #print(html)
    domtree = etree.HTML(html)
    location = domtree.xpath(u'//*[@id="leftinfo"]/div[3]/div[2]/p[2]/span[4]/text()')
    return location[0].encode('utf-8')                                                                             
    
def main(ip):
    print(location(ip))
    
if __name__ == '__main__':
    ip = '123.138.79.10'
    main(ip)
```
