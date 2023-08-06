# Let's Encrypt library for human beings

Note: The example below used the Let's Encrypt
[staging environment](https://letsencrypt.org/docs/staging-environment/).
Replace `letsencrypt.LetsEncryptStaging` with `letsencrypt.LetsEncrypt`
for production.

## Create account key

```bash
openssl genrsa -out account.key 4096
```

**WARNING: Keep the key safe!**

## Register on Let's Encrypt

```python3
with open('account.key') as f:
    account_key = f.read()
# phone, email, or both can be omitted
le = letsencrypt.LetsEncryptStaging(account_key, phone='...', email='...')
uri = le.uri
print('Please save your accound ID:')
print(uri)
```

## After you have an account

```python3
le = letsencrypt.LetsEncryptStaging(account_key, uri)
```

## Apply for some certificates!

```bash
openssl genrsa -out example.com.key 4096
```

**WARNING: Keep the key safe!**

```python3
# just an example, please use an automated function instead
def perform_dns01(domain, validation):
    print('Please add a TXT record:')
    print('domain:', domain)
    print('value:', validation)
    input('Press Enter after finished...')

with open('example.com.key') as f:
    cert_key = f.read()
with open('1.crt', 'w') as f:
    f.write(le.order(cert_key, ['example.com'], perform_dns01))
with open('2.crt', 'w') as f:
    f.write(le.order(cert_key, ['example.com', 'a.example.com'], perform_dns01))
with open('3.crt', 'w') as f:
    f.write(le.order(cert_key, ['a.b.example.com', '*.c.example.com'], perform_dns01))
```
