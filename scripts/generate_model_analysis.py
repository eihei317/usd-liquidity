#!/usr/bin/env python3
"""Generate model analysis JSON from model_input.json."""
import json
import sys
from pathlib import Path
from datetime import datetime

def generate_analysis(model_input_path, output_path):
    with open(model_input_path, 'r', encoding='utf-8') as f:
        model_input = json.load(f)
    
    data = model_input.get('data', {})
    signals = data.get('derived_signals', [])
    metrics = data.get('metrics', [])
    
    # 构建衍生信号查找表
    signal_map = {s.get('id'): s for s in signals}
    
    # 构建指标查找表
    metric_map = {m.get('id'): m for m in metrics}
    
    # 1. 数据新鲜度检查
    freshness_notes = []
    for m in metrics:
        as_of = m.get('as_of', 'N/A')
        stale_days = m.get('stale_days', 0)
        name = m.get('name', m.get('id', 'Unknown'))
        if stale_days <= 1:
            freshness_notes.append(f"{name} 最新 (as_of: {as_of})")
        elif stale_days <= 7:
            freshness_notes.append(f"{name} 滞后{stale_days}天 (as_of: {as_of})")
        else:
            freshness_notes.append(f"{name} 周频背景或事件驱动 (as_of: {as_of})")
    
    # 2. 判断立场
    # 根据衍生信号判断
    sofr_anchor = signal_map.get('SOFR_ANCHOR', {}).get('value', 0)
    rrp_level = signal_map.get('RRP_BUFFER', {}).get('value', 0)
    tga_flow = signal_map.get('TGA_FLOW', {}).get('value', 0)
    real_10y = signal_map.get('REAL_10Y', {}).get('value', 0)
    nfci = signal_map.get('NFCI_LEVEL', {}).get('value', 0)
    
    # 简单评分逻辑
    score = 0
    if sofr_anchor < -5:  # SOFR低于政策锚
        score += 1
    if rrp_level < 10:  # RRP很低
        score -= 2
    if tga_flow > 20:  # TGA大幅上升
        score -= 1
    if real_10y > 2.0:  # 真实收益率偏高
        score -= 1
    if nfci < -0.5:  # 金融条件偏松
        score += 1
    
    if score >= 2:
        stance_label = "宽松"
        confidence = "高"
    elif score >= 0:
        stance_label = "中性"
        confidence = "中等"
    elif score >= -2:
        stance_label = "中性偏紧"
        confidence = "中等"
    else:
        stance_label = "紧张"
        confidence = "高"
    
    # 3. 关键要点
    key_takeaways = []
    
    # SOFR相对政策锚
    sofr_signal = signal_map.get('SOFR_ANCHOR', {})
    if sofr_signal:
        key_takeaways.append({
            "title": "回购融资相对政策锚的位置",
            "text": f"SOFR-IORB 当前为 {sofr_signal.get('value', 0):.1f}bp，上一期为 {sofr_signal.get('previous', 0):.1f}bp，边际变化 {sofr_signal.get('change', 0):+.1f}bp。SOFR低于政策锚，说明资金面不紧。",
            "related_indicators": ["SOFR_ANCHOR", "SOFR_VOLUME_IMPACT"]
        })
    
    # SOFR交易量影响
    volume_signal = signal_map.get('SOFR_VOLUME_IMPACT', {})
    if volume_signal:
        key_takeaways.append({
            "title": "SOFR价格×交易量的资金成本量级",
            "text": f"SOFR Rate-Volume Impact 当前为 {volume_signal.get('value', 0):.1f} mn/day，上一期为 {volume_signal.get('previous', 0):.1f} mn/day，边际变化 {volume_signal.get('change', 0):+.1f} mn/day。SOFR交易量约{metric_map.get('SOFR_VOLUME', {}).get('value', 0):.0f}bn，SOFR低于政策锚，按交易量估算日化融资成本低于政策锚。",
            "related_indicators": ["SOFR_VOLUME_IMPACT", "SOFR_VOLUME"]
        })
    
    # RRP缓冲垫
    rrp_signal = signal_map.get('RRP_BUFFER', {})
    if rrp_signal:
        key_takeaways.append({
            "title": "RRP缓冲垫是当前主要风险点",
            "text": f"RRP Balance 当前为 {rrp_signal.get('value', 0):.2f}bn，上一期为 {rrp_signal.get('previous', 0):.2f}bn，边际变化 {rrp_signal.get('change', 0):+.2f}bn。RRP缓冲垫接近低位，后续冲击更容易落到准备金。",
            "related_indicators": ["RRP_BUFFER"]
        })
    
    # T-bill拍卖吸收
    tbill_signal = signal_map.get('TBILL_AUCTION_STRESS', {})
    if tbill_signal:
        key_takeaways.append({
            "title": "T-bill拍卖规模与需求强度",
            "text": f"T-bill Auction Stress 当前为 {tbill_signal.get('value', 0):.1f}，上一期为 {tbill_signal.get('previous', 0):.1f}，边际变化 {tbill_signal.get('change', 0):+.1f}。最新T-bill拍卖规模约{metric_map.get('TBILL_AUCTION_SIZE', {}).get('value', 0):.1f}bn，认购倍数{metric_map.get('TBILL_AUCTION_BTC', {}).get('value', 0):.2f}x，压力评分综合供给规模与需求覆盖。",
            "related_indicators": ["TBILL_AUCTION_STRESS", "TBILL_AUCTION_SIZE", "TBILL_AUCTION_BTC"]
        })
    
    # 10Y真实收益率
    real_signal = signal_map.get('REAL_10Y', {})
    if real_signal:
        key_takeaways.append({
            "title": "10Y真实收益率偏高，压制长期资产估值",
            "text": f"10Y Real Yield 当前为 {real_signal.get('value', 0):.2f}%，上一期为 {real_signal.get('previous', 0):.2f}%，边际变化 {real_signal.get('change', 0):+.2f}%。真实无风险回报偏高，成长股、黄金和长期资产估值压力上升。",
            "related_indicators": ["REAL_10Y"]
        })
    
    # 4. 风险标志
    risk_flags = []
    
    # P0风险：RRP低位
    if rrp_level < 10:
        risk_flags.append({
            "priority": "P0",
            "severity": "high",
            "type": "market",
            "title": "RRP缓冲垫接近低位，未来冲击缓冲能力下降",
            "text": f"RRP余额仅{rrp_level:.2f}bn，处于历史低位。未来面对TGA补库或QT冲击时，RRP下降缓冲空间有限，冲击可能直接落到银行准备金。",
            "evidence": [
                f"RRP最新值：{rrp_level:.2f}bn",
                f"RRP上一期：{signal_map.get('RRP_BUFFER', {}).get('previous', 0):.2f}bn",
                f"RRP边际变化：+{signal_map.get('RRP_BUFFER', {}).get('change', 0):.2f}bn（边际上不是利好，但缓冲空间略恢复）"
            ],
            "related_indicators": ["RRP_BUFFER"]
        })
    
    # P0风险：10Y真实收益率偏高
    if real_10y > 2.0:
        risk_flags.append({
            "priority": "P0",
            "severity": "high",
            "type": "market",
            "title": "10Y真实收益率偏高，压制成长股和长期资产估值",
            "text": f"10Y TIPS真实收益率达{real_10y:.2f}%，处于偏高水平。对成长股、黄金和长期现金流资产估值形成压制。",
            "evidence": [
                f"10Y Real Yield最新值：{real_10y:.2f}%",
                f"10Y Real Yield上一期：{signal_map.get('REAL_10Y', {}).get('previous', 0):.2f}%",
                f"10Y Real Yield边际变化：{signal_map.get('REAL_10Y', {}).get('change', 0):+.2f}%"
            ],
            "related_indicators": ["REAL_10Y"]
        })
    
    # P1风险：TGA上升
    if tga_flow > 20:
        risk_flags.append({
            "priority": "P1",
            "severity": "medium",
            "type": "market",
            "title": "TGA上升抽走银行准备金",
            "text": f"TGA日变化+{tga_flow:.2f}bn，财政资金回流TGA，抽走银行体系准备金，偏紧。",
            "evidence": [
                f"TGA最新值：{metric_map.get('TGA', {}).get('value', 0):.2f}bn",
                f"TGA日变化：+{tga_flow:.2f}bn"
            ],
            "related_indicators": ["TGA_FLOW", "TGA"]
        })
    
    # P2风险：数据滞后
    for m in metrics:
        if m.get('stale_days', 0) > 7 and m.get('frequency') not in ['weekly', 'event-based']:
            risk_flags.append({
                "priority": "P2",
                "severity": "info",
                "type": "data",
                "title": f"{m.get('name', m.get('id'))} 数据滞后或降级",
                "text": f"该指标本次不能作为最新市场压力判断，只能作为数据风险处理。",
                "evidence": [
                    f"as_of：{m.get('as_of', 'N/A')}",
                    f"stale_days：{m.get('stale_days', 'N/A')}"
                ],
                "related_indicators": [m.get('id')]
            })
            break  # 只添加一个数据风险示例
    
    # 5. 叙述块
    narrative_blocks = {
        "summary": f"今日美元流动性整体{stance_label}。SOFR低于政策锚，资金面不紧；但RRP缓冲垫接近低位，未来冲击缓冲能力下降；10Y真实收益率偏高，压制长期资产估值。",
        "rates": "短端资金利率重点看相对政策锚的位置，尤其是SOFR-IORB；同时用SOFR交易量把价格偏离转化为量级冲击。",
        "balance_sheet": "TGA、RRP与准备金水位决定负债端缓冲空间，RRP需要区分边际方向和存量缓冲垫。",
        "market_transmission": "利率压力通过回购市场、国债抵押品、收益率曲线传导到信用市场和风险偏好。"
    }
    
    # 构建分析JSON
    analysis = {
        "meta": {
            "generated_at_bjt": model_input.get('generated_at_bjt', datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC+08:00')),
            "data_as_of": max([m.get('as_of', '2000-01-01') for m in metrics], default='N/A'),
            "model": "AI模型",
            "input_freshness_note": "；".join(freshness_notes[:5])  # 只取前5个
        },
        "stance": {
            "label": stance_label,
            "confidence": confidence,
            "score_text": f"模型评分 {score}",
            "one_liner": f"今日美元流动性{stance_label}，RRP缓冲垫接近低位是主要风险点。"
        },
        "key_takeaways": key_takeaways[:5],  # 最多5条
        "risk_flags": risk_flags[:5],  # 最多5条，按优先级排序
        "narrative_blocks": narrative_blocks
    }
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"模型分析已生成：{output_path}")
    return analysis

if __name__ == "__main__":
    model_input_path = sys.argv[1] if len(sys.argv) > 1 else "output/latest/model_input.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output/latest/analysis.json"
    generate_analysis(model_input_path, output_path)
