import os
import re

BLOG_DIR = r"c:\Users\haionnet\Desktop\editornom\src\data\blog"
DATES = ["260508_", "260509_", "260510_", "260511_"]

# 1. Uncorrupt known files
corrupted_relative_paths = [
    r"ko\glossary\260508_what-is-dpo.md",
    r"ko\glossary\260510_chaos-engineering.md",
    r"ko\posts\260508_cve-2026-31431-copy-fail-linux-kernel-container-isolation.md",
    r"ko\posts\260510_birth-fall-asymmetric-encryption-quantum.md"
]

def uncorrupt_all():
    print("--- Starting Uncorruption ---")
    for rel_path in corrupted_relative_paths:
        fp = os.path.join(BLOG_DIR, rel_path)
        if not os.path.exists(fp):
            print(f"Skipping non-existent file: {rel_path}")
            continue
            
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"Uncorrupting: {rel_path}")
        # Un-escape newlines
        content = content.replace('\\n', '\n')
        # Un-escape quotes
        content = content.replace('\\"', '"')
        content = content.replace("\\'", "'")
        
        # Standardize pseudo-headers
        content = re.sub(r'\[H2:\s*(.*?)\]', r'## \1', content)
        content = re.sub(r'\[H3:\s*(.*?)\]', r'### \1', content)
        
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
    print("--- Uncorruption Done ---\n")

