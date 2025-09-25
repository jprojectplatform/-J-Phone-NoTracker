from tkinter import *
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import requests
import re

root = Tk()
root.title("J Phone NoTracker")
root.geometry("500x700")  # Increased size for better layout
root.configure(bg="#f0f0f0")
# Enable resizing
root.resizable(True, True)  # Changed to True for both width and height

def Track():
    try:
        # Get and validate input
        input_number = entry.get().strip()
        if not input_number:
            show_error("Please enter a phone number")
            return
        
        # Add + if not present and looks like a number
        if not input_number.startswith('+') and input_number.replace(' ', '').isdigit():
            input_number = '+' + input_number
        
        # Parse phone number
        number = phonenumbers.parse(input_number, None)
        
        if not phonenumbers.is_valid_number(number):
            show_error("Invalid phone number")
            return

        # Detect country
        locate = geocoder.description_for_number(number, 'en')
        country.config(text=locate if locate else "Unknown")

        # Detect Sim Card
        operator = carrier.name_for_number(number, 'en')
        sim.config(text=operator if operator else "Unknown")

        # Detect Timezone
        time_zones = timezone.time_zones_for_number(number)
        zone_text = ", ".join(time_zones) if time_zones else "Unknown"
        zone.config(text=zone_text)

        # Get accurate location using phone number prefix and advanced geocoding
        if locate and locate != "Unknown":
            try:
                # More specific geocoding using country and possible region
                geolocator = Nominatim(user_agent="j_phone_tracker_v1.0")
                
                # Try to get more specific location using phone number prefix
                country_code = phonenumbers.region_code_for_number(number)
                national_number = phonenumbers.national_significant_number(number)
                
                # Search for more specific location
                query = f"{locate} mobile phone"
                location = geolocator.geocode(query, exactly_one=True, timeout=10)
                
                if not location:
                    # Fallback to country capital
                    query = f"capital of {locate}"
                    location = geolocator.geocode(query, exactly_one=True, timeout=10)
                
                if location:
                    lng = round(location.longitude, 6)
                    lat = round(location.latitude, 6)
                    longitude.config(text=lng)
                    latitude.config(text=lat)

                    # Detect Phone Time
                    obj = TimezoneFinder()
                    result = obj.timezone_at(lng=lng, lat=lat)
                    
                    if result:
                        home = pytz.timezone(result)
                        local_time = datetime.now(home)
                        current_time = local_time.strftime("%I:%M:%S %p")
                        clock.config(text=current_time)
                    else:
                        clock.config(text="Unknown")
                else:
                    # Use country center coordinates with better accuracy
                    country_center = get_country_center(locate)
                    if country_center:
                        lng, lat, city = country_center
                        longitude.config(text=f"{lng} ({city})")
                        latitude.config(text=f"{lat} ({city})")
                        
                        # Get timezone for fallback coordinates
                        obj = TimezoneFinder()
                        result = obj.timezone_at(lng=lng, lat=lat)
                        if result:
                            home = pytz.timezone(result)
                            local_time = datetime.now(home)
                            current_time = local_time.strftime("%I:%M:%S %p")
                            clock.config(text=current_time)
                        else:
                            clock.config(text="Unknown")
                    else:
                        longitude.config(text="Unknown")
                        latitude.config(text="Unknown")
                        clock.config(text="Unknown")
                        
            except Exception as e:
                show_error(f"Location service error: {str(e)}")
                longitude.config(text="Service Error")
                latitude.config(text="Service Error")
                clock.config(text="Error")
        else:
            longitude.config(text="Unknown")
            latitude.config(text="Unknown")
            clock.config(text="Unknown")
            zone.config(text="Unknown")

    except phonenumbers.NumberParseException:
        show_error("Invalid phone number format. Use: +255XXXXXXXXX")
    except Exception as e:
        show_error(f"Unexpected error: {str(e)}")

