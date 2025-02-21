import subprocess

# Run the command and capture the output
command = "magick -list font"
try:
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
    output = ""

# Extract font names from every 6th line
font_names = []
lines = output.splitlines()
for i in range(len(lines)):
    if i % 6 == 2 and "bold" in lines[i].lower() and "italic" not in lines[i].lower():
        font_names.append(lines[i].strip())

# Display the font names
if font_names:
    print("Available Fonts:")
    for font in font_names:
        print(font)
else:
    print("No fonts found.")