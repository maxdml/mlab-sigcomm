This repository gather some code we put up together to build Paris-traceroute measurement profiles, for the purpose of analytic.

# MLAB
http://measurementlab.net/ is a platform providing a set of network measurements tools, with the goal to make data accessible to academia and industry.
Specifially, we interact with Paris-traceroute, and enhanced version of traceroute which can handle path splits between source and destination.

# Measurement Profiles
## Raw data

They take the form:

```
traceroute [(196.216.149.76:33459) -> (35.192.37.249:60808)], protocol icmp, algo exhaustive, duration 38 s
 1  P(6, 6) 196.216.149.65 (196.216.149.65)  0.331/0.433/0.499/0.052 ms
 2  P(6, 6) 197.211.51.177 (197.211.51.177)  0.878/3.573/9.833/3.585 ms
 3  P(6, 6) 197.211.32.190 (197.211.32.190)  1.625/10.609/19.741/6.787 ms !T0
 4  P(6, 6) 197.211.32.189 (197.211.32.189)  1.998/3.606/11.188/3.391 ms
 5  P(6, 6) 72.14.242.47 (72.14.242.47)  92.894/107.898/145.630/17.673 ms
 6  P(6, 6) 72.14.242.46 (72.14.242.46)  92.355/123.860/142.789/19.246 ms
 7  P(6, 6) 108.170.246.176 (108.170.246.176)  93.764/111.128/146.691/16.905 ms
 8  P(6, 6) 209.85.143.67 (209.85.143.67)  94.846/106.785/138.649/14.480 ms
   MPLS Label 29398 TTL=1
 9  P(6, 6) 72.14.235.117 (72.14.235.117)  169.123/268.355/332.180/53.570 ms !T2
   MPLS Label 35156 TTL=1
10  P(6, 6) 209.85.252.46 (209.85.252.46)  182.241/272.409/328.521/50.641 ms !T3
   MPLS Label 34089 TTL=1
11  P(6, 6) 209.85.247.5 (209.85.247.5)  196.570/279.092/340.974/45.795 ms !T4
   MPLS Label 34148 TTL=1
12  P(6, 6) 216.239.58.143 (216.239.58.143)  194.229/279.793/347.090/48.326 ms
13  P(0, 6)
14  P(0, 6)
15  P(0, 6)
```

We parse them to augment them with Country Code and AS, and get the following JSON format per measurement (see with pretty format on http://json.parser.online.fr/):

```
{"results": {"1": {"as": "3257", "cc": "IE", "ip": "77.67.114.129", "rtts": ["0.137", "0.178", "0.233", "0.033"]}, "2": {"as": "15169", "cc": "US", "ip": "72.14.223.208", "rtts": ["0.206", "0.258", "0.303", "0.033"]}, "3": {"as": "15169", "cc": "US", "ip": "108.170.245.51", "rtts": ["0.292", "0.311", "0.337", "0.016"]}, "4": {"as": "15169", "cc": "US", "ip": "216.239.46.49", "rtts": ["8.289", "18.369", "49.319", "14.944"]}, "5": {"ip": null, "as": null, "rtts": null, "cc": null}, "6": {"as": "15169", "cc": "US", "ip": "209.85.252.77", "rtts": ["8.522", "8.602", "8.804", "0.094"]}, "7": {"ip": null, "as": null, "rtts": null, "cc": null}, "8": {"as": "15169", "cc": "GB", "ip": "216.239.50.187", "rtts": ["17.623", "17.842", "17.920", "0.102"]}, "9": {"ip": null, "as": null, "rtts": null, "cc": null}, "10": {"as": "15169", "cc": "US", "ip": "216.239.42.90", "rtts": ["96.572", "105.658", "146.991", "18.538"]}, "11": {"ip": null, "as": null, "rtts": null, "cc": null}, "12": {"as": "15169", "cc": "US", "ip": "216.239.59.0", "rtts": ["109.439", "109.570", "109.700", "0.091"]}, "13": {"ip": null, "as": null, "rtts": null, "cc": null}, "14": {"as": "15169", "cc": "US", "ip": "209.85.247.5", "rtts": ["118.963", "119.068", "119.160", "0.066"]}, "15": {"ip": null, "as": null, "rtts": null, "cc": null}, "16": {"as": "15169", "cc": "US", "ip": "72.14.233.183", "rtts": ["119.305", "119.441", "119.613", "0.107"]}, "17": {"as": "15169", "cc": "US", "ip": "216.239.62.77", "rtts": ["120.252", "120.392", "120.719", "0.159"]}, "18": {"ip": null, "as": null, "rtts": null, "cc": null}, "19": {"ip": null, "as": null, "rtts": null, "cc": null}, "20": {"ip": null, "as": null, "rtts": null, "cc": null}, "21": {"ip": null, "as": null, "rtts": null, "cc": null}}, "srcIP": "77.67.114.153", "dstIP": "35.192.37.249", "srcAS": "3257", "dstAS": "15169"}
```

The parser operates as follow: #TODO (GeoLite DB, raw data path format and how to DL them, CAIDA files)

## Profiles
To enable basic statistical analysis on measurement data, we build an abstraction for individual measurements. The API looks as follow:

### MeasurementProfile
This class represent an entire Paris-traceroute measurement. We extend the base information (source and destination IPs, RTTs), by the source and
destination AS. Each instance includes a list of Hops objects, and global timing information (e.g. last RTT).

### Hops
This class represent an individual hop in a measurement. We extend the base information to include the country code of the destination IP, as well as
its AS.