def get_country_center(country_name):
    """Get approximate country center coordinates with major city"""
    country_centers = {
        "United States": (-98.5795, 39.8283, "Kansas"),
        "United Kingdom": (-0.1276, 51.5074, "London"),
        "Germany": (13.4050, 52.5200, "Berlin"),
        "France": (2.3522, 48.8566, "Paris"),
        "China": (116.4074, 39.9042, "Beijing"),
        "India": (77.2090, 28.6139, "New Delhi"),
        "Brazil": (-47.9292, -15.7801, "Brasilia"),
        "Russia": (37.6173, 55.7558, "Moscow"),
        "Canada": (-75.6972, 45.4215, "Ottawa"),
        "Australia": (149.1289, -35.2809, "Canberra"),
        "Japan": (139.6917, 35.6895, "Tokyo"),
        "Kenya": (36.8219, -1.2921, "Nairobi"),
        "Nigeria": (7.4891, 9.0579, "Abuja"),
        "South Africa": (28.1871, -25.7460, "Pretoria"),
        "Egypt": (31.2357, 30.0444, "Cairo"),
        "Tanzania": (35.7384, -6.1630, "Dar es Salaam"),
        "Uganda": (32.5825, 0.3476, "Kampala"),
        "Rwanda": (30.0619, -1.9441, "Kigali"),
        "Burundi": (29.9189, -3.3822, "Bujumbura"),
        "Democratic Republic of the Congo": (15.2663, -4.4419, "Kinshasa"),
        "Zambia": (28.3228, -15.3875, "Lusaka"),
        "Malawi": (33.7873, -13.9626, "Lilongwe"),
        "Mozambique": (32.5732, -25.9692, "Maputo"),
        "Zimbabwe": (31.0545, -17.8318, "Harare"),
        "Botswana": (25.9155, -24.6589, "Gaborone"),
        "Namibia": (17.0832, -22.5700, "Windhoek"),
        "Angola": (13.2344, -8.8159, "Luanda"),
        "Ethiopia": (38.7468, 9.0300, "Addis Ababa"),
        "Somalia": (45.3183, 2.0408, "Mogadishu"),
        "Sudan": (32.5599, 15.5007, "Khartoum"),
        "Ghana": (-0.1869, 5.6037, "Accra"),
        "Ivory Coast": (-5.5471, 7.5400, "Yamoussoukro"),
        "Senegal": (-17.3660, 14.7167, "Dakar"),
        "Morocco": (-6.8498, 34.0209, "Rabat"),
        "Algeria": (3.0588, 36.7538, "Algiers"),
        "Tunisia": (10.1815, 36.8065, "Tunis"),
        "Libya": (13.1873, 32.8872, "Tripoli"),
    }
    return country_centers.get(country_name)

def show_error(message):
    """Show error message"""
    error_window = Toplevel(root)
    error_window.title("Error")
    error_window.geometry("350x120")
    error_window.resizable(False, False)
    error_window.configure(bg="#f0f0f0")
    
    Label(error_window, text=message, fg="red", font=('arial', 11), 
          bg="#f0f0f0", wraplength=300).pack(pady=20)
    Button(error_window, text="OK", command=error_window.destroy, 
           bg="#ff6b6b", fg="white", font=('arial', 10)).pack()

def clear_fields():
    """Clear all fields"""
    entry.set("")
    country.config(text="")
    sim.config(text="")
    zone.config(text="")
    clock.config(text="")
    longitude.config(text="")
    latitude.config(text="")

def format_phone_number(event=None):
    """Auto-format phone number as user types"""
    current_text = entry.get()
    if current_text and not current_text.startswith('+'):
        # Remove any existing formatting
        cleaned = re.sub(r'[^\d+]', '', current_text)
        if cleaned and not cleaned.startswith('+'):
            entry.set('+' + cleaned)

def on_resize(event):
    """Handle window resize event"""
    # Update elements to be responsive
    pass

# ===== IMPROVED UI DESIGN WITH LOGO IN HEADER =====

# Header - J Project Platform with Logo
header_frame = Frame(root, bg="#2c3e50", height=100)
header_frame.pack(fill=X)
header_frame.pack_propagate(False)

# Header content frame
header_content = Frame(header_frame, bg="#2c3e50")
header_content.pack(expand=True, fill=BOTH, padx=20, pady=10)

# Logo on the left side
try:
    logo = PhotoImage(file="logo image.png")
    # Resize logo if needed (you can adjust the subsample factor)
    # logo = logo.subsample(2, 2)  # Reduce size by half
    logo_label = Label(header_content, image=logo, bg="#2c3e50")
    logo_label.image = logo  # Keep a reference
    logo_label.pack(side=LEFT, padx=(0, 15))
except:
    # Fallback logo
    logo_label = Label(header_content, text="J\nPNT", bg="#3498db", fg="white", 
                      width=6, height=3, font=('arial', 10, 'bold'))
    logo_label.pack(side=LEFT, padx=(0, 15))

# Title section in the center
title_frame = Frame(header_content, bg="#2c3e50")
title_frame.pack(side=LEFT, expand=True, fill=BOTH)

Label(title_frame, text="J Project Platform", font=('arial', 18, 'bold'), 
      bg="#2c3e50", fg="white").pack(pady=(5, 0))

Label(title_frame, text="J Phone NoTracker", font=('arial', 14, 'italic'), 
      bg="#2c3e50", fg="#ecf0f1").pack(pady=(0, 5))

# Main content area - now responsive
main_frame = Frame(root, bg="#f0f0f0")
main_frame.pack(fill=BOTH, expand=True, padx=20, pady=15)

# Centered input area that expands with window
input_container = Frame(main_frame, bg="#f0f0f0")
input_container.pack(fill=X, pady=(0, 20))

