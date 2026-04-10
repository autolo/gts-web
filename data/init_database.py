#!/usr/bin/env python3
"""
数据库初始化脚本
创建产业链知识图谱和映射规则的SQLite数据库
"""

import sqlite3
import json
from datetime import datetime
import os

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'mapping.db')

def get_db_path():
    """获取数据库路径"""
    return os.path.join(os.path.dirname(__file__), 'mapping.db')

def init_database():
    """初始化数据库"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建映射规则表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mapping_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type VARCHAR(50) NOT NULL,
            source_value VARCHAR(100) NOT NULL,
            target_stock VARCHAR(50) NOT NULL,
            target_code VARCHAR(10) NOT NULL,
            weight DECIMAL(3,2) DEFAULT 0.5,
            confidence DECIMAL(3,2) DEFAULT 0.5,
            reason TEXT,
            verified_count INTEGER DEFAULT 0,
            success_count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(source_type, source_value, target_stock)
        )
    ''')
    
    # 创建产业链表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS industry_chain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain VARCHAR(50) NOT NULL,
            chain_node VARCHAR(100) NOT NULL,
            keywords TEXT NOT NULL,
            stocks TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(domain, chain_node)
        )
    ''')
    
    # 创建验证记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS validation_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_name VARCHAR(200) NOT NULL,
            stock_name VARCHAR(50) NOT NULL,
            stock_code VARCHAR(10),
            recommend_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            recommend_score DECIMAL(3,2),
            price_on_recommend DECIMAL(10,2),
            price_after_7d DECIMAL(10,2),
            user_feedback VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mapping_source ON mapping_rules(source_type, source_value)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chain_domain ON industry_chain(domain)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_validation_repo ON validation_records(repo_name)')
    
    conn.commit()
    return conn, cursor

def init_industry_chains(cursor):
    """初始化产业链知识图谱"""
    
    # AI产业链
    ai_chain = [
        {
            "node": "AI.训练端",
            "keywords": ["training", "model training", "deep learning training", "pytorch training", 
                        "tensorflow training", "distributed training", "multi-gpu training", 
                        "fine-tuning", "pre-training", "mlops", "machine learning platform"],
            "stocks": [
                {"name": "寒武纪", "code": "688256", "role": "训练芯片", "market_share": "20%", "strength": "strong"},
                {"name": "海光信息", "code": "688041", "role": "训练芯片", "market_share": "15%", "strength": "medium"},
                {"name": "中科曙光", "code": "603019", "role": "AI服务器", "market_share": "25%", "strength": "strong"},
                {"name": "华为概念", "code": "NONE", "role": "昇腾芯片", "market_share": "30%", "strength": "strong"}
            ]
        },
        {
            "node": "AI.推理端",
            "keywords": ["inference", "model serving", "onnx", "tensorrt", "triton", "deployment",
                        "model optimization", "quantization", "openvino", "llm inference", 
                        "chatbot", "rag", "langchain", "semantic kernel"],
            "stocks": [
                {"name": "寒武纪", "code": "688256", "role": "推理芯片", "market_share": "25%", "strength": "strong"},
                {"name": "海光信息", "code": "688041", "role": "推理芯片", "market_share": "18%", "strength": "medium"},
                {"name": "科大讯飞", "code": "002230", "role": "AI应用", "market_share": "35%", "strength": "strong"},
                {"name": "云从科技", "code": "688327", "role": "AI应用", "market_share": "10%", "strength": "medium"}
            ]
        },
        {
            "node": "AI.数据端",
            "keywords": ["data pipeline", "etl", "data preprocessing", "data annotation",
                        "data labeling", "dataset", "data augmentation", "data validation",
                        "feature engineering", "data quality", "data governance"],
            "stocks": [
                {"name": "东方财富", "code": "300059", "role": "金融数据", "strength": "medium"},
                {"name": "恒生电子", "code": "600570", "role": "金融数据", "strength": "medium"},
                {"name": "同花顺", "code": "300033", "role": "数据服务", "strength": "weak"}
            ]
        },
        {
            "node": "AI.框架端",
            "keywords": ["pytorch", "tensorflow", "jax", "mxnet", "caffe", "deep learning framework",
                        "neural network library", "ml framework", "ai framework", "llm framework",
                        "modelscope", "swift", "transformers", "diffusers"],
            "stocks": [
                {"name": "寒武纪", "code": "688256", "role": "框架适配", "strength": "strong"},
                {"name": "海光信息", "code": "688041", "role": "框架优化", "strength": "medium"},
                {"name": "中科曙光", "code": "603019", "role": "算力支持", "strength": "medium"}
            ]
        }
    ]
    
    # 云计算产业链
    cloud_chain = [
        {
            "node": "云计算.基础设施",
            "keywords": ["cloud computing", "iaas", "server", "data center", "virtualization",
                        "kvm", "vmware", "hypervisor", "bare metal", "gpu cloud", "vpc"],
            "stocks": [
                {"name": "中科曙光", "code": "603019", "role": "服务器", "market_share": "25%", "strength": "strong"},
                {"name": "浪潮信息", "code": "000977", "role": "服务器", "market_share": "30%", "strength": "strong"},
                {"name": "紫光股份", "code": "000938", "role": "网络设备", "market_share": "15%", "strength": "medium"}
            ]
        },
        {
            "node": "云计算.平台层",
            "keywords": ["kubernetes", "docker", "container", "containerization", "helm",
                        "istio", "service mesh", "devops", "ci/cd", "jenkins", "argocd",
                        "microservice", "service discovery", "container orchestrator"],
            "stocks": [
                {"name": "中科曙光", "code": "603019", "role": "容器平台", "strength": "strong"},
                {"name": "浪潮信息", "code": "000977", "role": "云原生", "strength": "medium"},
                {"name": "用友网络", "code": "600588", "role": "企业云", "strength": "medium"}
            ]
        },
        {
            "node": "云计算.应用层",
            "keywords": ["saas", "paas", "serverless", "faas", "api gateway", "rest api",
                        "graphql", "backend as a service", "baas", "apigee", "aws lambda",
                        "cloud function", "serverless framework"],
            "stocks": [
                {"name": "用友网络", "code": "600588", "role": "企业SaaS", "strength": "strong"},
                {"name": "金山办公", "code": "688111", "role": "办公SaaS", "strength": "strong"},
                {"name": "东方财富", "code": "300059", "role": "金融SaaS", "strength": "medium"}
            ]
        }
    ]
    
    # 金融科技产业链
    fintech_chain = [
        {
            "node": "金融.交易系统",
            "keywords": ["trading", "exchange", "stock market", "cryptocurrency exchange",
                        "trading bot", "algorithmic trading", "quantitative trading",
                        "high frequency trading", "order book", "market maker"],
            "stocks": [
                {"name": "东方财富", "code": "300059", "role": "互联网券商", "strength": "strong"},
                {"name": "同花顺", "code": "300033", "role": "行情交易", "strength": "strong"},
                {"name": "恒生电子", "code": "600570", "role": "交易系统", "strength": "strong"},
                {"name": "金证股份", "code": "600446", "role": "证券系统", "strength": "strong"}
            ]
        },
        {
            "node": "金融.风控系统",
            "keywords": ["risk management", "fraud detection", "credit scoring", 
                        "compliance", "aml", "kyc", "anti-money laundering",
                        "risk assessment", "financial regulation", "audit"],
            "stocks": [
                {"name": "恒生电子", "code": "600570", "role": "风控系统", "strength": "strong"},
                {"name": "东方财富", "code": "300059", "role": "风控数据", "strength": "medium"},
                {"name": "同花顺", "code": "300033", "role": "风险分析", "strength": "medium"}
            ]
        },
        {
            "node": "金融.支付结算",
            "keywords": ["payment", "payment gateway", "mobile payment", "digital wallet",
                        "blockchain payment", "remittance", "settlement", "stripe",
                        "alipay", "wechat pay", "pos", "fintech payment"],
            "stocks": [
                {"name": "东方财富", "code": "300059", "role": "支付入口", "strength": "medium"},
                {"name": "恒生电子", "code": "600570", "role": "支付系统", "strength": "medium"}
            ]
        }
    ]
    
    # 游戏产业链
    game_chain = [
        {
            "node": "游戏.游戏引擎",
            "keywords": ["game engine", "unity", "unreal", "godot", "game development",
                        "3d engine", "rendering engine", "physics engine", "shader",
                        "game asset", "gameplay", "level design"],
            "stocks": [
                {"name": "中科曙光", "code": "603019", "role": "渲染计算", "strength": "medium"},
                {"name": "寒武纪", "code": "688256", "role": "游戏AI", "strength": "weak"}
            ]
        },
        {
            "node": "游戏.游戏服务",
            "keywords": ["game server", "multiplayer", "online game", "game backend",
                        " matchmaking", "game analytics", "unity services", "playfab",
                        "photon", "nakama", "game cloud"],
            "stocks": [
                {"name": "中科曙光", "code": "603019", "role": "游戏云", "strength": "strong"},
                {"name": "浪潮信息", "code": "000977", "role": "游戏服务器", "strength": "medium"}
            ]
        },
        {
            "node": "游戏.游戏AI",
            "keywords": ["game ai", "npc ai", "procedural generation", "game bot",
                        "reinforcement learning game", "ai opponent", "game automation",
                        "ai game testing", "game simulation"],
            "stocks": [
                {"name": "寒武纪", "code": "688256", "role": "游戏AI芯片", "strength": "strong"},
                {"name": "科大讯飞", "code": "002230", "role": "NLP游戏", "strength": "medium"}
            ]
        }
    ]
    
    all_chains = {
        "AI": ai_chain,
        "云计算": cloud_chain,
        "金融": fintech_chain,
        "游戏": game_chain
    }
    
    for domain, chains in all_chains.items():
        for chain in chains:
            cursor.execute('''
                INSERT OR REPLACE INTO industry_chain (domain, chain_node, keywords, stocks)
                VALUES (?, ?, ?, ?)
            ''', (domain, chain["node"], json.dumps(chain["keywords"], ensure_ascii=False), 
                  json.dumps(chain["stocks"], ensure_ascii=False)))
    
    return all_chains

def init_mapping_rules(cursor):
    """初始化映射规则"""
    
    rules = [
        # 编程语言映射
        ("language", "Python", "东方财富", "300059", 0.30, 0.75, "Python在量化交易、数据分析领域"),
        ("language", "Python", "同花顺", "300033", 0.30, 0.75, "Python金融数据分析"),
        ("language", "Python", "恒生电子", "600570", 0.25, 0.70, "Python金融系统开发"),
        ("language", "JavaScript", "科大讯飞", "002230", 0.25, 0.60, "JavaScript AI应用"),
        ("language", "TypeScript", "用友网络", "600588", 0.25, 0.70, "TypeScript企业开发"),
        ("language", "TypeScript", "金山办公", "688111", 0.25, 0.65, "TypeScript办公软件"),
        ("language", "Rust", "中科曙光", "603019", 0.35, 0.80, "Rust高性能计算"),
        ("language", "Rust", "浪潮信息", "000977", 0.35, 0.75, "Rust基础设施开发"),
        ("language", "Go", "中科曙光", "603019", 0.30, 0.75, "Go云原生"),
        ("language", "Go", "浪潮信息", "000977", 0.30, 0.70, "Go微服务架构"),
        ("language", "Java", "东方财富", "300059", 0.35, 0.80, "Java金融交易系统"),
        ("language", "Java", "恒生电子", "600570", 0.35, 0.85, "Java金融核心系统"),
        ("language", "Java", "金证股份", "600446", 0.30, 0.75, "Java证券交易系统"),
        ("language", "C++", "中科曙光", "603019", 0.35, 0.80, "C++高性能计算"),
        ("language", "C++", "寒武纪", "688256", 0.35, 0.85, "C++ AI芯片底层"),
        ("language", "Swift", "立讯精密", "002475", 0.30, 0.70, "iOS生态供应链"),
        ("language", "Swift", "歌尔股份", "002241", 0.30, 0.65, "Apple生态"),
        ("language", "C#", "用友网络", "600588", 0.25, 0.70, "C#企业开发"),
        ("language", "C#", "金山办公", "688111", 0.25, 0.65, "C#办公软件"),
        
        # 技术领域映射
        ("domain", "ai", "科大讯飞", "002230", 0.50, 0.85, "AI语音、NLP领域龙头"),
        ("domain", "ai", "寒武纪", "688256", 0.50, 0.80, "AI芯片核心标的"),
        ("domain", "ai", "海光信息", "688041", 0.50, 0.75, "AI算力芯片"),
        ("domain", "llm", "科大讯飞", "002230", 0.50, 0.85, "大模型研发"),
        ("domain", "llm", "寒武纪", "688256", 0.50, 0.80, "大模型推理芯片"),
        ("domain", "llm", "中科曙光", "603019", 0.40, 0.65, "大模型算力基础设施"),
        ("domain", "cloud", "中科曙光", "603019", 0.40, 0.80, "云计算基础设施"),
        ("domain", "cloud", "浪潮信息", "000977", 0.40, 0.80, "云服务器龙头"),
        ("domain", "cloud", "紫光股份", "000938", 0.35, 0.65, "云计算网络"),
        ("domain", "fintech", "东方财富", "300059", 0.45, 0.90, "互联网金融平台"),
        ("domain", "fintech", "同花顺", "300033", 0.45, 0.85, "金融数据分析"),
        ("domain", "fintech", "恒生电子", "600570", 0.45, 0.85, "金融系统"),
        ("domain", "blockchain", "恒生电子", "600570", 0.40, 0.60, "区块链金融应用"),
        ("domain", "game", "中科曙光", "603019", 0.30, 0.60, "游戏服务器"),
        ("domain", "game", "寒武纪", "688256", 0.30, 0.55, "游戏AI"),
        
        # 技术栈映射
        ("tech_stack", "pytorch", "寒武纪", "688256", 0.40, 0.80, "PyTorch深度学习框架"),
        ("tech_stack", "tensorflow", "海光信息", "688041", 0.35, 0.70, "TensorFlow AI推理"),
        ("tech_stack", "kubernetes", "中科曙光", "603019", 0.35, 0.75, "K8s容器编排"),
        ("tech_stack", "redis", "东方财富", "300059", 0.25, 0.60, "Redis高速缓存"),
        ("tech_stack", "kafka", "东方财富", "300059", 0.25, 0.60, "Kafka消息队列"),
        ("tech_stack", "react", "用友网络", "600588", 0.20, 0.55, "React前端框架"),
        ("tech_stack", "vue", "用友网络", "600588", 0.20, 0.55, "Vue前端框架"),
        ("tech_stack", "langchain", "科大讯飞", "002230", 0.35, 0.70, "LangChain应用开发"),
        ("tech_stack", "transformers", "寒武纪", "688256", 0.35, 0.75, "Transformers模型优化"),
        ("tech_stack", "onnx", "寒武纪", "688256", 0.35, 0.80, "ONNX推理加速"),
        ("tech_stack", "onnx", "海光信息", "688041", 0.30, 0.70, "ONNX推理优化"),
        ("tech_stack", "llama", "科大讯飞", "002230", 0.30, 0.65, "Llama模型应用"),
        ("tech_stack", "stable diffusion", "寒武纪", "688256", 0.35, 0.70, " Diffusion推理"),
    ]
    
    for rule in rules:
        cursor.execute('''
            INSERT OR REPLACE INTO mapping_rules 
            (source_type, source_value, target_stock, target_code, weight, confidence, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', rule)

def main():
    """主函数"""
    print(f"正在初始化数据库: {DB_PATH}")
    
    # 初始化数据库
    conn, cursor = init_database()
    
    # 初始化产业链知识图谱
    print("正在初始化产业链知识图谱...")
    init_industry_chains(cursor)
    
    # 初始化映射规则
    print("正在初始化映射规则...")
    init_mapping_rules(cursor)
    
    # 提交并关闭
    conn.commit()
    
    # 验证数据
    cursor.execute("SELECT COUNT(*) FROM industry_chain")
    chain_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM mapping_rules")
    rule_count = cursor.fetchone()[0]
    
    print(f"✅ 数据库初始化完成!")
    print(f"   - 产业链节点: {chain_count}")
    print(f"   - 映射规则: {rule_count}")
    
    conn.close()

if __name__ == "__main__":
    main()
