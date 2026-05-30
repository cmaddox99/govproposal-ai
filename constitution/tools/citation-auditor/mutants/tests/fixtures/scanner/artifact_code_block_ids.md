---
title: Code Block Artifact
---

Outside code block: ENG-4.1 should be found.

```python
# Inside fenced block: ENG-6.1 should NOT be found
x = "PRD-2.6"  # also NOT found
```

After block: BUS-7.1 should be found.

~~~
ENG-2.1 inside tilde fence — NOT found
~~~

After tilde block: ENG-3.4 should be found.