# Improved input area - centered and responsive
input_frame = Frame(input_container, bg="#ecf0f1", relief="ridge", bd=2)
input_frame.pack(padx=10, pady=10, fill=X)

Label(input_frame, text="Enter Phone Number:", font=('arial', 12, 'bold'), 
      bg="#ecf0f1").pack(pady=(15, 10))

# Modern input field - centered
entry = StringVar()
input_entry = Entry(input_frame, textvariable=entry, width=25, justify="center", 
                   font=("arial", 14), relief="flat", bg="white", bd=2)
input_entry.pack(pady=5, padx=20, fill=X)
input_entry.focus()

# Bind key release for auto-formatting
input_entry.bind('<KeyRelease>', format_phone_number)

# Format hints
Label(input_frame, text="Format: +[CountryCode][Number]", font=('arial', 9), 
      fg="#7f8c8d", bg="#ecf0f1").pack()

Label(input_frame, text="Example: +255712345678", font=('arial', 9), 
      fg="#e74c3c", bg="#ecf0f1").pack()

# Buttons frame - centered
button_frame = Frame(input_frame, bg="#ecf0f1")
button_frame.pack(pady=15)

# Search button
search_btn = Button(button_frame, text="🔍 TRACK", bg="#27ae60", fg="white", 
                   font=('arial', 11, 'bold'), cursor="hand2", command=Track,
                   relief="raised", bd=2, width=10)
search_btn.pack(side=LEFT, padx=10)

# Clear button
clear_btn = Button(button_frame, text="🗑️ CLEAR", bg="#e74c3c", fg="white", 
                  font=('arial', 11, 'bold'), cursor="hand2", command=clear_fields,
                  relief="raised", bd=2, width=10)
clear_btn.pack(side=LEFT, padx=10)

# Results section - responsive
results_container = Frame(main_frame, bg="#f0f0f0")
results_container.pack(fill=BOTH, expand=True)

results_frame = Frame(results_container, bg="#34495e", relief="ridge", bd=2)
results_frame.pack(fill=BOTH, expand=True, padx=10)

Label(results_frame, text="TRACKING RESULTS", font=('arial', 14, 'bold'), 
      bg="#34495e", fg="white").pack(pady=15)

# Results grid using Frame for better responsiveness
results_grid = Frame(results_frame, bg="#34495e")
results_grid.pack(fill=BOTH, expand=True, padx=20, pady=10)

# Create two columns for results
left_column = Frame(results_grid, bg="#34495e")
left_column.pack(side=LEFT, fill=BOTH, expand=True)

right_column = Frame(results_grid, bg="#34495e")
right_column.pack(side=RIGHT, fill=BOTH, expand=True)

# Results data with better spacing
results_data = [
    ("Country:", "country", left_column),
    ("SIM CARD:", "sim", left_column),
    ("Time Zone:", "zone", left_column),
    ("Phone Time:", "clock", right_column),
    ("Longitude:", "longitude", right_column),
    ("Latitude:", "latitude", right_column)
]

# Create result display labels with better layout
result_vars = {}
for text, var_name, parent_frame in results_data:
    row_frame = Frame(parent_frame, bg="#34495e")
    row_frame.pack(fill=X, pady=8)
    
    label = Label(row_frame, text=text, font=('arial', 10, 'bold'), 
                 bg="#34495e", fg="#bdc3c7", width=12, anchor="w")
    label.pack(side=LEFT)
    
    result_var = Label(row_frame, text="", font=('arial', 10), 
                      bg="#34495e", fg="white", wraplength=200, justify=LEFT)
    result_var.pack(side=LEFT, fill=X, expand=True)
    result_vars[var_name] = result_var

# Assign to global variables
country = result_vars["country"]
sim = result_vars["sim"]
zone = result_vars["zone"]
clock = result_vars["clock"]
longitude = result_vars["longitude"]
latitude = result_vars["latitude"]

# Footer - Created by j4ck3r
footer_frame = Frame(root, bg="#2c3e50", height=40)
footer_frame.pack(fill=X, side=BOTTOM)
footer_frame.pack_propagate(False)

Label(footer_frame, text="Created by j4ck3r", font=('arial', 10, 'italic'), 
      bg="#2c3e50", fg="#ecf0f1").pack(pady=10)

# Bind Enter key to Track function
root.bind('<Return>', lambda event: Track())

# Bind resize event
root.bind('<Configure>', on_resize)

# Test function
def test_app():
    """Auto-fill a test number"""
    entry.set("+255712345678")

# Auto-fill after 0.5 seconds
root.after(500, test_app)

# Set minimum window size
root.minsize(450, 650)

# Optional: Start maximized (uncomment if desired)
# root.state('zoomed')  # Maximized window

root.mainloop()
