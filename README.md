# SimpleBarcode
A web live barcode scanner with quantity for small enterprises that feeds the barcode input to the local network (offline or online). Lightweight and fully customizable for `Javascript` or `Python` developers. 

The application is running with Minhazav's **html5-qrcode** and Flask's websocket **SocketIO** API to communicate with the local server running on the "P.O.S. machine" or the computer.

### Features
 - Fully Customizable for both Python and HTML
 - System notification
 - UI included
 - After scan key and Hotbar inputs
 - Lightweight
 - Custom system tray for PC
 - Barcode to clipboard
 - Different scanning modes included
	 - *Scan Mode* - Scanning with quantity setting and custom hotbar
	 - *List Mode* - Scanning without quantity setting and with only enter key input
	 - *Quick Mode*- Instant Scan with a default quantity for continuous scanning like the traditional barcode scanners

# Usage
It is recommended to integrate it for Microsoft Excel spreadsheet *sales* or *product* inventory. However, it's recommended not to use it on public networks due to the application's lack of end-to-end encryption and security.

 1. Download Python v3.6 or newer version;
 2. Open `cmd` on the SimpleBarcode directory;
 3. Do `pip install -r requirements.txt`
 4. Run `pos server.py`;
 5. Search for the server's/computer's local IP Address, and add port 5000; (e.g. 192.168.254.102:5000)
 6. Enter the IP to the browser;
 7. Click the "Scan Product" header;
 8. then Start Scanning.

# Credits
Thank you ChatGPT for guiding me.

Initially developed for my family's business.
