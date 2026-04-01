# 领导.skill

> "这个事情很简单，你今天先弄一下，明天老板要看，细节我们后面再对齐。"

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-f1c40f?style=for-the-badge" alt="License MIT" />
  <img src="https://img.shields.io/badge/Python-3.11+-3498db?style=for-the-badge" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/Claude%20Code-Skill-8e44ad?style=for-the-badge" alt="Claude Code Skill" />
  <img src="https://img.shields.io/badge/AgentSkills-Standard-9acd32?style=for-the-badge" alt="AgentSkills Standard" />
</p>

你的领导说“先看一下”，其实是今晚交初稿？  
你的老板说“不复杂吧”，其实是需求还没定，但默认你先做？  
你的直属说“我们再对齐一下”，其实是口径、责任、验收都没锁？  
你的大领导半夜来一句“明天老板要看”，其实是全员今晚别睡？

**将模糊的圣意化为清晰的行动，将职场黑话转成可执行的 Skill，欢迎加入赛博升职。**

提供领导的原材料（飞书消息、钉钉文档、邮件、截图、会议纪要）加上你的主观描述  
生成一个真正能帮你理解领导、回复领导、预判风险、提前自保的 AI Skill  
用他的语气理解问题，用他的节奏安排优先级，知道他什么时候在画饼、什么时候在找人垫刀

