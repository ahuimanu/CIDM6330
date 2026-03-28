Develop: MVP Iterations + AI Process
Foundation: 3 - Trade-Off Reality & Distributed Systems
Weeks: 06–09
Phase: Develop (Double-Diamond)

Overview
Foundations 1 and 2 were about discovery and definition. Foundation 3 is about development - building working software while confronting the real costs of your architectural decisions.

This foundation has two intertwined goals:

Build: Produce MVP iterations of your data pipeline
Learn: Understand what your architecture actually costs when you implement it
You will also formalize your AI collaboration into a documented process. This is not bureaucracy — it's professional practice for AI-assisted development.

Deliverables
Submit via pull request to your forked repository. Markdown preferred for documentation; code in appropriate files.

1. MVP Iteration 1 - Data Acquisition
Demonstrate that you can reliably acquire your data.

Working code: Scripts or modules that fetch, download, or connect to your data sources. Must be runnable.

Data samples: Evidence that your code produces real data. Include sample outputs (appropriately sized).

Error handling: How does your code handle API failures, network issues, malformed data, rate limits?

Documentation: README or inline documentation sufficient for someone else to run your acquisition code.

2. MVP Iteration 2 - Data Transformation
Demonstrate that you can transform raw data toward your problem's needs.

Working code: Scripts or modules that clean, transform, aggregate, or enrich your data. Must be runnable.

Transformation logic: Document what transformations you're applying and why. Connect these to your problem definition.

Data quality handling: How do you handle missing values, outliers, inconsistencies? What assumptions are you making?

Output artifacts: The transformed data in a usable form (files, database tables, data structures).

3. MVP Iteration 3 - Pipeline Integration
Demonstrate end-to-end flow from source to output.

Working pipeline: Code that chains acquisition → transformation → output. Must be runnable as a coherent unit.

Configuration: How does someone configure the pipeline for different parameters (date ranges, filters, etc.)?

Logging and observability: Can you tell what the pipeline did? Where would you look if something went wrong?

Output demonstration: Show the pipeline producing meaningful output that addresses (even partially) your problem.

4. Architecture Reality Check
Confront what you've learned by building.

Style validation: Does your Foundation 2 architecture style still fit? What did implementation reveal that design didn't?

Characteristic assessment: For each of your driving characteristics, assess: Are you achieving it? What's harder than expected? What trade-offs have you actually made?

Component evolution: Have your components changed from Foundation 2? Have boundaries shifted? Has responsibility allocation changed?

What you would do differently: With hindsight, what architectural decisions would you reconsider? This is not about being wrong — it's about learning.

5. Distributed Considerations
Whether or not you're building a distributed system, engage with distributed thinking.

Current state: Is your pipeline monolithic or distributed? Why?

Distribution decision: If you chose not to distribute, defend that choice. What would you gain and lose by distributing?

If distributed: What communication style are you using (synchronous, asynchronous, events, messages)? What coordination challenges have you encountered?

Data ownership: Who owns what data? Where does truth live? How do you handle data that multiple components need?

6. Risk Identification
Identify the risks in your current implementation.

Technical risks: What could break? What dependencies are fragile? Where is complexity concentrated?

Data risks: What happens if your data source changes format, becomes unavailable, or contains unexpected values?

Architectural risks: What aspects of your design are you least confident about? What would require significant rework if assumptions prove wrong?

7. AI Process Documentation
This foundation requires explicit documentation of your AI collaboration process.

In AI_LOG.md, add a section for Foundation 3 that includes:

Process description: How are you working with AI? What's your workflow? When do you invoke AI assistance and when do you work independently?

Decision log: For significant decisions (architecture changes, implementation approaches, debugging strategies), document:

What you asked the AI
What it suggested
What you did (accepted, modified, rejected)
Why you made that choice
AI failures: Specific instances where AI-generated code didn't work, was wrong, or didn't fit your context. What did you do?

Verification practices: How do you verify AI-generated code works? How do you verify it's correct?

Judgment patterns: Where do you find yourself consistently overriding AI suggestions? What patterns are emerging in your collaboration?

This documentation is central to this foundation. You will defend your AI collaboration process in Drift consultation with the same rigor as your architectural decisions.

Code Requirements
Runnable: All code must execute. Include any setup instructions.
Tested: Include at least basic tests demonstrating your code works. (Test coverage requirements will be emphasized in Foundation 4.)
Readable: Code should be reasonably documented. Someone else should be able to understand what it does.
Organized: Clear file/folder structure. No single monolithic script unless that's genuinely the right design.
Constraints
Iteration evidence: You must show iterations, not just a final product. Git history should reflect progressive development.

Working beats complete: A working partial pipeline is better than a non-working complete design. Scope down if needed.

AI documentation is mandatory: Incomplete AI process documentation is a deliverable failure, regardless of code quality.

GzKit
I have a framework for you to try called gzkit, I will provide key extracts for you from it via a separate post. This contains the basics of specification, governance, construction, and validation.

In the meantime, you can look these up:

Product Requirements Document
Architecture Decision Record (also, chapter 21) 
Broad Resources on this subject:

PRD basics (Focus here, the rest is for your edification)
- https://www.atlassian.com/agile/product-management/requirements
- https://www.atlassian.com/software/confluence/templates/product-requirements

Agent PRD/spec templates
- https://raw.githubusercontent.com/GSA-TTS/devCrew_s1/master/docs/templates/AI%20Agent%20Specification%20Template.md

Agent architecture & patterns
- https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- https://www.anthropic.com/engineering/building-effective-agents
- https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html

Tools & integrations
- https://developers.openai.com/api/docs/guides/function-calling/
- https://developers.openai.com/api/docs/guides/agents-sdk/
- https://openai.github.io/openai-agents-python/guardrails/
- https://openai.github.io/openai-agents-python/tracing/
- https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- https://www.anthropic.com/news/model-context-protocol
- https://www.anthropic.com/engineering/writing-tools-for-agents

Evals
- https://developers.openai.com/api/docs/guides/evals/
- https://developers.openai.com/blog/eval-skills/
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://developers.openai.com/cookbook/examples/partners/agentic_governance_guide/agentic_governance_cookbook

Safety & governance
- https://owasp.org/www-project-top-10-for-large-language-model-applications/
- https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf
- https://techcommunity.microsoft.com/blog/microsoftdefendercloudblog/architecting-trust-a-nist-based-security-governance-framework-for-ai-agents/4490556
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/safety-overview
- https://google.github.io/adk-docs/safety/

Guardrails/observability
- https://docs.langchain.com/oss/python/langchain/guardrails
- https://langfuse.com/docs/security-and-guardrails
- https://docs.nvidia.com/nemo/guardrails/latest/integration/langchain/langgraph-integration.html

 