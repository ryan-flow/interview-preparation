#!/usr/bin/env python3
"""
面经搜索脚本

使用方法：
    python 面经搜索脚本.py [关键词]

示例：
    python 面经搜索脚本.py AI项目助理
    python 面经搜索脚本.py 后端开发 面试
    python 面经搜索脚本.py React 面试题
"""

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime


def search_csdn(keyword: str, page: int = 1, sort: str = "new") -> dict:
    """搜索CSDN博客"""
    url = "https://so.csdn.net/api/v3/search"
    params = {
        "q": keyword,
        "t": "blog",
        "p": page,
        "s": sort
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except Exception as e:
        return {"error": str(e)}


def format_result(result: dict, index: int) -> str:
    """格式化搜索结果"""
    if "error" in result:
        return f"❌ 错误: {result['error']}"
    
    title = result.get("title", "无标题")
    description = result.get("description", "无描述")
    url = result.get("url", "")
    author = result.get("author", "未知")
    view_num = result.get("view_num", "0")
    digg = result.get("digg", "0")
    create_time = result.get("create_time_str", "未知")
    
    # 清理HTML标签
    import re
    title = re.sub(r'<[^>]+>', '', title)
    description = re.sub(r'<[^>]+>', '', description)
    
    return f"""### {index}. {title}
- **作者**: {author}
- **阅读量**: {view_num} | **点赞**: {digg}
- **发布时间**: {create_time}
- **链接**: {url}
- **摘要**: {description[:200]}...
"""


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python 面经搜索脚本.py [关键词]")
        print("示例: python 面经搜索脚本.py AI项目助理")
        sys.exit(1)
    
    keyword = " ".join(sys.argv[1:])
    print(f"🔍 搜索关键词: {keyword}")
    print(f"⏰ 搜索时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 搜索CSDN
    print("\n📚 搜索CSDN博客...")
    result = search_csdn(keyword)
    
    if "error" in result:
        print(f"❌ 搜索失败: {result['error']}")
    else:
        total = result.get("total", 0)
        articles = result.get("result_vos", [])
        
        print(f"✅ 找到 {total} 篇相关文章")
        print(f"📋 显示前 {len(articles)} 篇:\n")
        
        for i, article in enumerate(articles, 1):
            print(format_result(article, i))
            print("-" * 60)
    
    # 保存结果
    output_file = f"面经搜索结果_{keyword.replace(' ', '_')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n💾 结果已保存到: {output_file}")


if __name__ == "__main__":
    main()
