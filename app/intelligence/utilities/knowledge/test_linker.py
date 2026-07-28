python -c "import os
for root, dirs, files in os.walk('app'):
    level=root.replace('app','').count(os.sep)
    indent='    '*level
    print(f'{indent}{os.path.basename(root)}/')
    for f in sorted(files):
        print(f'{indent}    {f}')"
    