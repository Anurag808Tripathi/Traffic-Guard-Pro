Traffic Guard Pro - Network Traffic Analyzer

1. Project Description
   Objective: Analyze captured packets to identify users downloading software from blacklisted/illegal websites. The project focuses on analyzing source and destination IP addresses, monitoring user packet traversal, and determining user locations. It includes the creation of a secure database storing geographical locations and packet details for future use.

Traffic Guard Pro
![Traffic Guard Pro](https://user-images.githubusercontent.com/22990797/124121209-7700fd80-da29-11eb-973a-2bc29969715b.PNG)

Application Workflow:

The admin monitors user activities and detects illegal downloads.
PyGeoIP correlates IP addresses to physical locations using the GeoLite City database.
The database returns records containing city, region name, postal code, country name, latitude, and longitude.
The information is plotted on Google Earth for visual representation.
The encrypted database stores URL, destination IP, timestamp, latitude, and longitude.
The stored data facilitates future analysis and the creation of statistics to enhance security. 2. Technologies and Tools
Analyzer: Developed using Python 2.7
Database: MySQL (Stores information in encrypted format)
GeoLite City Database: Provides visual location using Google Earth
PyGeoLite: Correlates IP addresses to physical locations (Retrieves latitude, longitude, and region)
Packet Capture: Wireshark (Captures pcap files)
Security Tool: Ettercap (Used for security auditing and network protocol analysis)
API: Google Earth API (Displays geographical location of the packet's destination) 3. Implementation
Packet Capture:

Use Wireshark to capture packets, both from stored pcap files and live packets using Ettercap.
Packet Analysis:

Utilize Dpkt, a Python module, for parsing packets. It analyzes each packet, providing the IP address of users downloading from blacklisted sites.
Geographical Location:

Use PyGeoIP to query the GeoLiteCity database, obtaining the geographical location of the packet.
Visualization:

Display the geographical location on Google Earth using the Google Earth API in KML format.
Database Storage:

Store all packet information, including source and destination IP, timestamp, URL, and geographical details, in the encrypted MySQL database.
Security Measures:

Encrypt all information stored in the database to enhance the overall security of the system.
This comprehensive Traffic Guard Pro project integrates Python, MySQL, GeoLite City Database, and Google Earth API for effective network traffic analysis. It emphasizes security through encryption and provides valuable insights for future analysis and security enhancements.
