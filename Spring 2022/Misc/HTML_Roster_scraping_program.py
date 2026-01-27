from bs4 import BeautifulSoup
import csv

html = """HTML code here"""

# Parse the HTML content
soup = BeautifulSoup(html, 'html.parser')

# Prepare the CSV output
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["First Name", "Last Name"])

    # Find all table rows
    rows = soup.find_all("tr")

    for row in rows:
        # Extract the last name and first name
        last_name = row.find("span", {"class": "profileCardAvatarThumb"}).text.strip()
        first_name = row.find_all("span", {"class": "table-data-cell-value"})[0].text.strip()

        # Write the names to the CSV file
        writer.writerow([first_name, last_name])