Задача

Пройти по списку блокировок и проверить:
* все ли ресурсы блокирует ваш провайдер;
* а блокируются ли доменные имена, на которых расположены ресурсы.

Список заблокированных сайтов качаем здесь:
```
git clone --depth=1 https://github.com/zapret-info/z-i
```

Структура файла
```
94.23.171.210;watch.hentaistream.com;https://watch.hentaistream.com/boku-no-pico-episode-01;������������;850973-URL-on;2019-11-27
94.23.171.210;watch.hentaistream.com;https://watch.hentaistream.com/boku-no-pico-episode-02;������������;851885-URL-on;2019-11-28
94.23.171.210;watch.hentaistream.com;https://watch.hentaistream.com/boku-no-pico-episode-03;������������;851884-URL-on;2019-11-28
```
где
0. 94.23.171.210 - IP адреса (не блокируется?!)
1. watch.hentaistream.com - доменное имя (не блокируется?!)
2. https://watch.hentaistream.com/boku-no-pico-episode-01 - ресурс (блокируется)
3. организация
4. номер решения
5. дата решения о блокировке

Ожидаемое поведение при блокировке:

Возвращается статус 302 Found — запрошенный документ временно доступен по другому URI, указанному в заголовке в поле Location.
Поле Location содержит ссылку на warning.rt.ru.

```
curl -v http://wb.kinopara.online/938-idealnaja-njanja-2020.html
*   Trying 172.67.170.107:80...
* TCP_NODELAY set
* Connected to wb.kinopara.online (172.67.170.107) port 80 (#0)
> GET /938-idealnaja-njanja-2020.html HTTP/1.1
> Host: wb.kinopara.online
> User-Agent: curl/7.68.0
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 302 Found
< Connection: close
< Content-Length: 2
< Location: http://warning.rt.ru/?id=21&st=0&dt=172.67.170.107&rs=http%3A%2F%2Fwb.kinopara.online%2F938-idealnaja-njanja-2020.html
```

Ожидаемое поведение, если сайт просто переехал:

Возвращает статус 301 Moved Permanently

```
$ curl -v watch.hentaistream.com
*   Trying 94.23.171.210:80...
* TCP_NODELAY set
* Connected to watch.hentaistream.com (94.23.171.210) port 80 (#0)
> GET / HTTP/1.1
> Host: watch.hentaistream.com
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 301 Moved Permanently
< Date: Tue, 30 Mar 2021 15:32:30 GMT
< Server: Apache
< Location: https://tube.hentaistream.com/
< Vary: Accept-Encoding
< Content-Length: 238
< Content-Type: text/html; charset=iso-8859-1
< 
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>301 Moved Permanently</title>
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="https://tube.hentaistream.com/">here</a>.</p>
</body></html>
* Connection #0 to host watch.hentaistream.com left intact
```

Асинхронная реализация на Python

Установить зависимости можно командами:
```
$ sudo apt install python3-pip
$ sudo pip3 install -r requirements.txt
```

Asynchronous HTTP Client/Server for asyncio and Python
https://docs.aiohttp.org/en/stable/

