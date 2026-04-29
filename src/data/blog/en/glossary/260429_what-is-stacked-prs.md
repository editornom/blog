---
title: "What are Stacked PRs?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-29 17:12:18.110264+09:00
slug: guide-to-stacked-prs-workflow-optimization
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Stacked PRs is a workflow strategy that maximizes review efficiency and productivity by breaking down large features into logical, small units managed hierarchically. Learn the definition, practical application, and management tips for continuous development."
references: []
modDatetime: 2026-04-29 17:22:18.110264+09:00
---

### Dictionary Definition
Stacked PRs is a workflow strategy that involves breaking down a large feature into logically complete, smaller units and layering multiple Pull Requests (PRs) hierarchically. Instead of using a single massive feature branch, each change is separated into an independent branch and connected through sequential dependencies. This approach allows developers to continue working on higher-level layers without waiting for lower PRs to be approved or merged, while reviewers can maximize efficiency by examining code within small, clear contexts.

### Practical Use Case
When developing a large new feature, it is divided into logical units such as database schema modifications, business logic implementation, API endpoint development, and UI layer work. Each stage is created as a separate PR, where the 'API endpoint' PR is built directly on top of the 'business logic' branch. Reviewers can examine each PR independently to provide fast feedback, and the developer continues UI work without interruption while the lower-level reviews are still in progress. However, if a lower PR is squash-merged, the parent commit hash of the dependent branches changes, necessitating history reconstruction through a rebase.

### Related Words
- **Rebase**: A Git command that resets the base of a branch to another commit to align commit history; it is a core tool for maintaining the integrity of Stacked PRs.
- **Squash Merge**: A method of merging that combines multiple commits into one; in a Stacked PRs structure, it can sometimes become a source of technical debt by breaking the connection with upstream branches.
- **Feature Branch**: The traditional method of managing an entire feature in a single branch, which stands in contrast to the Stacked PRs approach.