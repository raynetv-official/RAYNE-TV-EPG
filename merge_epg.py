
import urllib.request
import xml.etree.ElementTree as ET
import os

BASE = "https://raw.githubusercontent.com/raynetv-official/RAYNE-TV-EPG/refs/heads/main/"

FILES = [
    "epg.xml",
    "epg_hardcore_01.xml",
    "epg_hardcore_02.xml",
    "epg_hardcore_03.xml",
    "epg_hardcore_04.xml",
    "epg_hardcore_05.xml",
    "epg_hardcore_06.xml",
    "epg_hardcore_07.xml"
]

merged = ET.Element("tv")
channels = set()
programmes = set()

for filename in FILES:
    print("Downloading:", filename)

    url = BASE + filename
    request = urllib.request.Request(
        url, headers={"User-Agent": "RAYNE-TV-EPG-Merger"}
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        content = response.read()

    root = ET.fromstring(content)

    for item in root:
        if item.tag == "channel":
            channel_id = item.get("id")
            if channel_id and channel_id not in channels:
                merged.append(item)
                channels.add(channel_id)

        elif item.tag == "programme":
            key = (
                item.get("channel"),
                item.get("start"),
                item.get("stop"),
                item.findtext("title", default="")
            )

            if key not in programmes:
                merged.append(item)
                programmes.add(key)

ET.indent(merged, space="  ")

ET.ElementTree(merged).write(
    "epg_combined.xml",
    encoding="utf-8",
    xml_declaration=True
)

print("EPG MERGE COMPLETE")
print("Channels:", len(channels))
print("Programmes:", len(programmes))
