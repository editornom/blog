---
title: "Confused Deputy"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 18:48:35.245929+09:00
slug: "confused-deputy"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "A Confused Deputy is a security vulnerability where a privileged agent performs requests from lower-privileged entities without verification, leading to privilege misuse and data leakage. This post explains related risks like indirect prompt injection in AI agents and security measures."
references: []
modDatetime: 2026-05-29 18:58:35.245929+09:00
---

# What is the Confused Deputy?

### Dictionary Definition
A Confused Deputy is a security vulnerability that occurs when a privileged entity (the deputy) is tricked by a less-privileged entity into using its elevated permissions to perform an action on the requester's behalf without proper verification. This happens when a system authorizes a task based on the credentials of the deputy rather than the original requester, making it a primary cause of privilege misuse and data breaches.

### Practical Use Case
Consider an AI agent based on the Model Context Protocol (MCP) that can send emails or modify files based on user commands. If the agent executes a command—such as deleting a critical file—using its own high-level system permissions without first verifying if the user has the right to perform that action, it is acting as a "Confused Deputy."

### Related Words
Privilege Escalation, Indirect Prompt Injection, Access Control