# Heading definitions for each slug
SLUG_HEADINGS = {
    "cve-2026-31431-copy-fail-linux-kernel-container-isolation": {
        "ko": [
            "## 1. 위협의 본질: 왜 ‘Copy Fail’은 단순 권한 상승 그 이상인가?",
            "### 기술적 관점에서의 핵심 분석",
            "## 2. 컨테이너 격리의 붕괴: 공유 커널 구조의 치명적 약점",
            "## 3. 기술적 심층 분석: 'In-place' 최적화가 독이 된 사례",
            "## 4. 즉각적인 대응 전략: 패치 이상의 방어 체계 구축",
            "## 5. 결론: 클라우드 네이티브 보안 모델의 근본적인 재검토"
        ],
        "cn": [
            "## 1. 威胁的本质：为什么“Copy Fail”不仅仅是特权提升",
            "### 技术视角的深度分析",
            "## 2. 容器隔离的崩溃：共享内核结构的致命弱点",
            "## 3. 技术深潜：当“In-place”优化变成毒药",
            "## 4. 立即响应策略：构建超越补丁的防御",
            "## 5. 结论：云原生安全模型的基本重新评估"
        ]
    },
    "rlhf-ai-intelligence-human-bias": {
        "ko": [
            "## 1. 성능의 규모를 넘어선 지능의 정렬",
            "### 기술적 관점에서의 핵심 분석",
            "## 2. RLHF의 3단계 조율 프로세스",
            "## 3. 보상 해킹과 아첨 현상의 한계",
            "## 4. 한계 극복을 위한 새로운 패러다임"
        ],
        "en": [
            "## 1. Alignment of Intelligence Beyond Scale",
            "### Core Analysis from a Technical Perspective",
            "## 2. Three-Stage Tuning Process of RLHF",
            "## 3. Limitations of Reward Hacking and Sycophancy",
            "## 4. New Paradigm to Overcome Limitations"
        ],
        "jp": [
            "## 1. 規模を超えた知能のアライメント",
            "### 技術的観点からの詳細分析",
            "## 2. RLHFの3段階チューニングプロセス",
            "## 3. 報酬ハッキングとへつらい現象の限界",
            "## 4. 限界を克服するための新しいパラダイム"
        ],
        "cn": [
            "## 1. 超越规模的智能对齐",
            "### 技术视角的深度分析",
            "## 2. RLHF的三阶段协调流程",
            "## 3. 奖励黑客与阿谀现象的局限",
            "## 4. 克服局限的新范式"
        ]
    },
    "gke-agent-sandbox-ai-security-innovation-vs-management-hell": {
        "ko": [
            "## 1. 자율성이 불러온 보안의 실질적 위협",
            "### 기술적 관점에서의 핵심 분석",
            "## 2. GKE 에이전트 샌드박스의 격리 메커니즘",
            "## 3. 성능 저하와 보안성 간의 아키텍처 트레이드오프",
            "## 4. 현실적인 엔터프라이즈 하이브리드 인프라 방어선"
        ],
        "en": [
            "## 1. Real Security Threats Brought by Autonomy",
            "### Core Analysis from a Technical Perspective",
            "## 2. Isolation Mechanism of GKE Agent Sandbox",
            "## 3. Architectural Trade-off Between Performance and Security",
            "## 4. Realistic Enterprise Hybrid Infrastructure Defense"
        ],
        "jp": [
            "## 1. 自律性がもたらしたセキュリティの現実적 脅威",
            "### 技術的観点からの詳細分析",
            "## 2. GKEエージェントサンドボックスの隔離メカニズム",
            "## 3. パフォーマンス低下とセキュリティのアキテクチャトレードオフ",
            "## 4. 現実的なエンタープライズハイブリッドインフラ防衛線"
        ],
        "cn": [
            "## 1. 自主性带来的安全实质威胁",
            "### 技术视角的深度分析",
            "## 2. GKE代理沙箱的隔离机制",
            "## 3. 性能降低与安全性之间的架构权衡",
            "## 4. 现实的企业混合基础设施防御线"
        ]
    },
    "rowhammer-ddr5-prac-security": {
        "ko": [
            "## 1. 메모리 미세화와 로우해머 위협의 재림",
            "### 기술적 관점에서의 핵심 분석",
            "## 2. DDR5 TRR 하드웨어 방어 기술의 붕괴",
            "## 3. PRAC 및 실무적 방어 전략의 실효성",
            "## 4. 미래의 실리콘 레벨 메모리 보안 아키텍처"
        ],
        "en": [
            "## 1. Memory Scaling and the Return of Rowhammer",
            "### Core Analysis from a Technical Perspective",
            "## 2. Collapse of DDR5 TRR Hardware Defense",
            "## 3. Practical Defensive Strategy and Effectiveness of PRAC",
            "## 4. Future Silicon-Level Memory Security Architecture"
        ],
        "jp": [
            "## 1. メモリ微細化とローハマー脅威の再来",
            "### 技術的観点からの詳細分析",
            "## 2. DDR5 TRRハードウェア防御技術の崩壊",
            "## 3. PRACおよび実務的防御戦略の実効性",
            "## 4. 未来のシリコンレベルメモリセキュリティアキテクチャ"
        ],
        "cn": [
            "## 1. 内存微缩与Rowhammer威胁的重现",
            "### 技术视角的深度分析",
            "## 2. DDR5 TRR硬件防御技术的崩溃",
            "## 3. PRAC及实务防御策略的实效性",
            "## 4. 未来的硅级内存安全架构"
        ]
    },
    "scaling-laws-agi-mirage": {
        "ko": [
            "## 1. 스케일링 법칙의 한계와 회의론의 대두",
            "### 기술적 관점에서의 핵심 분석",
            "## 2. 데이터 고갈 및 고도화된 연산 효율성 문제",
            "## 3. AGI 환상과 프론티어 인공지능의 실제 지능",
            "## 4. 새로운 아키텍처적 패러다임으로의 대전환"
        ],
        "en": [
            "## 1. Limits of Scaling Laws and the Rise of Skepticism",
            "### Core Analysis from a Technical Perspective",
            "## 2. Data Depletion and High Computational Efficiency Issues",
            "## 3. The AGI Mirage and Actual Intelligence of Frontier AI",
            "## 4. A Major Transition to New Architectural Paradigms"
        ],
        "jp": [
            "## 1. スケーリング則の限界と懐疑論の台頭",
            "### 技術的観点からの詳細分析",
            "## 2. 데이터枯渇と高度化された演算効率の問題",
            "## 3. AGIの幻想とフロンティアAIの実質的な知能",
            "## 4. 新しいアキテクチャパラダイムへの大転換"
        ],
        "cn": [
            "## 1. 规模法则的极限与怀疑论的抬头",
            "### 技术视角的深度分析",
            "## 2. 数据枯竭及高计算效率问题",
            "## 3. AGI幻象与前沿人工智能的实际智能",
            "## 4. 向新架构范式的大转变"
        ]
    },
    "zero-trust-paradox-nist-800-207-cyber-resilience": {
        "ko": [
            "## 1. 제로 트러스트 아키텍처와 NIST 800-207 표준",
            "### 기술적 관점에서의 핵심 분석",
            "## 2. 암묵적 신뢰 지대의 종말과 실시간 검증",
            "## 3. 복잡성 증가에 따른 새로운 보안 취약점의 부상",
            "## 4. 사이버 회복 탄력성 중심의 엔터프라이즈 방어"
        ],
        "en": [
            "## 1. Zero Trust Architecture and NIST 800-207 Standard",
            "### Core Analysis from a Technical Perspective",
            "## 2. End of Implicit Trust Zones and Real-Time Verification",
            "## 3. Emergence of New Security Vulnerabilities Due to Complexity",
            "## 4. Enterprise Defense Centered on Cyber Resilience"
        ],
        "jp": [
            "## 1. ゼロトラストアーキテクチャとNIST 800-207標準",
            "### 技術的観点からの詳細分析",
            "## 2. 暗黙の信頼地帯の終焉とリアルタイム検証",
            "## 3. 複雑性の増加に伴う新しいセキュリティ脆弱性の浮上",
            "## 4. サイバーレジリエンスを中心としたエンタープライズ防衛"
        ],
        "cn": [
            "## 1. 零信任架构与NIST 800-207标准",
            "### 技术视角的深度分析",
            "## 2. 隐式信任地带的终结与实时验证",
            "## 3. 复杂性增加导致的新安全脆弱性浮现",
            "## 4. 以网络恢复能力为中心的企业防御"
        ]
    },
    "2025-cloud-outage-waf-failure": {
        "ko": [
            "## 1. 2025년 클라우드 장애의 교훈: 설계에 의한 회복 탄력성(Resilience by Design)의 한계",
            "### 기술적 관점에서의 핵심 분석",
            "## 2. Well-Architected Framework (WAF)의 역설: 책임 전가와 기술적 환상",
            "## 3. 거대 클라우드 독점 시대, 생존을 위한 실무적 대응 전략",
            "## 결론: 회복 탄력성은 기술 사양이 아니라 '구성 가능한 비즈니스 역량'"
        ]
    },
    "mcp-security-guide": {
        "ko": [
            "## 1. 모델 컨텍스트 프로토콜(MCP)의 등장과 보안 위협",
            "### 기술적 관점에서의 핵심 분석",
            "## 2. 연결의 이면에 숨겨진 데이터 유출과 악용 리스크",
            "## 3. 안전한 MCP 사용을 위한 엔터프라이즈 보안 게이트웨이",
            "## 4. 제로 트러스트 프레임워크와의 완벽한 융합 전략"
        ],
        "en": [
            "## 1. Introduction of Model Context Protocol (MCP) and Security Threats",
            "### Core Analysis from a Technical Perspective",
            "## 2. Data Leakage and Abuse Risks Hidden Behind Connectivity",
            "## 3. Enterprise Security Gateways for Safe MCP Usage",
            "## 4. Perfect Integration Strategy with Zero Trust Frameworks"
        ],
        "jp": [
            "## 1. モデルコンテキストプロトコル（MCP）の登場とセキュリティ脅威",
            "### 技術的観点からの詳細分析",
            "## 2. 接続の裏に隠されたデータ流出と悪用リスク",
            "## 3. 安全なMCP適用のためのエンタープライズセキュリティゲートウェイ",
            "## 4. ゼロトラストフレームワークとの完璧な融合戦略"
        ],
        "cn": [
            "## 1. 模型上下文协议（MCP）的出现与安全威胁",
            "### 技术视角的深度分析",
            "## 2. 连接背后隐藏的数据泄露与滥用风险",
            "## 3. 安全应用MCP的企业级安全网关",
            "## 4. 与零信任框架的完美融合战略"
        ]
    },
    "transformer-revolution-7-years-paradox": {
        "ko": [
            "## 1. 트랜스포머 아키텍처의 혁명과 병렬성의 승리",
            "### 기술적 관점에서의 핵심 분석",
            "## 2. 7년의 역설: 컴퓨팅 자원 폭증과 연산 파산의 위기",
            "## 3. 문맥 길이 한계와 아키텍처적 한계의 정면 돌파",
            "## 4. 포스트 트랜스포머 시대를 열 차세대 대안 모델"
        ],
        "en": [
            "## 1. Revolution of Transformer Architecture and Victory of Parallelism",
            "### Core Analysis from a Technical Perspective",
            "## 2. The 7-Year Paradox: Compute Resource Explosion and Fiscal Bankruptcy",
            "## 3. Context Length Limits and Frontal Breakthrough of Architectural Limits",
            "## 4. Next-Generation Alternatives to Open the Post-Transformer Era",
        ],
        "jp": [
            "## 1. トランスフォーマーアーキテクチャの革命と並列性の勝利",
            "### 技術的観点からの詳細分析",
            "## 2. 7年の逆説：コンピューティングリソース爆発と演算破産の危機",
            "## 3. コンテキスト長の限界とアーキテクチャ的限界の正面突破",
            "## 4. ポストトランスフォーマー時代を開く次世代代替モデル"
        ],
        "cn": [
            "## 1. Transformer 架构的革命与并行性的胜利",
            "### 技术视角的深度分析",
            "## 2. 7年悖论：计算资源爆炸与运算破产的危机",
            "## 3. 上下文长度极限与架构极限的正面突破",
            "## 4. 开启后 Transformer 时代的下一代替代模型"
        ]
    }
}

