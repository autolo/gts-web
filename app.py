import streamlit as st
import requests
import json
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="GitHub Trending Scout",
    page_icon="🔥",
    layout="wide"
)

# 标题
st.title("🔥 GitHub Trending Scout")
st.markdown("自动挖掘GitHub热门项目，智能识别技术趋势")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    language = st.selectbox(
        "编程语言",
        ["all", "python", "javascript", "typescript", "rust", "go", "java", "c++", "swift"]
    )
    since = st.selectbox(
        "时间范围",
        ["daily", "weekly", "monthly"]
    )
    limit = st.slider("项目数量", 5, 50, 25)
    
    st.markdown("---")
    st.markdown("### 📊 关于")
    st.markdown("""
    GitHub Trending Scout 是一个热门项目挖掘工具。
    
    - 🔍 自动获取热门项目
    - 📈 识别趋势信号
    - 💰 映射概念股
    - 🚀 部署难度评估
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ by 韬韬 Tao")

# 获取数据按钮
if st.button("🚀 获取热门项目", type="primary"):
    with st.spinner("正在获取数据..."):
        try:
            # 调用GitHub API
            url = f"https://api.github.com/search/repositories?q=stars:>1000+language:{language}&sort=stars&order=desc&per_page={limit}"
            headers = {"Accept": "application/vnd.github.v3+json"}
            
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            
            if "items" in data:
                st.success(f"✅ 获取到 {len(data['items'])} 个项目")
                
                # 显示项目列表
                for i, repo in enumerate(data["items"], 1):
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {i}. [{repo['full_name']}]({repo['html_url']})")
                            st.markdown(f"📝 {repo.get('description', '暂无描述')[:100]}...")
                            
                            # 标签
                            tags = []
                            if repo.get('language'):
                                tags.append(f"🖥️ {repo['language']}")
                            tags.append(f"⭐ {repo['stargazers_count']:,}")
                            tags.append(f"🍴 {repo['forks_count']:,}")
                            st.markdown(" | ".join(tags))
                        
                        with col2:
                            # 概念股映射（简化版）
                            lang_map = {
                                "Python": ["东方财富", "同花顺"],
                                "JavaScript": ["科大讯飞", "寒武纪"],
                                "TypeScript": ["科大讯飞", "寒武纪"],
                                "Rust": ["中科曙光", "浪潮信息"],
                                "Go": ["中科曙光", "浪潮信息"],
                            }
                            stocks = lang_map.get(repo.get('language', ''), ["待分析"])
                            st.metric("💰 概念股", stocks[0])
                        
                        st.markdown("---")
            else:
                st.error("获取数据失败，请稍后重试")
                
        except Exception as e:
            st.error(f"发生错误: {str(e)}")

# 底部信息
st.markdown("---")
st.markdown("💡 提示：点击项目名称可跳转到GitHub页面")
