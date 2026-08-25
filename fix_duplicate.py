with open('index.html', 'r') as f:
    content = f.read()

# There's a duplicated block
block = """        // Populate year dropdown on initial load
        if (targetYear === "ALL") {
            const dropdown = document.getElementById('year-select');
            if (dropdown.options.length === 1) {
                const uniqueYears = [...allYearsSet].sort((a, b) => b - a);
                uniqueYears.forEach(year => {
                    if (year > 0) {
                        const opt = document.createElement('option');
                        opt.value = year; opt.textContent = year;
                        dropdown.appendChild(opt);
                    }
                });
            }
        }"""

if content.count(block) > 1:
    content = content.replace(block, block, 1) # This replaces the first occurrence with itself
    # Wait, replace(old, new, 1) will only replace the FIRST instance. To remove the second,
    # let's just do:
    pass

import re
# Find all occurrences and replace with just one
content = re.sub(re.escape(block) + r'\s*' + re.escape(block), block, content)

with open('index.html', 'w') as f:
    f.write(content)
