import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import platform
import time
import requests

def scan_networks():
    """
    Scans WiFi networks available on the system.
    Uses `nmcli` on Linux and `netsh` on Windows.
    """
    os_type = platform.system()
    
    if os_type == "Linux":
        scan_result = subprocess.run(
            ['nmcli', '-t', '-f', 'SSID,SIGNAL,CHAN,BSSID,SECURITY', 'device', 'wifi', 'list'], 
            capture_output=True, text=True
        )
        networks = scan_result.stdout.strip().split('\n')
        
        network_data = []
        for net in networks:
            fields = net.split(":")
            if len(fields) >= 5:
                network_data.append({
                    'SSID': fields[0],
                    'Signal': int(fields[1]),
                    'Channel': fields[2],
                    'BSSID': fields[3],
                    'Security': fields[4]
                })

    elif os_type == "Windows":
        scan_result = subprocess.run(
            ['netsh', 'wlan', 'show', 'network', 'mode=Bssid'], 
            capture_output=True, text=True, shell=True
        )
        output = scan_result.stdout.strip().splitlines()
        
        network_data = []
        current_network = {}
        
        for line in output:
            line = line.strip()
            if line.startswith("SSID") and not line.startswith("SSID BSSID"):
                if current_network:  
                    network_data.append(current_network)
                current_network = {
                    'SSID': line.split(":")[1].strip(),
                    'Signal': None,
                    'Channel': None,
                    'BSSID': None,
                    'Security': None
                }
            elif "Signal" in line:
                current_network['Signal'] = int(line.split(":")[1].strip().replace("%", ""))
            elif "Channel" in line:
                current_network['Channel'] = line.split(":")[1].strip()
            elif line.startswith("BSSID"):
                bssid_parts = line.split(":")[1:]
                current_network['BSSID'] = ":".join(part.strip() for part in bssid_parts if len(part.strip()) == 2)
            elif "Authentication" in line:
                current_network['Security'] = line.split(":")[1].strip()
        
        if current_network:
            network_data.append(current_network)

    else:
        raise NotImplementedError("This script only supports Linux and Windows operating systems.")
    
    return pd.DataFrame(network_data)


def plot_signal_strength(df):
    plt.figure(figsize=(10, 6))
    plt.bar(df['SSID'], df['Signal'], color='skyblue')
    plt.xlabel("Network (SSID)")
    plt.ylabel("Signal Strength (%)")
    plt.title("WiFi Network Signal Strength")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def track_signal_strength(target_ssid, duration=30):
    signal_strengths = []
    times = []

    start_time = time.time()
    while (time.time() - start_time) < duration:
        df = scan_networks()
        target_network = df[df['SSID'] == target_ssid]
        
        if not target_network.empty:
            signal_strength = target_network.iloc[0]['Signal']
            signal_strengths.append(signal_strength)
            times.append(time.time() - start_time)
            print(f"Time: {times[-1]:.2f}s - Signal: {signal_strength} %")
        else:
            print(f"Network {target_ssid} not found.")

        time.sleep(1)

    plt.figure(figsize=(10, 6))
    plt.plot(times, signal_strengths, marker='o', linestyle='-')
    plt.xlabel("Time (s)")
    plt.ylabel("Signal Strength (%)")
    plt.title(f"Signal Strength Over Time for {target_ssid}")
    plt.show()

    
    if signal_strengths:
        print(f"\nSignal Stability Analysis for {target_ssid}:")
        print(f"  - Average Signal Strength: {sum(signal_strengths) / len(signal_strengths):.2f} %")
        print(f"  - Minimum Signal Strength: {min(signal_strengths)} %")
        print(f"  - Maximum Signal Strength: {max(signal_strengths)} %")


def analyze_channels(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df['Channel'].astype(int), bins=range(1, 15), edgecolor="black", align='left')
    plt.xlabel("Channel")
    plt.ylabel("Number of Networks")
    plt.title("Channel Distribution (Potential Interference)")
    plt.xticks(range(1, 14))
    plt.show()


def summarize_security_levels(df):
    security_counts = df['Security'].value_counts()
    print("\nSecurity Summary:")
    for sec_type, count in security_counts.items():
        print(f"{sec_type}: {count} networks")
    insecure_networks = df[df['Security'].str.contains("None", case=False)]
    print(f"\nInsecure Networks (Open): {len(insecure_networks)}")
    print(insecure_networks[['SSID', 'BSSID', 'Channel']])
    

def determine_frequency_band(df):
    """
    Adds a 'Frequency Band' column to the DataFrame based on channel numbers.
    """
    df['Frequency Band'] = df['Channel'].astype(int).apply(
        lambda x: '2.4GHz' if x <= 14 else '5GHz'
    )
    print("\nFrequency Band Distribution:")
    print(df['Frequency Band'].value_counts())
    return df


def lookup_mac_manufacturer(bssid):
    """
    Looks up the manufacturer of a device based on its MAC address prefix.
    """
    mac_prefix = bssid[:8].replace(":", "-").upper()
    try:
        response = requests.get(f"https://macvendors.co/api/{mac_prefix}/json")
        
        if response.status_code == 200:
            data = response.json()
            manufacturer = data.get("result", {}).get("company", "Unknown")
            print(f"BSSID {bssid} Manufacturer: {manufacturer}")
        else:
            print(f"Failed to retrieve manufacturer for BSSID {bssid} (Status code: {response.status_code})")
    
    except Exception as e:
        print(f"Error retrieving MAC manufacturer: {e}")



def save_analysis_report(df, filename="pulsepilot_report.csv"):
    """
    Saves the analysis results to a CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"\nAnalysis report saved as {filename}")


def select_target_ssid(df):
    print("\nAvailable Networks:")
    for i, ssid in enumerate(df['SSID']):
        print(f"{i + 1}: {ssid}")
    choice = int(input("\nEnter the number of the network to analyze: ")) - 1
    return df['SSID'].iloc[choice]



if __name__ == "__main__":

    #HERE IS ALL STEPS EXPLAINED

    #Scan and list networks
    networks_df = scan_networks()
    print("Available Networks:")
    print(networks_df)

    # Plot network signal strengths
    plot_signal_strength(networks_df)

    #Select target SSID and track its signal strength
    target_ssid = select_target_ssid(networks_df)
    print(f"Tracking signal strength for {target_ssid}")
    track_signal_strength(target_ssid)

    #Analyze channels for potential interference
    analyze_channels(networks_df)

    #Summarize security levels
    summarize_security_levels(networks_df)

    # Step 6: Determine frequency bands (2.4GHz vs 5GHz)
    networks_df = determine_frequency_band(networks_df)

    #MAC Address Lookup
    for bssid in networks_df['BSSID'].unique():
        lookup_mac_manufacturer(bssid)

    #Save analysis report to CSV
    save_analysis_report(networks_df)
