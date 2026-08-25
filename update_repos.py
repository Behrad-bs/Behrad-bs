import os
import requests
import re

USERNAME = "Behrad-bs"

def get_latest_repos():
    # دریافت لیست ریپازیتوری‌ها مرتب شده بر اساس آخرین آپدیت
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc&per_page=30"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching repos!")
        return ["ArduWorks", "ESPWorks-IoT", "BlockForge-Solidity", "STMWorks"]
        
    repos = response.json()
    
    # فیلتر کردن ریپوهایی که مال خودت هستن (فورک نیستن) و ریپوی پروفایل اصلی هم نیستن
    valid_repos = [repo['name'] for repo in repos if not repo['fork'] and repo['name'] != USERNAME]
    
    # برداشتن ۴ ریپوی برتر
    top_repos = valid_repos[:4]
    
    # اگر کمتر از ۴ تا ریپو داشتی (محض احتیاط) جای خالیش رو با اسم‌های پیش‌فرض پر می‌کنه
    fallbacks = ["ArduWorks", "ESPWorks-IoT", "BlockForge-Solidity", "STMWorks"]
    while len(top_repos) < 4:
        top_repos.append(fallbacks[len(top_repos)])
        
    return top_repos

def generate_markdown(repos):
    # ساختن ساختار جدول HTML مارک‌داون برای جایگزینی
    table = f"""<div align="center">

|  |  |
|:--:|:--:|
| <a href="https://github.com/{USERNAME}/{repos[0]}"><img src="https://github-readme-stats-five-sigma-99.vercel.app/api/pin/?username={USERNAME}&repo={repos[0]}&theme=tokyonight&hide_border=true&bg_color=00000000&title_color=D4AF37&icon_color=C97C4B&text_color=EDE6D6" /></a> | <a href="https://github.com/{USERNAME}/{repos[1]}"><img src="https://github-readme-stats-five-sigma-99.vercel.app/api/pin/?username={USERNAME}&repo={repos[1]}&theme=tokyonight&hide_border=true&bg_color=00000000&title_color=D4AF37&icon_color=C97C4B&text_color=EDE6D6" /></a> |
| <a href="https://github.com/{USERNAME}/{repos[2]}"><img src="https://github-readme-stats-five-sigma-99.vercel.app/api/pin/?username={USERNAME}&repo={repos[2]}&theme=tokyonight&hide_border=true&bg_color=00000000&title_color=D4AF37&icon_color=C97C4B&text_color=EDE6D6" /></a> | <a href="https://github.com/{USERNAME}/{repos[3]}"><img src="https://github-readme-stats-five-sigma-99.vercel.app/api/pin/?username={USERNAME}&repo={repos[3]}&theme=tokyonight&hide_border=true&bg_color=00000000&title_color=D4AF37&icon_color=C97C4B&text_color=EDE6D6" /></a> |

</div>"""
    return table

def update_readme(new_table):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # جایگزین کردن بخش بین تگ‌های کامنت
    new_content = re.sub(
        r"<!-- REPOS_START -->.*?<!-- REPOS_END -->",
        f"<!-- REPOS_START -->\n{new_table}\n<!-- REPOS_END -->",
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    latest_repos = get_latest_repos()
    print(f"Latest repos to showcase: {latest_repos}")
    markdown_table = generate_markdown(latest_repos)
    update_readme(markdown_table)
    print("README.md updated successfully!")
