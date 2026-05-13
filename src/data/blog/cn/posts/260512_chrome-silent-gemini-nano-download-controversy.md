---
title: "在用户不知情下下载4GB：谷歌Chrome“悄然”安装Gemini Nano与端侧AI的悖论"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-12 11:15:00+09:00
slug: chrome-silent-gemini-nano-download-controversy
featured: false
draft: false
ogImage: "../../../../../source/posts/chrome_silent_gemini_nano/og-image.webp"
description: "谷歌Chrome浏览器因在用户未明示同意的情况下，悄然下载并安装约4GB大小的Gemini Nano端侧AI模型，引发了巨大争议。本文将深入分析这一事件对存储空间和网络带宽的侵占，其隐私利弊，以及彻底禁用并删除该模型的方法。"
references:
- https://www.bleepingcomputer.com/news/google/google-chrome-is-silently-downloading-gemini-nano-ai-model-on-desktops/
- https://www.androidauthority.com/chrome-gemini-nano-download-3465812/
modDatetime: 2026-05-12 11:15:00+09:00
faqs:
- q: 为什么Chrome会在用户没有同意的情况下下载Gemini Nano？
  a: 谷歌旨在让Chrome的端侧AI功能（如“帮我写”、标签页整理、AI历史记录搜索等）直接在用户设备上本地运行，从而在无需向谷歌云端服务器发送数据的情况下提供低延迟与隐私保护。如果用户硬件性能符合要求，浏览器便会在后台自动触发该模型的下载。
- q: 如何确认我的电脑中是否已经安装了该AI模型？
  a: 您可以在Chrome地址栏中输入 `chrome://components`，然后查找“Optimization Guide On Device Model”项目；或者在您的本地Chrome User Data目录中，检查 `OptGuideOnDeviceModel` 文件夹下是否存在一个约4GB大小的 `weights.bin` 文件。
- q: 如果想释放磁盘空间，直接手动删除这个文件夹可以吗？
  a: 仅进行单纯的手动删除是无法彻底解决问题的。如果Chrome内的端侧AI功能或实验性标志（Flags）仍处于启用状态，浏览器在下次启动时依然会自动在后台重新下载这4GB的数据。您必须先禁用相关Flags，然后再删除文件夹。
- q: 这次自动下载为什么会引起如此巨大的争议？
  a: 对于配备128GB或256GB低容量SSD的笔记本用户来说，4GB的磁盘空间非常宝贵。而在使用限额套餐或移动热点的网络环境下，未通知用户便消耗数G流量会带来意料之外的话费。此外，评论者认为此举无视了用户的控制权与知情透明度。
- q: 彻底禁用这些功能并完全清除该模型的步骤是什么？
  a: "访问 chrome://flags，搜索“on-device”或“optimization guide”，将相关Flag设置为“Disabled”，重启Chrome。然后手动进入本地Chrome数据路径，将整个 OptGuideOnDeviceModel 文件夹彻底删除。"
---

<div class="bluf"><strong>[BLUF]</strong><p>谷歌Chrome在未征得用户明示同意的情况下，悄然在后台强制安装4GB大小的端侧AI模型“Gemini Nano”，引发了关于用户知情透明度的激烈争议。虽然此举标榜能增强隐私，但却在实质上侵占了用户的本地存储与网络带宽。本文深度剖析了这一事件带来的资源权衡，并提供了彻底禁用与删除该模型的实操指南。</p></div>

 随着人工智能技术迈向“端侧AI（On-device AI）”时代，将AI模型部署在本地设备上运行已成为不可逆转的趋势。然而，无论技术本身多么令人瞩目，如果它在未经用户许可的情况下悄然强占本地设备资源，它带给用户的感受便将从“创新”沦为“侵犯”。

