import requests
import pandas as pd
import time

API_KEY = "Zj0owtJIgmogTTHoJdfmGWV6pdzwGAX6"
url = "https://app.ticketmaster.com/discovery/v2/events.json"

params = {
    'apikey': API_KEY,
    'size': 200,  
    'startDateTime': '2025-01-01T00:00:00Z',
    'endDateTime': '2025-12-31T23:59:59Z',
    'page': 0
}

events_list = []
MAX_EVENTS = 5000  
event_count = 0

while event_count < MAX_EVENTS:
    response = requests.get(url, params=params)
    data = response.json()

    if "_embedded" in data:
        events = data["_embedded"]["events"]
        for event in events:
            event_details = {
                "Event": event.get('name', 'N/A'),
                "Date": event.get('dates', {}).get('start', {}).get('localDate', 'N/A'),
                "Time": event.get('dates', {}).get('start', {}).get('localTime', 'N/A'),
                "Venue": event.get('_embedded', {}).get('venues', [{}])[0].get('name', 'N/A'),
                "City": event.get('_embedded', {}).get('venues', [{}])[0].get('city', {}).get('name', 'N/A'),
                "State": event.get('_embedded', {}).get('venues', [{}])[0].get('state', {}).get('name', 'N/A'),
                "Genre": event.get('classifications', [{}])[0].get('genre', {}).get('name', 'N/A'),
                "Sub-Genre": event.get('classifications', [{}])[0].get('subGenre', {}).get('name', 'N/A'),
                "Segment": event.get('classifications', [{}])[0].get('segment', {}).get('name', 'N/A'),
                "Performer": event.get('_embedded', {}).get('attractions', [{}])[0].get('name', 'N/A'),
                "Venue Capacity": event.get('_embedded', {}).get('venues', [{}])[0].get('capacity', 'N/A'),
                "Min Price": event.get('priceRanges', [{}])[0].get('min', 'N/A'),
                "Max Price": event.get('priceRanges', [{}])[0].get('max', 'N/A'),
                "Sales Status": event.get('dates', {}).get('status', {}).get('code', 'N/A'),
                "On-Sale Date": event.get('sales', {}).get('public', {}).get('startDateTime', 'N/A'),
                "Promoter": event.get('promoter', {}).get('name', 'N/A'),
                "Accessibility Info": event.get('accessibility', {}).get('info', 'N/A'),
                "Ticket URL": event.get('url', 'N/A')
            }
            events_list.append(event_details)
            event_count += 1

        print(f"✅ Collected {event_count} events so far...")

        if event_count >= MAX_EVENTS:
            break

        # Move to the next page
        if "page" in data and data["page"]["number"] < data["page"]["totalPages"] - 1:
            params["page"] += 1  
            time.sleep(1)  
        else:
            break  
    else:
        break  

# Convert to DataFrame and save as CSV
df = pd.DataFrame(events_list)
df.to_csv("ticketmaster_events_2025_detailed.csv", index=False)
print(f"🎉 Data saved to 'ticketmaster_events_2025_detailed.csv' with {len(df)} events!")



