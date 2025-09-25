import base64

text = "hello world"
encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
print(encoded)