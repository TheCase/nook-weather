Utilizes the wonderful API from
[Dark Sky](https://darksky.net/dev)!

I display this on my [rooted Nook Simple Touch](https://forum.xda-developers.com/showthread.php?t=2040351) with the help of the [ElectricSign](https://apkpure.com/electric-sign/com.sugoi.electricsign) app.  The Electric-Sign source can be found [here](https://github.com/jfriesne/Electric-Sign).

```
docker run -d -p 8080:8080 -e DARKSKY_API_KEY=<yourapikey> thecase/nook-weather
```

![screenshot](https://github.com/TheCase/nook-weather/raw/master/screenshot.png)