近日，谷歌Chrome（Google Chrome）浏览器在未经任何明确告知的情况下，悄然在全球数亿用户的电脑中下载并安装数GB大小的AI模型，从而深陷舆论漩涡。

 ![chrome gemini nano silent - 昏暗而极具科技感的未来背景中，谷歌Chrome标志被印在透明玻璃球体上，约4GB发光的微型芯片和复杂的神经网络数据正在悄悄汇入其中，呈现出极具戏剧性的秘密下载场景。](../../../../../source/posts/chrome_silent_gemini_nano/og-image.webp)

## 1. 悄然而至的4GB：事件的来龙去脉

### 1.1 披着“Optimization Guide”外衣的隐形触角
如果某天您突然发现硬盘空间凭空消失了将近4GB，您首先会怀疑什么？大多数用户可能会认为这是系统更新或巨大的软件缓存，但真凶实际上是大家每天都在使用的Chrome浏览器。

谷歌为了在Chrome中运行其本地AI工具，悄然开始在配置达标的本地设备上部署其 <a href="/cn/glossary/gemini-nano" class="glossary-tooltip" data-definition="谷歌开发的针对端侧设备优化的轻量级大语言模型，无需依赖云端网络连接，即可在本地设备上高效、安全地处理文本摘要、智能回复、纠错等AI推理计算。">Gemini Nano</a> 模型。

在Chrome的组件页面（`chrome://components`）中，这项下载以并不显眼的 <b>'Optimization Guide On Device Model'</b>（端侧模型优化指南）之名悄悄启动。下载完成后，它会在本地Chrome用户数据目录下存储为一个约4GB大小的 `weights.bin` 权重文件。

### 1.2 “我从未同意过”：用户愤怒的根源
端侧AI确实带来了高推理速度和强隐私保障等显而易见的优势。然而，谷歌此次采取的后台静默分发手段，因其严重缺乏透明度而备受指责。

* <b>未经授权占用带宽</b>：对于使用计费网络、移动热点或处于低宽带地区的用户而言，在无任何提示的情况下静默下载4GB数据，会导致巨额的流量超额话费和突发性的网络拥堵。
* <b>磁盘空间强行垄断</b>：在仅配备128GB或256GB SSD的轻薄本（如入门款Macbook和低端Windows笔记本）上，4GB是一笔绝对不容忽视的存储成本，会直接影响系统的运行稳定性。
* <b>掌控权的丧失</b>：浏览器擅自扫描本地硬件配置（尤其是GPU显存及性能），并自作主张地强行下载模型，而未向用户弹出任何“您是否想要开启AI功能”的提示。这种强行推广的做法，正在加速部分用户流向Firefox或Safari。

---

## 2. 端侧AI的悖论：是强化隐私，还是侵占资源？

<blockquote>“端侧AI那‘不将个人数据上传至云端从而保障隐私’的美好承诺，却因其无视用户知情权、强行劫持本地硬件资源的行为而显得讽刺。”</blockquote>

### 2.1 本地运算的“大义名分”与现实的权衡
谷歌解释称，该模型是Chrome本地AI功能（如“帮我写”文章辅助、智能标签页整理、以及AI加持的历史记录搜索）正常运转的基石。在本地处理数据避免了将用户隐私数据传输到云端，实现了完美的隐私保护。

但这背后有着不可避免的硬性代价。在云端AI模式下，服务器的算力和存储成本由企业承担；而端侧AI则是将算力开销（GPU、RAM）和模型存储负担，完全转嫁给了<b>用户的硬件寿命</b>和<b>机器电池</b>。

 ![on device ai private - 在完全断开外部网络连线的离线笔记本电脑内部，一个设计精致、呈现黑金奢华质感的AI处理器芯片正在高亮闪烁，自律地在本地进行AI推理计算。](../../../../../source/posts/chrome_silent_gemini_nano/on-device-ai.webp)

### 2.2 系统性能影响及资源指标对比
我们可以对传统的云端AI功能与强行下载在本地运行的Gemini Nano，在其对系统资源的消耗上进行对比分析：

