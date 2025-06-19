# HTTP Duplicator

Bu proje, gelen HTTP POST isteklerini belirlenen hedef sunuculara yönlendiren bir Flask tabanlı uygulamadır. İlk hedeften gelen başarılı yanıt isteğe bağlı olarak başka bir adrese de yönlendirilir.

## Özellikler

- Çoklu hedeflere veri iletme
- Yanıta göre üçüncü hedefe yönlendirme
- `/healthz` endpoint'i ile sağlık kontrolü
- Dışa log yazımı (container dışı)

## Kurulum

1. Docker image oluşturun:

```bash
docker build -t http-duplicator .
```

2. Docker Compose ile başlatın:

```bash
docker-compose up -d
```

## Parametreler

- `LISTEN_PORT`: Container içi dinlenecek port
- `TARGET1`, `TARGET2`: Hedef sunucular
- `FORWARD_IF_RESP_TARGET`: İlk hedef başarılıysa yönlendirilecek adres
- `LOG_DIR`: Logların yazılacağı dizin (host sistemden bağlanır)

## Sağlık Kontrolü

```bash
curl http://localhost:9401/healthz
```

## Loglar

Container dışındaki dizine yazılır: `/var/log/duplicator_logs/<port>`
