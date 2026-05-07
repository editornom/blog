---
title: "What is CRD (Custom Resource Definition)?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 11:29:40.487351+09:00
slug: kubernetes-crd-custom-resource-definition-explained
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Custom Resource Definition (CRD) is a standard mechanism that extends the Kubernetes API, allowing users to define and manage their own object types beyond the built-in resources. It is essential for creating resources optimized for specific application requirements and automating operations, such as in the Operator pattern or Gateway API."
references: []
modDatetime: 2026-05-07 11:39:40.487351+09:00
---

# What is CRD?

### Dictionary Definition
A Custom Resource Definition (CRD) is a standard mechanism for extending the Kubernetes API. It allows users to define unique object types beyond the default resources (such as Pods, Services, etc.) and add them to a cluster. This enables developers or operators to create custom resources tailored to the specific requirements of an application and manage them through the Kubernetes API server in the same way as standard resources.

### Practical Use Case
The Kubernetes Gateway API defines and deploys resources such as GatewayClass, Gateway, and HTTPRoute in the form of CRDs to overcome the limitations of the existing Ingress. Additionally, CRDs are essentially used as the data specification for defining and controlling application states in the Operator pattern, which handles complex operational logic such as database management or automated backups.

### Related Terms
- Custom Resource (CR)
- Operator Pattern
- Kubernetes API Server
- Gateway API