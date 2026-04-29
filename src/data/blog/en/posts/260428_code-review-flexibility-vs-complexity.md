---
title: "Flexibility for Code Reviews or a Harbinger of Complexity? A Deep Dive into Stacked PRs"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-28 09:00:00+09:00
slug: stacked-prs-code-review-workflow-guide
featured: false
draft: false
ogImage: "../../../../../source/posts/Stacked_PRs/9bd9f4f0-0.webp"
description: "Stacked PRs is a workflow strategy that breaks down large features into logical units to maximize code review efficiency and development speed. This post explores its core principles, benefits, and the technical debt associated with management and squash merging."
references:
- https://swizec.com/blog/in-praise-of-the-stacked-pull-request/
- https://www.davepacheco.net/blog/2025/stacked-prs-on-github/
- https://andrewlock.net/working-with-stacked-branches-in-git-part-1/
modDatetime: 2026-04-29 17:21:51.923891+09:00
faqs:
- q: "What are Stacked PRs?"
  a: "It is a development workflow where large features are broken down into logical units and several related pull requests are stacked hierarchically. The core idea is to increase review efficiency by splitting large tasks into smaller pieces."
- q: "Why is this method gaining attention?"
  a: "In large organizations, code reviews often become a bottleneck. Stacked PRs reduce the size of individual reviews, speeding up the feedback loop and allowing developers to continue working without waiting for approval."
- q: "What are the main characteristics of Stacked PRs?"
  a: "Features are logically separated—such as database schemas, business logic, and UI—to create independent PRs. Each PR has a hierarchical structure depending on the previous stage, clearly communicating the context of the work."
- q: "What are the benefits for reviewers?"
  a: "Instead of reviewing thousands of lines at once, reviewers can examine segmented code within a few hundred lines following a logical flow. This reduces cognitive load and enables more thorough reviews."
- q: "What is the biggest challenge in maintaining this workflow?"
  a: "Managing complex dependencies between branches. Every time a lower branch is modified or merged, the upper branches must be manually rebased and synchronized, which can be a significant burden."
- q: "What technical debt arises when using squash merges?"
  a: "When a lower PR is squash-merged, the commit hash changes, breaking the link with the upper branches. This forces developers to manually reconstruct the history, which can be a tedious process."
- q: "How does it differ from the traditional feature branch method?"
  a: "Feature branches have simpler history management but higher review fatigue. In contrast, Stacked PRs maximize review efficiency but carry a higher risk of human error due to frequent rebasing and complex synchronization."
- q: "Are there specific tools to consider for implementation?"
  a: "Manual management is risky, so dedicated tools like Graphite or jj should be considered. However, it is important to realize that these tools may have OS dependencies or installation constraints."
- q: "How can I prevent history conflicts when managing Stacked PRs with Git?"
  a: "Avoid forced commands like 'git merge -X ours'. Instead, use tools like git-absorb or the '--update-refs' option during rebasing to manage history precisely. Unautomated complexity can undermine system stability."
- q: "Is using Stacked PRs really faster than the traditional way for code reviews?"
  a: "Review feedback is definitely faster, but the extra effort required to organize Git history and align branches is substantial. Without dedicated tool support, relying solely on individual skill can actually slow down the overall process."
---

In growing software development organizations, code review is a vital mechanism for maintaining quality, yet it is often cited as the primary bottleneck slowing down development. Organizations in the hyper-growth stage, in particular, find themselves constantly seeking a compromise between speed and quality. <a href="/en/glossary/what-is-stacked-prs" class="glossary-tooltip" data-definition="A development workflow strategy that breaks down large features into logical units and stacks several related Pull Requests (PRs) hierarchically. While it improves review efficiency and reduces bottlenecks, it increases the complexity of Git history management and synchronization.">Stacked PRs</a> has emerged among senior engineers as a technical answer to this dilemma. By splitting a single massive feature into logically complete, smaller branches and stacking them layer by layer, this method theoretically aims for a highly efficient structure.

