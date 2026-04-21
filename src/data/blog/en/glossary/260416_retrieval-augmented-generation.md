---
title: RAG (Retrieval-Augmented Generation)
author: editornom
pubDatetime: 2026-04-16 17:10:54+09:00
slug: retrieval-augmented-generation
featured: false
draft: false
tags:
- glossary
- LLM
- GenerativeAI
- AI
ogImage: ../../../../../source/glossary/RAG_(Retrieval-Augmented_Generation)/3f23135c-0.png
description: This article explains Retrieval-Augmented Generation (RAG), a technique
  that improves the accuracy and reliability of large language models by retrieving
  and integrating information from external knowledge sources into the generation
  process.
faqs:
- q: What is RAG?
  a: RAG (Retrieval-Augmented Generation) is a technique that allows a Large Language
    Model (LLM) to look up relevant information from trusted external data sources
    before generating a response and then use that information as a reference. The
    key is to have the model "find" the necessary information in real-time instead
    of relying solely on pre-trained knowledge.
- q: What does RAG stand for, and what is its Korean name?
  a: The abbreviation is RAG, which stands for 'Retrieval-Augmented Generation.' In
    Korean, it is translated literally as '검색 증강 생성' (Geomsaek Jeunggang Saengseong).
- q: What is the background behind the emergence of RAG technology?
  a: It emerged because LLMs often exhibit 'hallucinations'—providing incorrect facts
    because they lack information on events occurring after their training or private
    data. RAG was designed to provide models with accurate external data rather than
    requiring them to be retrained every time.
- q: What are the primary technologies required to build a RAG system?
  a: Core technologies include the LLM (which serves as the foundation for answers),
    a Vector Database for storing and searching data, Embedding for numerical text
    conversion, and semantic search technologies for meaning-based retrieval.
- q: What are the advantages of using RAG?
  a: It overcomes the limitations of a model's training data to provide accurate,
    up-to-date information and specialized knowledge. It also effectively suppresses
    hallucinations and offers high reliability to users by clearly identifying the
    sources of information.
- q: What is the critical difference between RAG and Fine-tuning?
  a: RAG is like an 'open-book exam' where the model refers to external materials,
    whereas Fine-tuning is like 'studying' to acquire knowledge by directly modifying
    the model's parameters. RAG is faster for updates and more cost-effective, while
    Fine-tuning is better for mastering specific styles or formats.
- q: How does RAG reduce AI 'hallucinations'?
  a: By including actual document fragments related to the query in the prompt and
    instructing the model to 'answer based on this content,' it prevents the model
    from fabricating answers. This induces evidence-based generation, minimizing factual
    errors.
- q: What role does the 'Vector Database' play in the RAG process?
  a: It serves as a repository that converts user queries into vectors and then quickly
    identifies the document fragments that are semantically most similar among vast
    amounts of data. This allows it to supply the LLM with the most relevant reference
    materials for the user's intent.
- q: How does a RAG system respond when new information arises?
  a: There is no need to retrain the model. You simply update the external database
    with documents containing the latest information. This significantly reduces operational
    resources while ensuring the system stays current through real-time knowledge
    updates.
- q: How can companies practically implement RAG in their business?
  a: Companies can operate AI customer support chatbots based on extensive internal
    technical documents or product manuals. This improves efficiency by providing
    real-time, manual-based accurate answers to customer questions along with links
    to the supporting evidence pages.
---

![Conceptual diagram showing the RAG workflow where a user query triggers a search](../../../../../source/glossary/RAG_(Retrieval-Augmented_Generation)/3f23135c-0.png)

### 1. RAG Core Summary

| Item | Details |
| :--- | :--- |
| **English Name** | Retrieval-Augmented Generation |
| **Abbreviation** | RAG |
| **Key Technologies** | LLM, Vector Database, Embedding, Semantic Search, Prompt Engineering |
| **Originally Proposed by** | Patrick Lewis et al. (2020) |

### 2. Concept and Definition
Retrieval-Augmented Generation (RAG) is a technique that enables a Large Language Model (LLM) to search for relevant information in trusted external data sources before generating a response, then incorporating that information into the prompt. The core concept is to have the model "look up" the necessary information in real-time rather than relying solely on the knowledge it already acquired during training. This approach overcomes the limitations of a model's training data, allowing it to provide accurate information on the latest events or specific domain-specific expertise. It is also highly effective at mitigating "hallucinations," a common side effect where AI generates plausible-sounding but incorrect information.

### 3. Background of Adoption
LLMs only remember data up to the point where their pre-training was completed. Consequently, they are unaware of events occurring after training or confidential internal corporate data that is not publicly available. This is why hallucinations occur—when asked about information the model doesn't know, it relies on its internal parameters to produce a response that sounds convincing but is factually incorrect. Re-training (Fine-tuning) the model every time new information emerges is prohibitively expensive and time-consuming. RAG solves these constraints by retrieving accurate data from an external repository and providing it to the model as "reference material."

### 4. How It Works and Key Features
*   **Retrieval and Information Augmentation:** When a user query is received, it is converted into a vector to find semantically similar document fragments in a Vector Database. These retrieved pieces of information are then combined with the user's original query and passed to the LLM.
*   **Evidence-Based Response Generation:** The LLM prioritizes the external documents provided in the prompt over its pre-existing internal knowledge to formulate a response. This not only increases accuracy but also makes it easier to verify reliability by clearly identifying the sources used in the response.
*   **Flexibility in Knowledge Updates:** There is no need to retrain the model itself. By simply updating the external database with the latest information, the model can immediately provide responses reflecting those updates, significantly reducing operational resource requirements.

### 5. RAG vs. Fine-tuning
*   **RAG:** Comparable to an "open-book exam," where the model’s structure remains unchanged while it pulls external data to find answers. Its strengths lie in fast updates and the ability to provide evidence.
*   **Fine-tuning:** Comparable to "studying," where the model's parameters are directly modified using a specific dataset. While it is suitable for learning specific tones, formats, or complex patterns, it incurs re-training costs for every update and makes it difficult to fully control hallucination issues.

### 6. Practical Applications and Related Terms
*   **Real-world Use:** Enterprises can build vector databases containing vast technical documents or product manuals to operate AI customer support chatbots. These bots provide real-time, manual-based accurate responses and can provide links to the source pages as evidence.
*   **Related Key Terms:**
    1.  **Vector Database:** A dedicated storage system that stores and searches vector data, designed to calculate the semantic similarity of text numerically.
    2.  **Embedding:** The essential process of converting unstructured data, such as text, into high-dimensional vectors that a computer can understand and process.
    3.  **Hallucination:** An error where an AI model confidently outputs factually incorrect information as if it were true.
