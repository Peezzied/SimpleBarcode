# SimpleBarcode
A web live barcode scanner with quantity for small enterprises that feeds the barcode input to the local network (offline or online). Lightweight and fully-customizable for `Javascript` or `Python` developers. 

The application running with minhazav's **html5-qrcode** and flask's websocket **SocketIO** API to communicate with the local server running on the "P.O.S. machine" or the computer.

### Features
 - Fully Customizable
 - UI included
 - After scan key and hotbar inputs
 - Lightweight
 - Custom system tray for PC
 - Barcode to clipboard
 - Different scanning modes included
	 - *Scan Mode* - Scanning with quantity setting and custom hotbar
	 - *List Mode* - Scanning without quanitity setting and with only enter key input
	 - *Quick Mode*- Instant Scan with a default quantity for continous scanning like the traditional barcode scanners

# Usage
Recommended to intergrate it for Microsoft Excel spreadsheet *sales* or *product* inventory. However it's recommended to use it on public networks due to the application's lack of end-to-end encryption and security.

 1. Download Python v3.6 or newer version;
 2. Run `pos server.py`;
 3. Search for the server's/computer's local IP Address;
 4. Enter the IP to browser;
 5. Click the "Scan Product" header;
 6. then Start Scanning.

# Credits
Thank you ChatGPT for guiding me.

Originally developed for my family's business.
