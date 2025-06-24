# HTTP Duplicator (Güncellenmiş)

Bu proje, gelen HTTP POST isteklerini iki farklı hedefe yönlendirir. Eğer ilk hedef başarılı şekilde yanıt dönerse, bu yanıt doğrudan client'a response olarak iletilir. Artık üçüncü bir hedefe yeniden POST edilmez.

## Kullanım

```bash
podman build -t http-duplicator .
podman run -d \
  -p 9401:9401 \
  -e LISTEN_PORT=9401 \
  -e TARGET1=10.49.77.153:9501 \
  -e TARGET2=10.49.77.153:9502 \
  -e LOG_DIR=/logs \
  -v /var/log/duplicator_logs/9401:/logs:Z \
  --name duplicator_9401 \
  http-duplicator
```

## Sağlık Kontrolü

```bash
curl http://localhost:9401/healthz
```

## Loglar

Loglar host sistemde `/var/log/duplicator_logs/9401/duplicator.log` dosyasına yazılır.
