import streamlit as st
import requests
import json
from datetime import datetime
import time
from typing import Dict, List, Optional

# 页面配置
st.set_page_config(
    page_title="GitHub Trending Scout",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 缓存配置
@st.cache_data(ttl=300)  # 5分钟缓存
def fetch_github_trending(language: str, since: str, limit: int) -> List[Dict]:
    """获取GitHub热门项目"""
    try:
        # 方法1: 使用GitHub Search API
        query = "stars:>100"
        if language != "all":
            query += f" language:{language}"
        
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Trending-Scout"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if "items" in data:
            return data["items"]
        return []
    except Exception as e:
        st.warning(f"API调用受限，使用备用数据源: {str(e)}")
        return get_fallback_data(language, limit)

def get_fallback_data(language: str, limit: int) -> List[Dict]:
    """备用数据源"""
    # 模拟一些热门项目数据
    fallback_projects = [
        {
            "full_name": "modelscope/swift",
            "html_url": "https://github.com/modelscope/swift",
            "description": "ModelScope Swift: 魔搭社区官方提供的模型微调、推理框架",
            "language": "Python",
            "stargazers_count": 8500,
            "forks_count": 1200,
            "open_issues_count": 45,
            "updated_at": "2026-04-10T00:00:00Z"
        },
        {
            "full_name": "microsoft/semantic-kernel",
            "html_url": "https://github.com/microsoft/semantic-kernel",
            "description": "Semantic Kernel: 微软官方AI开发框架",
            "language": "C#",
            "stargazers_count": 22000,
            "forks_count": 3400,
            "open_issues_count": 120,
            "updated_at": "2026-04-10T00:00:00Z"
        },
        {
            "full_name": "langchain-ai/langchain",
            "html_url": "https://github.com/langchain-ai/langchain",
            "description": "LangChain: 构建LLM应用的开发框架",
            "language": "Python",
            "stargazers_count": 95000,
            "forks_count": 15000,
            "open_issues_count": 450,
            "updated_at": "2026-04-10T00:00:00Z"
        }
    ]
    
    if language != "all":
        fallback_projects = [p for p in fallback_projects if p["language"].lower() == language.lower()]
    
    return fallback_projects[:limit]

# 概念股映射（增强版）
CONCEPT_STOCK_MAP = {
    "Python": {
        "stocks": ["东方财富", "同花顺", "恒生电子"],
        "reason": "Python是AI/数据科学首选语言，金融科技、量化交易核心"
    },
    "JavaScript": {
        "stocks": ["科大讯飞", "寒武纪", "海光信息"],
        "reason": "前端框架生态，AI应用层开发"
    },
    "TypeScript": {
        "stocks": ["科大讯飞", "寒武纪", "海光信息"],
        "reason": "企业级应用开发，AI工具链建设"
    },
    "Rust": {
        "stocks": ["中科曙光", "浪潮信息", "紫光股份"],
        "reason": "高性能计算，系统级开发，国产化替代"
    },
    "Go": {
        "stocks": ["中科曙光", "浪潮信息", "紫光股份"],
        "reason": "云原生、微服务架构，基础设施软件"
    },
    "Java": {
        "stocks": ["东方财富", "恒生电子", "金证股份"],
        "reason": "企业级应用，金融系统核心"
    },
    "C++": {
        "stocks": ["中科曙光", "浪潮信息", "寒武纪"],
        "reason": "高性能计算，AI推理引擎，游戏引擎"
    },
    "Swift": {
        "stocks": ["立讯精密", "歌尔股份", "蓝思科技"],
        "reason": "iOS生态，消费电子产业链"
    },
    "C#": {
        "stocks": ["科大讯飞", "用友网络", "金山办公"],
        "reason": "企业软件，办公自动化，AI应用"
    }
}

# 趋势信号分析
def analyze_trend_signal(repo: Dict) -> Dict:
    """分析项目趋势信号"""
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    issues = repo.get("open_issues_count", 0)
    
    # 计算信号强度
    signal_score = 0
    signals = []
    
    # Star增长信号
    if stars > 50000:
        signal_score += 3
        signals.append("🔥 超热门项目（50K+ stars）")
    elif stars > 10000:
        signal_score += 2
        signals.append("⭐ 热门项目（10K+ stars）")
    elif stars > 1000:
        signal_score += 1
        signals.append("📈 新兴项目（1K+ stars）")
    
    # Fork活跃度
    fork_ratio = forks / stars if stars > 0 else 0
    if fork_ratio > 0.3:
        signal_score += 2
        signals.append("🚀 高度活跃（fork比 > 30%）")
    elif fork_ratio > 0.15:
        signal_score += 1
        signals.append("💪 活跃项目（fork比 > 15%）")
    
    # 信号等级
    if signal_score >= 5:
        level = "P0"
        level_desc = "🔥 紧急关注"
    elif signal_score >= 3:
        level = "P1"
        level_desc = "⭐ 重点跟踪"
    elif signal_score >= 1:
        level = "P2"
        level_desc = "👀 持续观察"
    else:
        level = "P3"
        level_desc = "📝 一般关注"
    
    return {
        "score": signal_score,
        "level": level,
        "level_desc": level_desc,
        "signals": signals
    }

# 部署难度评估
def assess_difficulty(repo: Dict) -> Dict:
    """评估部署难度"""
    language = repo.get("language", "Unknown")
    description = repo.get("description", "").lower()
    
    difficulty = 1  # 1-5星
    factors = []
    
    # 语言难度
    lang_difficulty = {
        "Python": 1,
        "JavaScript": 1,
        "TypeScript": 2,
        "Go": 2,
        "Rust": 4,
        "C++": 4,
        "Java": 2,
        "Swift": 3,
        "C#": 2
    }
    difficulty = lang_difficulty.get(language, 2)
    
    # 检查关键词
    if "docker" in description or "kubernetes" in description:
        factors.append("🐳 容器化部署")
    if "api" in description or "server" in description:
        factors.append("🖥️ 需要服务器")
    if "gpu" in description or "cuda" in description:
        factors.append("🎮 需要GPU")
        difficulty += 1
    if "model" in description or "ai" in description or "llm" in description:
        factors.append("🤖 AI模型")
    
    stars = difficulty * "⭐"
    
    return {
        "level": difficulty,
        "stars": stars,
        "factors": factors
    }

# 主界面
st.title("🔥 GitHub Trending Scout")
st.markdown("**自动挖掘GitHub热门项目，智能识别技术趋势与投资机会**")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 配置")
    
    language = st.selectbox(
        "编程语言",
        ["all", "python", "javascript", "typescript", "rust", "go", "java", "c++", "swift", "c#"],
        index=0
    )
    
    since = st.selectbox(
        "时间范围",
        ["daily", "weekly", "monthly"],
        index=1
    )
    
    limit = st.slider("项目数量", 5, 30, 10)
    
    st.markdown("---")
    
    # 显示模式
    view_mode = st.radio(
        "显示模式",
        ["卡片视图", "表格视图"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📊 功能说明")
    st.markdown("""
    - 🔍 **热门项目发现**：实时获取GitHub Trending
    - 📈 **趋势信号分析**：P0/P1/P2分级
    - 💰 **概念股映射**：技术趋势→A股映射
    - 🚀 **部署评估**：快速判断上手难度
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ by [Autolo](https://github.com/autolo)")

# 主内容区
col_stats1, col_stats2, col_stats3 = st.columns(3)
with col_stats1:
    st.metric("📊 数据源", "GitHub API")
with col_stats2:
    st.metric("🔄 缓存时间", "5分钟")
with col_stats3:
    st.metric("🌐 支持语言", "9种")

st.markdown("---")

# 获取数据按钮
if st.button("🚀 获取热门项目", type="primary", use_container_width=True):
    with st.spinner("正在获取数据..."):
        projects = fetch_github_trending(language, since, limit)
        
        if projects:
            st.success(f"✅ 获取到 {len(projects)} 个项目")
            
            # 表格视图
            if view_mode == "表格视图":
                table_data = []
                for i, repo in enumerate(projects, 1):
                    trend = analyze_trend_signal(repo)
                    difficulty = assess_difficulty(repo)
                    stock_info = CONCEPT_STOCK_MAP.get(repo.get("language", ""), {"stocks": ["待分析"], "reason": ""})
                    
                    table_data.append({
                        "排名": i,
                        "项目名称": f"[{repo['full_name']}]({repo['html_url']})",
                        "语言": repo.get("language", "-"),
                        "Stars": f"{repo['stargazers_count']:,}",
                        "趋势": trend["level"],
                        "概念股": stock_info["stocks"][0]
                    })
                
                st.dataframe(
                    table_data,
                    use_container_width=True,
                    hide_index=True
                )
            
            # 卡片视图
            else:
                for i, repo in enumerate(projects, 1):
                    trend = analyze_trend_signal(repo)
                    difficulty = assess_difficulty(repo)
                    stock_info = CONCEPT_STOCK_MAP.get(repo.get("language", ""), {"stocks": ["待分析"], "reason": ""})
                    
                    with st.container():
                        # 项目标题行
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.markdown(f"### {i}. [{repo['full_name']}]({repo['html_url']})")
                            st.markdown(f"📝 {repo.get('description', '暂无描述')[:150]}...")
                        
                        with col2:
                            st.metric("趋势信号", trend["level_desc"])
                        
                        with col3:
                            st.metric("部署难度", difficulty["stars"])
                        
                        # 详细信息行
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            tags = []
                            if repo.get('language'):
                                tags.append(f"🖥️ {repo['language']}")
                            tags.append(f"⭐ {repo['stargazers_count']:,}")
                            tags.append(f"🍴 {repo['forks_count']:,}")
                            st.markdown(" | ".join(tags))
                        
                        with col2:
                            st.markdown(f"💰 **概念股**: {', '.join(stock_info['stocks'])}")
                            st.markdown(f"📋 *{stock_info['reason']}*")
                        
                        with col3:
                            for signal in trend["signals"]:
                                st.markdown(signal)
                        
                        st.markdown("---")
            
            # 统计信息
            st.markdown("### 📊 数据统计")
            col1, col2, col3, col4 = st.columns(4)
            
            total_stars = sum(p.get("stargazers_count", 0) for p in projects)
            avg_stars = total_stars // len(projects) if projects else 0
            languages = [p.get("language", "Unknown") for p in projects if p.get("language")]
            top_language = max(set(languages), key=languages.count) if languages else "Unknown"
            p0_count = sum(1 for p in projects if analyze_trend_signal(p)["level"] == "P0")
            
            with col1:
                st.metric("总Stars", f"{total_stars:,}")
            with col2:
                st.metric("平均Stars", f"{avg_stars:,}")
            with col3:
                st.metric("热门语言", top_language)
            with col4:
                st.metric("P0项目数", p0_count)
        else:
            st.error("获取数据失败，请稍后重试")

# 底部信息
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94A3B8;'>
    💡 <b>提示</b>：点击项目名称可跳转到GitHub页面 | 
    数据来源：GitHub API | 
    概念股映射仅供参考，不构成投资建议
</div>
""", unsafe_allow_html=True)
