import csv
import folium
from folium.features import DivIcon
from folium.plugins import PolyLineTextPath

def create_map(pois, output_file):
    if not pois:
        print("No valid coordinates found.")
        return

    m = folium.Map(location=pois[0][1], zoom_start=13)

    for idx, (name, coord, url, other) in enumerate(pois, start=1):
        icon = DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html=f"<div style='background-color: white; padding: 3px; border: 1px solid black;'>{idx}. {name}</div>",
        )
        marker = folium.Marker(
            location=coord,
            icon=icon
        )
        marker.add_child(folium.Popup(f'<a href="{url}" target="_blank">{url}</a><br>{other}'))
        marker.add_to(m)

    coords = [coord for _, coord, _, _ in pois]
    polyline = folium.PolyLine(coords, color="blue", weight=2.5, opacity=0.7).add_to(m)

    arrows = PolyLineTextPath(
        polyline,
        ">>>",
        repeat=True,
        offset=0,
        text_opacity=0,
        font_size=14,
        center=True
    ).add_to(m)

    m.save(output_file)

def read_pois_from_csv(file_path):
    pois = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            map_name = row['map']
            name = row['cute_name']
            coord = (float(row['lat']), float(row['long']))
            url = row['url']
            other = row['other']
            if map_name not in pois:
                pois[map_name] = []
            pois[map_name].append((name, coord, url, other))

    return pois

csv_file = "pois.csv"
pois_per_map = read_pois_from_csv(csv_file)

for map_name, pois in pois_per_map.items():
    create_map(pois, f"{map_name}.html")
