import base64

text = "level three file"
encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
print(encoded)