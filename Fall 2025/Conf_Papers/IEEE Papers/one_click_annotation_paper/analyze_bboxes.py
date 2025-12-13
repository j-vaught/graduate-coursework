import os
import glob
import xml.etree.ElementTree as ET
import csv

def analyze_annotations(annotations_dir):
    sizes_data = []
    centers_data = []

    # Get all XML files
    xml_files = glob.glob(os.path.join(annotations_dir, "*.xml"))
    print(f"Found {len(xml_files)} XML files in {annotations_dir}")

    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            filename = root.find('filename').text if root.find('filename') is not None else os.path.basename(xml_file)

            for obj in root.findall('object'):
                bndbox = obj.find('bndbox')
                if bndbox is not None:
                    try:
                        xmin = float(bndbox.find('xmin').text)
                        ymin = float(bndbox.find('ymin').text)
                        xmax = float(bndbox.find('xmax').text)
                        ymax = float(bndbox.find('ymax').text)

                        width = xmax - xmin
                        height = ymax - ymin
                        center_x = (xmin + xmax) / 2
                        center_y = (ymin + ymax) / 2

                        sizes_data.append([filename, width, height])
                        centers_data.append([filename, center_x, center_y])
                    except (ValueError, AttributeError) as e:
                        print(f"Error parsing bbox in {xml_file}: {e}")

        except ET.ParseError as e:
            print(f"Error parsing XML file {xml_file}: {e}")

    # Write sizes CSV
    with open('bbox_sizes.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'width', 'height'])
        writer.writerows(sizes_data)
    print(f"Wrote {len(sizes_data)} entries to bbox_sizes.csv")

    # Write centers CSV
    with open('bbox_centers.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'center_x', 'center_y'])
        writer.writerows(centers_data)
    print(f"Wrote {len(centers_data)} entries to bbox_centers.csv")

if __name__ == "__main__":
    annotations_path = "/Volumes/MacShare/radar3000/Annotations"
    if os.path.exists(annotations_path):
        analyze_annotations(annotations_path)
    else:
        print(f"Error: Directory not found: {annotations_path}")
