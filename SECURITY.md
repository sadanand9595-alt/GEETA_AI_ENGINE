# Security Policy

Thank you for helping keep **GEETA AI Engine** secure.

We take security seriously and appreciate responsible disclosure of potential vulnerabilities.

---

# Supported Versions

The following table indicates which versions receive security updates.

| Version | Supported |
|----------|-----------|
| 1.x | ✅ Yes |
| < 1.0 | ❌ No |

Only the latest stable release will receive security updates.

---

# Reporting a Vulnerability

If you discover a security vulnerability, **please do not create a public GitHub Issue**.

Instead, report it privately to the project maintainers.

Your report should include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Proof of Concept (if available)
- Suggested mitigation (optional)

Providing complete information helps us investigate and resolve the issue more efficiently.

---

# Response Process

After receiving a security report, the maintainers will:

1. Acknowledge receipt of the report.
2. Investigate the reported issue.
3. Assess the severity and impact.
4. Develop and test a fix.
5. Publish a security update.
6. Credit the reporter when appropriate.

---

# Responsible Disclosure

We ask security researchers to:

- Give maintainers reasonable time to investigate.
- Avoid public disclosure until a fix is available.
- Avoid accessing data that does not belong to you.
- Avoid disrupting production systems.
- Report findings in good faith.

---

# Security Best Practices

When using GEETA AI Engine:

- Keep Python up to date.
- Use the latest stable release.
- Store API keys securely.
- Never commit `.env` files.
- Review generated patches before applying them.
- Restrict access to sensitive configuration files.
- Regularly update project dependencies.

---

# AI Provider Security

GEETA AI Engine may communicate with third-party AI providers.

Before enabling a provider:

- Review the provider's privacy policy.
- Understand how prompts are processed.
- Avoid sending confidential information unless appropriate safeguards are in place.
- Use local AI providers when handling highly sensitive source code.

---

# Dependency Security

Project dependencies should be:

- Trusted
- Actively maintained
- Regularly updated
- Reviewed before adoption

New dependencies should only be added when they provide clear value.

---

# Secret Management

Never store secrets directly in source code.

Sensitive information should be stored using:

- Environment variables
- Secret management services
- Secure credential storage

Examples of sensitive information include:

- API Keys
- Access Tokens
- Database Credentials
- Private Certificates

---

# Security Reviews

Security should be considered during:

- Architecture reviews
- Code reviews
- Pull requests
- Dependency updates
- Release preparation

Every significant feature should be evaluated for potential security implications.

---

# Scope

This security policy applies to:

- Source Code
- Documentation
- Configuration Files
- Build Scripts
- APIs
- Plugins
- VS Code Extension

---

# Contact

For security-related matters, please contact the project maintainers through the designated private communication channel.

Do not disclose vulnerabilities publicly until they have been investigated and addressed.

---

Thank you for helping improve the security of **GEETA AI Engine**.