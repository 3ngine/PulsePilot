
# PulsePilot

PulsePilot is an advanced, cross-platform WiFi analyzer written in Python. It helps users scan WiFi networks, analyze signal strength, evaluate security, identify channel interference, and track signal stability in real-time. Designed for network troubleshooting and optimization, PulsePilot provides detailed insights into nearby wireless networks.

## Features

- **Network Scanning**: Discovers nearby WiFi networks and lists SSID, signal strength, channel, BSSID, and security type.
- **Signal Strength Visualization**: Plots real-time signal strength for a target network to analyze stability and performance.
- **Channel Analysis**: Displays channel distribution to help identify potential interference.
- **Security Level Summary**: Summarizes and identifies insecure (open) networks in the area.
- **Frequency Band Analysis**: Differentiates between 2.4GHz and 5GHz networks based on channels.
- **MAC Address Lookup**: Identifies the manufacturer of a network device based on its MAC address using the [macvendors.co](https://macvendors.co) API.
- **Export to CSV**: Saves network scan results and analysis to a CSV file for offline review and documentation.

## Requirements

PulsePilot requires the following Python libraries:

```bash
pip install pandas matplotlib requests
```

### Platform Requirements

- **Linux**: Requires `nmcli` (NetworkManager CLI) for WiFi scanning.
- **Windows**: Requires `netsh` (Windows native command) for WiFi scanning.

## Installation

Clone the repository:

```bash
git clone https://github.com/3ngine/PulsePilot.git
cd PulsePilot
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Ensure you have either `nmcli` (Linux) or `netsh` (Windows) installed for WiFi network scanning.

## Usage

Run the Script: Execute `pulsepilot.py` to start the WiFi analyzer.

```bash
python pulsepilot.py
```

Select Target Network: After scanning, choose a target SSID for detailed tracking and analysis.

View Results: PulsePilot provides multiple insights:
- **Signal Strength Plot**: Visualizes the real-time signal strength of the selected network.
- **Channel Analysis**: Shows channel distribution across detected networks to assess interference.
- **Security Summary**: Lists security levels, highlighting open networks.
- **Frequency Band Information**: Distinguishes 2.4GHz and 5GHz networks.

Export Analysis: PulsePilot saves the analysis report to a CSV file for further inspection.

## Features in Detail

1. **Network Scanning**

PulsePilot uses platform-specific commands to gather detailed WiFi network information, including SSID, signal strength, channel, BSSID, and security type.

2. **Signal Strength Tracking**

The tool allows you to select a network and track its signal strength over a customizable time duration. PulsePilot then provides:

- Real-time Signal Strength Plot
- Average, Minimum, and Maximum Signal Strength for stability analysis

3. **Channel Analysis**

PulsePilot analyzes the channel distribution of detected networks and visualizes potential channel interference to help you optimize your network’s performance.

4. **Security Level Summary**

This feature provides a summary of security protocols across networks and highlights insecure networks.

5. **Frequency Band Analysis**

PulsePilot identifies whether networks are operating on the 2.4GHz or 5GHz bands to help you choose the optimal network.

6. **MAC Address Lookup**

Using the [macvendors.co](https://macvendors.co) API, PulsePilot identifies the manufacturer associated with each network's MAC address (BSSID). This can provide insights into network device types and help pinpoint unfamiliar devices.

7. **Save Analysis Report**

PulsePilot allows you to export your WiFi network analysis results to a CSV file for future reference.

## Example

```plaintext
Available Networks:
   SSID      Signal  Channel  BSSID             Security
1  Network1  75%     6        00:14:22:01:23:45 WPA2
2  Network2  55%     11       00:25:AB:CD:34:56 WPA
...

Sample Analysis Output

Tracking signal strength for Network1...
Signal Strength Stability:
   - Average Signal Strength: 73%
   - Minimum Signal Strength: 65%
   - Maximum Signal Strength: 80%
```

## API Usage

PulsePilot uses the [macvendors.co](https://macvendors.co) API to identify the manufacturer of a network device based on its MAC address. Please ensure internet access for this feature.

## License

This project is licensed under the MIT License.
