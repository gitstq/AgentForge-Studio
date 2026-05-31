"""
Built-in skill templates - 20+ pre-configured skill templates.

Each template provides a complete skill definition with instructions,
parameters, inputs, and outputs that can be applied to create new skills.
"""

import copy
from typing import Dict, List

from ..core.skill import Skill, SkillParameter, SkillIO


def _build_templates() -> Dict[str, Skill]:
    """Build and return all built-in skill templates."""
    templates = {}

    # 1. Code Review
    templates["code-review"] = Skill(
        name="code-review",
        description="Review source code for quality, bugs, and best practices",
        version="1.0.0",
        instructions=(
            "You are a senior code reviewer. Analyze the provided code for:\n"
            "1. Bug detection and potential issues\n"
            "2. Code quality and readability\n"
            "3. Performance concerns\n"
            "4. Security vulnerabilities\n"
            "5. Best practices compliance\n"
            "6. Naming conventions\n"
            "Provide specific line references and actionable suggestions."
        ),
        parameters=[
            SkillParameter(name="code", type="string", required=True,
                           description="The source code to review"),
            SkillParameter(name="language", type="string", required=False,
                           default="auto", description="Programming language"),
            SkillParameter(name="focus_areas", type="array", required=False,
                           default=["all"],
                           description="Specific areas to focus on"),
            SkillParameter(name="severity_level", type="string", required=False,
                           default="all",
                           description="Minimum severity to report: critical, major, minor, all"),
        ],
        inputs=[
            SkillIO(name="code", type="string", description="Source code content"),
            SkillIO(name="language", type="string", description="Programming language hint"),
        ],
        outputs=[
            SkillIO(name="review_report", type="object",
                    description="Structured review findings"),
            SkillIO(name="score", type="integer", description="Overall code quality score (0-100)"),
            SkillIO(name="suggestions", type="array", description="List of improvement suggestions"),
        ],
        tags=["code", "review", "quality"],
    )

    # 2. Documentation Generator
    templates["doc-generator"] = Skill(
        name="doc-generator",
        description="Generate comprehensive documentation from source code or descriptions",
        version="1.0.0",
        instructions=(
            "You are a technical documentation specialist. Generate clear, comprehensive "
            "documentation that includes:\n"
            "1. Overview and purpose\n"
            "2. API reference with parameter descriptions\n"
            "3. Usage examples with code snippets\n"
            "4. Error handling and edge cases\n"
            "5. Configuration options\n"
            "Use clear language and structure the documentation logically."
        ),
        parameters=[
            SkillParameter(name="source", type="string", required=True,
                           description="Source code or description to document"),
            SkillParameter(name="doc_type", type="string", required=False,
                           default="api",
                           description="Type: api, user_guide, developer_guide, readme"),
            SkillParameter(name="format", type="string", required=False,
                           default="markdown",
                           description="Output format: markdown, html, rst"),
        ],
        inputs=[
            SkillIO(name="source", type="string", description="Source material"),
            SkillIO(name="doc_type", type="string", description="Documentation type"),
        ],
        outputs=[
            SkillIO(name="documentation", type="string", description="Generated documentation"),
            SkillIO(name="toc", type="array", description="Table of contents"),
        ],
        tags=["documentation", "generation", "writing"],
    )

    # 3. Data Analyst
    templates["data-analyst"] = Skill(
        name="data-analyst",
        description="Analyze data and generate insights, statistics, and visualizations",
        version="1.0.0",
        instructions=(
            "You are a data analysis expert. Analyze the provided data to:\n"
            "1. Identify patterns and trends\n"
            "2. Calculate key statistics (mean, median, std, percentiles)\n"
            "3. Detect anomalies and outliers\n"
            "4. Generate actionable insights\n"
            "5. Suggest correlations between variables\n"
            "Present findings in a clear, structured format with supporting numbers."
        ),
        parameters=[
            SkillParameter(name="data", type="string", required=True,
                           description="Data to analyze (CSV, JSON, or text format)"),
            SkillParameter(name="analysis_type", type="string", required=False,
                           default="general",
                           description="Type: general, statistical, trend, anomaly"),
            SkillParameter(name="columns", type="array", required=False,
                           description="Specific columns to focus on"),
        ],
        inputs=[
            SkillIO(name="data", type="string", description="Raw data"),
            SkillIO(name="analysis_type", type="string", description="Analysis type"),
        ],
        outputs=[
            SkillIO(name="summary", type="object", description="Analysis summary"),
            SkillIO(name="statistics", type="object", description="Key statistics"),
            SkillIO(name="insights", type="array", description="Key findings"),
        ],
        tags=["data", "analysis", "statistics"],
    )

    # 4. API Tester
    templates["api-tester"] = Skill(
        name="api-tester",
        description="Test API endpoints and generate test cases",
        version="1.0.0",
        instructions=(
            "You are an API testing specialist. For the given API endpoint:\n"
            "1. Generate comprehensive test cases covering:\n"
            "   - Happy path scenarios\n"
            "   - Edge cases and boundary values\n"
            "   - Error handling scenarios\n"
            "   - Authentication/authorization tests\n"
            "2. Define expected request/response pairs\n"
            "3. Specify status codes and response schemas\n"
            "4. Identify potential security issues"
        ),
        parameters=[
            SkillParameter(name="endpoint", type="string", required=True,
                           description="API endpoint URL or definition"),
            SkillParameter(name="method", type="string", required=False,
                           default="GET",
                           description="HTTP method: GET, POST, PUT, DELETE, PATCH"),
            SkillParameter(name="auth_type", type="string", required=False,
                           default="none",
                           description="Authentication type: none, bearer, api_key, oauth"),
        ],
        inputs=[
            SkillIO(name="endpoint", type="string", description="API endpoint"),
            SkillIO(name="method", type="string", description="HTTP method"),
        ],
        outputs=[
            SkillIO(name="test_cases", type="array", description="Generated test cases"),
            SkillIO(name="coverage_report", type="object", description="Test coverage summary"),
        ],
        tags=["api", "testing", "quality"],
    )

    # 5. Security Scanner
    templates["security-scanner"] = Skill(
        name="security-scanner",
        description="Scan code for security vulnerabilities and best practice violations",
        version="1.0.0",
        instructions=(
            "You are a security analysis expert. Scan the provided code for:\n"
            "1. OWASP Top 10 vulnerabilities\n"
            "2. Injection flaws (SQL, XSS, command injection)\n"
            "3. Authentication and authorization issues\n"
            "4. Sensitive data exposure\n"
            "5. Insecure dependencies\n"
            "6. Misconfigurations\n"
            "7. Cryptographic weaknesses\n"
            "Provide severity ratings (Critical/High/Medium/Low) and remediation steps."
        ),
        parameters=[
            SkillParameter(name="code", type="string", required=True,
                           description="Code to scan for vulnerabilities"),
            SkillParameter(name="language", type="string", required=False,
                           default="auto", description="Programming language"),
            SkillParameter(name="scan_level", type="string", required=False,
                           default="standard",
                           description="Scan depth: quick, standard, deep"),
        ],
        inputs=[
            SkillIO(name="code", type="string", description="Source code"),
        ],
        outputs=[
            SkillIO(name="vulnerabilities", type="array", description="Found vulnerabilities"),
            SkillIO(name="risk_score", type="integer", description="Overall risk score (0-100)"),
            SkillIO(name="remediation", type="array", description="Remediation steps"),
        ],
        tags=["security", "scanning", "vulnerability"],
    )

    # 6. Code Refactorer
    templates["code-refactorer"] = Skill(
        name="code-refactorer",
        description="Refactor code for better structure, readability, and performance",
        version="1.0.0",
        instructions=(
            "You are a code refactoring expert. Analyze the provided code and:\n"
            "1. Identify code smells and anti-patterns\n"
            "2. Suggest structural improvements\n"
            "3. Apply design patterns where appropriate\n"
            "4. Improve naming and organization\n"
            "5. Reduce code duplication\n"
            "6. Enhance testability\n"
            "Provide the refactored code with explanations for each change."
        ),
        parameters=[
            SkillParameter(name="code", type="string", required=True,
                           description="Code to refactor"),
            SkillParameter(name="language", type="string", required=False,
                           default="auto", description="Programming language"),
            SkillParameter(name="refactor_type", type="string", required=False,
                           default="all",
                           description="Focus: all, performance, readability, structure"),
        ],
        inputs=[
            SkillIO(name="code", type="string", description="Source code"),
        ],
        outputs=[
            SkillIO(name="refactored_code", type="string", description="Refactored code"),
            SkillIO(name="changes", type="array", description="List of changes made"),
            SkillIO(name="improvement_score", type="integer",
                    description="Estimated improvement (0-100)"),
        ],
        tags=["refactoring", "code-quality", "design-patterns"],
    )

    # 7. Translator
    templates["translator"] = Skill(
        name="translator",
        description="Translate text between languages with context awareness",
        version="1.0.0",
        instructions=(
            "You are a professional translator. Translate the provided text:\n"
            "1. Maintain the original meaning and tone\n"
            "2. Adapt cultural references appropriately\n"
            "3. Preserve technical terminology accurately\n"
            "4. Handle idioms and expressions naturally\n"
            "5. Maintain formatting and structure\n"
            "Provide the translation and note any cultural adaptations made."
        ),
        parameters=[
            SkillParameter(name="text", type="string", required=True,
                           description="Text to translate"),
            SkillParameter(name="source_lang", type="string", required=False,
                           default="auto", description="Source language (auto-detect if not set)"),
            SkillParameter(name="target_lang", type="string", required=True,
                           description="Target language"),
            SkillParameter(name="domain", type="string", required=False,
                           default="general",
                           description="Domain: general, technical, legal, medical"),
        ],
        inputs=[
            SkillIO(name="text", type="string", description="Source text"),
            SkillIO(name="target_lang", type="string", description="Target language"),
        ],
        outputs=[
            SkillIO(name="translated_text", type="string", description="Translated text"),
            SkillIO(name="confidence", type="number", description="Translation confidence score"),
        ],
        tags=["translation", "language", "localization"],
    )

    # 8. Summarizer
    templates["summarizer"] = Skill(
        name="summarizer",
        description="Generate concise summaries of long texts, documents, or conversations",
        version="1.0.0",
        instructions=(
            "You are a summarization expert. Create a concise summary that:\n"
            "1. Captures the main points and key information\n"
            "2. Maintains factual accuracy\n"
            "3. Preserves important details and nuance\n"
            "4. Uses clear and concise language\n"
            "5. Follows the requested length and format\n"
            "Provide both a brief summary and key takeaways."
        ),
        parameters=[
            SkillParameter(name="text", type="string", required=True,
                           description="Text to summarize"),
            SkillParameter(name="max_length", type="integer", required=False,
                           default=200, description="Maximum summary length in words"),
            SkillParameter(name="style", type="string", required=False,
                           default="informative",
                           description="Style: informative, executive, bullet_points"),
            SkillParameter(name="language", type="string", required=False,
                           default="original", description="Summary language"),
        ],
        inputs=[
            SkillIO(name="text", type="string", description="Source text"),
        ],
        outputs=[
            SkillIO(name="summary", type="string", description="Generated summary"),
            SkillIO(name="key_points", type="array", description="Key takeaways"),
        ],
        tags=["summarization", "nlp", "extraction"],
    )

    # 9. Bug Fixer
    templates["bug-fixer"] = Skill(
        name="bug-fixer",
        description="Identify and fix bugs in source code with detailed explanations",
        version="1.0.0",
        instructions=(
            "You are a debugging expert. Analyze the provided code and bug report:\n"
            "1. Identify the root cause of the bug\n"
            "2. Explain why the bug occurs\n"
            "3. Provide the fix with minimal changes\n"
            "4. Explain the fix and its impact\n"
            "5. Suggest preventive measures\n"
            "6. Check for similar bugs in the codebase"
        ),
        parameters=[
            SkillParameter(name="code", type="string", required=True,
                           description="Code containing the bug"),
            SkillParameter(name="bug_description", type="string", required=True,
                           description="Description of the bug behavior"),
            SkillParameter(name="error_message", type="string", required=False,
                           description="Error message or stack trace"),
            SkillParameter(name="language", type="string", required=False,
                           default="auto", description="Programming language"),
        ],
        inputs=[
            SkillIO(name="code", type="string", description="Buggy code"),
            SkillIO(name="bug_description", type="string", description="Bug description"),
        ],
        outputs=[
            SkillIO(name="fixed_code", type="string", description="Fixed code"),
            SkillIO(name="root_cause", type="string", description="Root cause analysis"),
            SkillIO(name="fix_explanation", type="string", description="Explanation of the fix"),
        ],
        tags=["debugging", "bug-fix", "troubleshooting"],
    )

    # 10. Performance Optimizer
    templates["perf-optimizer"] = Skill(
        name="perf-optimizer",
        description="Optimize code performance with profiling and benchmarking suggestions",
        version="1.0.0",
        instructions=(
            "You are a performance optimization expert. Analyze the code for:\n"
            "1. Algorithmic complexity issues\n"
            "2. Memory inefficiencies\n"
            "3. Unnecessary computations\n"
            "4. I/O bottlenecks\n"
            "5. Concurrency opportunities\n"
            "6. Caching strategies\n"
            "Provide optimized code with before/after performance estimates."
        ),
        parameters=[
            SkillParameter(name="code", type="string", required=True,
                           description="Code to optimize"),
            SkillParameter(name="language", type="string", required=False,
                           default="auto", description="Programming language"),
            SkillParameter(name="target_improvement", type="string", required=False,
                           default="auto",
                           description="Focus: latency, throughput, memory, all"),
        ],
        inputs=[
            SkillIO(name="code", type="string", description="Source code"),
        ],
        outputs=[
            SkillIO(name="optimized_code", type="string", description="Optimized code"),
            SkillIO(name="analysis", type="object", description="Performance analysis"),
            SkillIO(name="improvements", type="array", description="List of optimizations"),
        ],
        tags=["performance", "optimization", "profiling"],
    )

    # 11. Test Generator
    templates["test-generator"] = Skill(
        name="test-generator",
        description="Generate comprehensive unit and integration tests for source code",
        version="1.0.0",
        instructions=(
            "You are a test engineering expert. Generate tests that:\n"
            "1. Cover all public methods and functions\n"
            "2. Include edge cases and boundary conditions\n"
            "3. Test error handling paths\n"
            "4. Use appropriate assertions\n"
            "5. Follow testing best practices (AAA pattern)\n"
            "6. Include both positive and negative test cases\n"
            "Generate tests using the appropriate framework for the language."
        ),
        parameters=[
            SkillParameter(name="code", type="string", required=True,
                           description="Code to generate tests for"),
            SkillParameter(name="language", type="string", required=False,
                           default="auto", description="Programming language"),
            SkillParameter(name="test_framework", type="string", required=False,
                           default="auto",
                           description="Test framework: pytest, junit, jest, go_test, auto"),
            SkillParameter(name="coverage_target", type="integer", required=False,
                           default=80, description="Target coverage percentage"),
        ],
        inputs=[
            SkillIO(name="code", type="string", description="Source code"),
        ],
        outputs=[
            SkillIO(name="test_code", type="string", description="Generated test code"),
            SkillIO(name="coverage_plan", type="object", description="Coverage plan"),
        ],
        tags=["testing", "unit-test", "quality"],
    )

    # 12. Code Explainer
    templates["code-explainer"] = Skill(
        name="code-explainer",
        description="Explain source code in natural language with varying detail levels",
        version="1.0.0",
        instructions=(
            "You are a code explanation expert. Explain the provided code:\n"
            "1. Give a high-level overview of what the code does\n"
            "2. Break down each function/component\n"
            "3. Explain the data flow and control flow\n"
            "4. Identify key design decisions and patterns\n"
            "5. Note any non-obvious behavior or gotchas\n"
            "Adapt the explanation depth to the requested level."
        ),
        parameters=[
            SkillParameter(name="code", type="string", required=True,
                           description="Code to explain"),
            SkillParameter(name="detail_level", type="string", required=False,
                           default="medium",
                           description="Detail level: brief, medium, detailed"),
            SkillParameter(name="audience", type="string", required=False,
                           default="developer",
                           description="Target audience: beginner, developer, expert"),
            SkillParameter(name="language", type="string", required=False,
                           default="auto", description="Programming language"),
        ],
        inputs=[
            SkillIO(name="code", type="string", description="Source code"),
        ],
        outputs=[
            SkillIO(name="explanation", type="string", description="Code explanation"),
            SkillIO(name="complexity_analysis", type="object",
                    description="Code complexity metrics"),
        ],
        tags=["explanation", "documentation", "education"],
    )

    # 13. Requirements Analyst
    templates["req-analyst"] = Skill(
        name="req-analyst",
        description="Analyze and structure software requirements into actionable specifications",
        version="1.0.0",
        instructions=(
            "You are a requirements analysis expert. Analyze the provided requirements:\n"
            "1. Identify functional and non-functional requirements\n"
            "2. Detect ambiguities and gaps\n"
            "3. Structure requirements hierarchically\n"
            "4. Define acceptance criteria\n"
            "5. Identify dependencies and constraints\n"
            "6. Prioritize requirements (MoSCoW method)\n"
            "Output a structured requirements document."
        ),
        parameters=[
            SkillParameter(name="requirements", type="string", required=True,
                           description="Raw requirements text or description"),
            SkillParameter(name="format", type="string", required=False,
                           default="user_stories",
                           description="Output format: user_stories, use_cases, spec"),
            SkillParameter(name="domain", type="string", required=False,
                           default="general",
                           description="Application domain"),
        ],
        inputs=[
            SkillIO(name="requirements", type="string", description="Raw requirements"),
        ],
        outputs=[
            SkillIO(name="structured_reqs", type="object",
                    description="Structured requirements"),
            SkillIO(name="acceptance_criteria", type="array",
                    description="Acceptance criteria"),
            SkillIO(name="gaps", type="array", description="Identified gaps"),
        ],
        tags=["requirements", "analysis", "specification"],
    )

    # 14. Architecture Designer
    templates["arch-designer"] = Skill(
        name="arch-designer",
        description="Design software architecture with patterns, components, and diagrams",
        version="1.0.0",
        instructions=(
            "You are a software architecture expert. Design the architecture:\n"
            "1. Identify key components and services\n"
            "2. Define component interactions and data flow\n"
            "3. Select appropriate design patterns\n"
            "4. Consider scalability, reliability, and maintainability\n"
            "5. Define technology stack recommendations\n"
            "6. Create architecture diagrams (ASCII/Mermaid)\n"
            "Provide a comprehensive architecture document."
        ),
        parameters=[
            SkillParameter(name="requirements", type="string", required=True,
                           description="Requirements or problem description"),
            SkillParameter(name="arch_style", type="string", required=False,
                           default="auto",
                           description="Style: microservices, monolith, serverless, event-driven, auto"),
            SkillParameter(name="scale", type="string", required=False,
                           default="medium",
                           description="Project scale: small, medium, large, enterprise"),
        ],
        inputs=[
            SkillIO(name="requirements", type="string", description="Requirements"),
        ],
        outputs=[
            SkillIO(name="architecture", type="object", description="Architecture design"),
            SkillIO(name="diagram", type="string", description="ASCII/Mermaid diagram"),
            SkillIO(name="tech_stack", type="array", description="Recommended technologies"),
        ],
        tags=["architecture", "design", "system-design"],
    )

    # 15. Project Manager
    templates["project-manager"] = Skill(
        name="project-manager",
        description="Plan and manage software projects with tasks, milestones, and timelines",
        version="1.0.0",
        instructions=(
            "You are a project management expert. Help plan the project:\n"
            "1. Break down the project into tasks and subtasks\n"
            "2. Define milestones and deliverables\n"
            "3. Estimate effort and timeline\n"
            "4. Identify dependencies and critical path\n"
            "5. Assign resources and responsibilities\n"
            "6. Define risk mitigation strategies\n"
            "Output a structured project plan."
        ),
        parameters=[
            SkillParameter(name="project_description", type="string", required=True,
                           description="Project description and goals"),
            SkillParameter(name="team_size", type="integer", required=False,
                           default=5, description="Number of team members"),
            SkillParameter(name="duration_weeks", type="integer", required=False,
                           default=8, description="Project duration in weeks"),
            SkillParameter(name="methodology", type="string", required=False,
                           default="agile",
                           description="Methodology: agile, waterfall, hybrid"),
        ],
        inputs=[
            SkillIO(name="project_description", type="string", description="Project goals"),
        ],
        outputs=[
            SkillIO(name="project_plan", type="object", description="Project plan"),
            SkillIO(name="milestones", type="array", description="Key milestones"),
            SkillIO(name="risk_assessment", type="array", description="Risk assessment"),
        ],
        tags=["project-management", "planning", "agile"],
    )

    # 16. Code Migrator
    templates["code-migrator"] = Skill(
        name="code-migrator",
        description="Migrate code between programming languages or frameworks",
        version="1.0.0",
        instructions=(
            "You are a code migration expert. Migrate the provided code:\n"
            "1. Translate syntax and idioms to the target language\n"
            "2. Adapt data structures and algorithms appropriately\n"
            "3. Map APIs and libraries to target equivalents\n"
            "4. Handle language-specific patterns and conventions\n"
            "5. Preserve the original logic and behavior\n"
            "6. Add comments for non-trivial adaptations\n"
            "Provide the migrated code with a migration notes section."
        ),
        parameters=[
            SkillParameter(name="code", type="string", required=True,
                           description="Source code to migrate"),
            SkillParameter(name="source_lang", type="string", required=True,
                           description="Source programming language"),
            SkillParameter(name="target_lang", type="string", required=True,
                           description="Target programming language"),
            SkillParameter(name="framework", type="string", required=False,
                           default="none",
                           description="Target framework if applicable"),
        ],
        inputs=[
            SkillIO(name="code", type="string", description="Source code"),
        ],
        outputs=[
            SkillIO(name="migrated_code", type="string", description="Migrated code"),
            SkillIO(name="migration_notes", type="array", description="Migration notes"),
            SkillIO(name="compatibility_issues", type="array",
                    description="Potential compatibility issues"),
        ],
        tags=["migration", "translation", "cross-language"],
    )

    # 17. Configuration Manager
    templates["config-manager"] = Skill(
        name="config-manager",
        description="Generate and manage application configuration files",
        version="1.0.0",
        instructions=(
            "You are a configuration management expert. Generate or manage configs:\n"
            "1. Create well-structured configuration files\n"
            "2. Define environment-specific settings\n"
            "3. Set sensible defaults\n"
            "4. Document all configuration options\n"
            "5. Validate configuration completeness\n"
            "6. Generate .env files, YAML, JSON, TOML configs as needed"
        ),
        parameters=[
            SkillParameter(name="app_type", type="string", required=True,
                           description="Application type: web_api, cli, worker, service"),
            SkillParameter(name="framework", type="string", required=False,
                           default="generic",
                           description="Framework: django, flask, fastapi, generic"),
            SkillParameter(name="format", type="string", required=False,
                           default="yaml",
                           description="Config format: yaml, json, toml, env"),
            SkillParameter(name="environment", type="string", required=False,
                           default="development",
                           description="Environment: development, staging, production"),
        ],
        inputs=[
            SkillIO(name="app_type", type="string", description="Application type"),
        ],
        outputs=[
            SkillIO(name="config", type="string", description="Configuration file content"),
            SkillIO(name="env_template", type="string", description="Environment template"),
            SkillIO(name="docs", type="string", description="Configuration documentation"),
        ],
        tags=["configuration", "setup", "deployment"],
    )

    # 18. Log Analyzer
    templates["log-analyzer"] = Skill(
        name="log-analyzer",
        description="Analyze application logs to identify errors, patterns, and root causes",
        version="1.0.0",
        instructions=(
            "You are a log analysis expert. Analyze the provided logs:\n"
            "1. Identify error patterns and frequencies\n"
            "2. Detect anomalies and unusual behavior\n"
            "3. Trace request flows across services\n"
            "4. Identify root causes of failures\n"
            "5. Summarize log statistics (error rates, response times)\n"
            "6. Provide actionable recommendations\n"
            "Present findings in a structured report."
        ),
        parameters=[
            SkillParameter(name="logs", type="string", required=True,
                           description="Log content to analyze"),
            SkillParameter(name="log_format", type="string", required=False,
                           default="auto",
                           description="Log format: json, text, syslog, auto"),
            SkillParameter(name="time_range", type="string", required=False,
                           default="all", description="Time range to focus on"),
            SkillParameter(name="severity", type="string", required=False,
                           default="error",
                           description="Minimum severity: debug, info, warn, error"),
        ],
        inputs=[
            SkillIO(name="logs", type="string", description="Log content"),
        ],
        outputs=[
            SkillIO(name="analysis_report", type="object", description="Analysis report"),
            SkillIO(name="error_summary", type="array", description="Error summary"),
            SkillIO(name="recommendations", type="array", description="Recommendations"),
        ],
        tags=["logs", "analysis", "monitoring"],
    )

    # 19. Deploy Helper
    templates["deploy-helper"] = Skill(
        name="deploy-helper",
        description="Generate deployment configurations and CI/CD pipeline definitions",
        version="1.0.0",
        instructions=(
            "You are a DevOps and deployment expert. Generate deployment resources:\n"
            "1. Create Dockerfile with best practices\n"
            "2. Generate docker-compose configuration\n"
            "3. Create CI/CD pipeline definitions\n"
            "4. Generate Kubernetes manifests if needed\n"
            "5. Define deployment scripts and health checks\n"
            "6. Set up environment variable management\n"
            "Provide production-ready configurations."
        ),
        parameters=[
            SkillParameter(name="app_type", type="string", required=True,
                           description="Application type: web_api, worker, static, ml_service"),
            SkillParameter(name="language", type="string", required=True,
                           description="Primary programming language"),
            SkillParameter(name="target_platform", type="string", required=False,
                           default="docker",
                           description="Target: docker, kubernetes, aws, gcp, azure"),
            SkillParameter(name="ci_tool", type="string", required=False,
                           default="github_actions",
                           description="CI tool: github_actions, gitlab_ci, jenkins"),
        ],
        inputs=[
            SkillIO(name="app_type", type="string", description="Application type"),
            SkillIO(name="language", type="string", description="Programming language"),
        ],
        outputs=[
            SkillIO(name="dockerfile", type="string", description="Dockerfile content"),
            SkillIO(name="ci_pipeline", type="string", description="CI/CD pipeline definition"),
            SkillIO(name="deploy_scripts", type="array", description="Deployment scripts"),
        ],
        tags=["deployment", "devops", "cicd"],
    )

    # 20. Monitor Analyst
    templates["monitor-analyst"] = Skill(
        name="monitor-analyst",
        description="Design monitoring, alerting, and observability solutions",
        version="1.0.0",
        instructions=(
            "You are an observability and monitoring expert. Design monitoring solutions:\n"
            "1. Define key metrics and KPIs to track\n"
            "2. Design dashboard layouts and visualizations\n"
            "3. Define alerting rules and thresholds\n"
            "4. Create SLA/SLO definitions\n"
            "5. Design log aggregation strategies\n"
            "6. Plan distributed tracing implementation\n"
            "Provide a comprehensive monitoring strategy."
        ),
        parameters=[
            SkillParameter(name="service_type", type="string", required=True,
                           description="Service type: web_api, microservice, worker, database"),
            SkillParameter(name="stack", type="string", required=False,
                           default="generic",
                           description="Tech stack for tool recommendations"),
            SkillParameter(name="monitoring_tool", type="string", required=False,
                           default="prometheus",
                           description="Tool: prometheus, datadog, grafana, cloudwatch"),
        ],
        inputs=[
            SkillIO(name="service_type", type="string", description="Service type"),
        ],
        outputs=[
            SkillIO(name="monitoring_plan", type="object", description="Monitoring plan"),
            SkillIO(name="alerts", type="array", description="Alert definitions"),
            SkillIO(name="dashboards", type="array", description="Dashboard configurations"),
        ],
        tags=["monitoring", "alerting", "observability"],
    )

    return templates


