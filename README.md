<div align="center">

<img src="assets/banner.svg" width="100%" alt="Shailesh Gupta — Cloud Solution Architect" />

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=2F81F7&center=true&vCenter=true&width=600&lines=Cloud+Solution+Architect+%40+Kyndryl+India;Designing+secure%2C+scalable+cloud+platforms;AWS+%7C+Azure+%7C+Hybrid+Cloud;Cloud+Migration+%26+Modernisation;Landing+Zones+%7C+IaC+%7C+FinOps;Generative+AI+on+AWS+%7C+Amazon+Bedrock)](https://git.io/typing-svg)

![Profile views](https://komarev.com/ghpvc/?username=ShailAdmin&label=Profile%20views&color=0e75b6&style=flat)
![Followers](https://img.shields.io/github/followers/ShailAdmin?label=Followers&style=flat&color=2F81F7)
![Experience](https://img.shields.io/badge/Experience-10%2B%20years-success?style=flat)
![Role](https://img.shields.io/badge/Role-Cloud%20Solution%20Architect-8A2BE2?style=flat)

</div>

**Cloud Solution Architect @ Kyndryl India** · AWS & Azure · Hybrid Cloud · Migration & Modernisation · Generative AI · DevOps · FinOps

I design cloud solutions that are secure, scalable and cost-effective, and lead them from the first architecture workshop through migration and day-2 operations. 10+ years across infrastructure operations, DevOps and solution architecture, delivering migration and modernisation programmes for enterprise clients on AWS, Azure and hybrid cloud. I also bring AI and generative AI into cloud solutions, both as workloads to host and as tools that speed up delivery and operations.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-shailesh74-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shailesh74)
[![Credly](https://img.shields.io/badge/Credly-Certifications-FF6B00?logo=credly&logoColor=white)](https://www.credly.com/users/shaileshgupta.74)
[![Medium](https://img.shields.io/badge/Medium-Articles-000000?logo=medium&logoColor=white)](https://medium.com/@shailesh.gupta.ext)
[![YouTube](https://img.shields.io/badge/YouTube-Hybrid%20Cloud%20Community-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/@hybridcloudcommunity)

---

## 🏗️ What I do as a Cloud Solution Architect

I turn business requirements into cloud architectures that are secure, resilient and cost-effective, then see them through migration, build and day-2 operations. My designs follow the AWS Well-Architected and Azure Well-Architected frameworks.

| Capability | What I deliver |
|---|---|
| 📐 **Solution design** | Requirements and current-state assessments, high- and low-level designs (HLD/LLD), architecture decision records, and reference architectures across AWS, Azure and hybrid |
| 🚚 **Migration & modernisation** | Portfolio discovery, 7R strategy per application, dependency mapping and wave plans; rehost and replatform with AWS MGN and DMS; modernising to containers on EKS |
| 🏛️ **Landing zones & governance** | Multi-account foundations with AWS Control Tower and Organizations, service control policies, tagging standards and IAM guardrails |
| 🌐 **Networking & hybrid connectivity** | VPC design, Direct Connect and VPN, DNS with Route 53, and load balancing and content delivery with ELB and CloudFront |
| 🔐 **Security & compliance** | Least-privilege IAM, encryption with KMS, audit trails with CloudTrail and AWS Config, and edge protection with WAF and Shield |
| 🛡️ **Resilience & DR** | High-availability designs and disaster recovery from backup-and-restore to warm standby, sized to agreed RTO and RPO |
| ⚙️ **Automation & DevOps** | Infrastructure as Code with Terraform, CloudFormation and Ansible; CI/CD with Jenkins and GitHub Actions |
| 📈 **Observability & operations** | Monitoring, logging and alerting with CloudWatch, Grafana and Elasticsearch; runbooks for day-2 operations |
| 💰 **Cost optimisation (FinOps)** | Cost visibility and showback, rightsizing, and savings plans and reservations, as a FinOps Certified Practitioner |
| 🤖 **AI & Generative AI solutions** | Architectures for generative AI applications on Amazon Bedrock and Azure OpenAI, including RAG over enterprise data, guardrails and secure private access |
| 🤝 **Stakeholder leadership** | Architecture workshops, design reviews and guiding delivery teams through agile execution |

### 🤖 AI & Generative AI on the cloud

How I apply AI as a Cloud Solution Architect:

- **Generative AI applications:** assistants and knowledge search built on Amazon Bedrock and Azure OpenAI, grounded in company data through retrieval-augmented generation (RAG)
- **Secure, governed AI platforms:** private endpoints, IAM and encryption for model access, Bedrock Guardrails for content safety, and data that stays inside the client's account
- **AI-assisted operations (AIOps):** LLMs that summarise logs and alerts, help triage incidents and draft runbook steps
- **AI-assisted migration:** faster discovery, dependency analysis and wave planning, with AI turning inventory data into migration recommendations
- **Cost control for AI (FinOps):** visibility of model-invocation, token and GPU spend, with right-sized model choices and budgets

**Reference architecture: RAG-based enterprise assistant on AWS**

```mermaid
flowchart LR
    U["👤 Users"] --> UI["🖥️ Web or chat app"]
    UI --> GW["🔐 API Gateway<br/>+ Cognito"]
    GW --> L["⚡ Lambda<br/>orchestration"]
    L --> KB["📚 Bedrock<br/>Knowledge Base"]
    KB --> VS[("🧭 Vector store<br/>OpenSearch Serverless")]
    S3[("🗂️ S3<br/>enterprise documents")] -. ingest and embed .-> KB
    L --> FM["🤖 Bedrock<br/>foundation model"]
    FM --> GR["🛡️ Bedrock<br/>Guardrails"]
    GR --> L
    L --> CW["📈 CloudWatch<br/>logs and cost metrics"]
```

### 🔄 How I deliver a cloud solution

```mermaid
flowchart LR
    A["🔍 Discover<br/>requirements and<br/>current state"] --> B["📐 Design<br/>Well-Architected<br/>target architecture"]
    B --> C["🏛️ Build<br/>landing zone<br/>and IaC"]
    C --> D["🚚 Migrate<br/>waves with<br/>MGN and DMS"]
    D --> E["⚙️ Operate<br/>CI/CD and<br/>observability"]
    E --> F["💰 Optimise<br/>cost, performance<br/>and resilience"]
    F --> G["🤖 AI-enable<br/>generative AI<br/>and AIOps"]
    G -. continuous improvement .-> B
```

### 🧰 Toolkit

| Area | Tools |
|---|---|
| **Cloud** | ![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white) ![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white) |
| **Infrastructure as Code** | ![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white) ![CloudFormation](https://img.shields.io/badge/CloudFormation-FF4F8B?style=flat-square&logo=amazonwebservices&logoColor=white) ![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white) |
| **Containers** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white) ![Amazon EKS](https://img.shields.io/badge/Amazon%20EKS-FF9900?style=flat-square&logo=amazoneks&logoColor=white) |
| **CI/CD** | ![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white) ![Maven](https://img.shields.io/badge/Maven-C71A36?style=flat-square&logo=apachemaven&logoColor=white) |
| **Observability** | ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white) ![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=flat-square&logo=elasticsearch&logoColor=white) ![CloudWatch](https://img.shields.io/badge/CloudWatch-FF4F8B?style=flat-square&logo=amazoncloudwatch&logoColor=white) |
| **AI & Generative AI** | ![Amazon Bedrock](https://img.shields.io/badge/Amazon%20Bedrock-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white) ![Amazon Q](https://img.shields.io/badge/Amazon%20Q-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white) ![SageMaker](https://img.shields.io/badge/SageMaker-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white) ![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-0078D4?style=flat-square&logo=microsoftazure&logoColor=white) ![OpenSearch](https://img.shields.io/badge/OpenSearch-005EB8?style=flat-square&logo=opensearch&logoColor=white) |
| **OS & scripting** | ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black) ![Red Hat](https://img.shields.io/badge/Red%20Hat-EE0000?style=flat-square&logo=redhat&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=flat-square&logo=ubuntu&logoColor=white) ![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) |

## 📊 GitHub stats

<div align="center">

<!-- Stats, streak and repo cards: generated daily by .github/workflows/snake.yml into the "output" branch -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/stats-dark.svg" />
  <img height="165" alt="GitHub stats" src="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/stats.svg" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/streak-dark.svg" />
  <img height="165" alt="GitHub contribution streak" src="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/streak.svg" />
</picture>

<!-- Activity graph: generated daily by .github/workflows/snake.yml into the "output" branch -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/activity-graph-dark.svg" />
  <img width="100%" alt="Contribution activity graph" src="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/activity-graph.svg" />
</picture>

</div>

<!-- Contribution snake: generated daily by .github/workflows/snake.yml into the "output" branch -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/github-snake-dark.svg" />
  <img alt="Contribution snake" src="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/github-snake.svg" />
</picture>

## 📂 Featured repositories

<div align="center">

<a href="https://github.com/ShailAdmin/Cloud_Architect">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/repo-Cloud_Architect-dark.svg" />
  <img alt="Cloud_Architect repository" src="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/repo-Cloud_Architect.svg" />
</picture>
</a>
<a href="https://github.com/ShailAdmin/CheatSheet">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/repo-CheatSheet-dark.svg" />
  <img alt="CheatSheet repository" src="https://raw.githubusercontent.com/ShailAdmin/ShailAdmin/output/repo-CheatSheet.svg" />
</picture>
</a>

</div>

## 🏆 Certifications

<p>
<a href="https://www.credly.com/badges/ece99f42-f526-4763-b4d8-a38171c258d5/public_url"><img src="https://img.shields.io/badge/AWS-Solutions%20Architect%20Associate-FF9900?style=for-the-badge&logo=amazonwebservices&logoColor=white" alt="AWS Certified Solutions Architect – Associate" /></a>
<a href="https://www.credly.com/badges/f8265be0-cea1-4843-8e75-9d4503817c7d/public_url"><img src="https://img.shields.io/badge/FinOps-Certified%20Practitioner-2E7D32?style=for-the-badge&logo=linuxfoundation&logoColor=white" alt="FinOps Certified Practitioner" /></a>
<a href="https://www.credly.com/badges/34f8657f-a29e-4e3a-a87b-6998c0a11ecb/public_url"><img src="https://img.shields.io/badge/AWS-Generative%20AI%20Essentials-8A2BE2?style=for-the-badge&logo=amazonwebservices&logoColor=white" alt="AWS Partner: Generative AI Essentials" /></a>
</p>

- [AWS Certified Solutions Architect – Associate](https://www.credly.com/badges/ece99f42-f526-4763-b4d8-a38171c258d5/public_url)
- [FinOps Certified Practitioner](https://www.credly.com/badges/f8265be0-cea1-4843-8e75-9d4503817c7d/public_url)
- [AWS Partner: Generative AI Essentials (Business)](https://www.credly.com/badges/34f8657f-a29e-4e3a-a87b-6998c0a11ecb/public_url)

<details>
<summary>Other AWS training badges</summary>

- [AWS Cloud Quest: Cloud Practitioner](https://www.credly.com/badges/e14ea744-6673-4938-90c3-88b1c89f56c0/public_url)
- [AWS Knowledge: Migration Foundations](https://www.credly.com/badges/14d96cc9-d16c-4261-8baa-f21af81a719e/public_url)
- [AWS Knowledge: File Storage](https://www.credly.com/badges/e3d60348-e004-4280-a3fa-d8642241c66b/public_url)
- [AWS Educate: Getting Started with Compute](https://www.credly.com/badges/99cc47fe-1baf-496e-b29e-4dda4fcf54cd/public_url)

</details>

## 🌱 Currently exploring

- Agentic AI for cloud operations: assistants that can investigate incidents and run approved runbooks
- Retrieval-augmented generation (RAG) over architecture docs and runbooks with Amazon Bedrock
- Model Context Protocol (MCP) servers that connect AI assistants to cloud tooling
- Cost and governance patterns for running LLM workloads at enterprise scale

## 🤝 Community

Member of the [Linux Foundation community](https://community.linuxfoundation.org/) and the [FinOps Foundation](https://www.finops.org/); I share hybrid-cloud content on [YouTube](https://www.youtube.com/@hybridcloudcommunity) and [Medium](https://medium.com/@shailesh.gupta.ext).

📫 Open to conversations on cloud architecture, migration and modernisation, generative AI on the cloud, hybrid cloud and FinOps — reach me on [LinkedIn](https://www.linkedin.com/in/shailesh74).
