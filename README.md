# cloudflare-workers-httpx

This repository is a demo of an issue I'm having using httpx in a python worker.

The worker in 'simple' works.

The workers in 'mcp' and 'mcp2' fail.

## mcp
This version pulls in the 'httpx' package from the vendor build and tries to use it directly.

<pre>
    File "/session/metadata/vendor/httpx/_decoders.py", line 97, in decode
      return self.decompressor.decompress(data)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  zlib.error: Error -3 while decompressing data: incorrect header check
  
  The above exception was the direct cause of the following exception:
  
  Traceback (most recent call last):
    File "/session/metadata/entry.py", line 12, in on_fetch
      res = await client.get("https://www.example.com")
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/session/metadata/vendor/httpx/_client.py", line 1773, in get
      return await self.request(
             ^^^^^^^^^^^^^^^^^^^
    File "/session/metadata/vendor/httpx/_client.py", line 1545, in request
      return await self.send(request, auth=auth, follow_redirects=follow_redirects)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/session/metadata/vendor/httpx/_client.py", line 1648, in send
      raise exc
    File "/session/metadata/vendor/httpx/_client.py", line 1642, in send
      await response.aread()
    File "/session/metadata/vendor/httpx/_models.py", line 979, in aread
      self._content = b"".join([part async for part in self.aiter_bytes()])
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/session/metadata/vendor/httpx/_models.py", line 998, in aiter_bytes
      decoded = decoder.decode(raw_bytes)
                ^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/session/metadata/vendor/httpx/_decoders.py", line 99, in decode
      raise DecodingError(str(exc)) from exc
  httpx.DecodingError: Error -3 while decompressing data: incorrect header check
  
      at new_error (pyodide-internal:generated/emscriptenSetup:691:14)
      at wasm://wasm/0265dd42:wasm-function[300]:0x16c818
      at wasm://wasm/0265dd42:wasm-function[454]:0x17437e
      at _PyEM_TrampolineCall_JS (pyodide-internal:generated/emscriptenSetup:5226:33)
      at wasm://wasm/0265dd42:wasm-function[1096]:0x1bf539
      at wasm://wasm/0265dd42:wasm-function[3566]:0x2c1c2d
      at wasm://wasm/0265dd42:wasm-function[2129]:0x206dd5
      at wasm://wasm/0265dd42:wasm-function[1104]:0x1bfc1b
      at wasm://wasm/0265dd42:wasm-function[1107]:0x1bff2a
      at wasm://wasm/0265dd42:wasm-function[1108]:0x1bffa8
      at wasm://wasm/0265dd42:wasm-function[3372]:0x29a879
      at wasm://wasm/0265dd42:wasm-function[3373]:0x2a0fde
      at wasm://wasm/0265dd42:wasm-function[1110]:0x1c00e8
      at wasm://wasm/0265dd42:wasm-function[1105]:0x1bfd51
      at wasm://wasm/0265dd42:wasm-function[442]:0x173a25
      at Module.callPyObjectKwargs (pyodide-internal:generated/emscriptenSetup:3093:54)
      at Module.callPyObject (pyodide-internal:generated/emscriptenSetup:3130:25)
      at wrapper (pyodide-internal:generated/emscriptenSetup:1778:27)
</pre>


## mcp2
If instead we remove the built-in packages from the vendor.txt file and add what we need to requirements.txt, we get a different failure:

<pre>
    File "<string>", line 1, in <module>
  ModuleNotFoundError: No module named 'IPython'
  Error: Failed to run Python code
      at simpleRunPython (pyodide-internal:util:43:15)
      at memorySnapshotDoImports (pyodide-internal:snapshot:251:9)
      at maybeCollectSnapshot (pyodide-internal:snapshot:381:33)
      at loadPyodide (pyodide-internal:python:88:9)
      at async getPyodide (pyodide:python-entrypoint-helper:32:12)
      at async preparePython (pyodide:python-entrypoint-helper:112:25)
      at null.<anonymous> (async pyodide:python-entrypoint-helper:146:77)
      at async Object.fetch (pyodide:python-entrypoint-helper:146:28)
  Error: Failed to run Python code
      at simpleRunPython (pyodide-internal:util:43:15)
      at memorySnapshotDoImports (pyodide-internal:snapshot:251:9)
      at maybeCollectSnapshot (pyodide-internal:snapshot:381:33)
      at loadPyodide (pyodide-internal:python:88:9)
      at async getPyodide (pyodide:python-entrypoint-helper:32:12)
      at async preparePython (pyodide:python-entrypoint-helper:112:25)
      at null.<anonymous> (async pyodide:python-entrypoint-helper:146:77)
      at async Object.fetch (pyodide:python-entrypoint-helper:146:28)
</pre>

In mcp2, I've also tried the following and it still fails:
* Move the import above the lines that add vendor to path.
* Don't modify path at all i.e. comment out the lines that modify sys.path.

Just having the vendor directory seems to generate that strange error.