<table><thead><tr><th>资源评估指标</th><th>基于云端的传统AI功能</th><th>强行下载的本地Gemini Nano (Chrome)</th></tr></thead><tbody><tr><td>磁盘存储开销</td><td><strong>0 MB (无任何影响)</strong></td><td>约3.8GB 至 4.2GB (`weights.bin` 文件)</td></tr><tr><td>首次下载占用流量</td><td>无 (仅有轻微的API请求传输)</td><td>至少1.5GB 至 2.0GB的压缩包静默下载</td></tr><tr><td>运行时对RAM的占用</td><td>微乎其微 (仅处理基础的HTTP连接)</td><td>运行推理时，至少会强行霸占1GB 至 2GB以上的系统空闲内存</td></tr><tr><td>电池续航与硬件发热</td><td>极低</td><td>在本地进行密集推理计算时，会导致功耗骤增并伴随发热</td></tr><tr><td>数据隐私保障级别</td><td>标准 (数据必须发往云端)</td><td><strong>极佳 (完全在本地的安全沙箱中封闭处理)</strong></td></tr></tbody></table>

---

## 3. 如何彻底禁用并清除这4GB无用模型

谷歌将该组件的删除过程设计得有些繁琐。如果您直接前往文件夹删除 `weights.bin`，在Chrome的AI功能仍旧启用的状态下，浏览器会在下次启动后立即在后台重新下载这4GB的文件。

因此，为了确保不留死角、彻底清除该模型，您必须按照<b>“先在Flags中禁用，再手动物理删除”</b>的2步法进行：

### 第一步：在Chrome Flags中禁用端侧AI
1. 在Chrome地址栏输入 `chrome://flags` 并按回车。
2. 在上方的搜索框中输入 `on-device` 或 `optimization`。
3. 找到以下两项实验性标志，并将其状态修改为 <b>[Disabled]</b>（禁用）：
   * `Enables optimization guide on device`
   * `Prompt API for Gemini Nano`
4. 点击右下角的 <b>[Relaunch]</b> 按钮，使Chrome浏览器完全重启。

### 第二步：物理删除本地的4GB文件夹
成功禁用Flags后，Chrome的后台自动下载逻辑已被切断。此时，您可以安全地删除本地残留文件以收回宝贵的磁盘空间。根据您的操作系统，前往相应路径并将整个 `OptGuideOnDeviceModel` 文件夹直接移入垃圾箱：

* <b>Windows系统用户路径：</b>
  `%LOCALAPPDATA%\Google\Chrome\User Data\OptGuideOnDeviceModel`
* <b>macOS系统用户路径：</b>
  `~/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel`

*物理删除后，您可以在浏览器中访问 `chrome://on-device-internals` 确认状态。如果模型的加载状态显示为空或未启用，则说明已成功清除。*

---

## 4. 结论：失去透明度的技术创新无异于鸩毒

 谷歌此次的“静默4GB分发”风波，给未来所有试图在客户端推广本地AI模型的科技企业敲响了警钟。无论端侧算力的隐私优势多么引人入胜，<b>“用户的存储介质和网络带宽必须始终处于用户自己的绝对掌控之下”</b>，这一基本的数字权利底线不容践踏。

科技巨头在推出这些开创性功能前，理应拿出应有的坦诚与责任感，在下载数GB文件前向用户询问一句最基本的常识性问题：“为了体验更智能的写作与搜索功能，我们需要为您额外下载4GB的本地AI模型，请问您同意吗？”

---

## 🔗 推荐阅读
- [GPT-5.5 vs Claude Opus 4.7：72%的标记节约所隐藏的“技术负债”警告](/cn/posts/gpt-5-5-vs-claude-opus-4-7-maintenance-debt)
- [AgentOps：是自主化管理时代的到来，还是无法掌控的“黑匣子”？](/cn/posts/agentops-autonomy-or-black-box)
