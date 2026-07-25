from app.parser.readers import ResumeReader

resume = r"D:\Self Projects\gethired\gethired\uploads\project_2\resume_original.docx"

reader = ResumeReader()

lines = reader.read(resume)

print("=" * 80)
print("TOTAL LINES:", len(lines))
print("=" * 80)

for i, line in enumerate(lines, start=1):
    print(f"{i:03d}: {line}")