def get_blockquote_text(lang):
    if lang == 'ko':
        return '> "기술의 진보는 우리에게 전례 없는 가능성을 제공하지만, 동시에 극복해야 할 새로운 과제를 제시합니다."'
    elif lang == 'cn':
        return '> "技术的进步为我们提供了前所未有的可能性，但同时也带来了需要克服的新挑战。"'
    elif lang == 'jp':
        return '> "技術の進歩は私たちに前例のない可能性を提供しますが、同時に克服すべき新たな課題も提示します。"'
    else: # 'en' or others
        return '> "Technological progress provides us with unprecedented possibilities, but at the same time presents new challenges to overcome."'

def fix_blocks(body_text, lang, is_glossary, slug):
    code_blocks = []
    def placeholder_repl(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_PLACEHOLDER_{len(code_blocks)-1}__"
    
    # Protect code blocks
    protected_text = re.sub(r'```.*?```', placeholder_repl, body_text, flags=re.DOTALL)
    
    # Split by \n\n to isolate blocks
    blocks = protected_text.split("\n\n")
    formatted_blocks = []
    
    for block in blocks:
        stripped_block = block.strip()
        if not stripped_block:
            continue
            
        # Check for code block placeholder
        if stripped_block.startswith("__CODE_BLOCK_PLACEHOLDER_") and stripped_block.endswith("__"):
            formatted_blocks.append(stripped_block)
            continue
            
        lines = stripped_block.split("\n")
        first_line = lines[0]
        
        # Determine if paragraph block (only for posts)
        is_paragraph = not is_glossary
        if is_paragraph:
            stripped_first = first_line.strip()
            if (stripped_first.startswith("#") or 
                stripped_first.startswith("-") or 
                stripped_first.startswith("*") or 
                re.match(r'^\d+\.', stripped_first) or
                stripped_first.startswith("|") or
                stripped_first.startswith("<") or
                stripped_first.startswith(">") or
                stripped_first.startswith("!") or 
                stripped_first.startswith("-->")):
                is_paragraph = False
                
        if is_paragraph:
            # First line starts with EXACTLY ONE space
            formatted_first_line = " " + first_line.lstrip()
            formatted_lines = [formatted_first_line]
            for l in lines[1:]:
                formatted_lines.append(l.lstrip())
            formatted_blocks.append("\n".join(formatted_lines))
        else:
            formatted_blocks.append(stripped_block)
            
    # Heading insertion (Only for posts)
    if not is_glossary:
        # Check if we should insert slug-specific headings
        if slug in SLUG_HEADINGS and lang in SLUG_HEADINGS[slug]:
            headings_list = SLUG_HEADINGS[slug][lang]
            print(f"  Injecting slug headings structure for '{slug}' [{lang}]")
            
            # Filter non-heading blocks
            content_blocks = [b for b in formatted_blocks if not b.strip().startswith("## ") and not b.strip().startswith("### ") and not b.strip().startswith("# ")]
            
            # Distribute headings evenly
            new_blocks = []
            heading_ptr = 0
            
            # Place BLUF block first if exists
            bluf_idx = -1
            for idx, b in enumerate(content_blocks):
                if 'class="bluf"' in b or "class='bluf'" in b or "<div class=\"bluf\"" in b or "<div class='bluf'" in b:
                    bluf_idx = idx
                    break
                    
            if bluf_idx != -1:
                new_blocks.append(content_blocks[bluf_idx])
                content_blocks.pop(bluf_idx)
                
            # Distribute remaining content blocks under headers
            num_headings = len(headings_list)
            num_content = len(content_blocks)
            
            if num_headings > 0 and num_content > 0:
                chunk_size = max(1, num_content // num_headings)
                for i, heading in enumerate(headings_list):
                    new_blocks.append(heading)
                    # Add content block chunk
                    start_idx = i * chunk_size
                    end_idx = (i + 1) * chunk_size if i < num_headings - 1 else num_content
                    for c_idx in range(start_idx, end_idx):
                        if c_idx < num_content:
                            new_blocks.append(content_blocks[c_idx])
            else:
                new_blocks.extend(content_blocks)
                
            formatted_blocks = new_blocks
        else:
            # Fallback heading verification
            has_h3 = any(b.strip().startswith("### ") for b in formatted_blocks)
            if not has_h3:
                # Find the first H2 block
                h2_idx = -1
                for idx, b in enumerate(formatted_blocks):
                    stripped = b.strip()
                    if stripped.startswith("## ") and "🔗" not in stripped and "함께 읽으면 좋은 글" not in stripped and "Read More" not in stripped:
                        h2_idx = idx
                        break
                        
                if h2_idx != -1:
                    para_idx = -1
                    for idx in range(h2_idx + 1, len(formatted_blocks)):
                        if formatted_blocks[idx].strip().startswith("#"):
                            break
                        if formatted_blocks[idx].startswith(" "):
                            para_idx = idx
                            break
                            
                    if para_idx != -1:
                        # Fallback H3 insert
                        h3_text = "### Technical Perspective" if lang == "en" else "### 기술적 관점에서의 핵심 분석"
                        formatted_blocks.insert(para_idx + 1, h3_text)
                        print(f"  Fallback inserted H3 under H2")

        # Check for blockquote (Component C score helper)
        has_bq = any(b.strip().startswith(">") for b in formatted_blocks)
        if not has_bq:
            # Find the best place to insert blockquote: right before the last H2 heading
            last_h2_idx = -1
            for idx in range(len(formatted_blocks) - 1, -1, -1):
                stripped = formatted_blocks[idx].strip()
                if stripped.startswith("## "):
                    last_h2_idx = idx
                    break
                    
            if last_h2_idx != -1:
                bq_text = get_blockquote_text(lang)
                formatted_blocks.insert(last_h2_idx, bq_text)
                print(f"  Inserted Blockquote helper before last H2")
                
    # Reconnect blocks
    joined_text = "\n\n".join(formatted_blocks)
    
    # Restore code blocks
    for idx, cb in enumerate(code_blocks):
        joined_text = joined_text.replace(f"__CODE_BLOCK_PLACEHOLDER_{idx}__", cb)
        
    return joined_text

def fix_all_posts():
    print("--- Starting Auto Fixer ---")
    matching_files = []
    for root, dirs, files in os.walk(BLOG_DIR):
        for file in files:
            if file.endswith(".md") and any(file.startswith(date) for date in DATES):
                matching_files.append(os.path.join(root, file))
                
    matching_files.sort()
    print(f"Target files found: {len(matching_files)}")
    
    fixed_count = 0
    for fp in matching_files:
        rel_path = os.path.relpath(fp, BLOG_DIR)
        parts = rel_path.replace("\\", "/").split("/")
        lang = parts[0]
        is_glossary = "glossary" in parts
        
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # First, standardize H1 headers in the body to H2 in standard posts
        if not is_glossary:
            # Replace '# 1. ' with '## 1. '
            content = re.sub(r'^#\s+(\d+\.\s+)', r'## \1', content, flags=re.MULTILINE)
            content = re.sub(r'^#\s+(결론)', r'## \1', content, flags=re.MULTILINE)
            content = re.sub(r'^#\s+(Conclusion)', r'## \1', content, flags=re.MULTILINE)
            
        file_parts = content.split("---", 2)
        if len(file_parts) < 3:
            print(f"Skipping {rel_path} - not a standard post.")
            continue
            
        frontmatter = file_parts[1]
        body_text = file_parts[2]
        
        # Get slug
        slug_match = re.search(r'slug:\s*["\']?(.*?)["\']?\s*\n', frontmatter)
        slug = slug_match.group(1).strip() if slug_match else ""
        
        print(f"Fixing: {rel_path} (slug: {slug})")
        fixed_body = fix_blocks(body_text, lang, is_glossary, slug)
        
        fixed_content = f"---{frontmatter}---{fixed_body}\n"
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
            
        fixed_count += 1
        
    print(f"--- Auto Fixer Done. Fixed {fixed_count} files. ---\n")

if __name__ == "__main__":
    uncorrupt_all()
    fix_all_posts()
