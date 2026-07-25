from app.parser import ResumeParser

resume = r"D:\Self Projects\gethired\gethired\uploads\project_2\resume_original.docx"

parser = ResumeParser()

sections = parser.parse(resume)

print("\nDetected sections\n")

for name in sections:
    print(name)