# Module-level template registry
_BUILTIN_TEMPLATES: Dict[str, Skill] = _build_templates()


def get_builtin_templates() -> Dict[str, Skill]:
    """Get all built-in skill templates.

    Returns:
        Dictionary mapping template names to Skill objects.
    """
    return dict(_BUILTIN_TEMPLATES)


def get_template_names() -> list:
    """Get a list of all built-in template names.

    Returns:
        Sorted list of template name strings.
    """
    return sorted(_BUILTIN_TEMPLATES.keys())


def get_template(name: str) -> Skill:
    """Get a specific built-in template by name.

    Args:
        name: The template name.

    Returns:
        The Skill template.

    Raises:
        KeyError: If the template name is not found.
    """
    if name not in _BUILTIN_TEMPLATES:
        available = ", ".join(sorted(_BUILTIN_TEMPLATES.keys()))
        raise KeyError(
            f"Template '{name}' not found. Available templates: {available}"
        )
    return _BUILTIN_TEMPLATES[name]


def apply_template(template_name: str, new_name: str) -> Skill:
    """Apply a template to create a new skill with a custom name.

    Args:
        template_name: The name of the built-in template.
        new_name: The name for the new skill.

    Returns:
        A new Skill instance based on the template.

    Raises:
        KeyError: If the template name is not found.
    """
    template = get_template(template_name)
    new_skill = copy.deepcopy(template)
    new_skill.name = new_name
    return new_skill
