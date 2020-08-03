# Component for [Home Assistant](<https://www.home-assistant.io/>)

## Data from: [LTA DataMall](<https://www.mytransport.sg/content/mytransport/home/dataMall.html>)

- accountKey can be requested from: [here](https://www.mytransport.sg/content/mytransport/home/dataMall/request-for-api.html)
- default configuration includes train disruption information
- window is the refresh window timing; if this is not provided; it will keep refreshing every MIN_TIME_BETWEEN_UPDATES (30) seconds

```yaml
LTADataMall:
  accountKey: <account-key>
  sensors:
    - name: "BakauLRT-86"
      busStopNumber: "67131"
      serviceNumber: "86"
      window:
        - startTime: "07:00"
          endTime: "23:59"
        - startTime: "07:00"
          endTime: "08:15"
    - name: "BakauLRT-119"
      busStopNumber: "67131"
      serviceNumber: "119"
      window:
        - startTime: "07:00"
          endTime: "08:15"
    - name: "BakauLRT-85"
      busStopNumber: "67131"
      serviceNumber: "85"
```
