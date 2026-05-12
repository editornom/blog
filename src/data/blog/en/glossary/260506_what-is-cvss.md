---
title: "What is CVSS?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-06 11:25:09.238064+09:00
slug: guide-to-common-vulnerability-scoring-system-cvss
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "The Common Vulnerability Scoring System (CVSS) is a standardized framework used to evaluate the severity of security vulnerabilities on a scale from 0.0 to 10.0. Learn how to objectively analyze risk levels and establish efficient security patching strategies."
references: []
modDatetime: 2026-05-06 11:35:09.238064+09:00
---

# What is CVSS?

### Dictionary Definition
The Common Vulnerability Scoring System (CVSS) is a standardized, open framework designed to assess the severity of information security vulnerabilities. By quantifying the technical characteristics of a vulnerability, it assigns a numerical score ranging from 0.0 to 10.0. This system allows organizations to objectively compare the risk levels of discovered security flaws and quantitatively determine the priority of security patches and responses.

### Practical Use Case
When responding to the CVE-2026-31431 (Copy Fail) vulnerability, a security operations team refers to its CVSS 3.1 Base Score of 7.8 (High). Recognizing that this score falls into the high-risk category, and combining it with the technical detail that container escape is possible despite the Attack Vector (AV) being Local (L), the team uses this data as the rationale for prioritizing the Linux kernel patch within their cloud infrastructure.

### Related Words
* <b>CVE (Common Vulnerabilities and Exposures):</b> A list of unique, standardized identifiers assigned to publicly disclosed security vulnerabilities.
* <b>CWE (Common Weakness Enumeration):</b> A community-developed list of software and hardware weakness types that serve as a common language for describing security vulnerabilities.
* <b>NVD (National Vulnerability Database):</b> The U.S. government repository of standards-based vulnerability management data, which provides CVSS scores and detailed analysis for CVEs.