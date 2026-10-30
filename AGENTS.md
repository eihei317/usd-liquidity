# 美元流动性监控
唯一部署为本目录。使用 .runtime/python/python.exe -B -X utf8 -u scripts/pipeline.py。
更新通过pipeline update；重新分析通过pipeline reanalyze；先status检查，不并发修改。
历史：官方源长历史抓取→历史逐项审计→按同一观测日期重建所有可计算派生信号→入库→绘图。禁止一条派生值遮蔽底层完整历史。history_coverage.json必须保留并显示所有缺口，源未提供历史不得补零或用最新值倒填。
GitHub：用户授权每次抓完将捕获数据推送到 https://github.com/eihei317/usd-liquidity ，分析结束再推结果。必须使用scripts/sync_to_github.py，保存导出哈希并验证远端提交；失败明确报错，不能宣称同步成功。抓取/推送/模型分析用已批准的网络执行路径，凭据留本机。
通过校验及GitHub同步后才切换output/current.json。失败保留上次完整结果；不修改旧run产物；支持rollback。
数据和模型结果均为研究资料，回抓历史不是历史当时可见版本；不宣称已验证投资预测优势。
