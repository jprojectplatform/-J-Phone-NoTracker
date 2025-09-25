# 🔍 J Phone NoTracker

A sophisticated Python-based phone number tracking application that provides detailed information about phone numbers including geographic location, carrier details, timezone, and real-time location data.

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### 📱 Phone Number Intelligence
- **Country Detection**: Automatically identifies the country of any phone number
- **Carrier Information**: Detects mobile network operators and SIM card details
- **Timezone Recognition**: Shows precise timezone information
- **Real-time Phone Time**: Displays current local time for the phone number's location

### 🗺️ Advanced Geolocation
- **GPS Coordinates**: Provides accurate latitude and longitude data
- **City-Level Accuracy**: Pinpoints major cities and capitals worldwide
- **Multi-country Support**: Works with phone numbers from 30+ countries
- **African Focus**: Specialized support for Tanzanian and East African numbers

### 💻 User-Friendly Interface
- **Modern GUI**: Clean, professional dark-themed interface
- **Responsive Design**: Adapts to different window sizes
- **Easy Input**: Auto-formatting for international phone numbers
- **One-Click Tracking**: Instant results with search and clear functions

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/j4ck3r/j-phone-notracker.git
cd j-phone-notracker
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Usage

1. **Run the application**
```bash
python phoneNumber.py
```

2. **Enter phone number** in international format:
   - Example: `+255712345678` (Tanzania)
   - Example: `+1234567890` (USA)

3. **Click TRACK** to get detailed information

## 📋 Requirements

The application requires the following Python packages:

```txt
phonenumbers==8.13.27
timezonefinder==6.2.0
geopy==2.4.0
pytz==2024.1
```

Install automatically using:
```bash
pip install -r requirements.txt
```

## 🎯 Supported Countries

The application specializes in but not limited to:

### 🌍 Africa
- **Tanzania** (+255) - Full support with Dar es Salaam coordinates
- Kenya, Uganda, Rwanda, Burundi
- Nigeria, Ghana, South Africa
- Ethiopia, Somalia, Sudan
- And 20+ other African nations

### 🌎 Other Regions
- United States, United Kingdom, Canada
- Germany, France, Russia
- China, Japan, India, Australia
- Brazil, and many more...

## 📸 Screenshot

```
┌─────────────────────────────────────────┐
│           J Project Platform            │
│            J Phone NoTracker            │
└─────────────────────────────────────────┘

Enter Phone Number: [+255712345678]

[🔍 TRACK]   [🗑️ CLEAR]

TRACKING RESULTS:
• Country: Tanzania
• SIM CARD: Vodacom
• Time Zone: Africa/Dar_es_Salaam
• Phone Time: 02:30:45 PM
• Longitude: 35.7384 (Dar es Salaam)
• Latitude: -6.1630 (Dar es Salaam)
```

## 🛠️ Technical Details

### Architecture
- **Frontend**: Tkinter for cross-platform GUI
- **Backend**: phonenumbers library for number parsing
- **Geolocation**: Geopy with Nominatim service
- **Timezone**: TimezoneFinder for accurate time data

### Key Components
- `phoneNumber.py` - Main application file
- `requirements.txt` - Dependency list
- Image assets for enhanced UI (optional)

## 🔧 Customization

### Adding New Countries
Edit the `get_country_center()` function in the code:

```python
"Your Country": (longitude, latitude, "Capital City"),
```

### UI Modifications
- Colors: Modify hex codes in the code
- Layout: Adjust geometry and packing parameters
- Images: Replace logo and icon files in `py-pics/` folder

## ⚠️ Important Notes

- **Legal Use Only**: Intended for legitimate purposes only
- **Privacy Respect**: Use responsibly and respect privacy laws
- **Accuracy**: Location data is approximate to city level
- **Carrier Data**: SIM card detection depends on database accuracy

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid phone number" error**
   - Ensure correct international format (+CountryCodeNumber)
   - Remove spaces and special characters

2. **"Service Error" for location**
   - Check internet connection
   - Geolocation service might be temporarily unavailable

3. **Missing images**
   - Application will work with fallback text labels
   - Ensure image files are in correct directory

### Debug Mode
Uncomment the auto-test line in code for testing:
```python
root.after(500, test_app)  # Remove comment to auto-test
```

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests for:
- New country support
- UI improvements
- Bug fixes
- Feature enhancements

## 📄 License

This project is licensed under the GPL-3.6 License - see the LICENSE file for details.

## 👨‍💻 Author

**Created by j4ck3r**

- MEET ME: [@j4ck3r](https://jprojectplatform.com/)
- Project: J Project Platform

## 🙏 Acknowledgments

- **phonenumbers** library for phone number parsing
- **Geopy** for geolocation services
- **TimezoneFinder** for timezone data
- **Tkinter** community for GUI support

---

**⭐ If you find this project useful, please give it a star on GitHub!**

---

*Note: This tool is for educational and legitimate purposes only. Always respect privacy laws and regulations when using phone number tracking capabilities.*
