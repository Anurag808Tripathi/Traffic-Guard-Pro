import sys
from geopy.geocoders import Nominatim
import dpkt
import socket
import webbrowser

# Dictionaries for IP addresses and their corresponding lat-long positions
source_ip_positions = {}
destination_ip_positions = {}

# Blacklisted IP addresses
black_listed_ip = ['217.168.1.2', '192.37.115.0', '212.242.33.35', '147.137.21.94']

# Authorized users
auth_users = {"root": "root", "jack": "jack"}

# Function for generating information from IP addresses using GeoLiteCity database
def geoip_city(ip_address):
    if ip_address in black_listed_ip:
        try:
            geolocator = Nominatim(user_agent="geoip")
            location = geolocator.reverse(ip_address, language="en")
            address = location.address.split(', ')
            city, region, country = address[-4], address[-3], address[-1]
            latitude, longitude = location.latitude, location.longitude

            print(f'\n[*] Target: {ip_address} Geo Located.')
            print(f'[+] City: {city}, Region: {region}, Country: {country}')
            print(f'[+] Latitude: {latitude}, Longitude: {longitude}\n')

        except:
            print("\n********** IP Unregistered **********")
    else:
        pass

# Function for generating latitudes and longitudes for source IP addresses
def kml_geoip_city(ip_address):
    if ip_address in black_listed_ip:
        try:
            geolocator = Nominatim(user_agent="geoip")
            location = geolocator.geocode(ip_address)
            latitude, longitude = location.latitude, location.longitude
            source_ip_positions[str(ip_address)] = f'{latitude},{longitude}'
        except:
            pass
    else:
        pass

# Function for generating latitudes and longitudes for destination IP addresses
def kml_dest_geoip_city(ip_address):
    if ip_address in black_listed_ip:
        try:
            geolocator = Nominatim(user_agent="geoip")
            location = geolocator.geocode(ip_address)
            latitude, longitude = location.latitude, location.longitude
            destination_ip_positions[str(ip_address)] = f'{latitude},{longitude}'
        except:
            pass
    else:
        pass

# Function for printing information related to a particular IP address from a pcap
def printpcap(pcap):
    for (timestamp, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src_ip = socket.inet_ntoa(ip.src)
            dst_ip = socket.inet_ntoa(ip.dst)

            if src_ip in black_listed_ip:
                print("\n-------------------------------------------------------------------------------------------------")
                print(f'[+] Source IP: {src_ip} -------> Destination IP: {dst_ip}')
                print("Source IP Information:")
                geoip_city(str(src_ip))

            elif dst_ip in black_listed_ip:
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-")
                print("Destination IP Information:")
                geoip_city(str(dst_ip))
                print("--------------------------------------------------------------------------------------------------")

            else:
                pass

        except:
            pass

# Function for generating KML format of the data for source IP addresses
def print_placemarks_in_kml(ip_positions):
    for ip, position in ip_positions.items():
        print(f"""
  <Placemark>
    <name> SOURCE IP Address: {ip}</name>
    <styleUrl>#exampleStyleDocument</styleUrl>
    <Point>
      <coordinates>{position}</coordinates>
    </Point>
  </Placemark>
""")

# Function for generating KML format of the data for destination IP addresses
def print_dest_placemarks_in_kml(ip_positions):
    for ip, position in ip_positions.items():
        print(f"""
  <Placemark>
    <name> DESTINATION IP Address: {ip}</name>
    <styleUrl>#exampleStyleDocument</styleUrl>
    <Point>
      <coordinates>{position}</coordinates>
    </Point>
  </Placemark>
""")

# Function for viewing data on Google Maps
def view_google(pcap):
    for (timestamp, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src_ip = socket.inet_ntoa(ip.src)
            dst_ip = socket.inet_ntoa(ip.dst)
            kml_geoip_city(str(src_ip))
            kml_dest_geoip_city(str(dst_ip))

        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("\n -------------------- Please enter the required arguments------------------------- ")
        print("\n Correct syntax is: <FileName>.py username password cli/kml\n")
        print("\ncli - stands for Command Line Output")
        print("\nkml - stands for a KML output which is required for visualization using a Google Map")
    else:
        try:
            if sys.argv[1] in auth_users:
                try:
                    if sys.argv[2] == auth_users[sys.argv[1]]:
                        try:
                            if sys.argv[3] == "cli":
                                with open('/home/soumil/Downloads/fuzz-2006-06-26-2594.pcap', 'rb') as f:
                                    pcap = dpkt.pcap.Reader(f)
                                    printpcap(pcap)
                                sys.exit(1)

                            elif sys.argv[3] == "kml":
                                print("""
                            <?xml version="1.0" encoding="UTF-8"?>
                            <kml xmlns="http://www.opengis.net/kml/2.2">
                            <Document>
                              <name>sourceip.kml</name>
                              <open>1</open>
                              <Style id="exampleStyleDocument">
                                <LabelStyle>
                                  <color>ff0000cc</color>
                                </LabelStyle>
                              </Style>
                                """)
                                with open('/home/soumil/Downloads/fuzz-2006-06-26-2594.pcap', 'rb') as f:
                                    pcap = dpkt.pcap.Reader(f)
                                    view_google(pcap)
                                print_dest_placemarks_in_kml(destination_ip_positions)
                                print_placemarks_in_kml(source_ip_positions)
                                print("""
                            </Document>
                            </kml>
                            """)
                                new = 1
                                url = "https://www.google.com/maps/d/splash?app=mp"
                                webbrowser.open(url, new=new)

                            else:
                                raise Exception

                        except:
                            print("\nYou Entered a wrong option. Or maybe your Syntax is wrong")
                            print("\n Correct syntax is: <FileName>.py username password cli/kml\n")
                            print("\ncli - stands for Command Line Output")
                            print("\nkml - stands for a KML output which is required for visualization using a Google Map")
                    else:
                        raise Exception

                except:
                    print("\n The PASSWORD you entered is NOT CORRECT !!!!!! ")
                    print("\n Correct syntax is: <FileName>.py username password cli/kml\n")
                    print("\ncli - stands for Command Line Output")
                    print("\nkml - stands for a KML output which is required for visualization using a Google Map")

            else:
                raise Exception

        except:
            print("\n Sorry %s. You are NOT AUTHORIZED to use this tool!!!!!!!!!!!" % str(sys.argv[1]))
            print("\n Correct syntax is: <FileName>.py username password cli/kml\n")
            print("\ncli - stands for Command Line Output")
            print("\nkml - stands for a KML output which is required for visualization using a Google Map")