[数据来源](#支持的数据来源) · [安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [详细安装说明](./INSTALL.md) · [English](./README_EN.md)

---

## 灵感来源

这个项目的表达方式和信息架构，直接参考了：

- [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)
- [therealXiaomanChu/ex-skill](https://github.com/therealXiaomanChu/ex-skill)

思路上尽量复刻它们那种：

- 第一屏就把情绪和场景打满
- 纯文本也能排得清楚、密、顺
- 先让人想笑，再让人觉得“这玩意真能用”

不同的是，这次我们分析的对象不是同事，不是前任，而是最影响你排期、绩效、情绪价值和加班概率的那个人：**领导**。

---

## 支持的数据来源

> 当前版本坚持 `local-first`。优先让你用手上已经有的材料，而不是强迫你接复杂的在线权限。

| 数据来源 | 当前状态 | 获取方式 | 备注 |
| --- | --- | --- | --- |
| 领导原话文本 | 已支持 | 手动粘贴 | 最适合快速试用 |
| 飞书 / 钉钉截图 | 已支持 | 图片 + OCR sidecar | 建议先打码 |
| Markdown / TXT 纪要 | 已支持 | 本地文件导入 | 适合会议纪要、项目记录 |
| PDF 文档 | 已支持 | 本地文件导入 | 适合通知、汇报材料、附件 |
| `.eml` / `.mbox` 邮件 | 已支持 | 本地文件导入 | 适合邮件往来归档 |
| 聊天导出 JSON | 已支持 | 本地文件导入 | 适合协作平台导出 |
| 飞书 / 钉钉在线自动采集 | 规划中 | 后续迭代 | 首发不强依赖在线权限 |

---

## 安装

### Claude Code

> 重要：Claude Code 默认从 `.claude/skills/` 目录发现 Skill。

当前项目安装：

```bash
mkdir -p .claude/skills
git clone https://github.com/Dewensong/leader-skill .claude/skills/create-leader
```

全局安装：

```bash
git clone https://github.com/Dewensong/leader-skill ~/.claude/skills/create-leader
```

### 本地 CLI 试玩

```bash
git clone https://github.com/Dewensong/leader-skill.git
cd leader-skill
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py"
```

---

## 使用

### 快速体验一句领导黑话

```bash
python -m tools.cli translate --text "这个你先看一下，晚点我们再对齐。"
```

### 创建一个领导画像

```bash
python -m tools.cli create-leader \
  --slug sharp-director \
  --name "高压型总监" \
  --text "这个不复杂吧，你今天先出个方案，明天我们同步一下。"
```

### 查看这个领导的完整画像

```bash
python -m tools.cli show-leader --slug sharp-director
```

### 删除一个领导实例

```bash
python -m tools.cli delete-leader --slug sharp-director --yes
```

### 管理命令

| 命令 | 说明 |
| --- | --- |
| `python -m tools.cli create-leader` | 创建一个新领导画像 |
| `python -m tools.cli list-leaders` | 查看已有领导实例 |
| `python -m tools.cli show-leader` | 查看完整领导画像 bundle |
| `python -m tools.cli translate` | 领导黑话翻译 |
| `python -m tools.cli priority` | 优先级判断 |
| `python -m tools.cli persona` | 领导画像摘要 |
| `python -m tools.cli reply` | 建议回复 + 建议追问 |
| `python -m tools.cli risk` | 风险分析 |
| `python -m tools.cli promotion` | 向上管理建议 |
| `python -m tools.cli leader-rollback` | 回滚到旧版本 |
| `python -m tools.cli delete-leader` | 删除实例 |

### 对应的 slash command 设计

```text
/create-leader
/list-leaders
/{slug}
/{slug}-translate
/{slug}-priority
/{slug}-reply
/{slug}-risk
/{slug}-promotion
/leader-rollback {slug} {version}
/delete-leader {slug}
```

---

## 效果示例

> 下面的风格，刻意向 `colleague-skill` 和 `ex-skill` 靠拢，尽量做到“光看 README 就想玩一下”。

### 场景一：领导说“这个你先看一下”

```text
用户      ❯ 帮我理解一下这句：这个你先看一下，晚点我们再对齐。

领导.skill ❯ 这不是“有空的时候看看”
             而是希望你先垫一版能讨论的东西
             今晚最好给初稿，明天同步时锁范围、优先级和验收标准
```

### 场景二：领导说“这个不复杂吧”

```text
用户      ❯ 领导说：这个不复杂吧，你今天先出个方案，明天我们同步一下。

领导.skill ❯ “不复杂”通常不代表简单
             通常代表需求还没完全定义，但默认你先做
             这时候最危险的不是做不完
             是你先承诺了，明天再被改口
```

### 场景三：帮我回一句

```text
用户      ❯ 那我应该怎么回？

领导.skill ❯ 我先按当前理解出一版方案，今晚给你可评审版本
             同时把目标、范围和验收标准整理出来
             明天同步时我们一起确认，避免后续返工
```

### 场景四：预判是不是要背锅

```text
用户      ❯ 这句话危险吗：这个你灵活处理一下。

领导.skill ❯ 危险
             这类表达通常意味着他暂时不想明确拍板
             但结果仍然希望由你兜住
             最好立刻追问边界、目标和验收标准
```

### 场景五：先看现成效果

不想先跑命令的话，可以直接打开：

- [examples/demo-leader/README.md](./examples/demo-leader/README.md)
- [examples/demo-leader/persona.md](./examples/demo-leader/persona.md)
- [examples/demo-leader/intent-map.md](./examples/demo-leader/intent-map.md)
- [examples/demo-leader/playbook.md](./examples/demo-leader/playbook.md)

---

## 功能特性

### 生成的 Skill 结构

每个领导实例都会生成一个完整 bundle：

- `README.md`
- `persona.md`
- `intent-map.md`
- `playbook.md`
- `sources.json`
- `corrections.md`
- `versions/`

你可以把它理解成三层结构：

#### Part A - Leader Persona

识别这个领导是什么风格的人：

- 口头优先级高不高
- 会不会会前补需求
- 更重视速度还是质量
- 口径敏不敏感
- 会不会模糊放权但保留追责权

#### Part B - Intent Map

把每句黑话翻译成真实意图：

- 实际意思
- 优先级判断
- 风险点
- 指数分

#### Part C - Survival Playbook

把理解结果转成可执行动作：

- 建议回复
- 建议追问
- 汇报打法
- 向上管理建议

### 支持的标签

#### 领导风格

- 会前补需求
- 口头优先级偏高
- 口径敏感
- 责任边界模糊
- 默认先给初稿
- 时间预期偏紧
- 拖延拍板
- 结果导向
- 细节洁癖
- 画饼能力强

#### 组织氛围

- OKR 驱动
- KPI 驱动
- 赛马机制
- 强汇报文化
- 高压推进
- 先开会再说
- 先立项再补需求

#### 适配的领导层级

- 组长 / TL
- 经理
- 总监
- VP
- 创始人 / CXO

### 进化机制

这个项目不是一次性吐槽，而是可持续纠正和进化的：

- 新增材料后会更新画像
- 纠正信息会沉淀到 `corrections.md`
- 每次变更都会留版本快照
- 可以回滚到旧版本

---

## 项目结构

```text
leader-skill/
├── SKILL.md
├── README.md
├── README_EN.md
├── INSTALL.md
├── assets/
├── docs/
├── examples/
├── prompts/
├── tests/
└── tools/
```

---

## 安全说明

- 默认本地导入、本地分析
- 截图建议先脱敏
- 不鼓励骚扰、伪造、监控或针对真实个人
- 目标是让沟通更清楚，不是让关系更糟

---

## 参考项目

- [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)
- [therealXiaomanChu/ex-skill](https://github.com/therealXiaomanChu/ex-skill)