![Stacked PRs - A 3D diagram against a dark office background showing software code modules stacked in layers and connected by glowing lines.](../../../../../source/posts/Stacked_PRs/9bd9f4f0-0.webp)

The core of Stacked PRs lies in subdividing large features into components such as database schemas, business logic, API endpoints, and UI layers, creating independent Pull Requests (PRs) for each. Reviewers can quickly examine code within a few hundred lines with clear context, while authors can proceed to the next task without waiting for approval of the previous stage. However, behind this sophisticated workflow lies technical debt in the form of manual operations and high cognitive load for the developer.

The most concerning point is the conflict with 'Squash Merge,' a common practice used to keep the main branch history clean. The moment a lower PR is squash-merged on platforms like GitHub, the upper branches stacked on top of it lose their connection because the hash value of the parent commit they were referencing changes. From this point on, the developer must spend significant time reconstructing the history through rebasing.

In practice, forced synchronization using commands such as `git merge -X ours` is a factor that compromises system stability. This is not a logical resolution of conflicts but an act of overwriting changes from the parent branch by prioritizing the current branch's state. Even if a colleague has modified a common module, those changes can be silently dropped during this process, leading to the destruction of code integrity.

![Stacked PRs - A developer at a glowing keyboard looking at a screen where multiple complex development paths are merging into one.](../../../../../source/posts/Stacked_PRs/7b57aece-1.webp)

When comparing the traditional feature branch method with the Stacked PRs workflow, the costs and benefits of each approach are starkly different.

- **Traditional Feature Branch**
  - **Review Size**: Large (often over 1,000 lines, leading to high review fatigue)
  - **Development Flow**: Difficult to proceed with follow-up work until the PR is approved
  - **History Management**: Relatively simple, as standard Git functions are sufficient
  - **Risk of Human Error**: Relatively low, following standard merge processes

- **Stacked PRs Workflow**
  - **Review Size**: Small (segmented into logical units, providing high readability)
  - **Development Flow**: Work on upper layers can continue even while waiting for approval
  - **History Management**: Highly complex, requiring frequent rebasing and reference updates
  - **Risk of Human Error**: High potential for manual conflict resolution and branch pointing errors

The 'fast feedback loop' promised by Stacked PRs is attractive, but the lack of a robust toolchain to support it is a major obstacle. While tools like Graphite and jj are being proposed as alternatives, issues with universal accessibility—such as installation constraints on certain operating systems or forced Node.js environments—persist. Attempting to maintain this system manually without dedicated tools is akin to betting the fate of the system on the technical virtuosity of individuals rather than an automated pipeline.

Improving the efficiency of a review system is not just about reducing the volume of code. An environment where a developer must constantly worry if their history is tangled, frequently checking options like `git-absorb` or `--update-refs`, actually distracts from their focus. Attempting to bridge process flaws with technical trickery can lead to a situation where one becomes more obsessed with the aesthetic cleanliness of Git history than with validating business value.

![Stacked PRs - A human hand barely supporting a pillar made of glowing code, illustrating how precarious a complex development process can be when relying on manual labor.](../../../../../source/posts/Stacked_PRs/fab00fa7-2.webp)

Ultimately, attempting to overcome system limitations through individual proficiency will likely remain a precarious art for a few experts without the support of mature, dedicated tools. If an obsession with linear history is hindering the collaboration efficiency of the entire team, priority should be given to the essential simplification of the workflow itself rather than the choice of tools. Unautomated complexity can never be true innovation; one must remember that it can become a silent variable that threatens system stability from within.

## 🔗 Recommended Reading
- [The Technological Landscape Reshaped by Attention and the Pros and Cons of Transformers](/en/posts/attention-transformers-tech-landscape)
- [Agentic Cybersecurity: The Reality of Autonomous Defense and the Paradox of Control](/en/posts/agentic-cybersecurity-autonomous-defense)