# AI Whisperers E.A.S. - Information Security Policy

**Effective Date:** [Date]
**Version:** 1.0
**Classification:** Internal
**Policy Owner:** Partners

---

## 1. PURPOSE AND SCOPE

### 1.1 Purpose

This Information Security Policy establishes the framework for protecting AI Whisperers E.A.S.'s information assets, including:
- Client data and intellectual property
- Company confidential information
- Technical systems and infrastructure
- Employee and business partner data

### 1.2 Scope

This policy applies to:
- All employees, contractors, and partners
- All information systems and devices
- All physical and virtual locations
- All third parties with system access

---

## 2. SECURITY OBJECTIVES

**Confidentiality:** Ensure information is accessible only to authorized individuals
**Integrity:** Maintain accuracy and completeness of information
**Availability:** Ensure authorized access when needed

---

## 3. INFORMATION CLASSIFICATION

### 3.1 Classification Levels

**PUBLIC**
- Can be freely shared
- No impact if disclosed
- Examples: Marketing materials, public website content

**INTERNAL**
- For company use only
- Low impact if disclosed
- Examples: Internal memos, general policies

**CONFIDENTIAL**
- Restricted to authorized personnel
- Moderate impact if disclosed
- Examples: Client contracts, financial data, source code

**HIGHLY CONFIDENTIAL**
- Strictly need-to-know basis
- Severe impact if disclosed
- Examples: Client credentials, encryption keys, strategic plans

### 3.2 Handling Requirements

| Classification | Storage | Transmission | Disposal |
|----------------|---------|--------------|----------|
| Public | No restrictions | No encryption required | Standard deletion |
| Internal | Secure storage | Internal networks only | Secure deletion |
| Confidential | Encrypted storage | Encrypted transmission | Secure destruction |
| Highly Confidential | Encrypted + access logs | MFA + encrypted | Certified destruction |

---

## 4. ACCESS CONTROL

### 4.1 Principles

**Least Privilege:** Users receive minimum access needed
**Need-to-Know:** Access based on job requirements
**Separation of Duties:** Critical functions require multiple people
**Regular Review:** Access rights reviewed quarterly

### 4.2 Authentication

**Password Requirements:**
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- Changed every 90 days
- No password reuse (last 5 passwords)
- No sharing of credentials

**Multi-Factor Authentication (MFA):**
- Required for:
  - Email accounts
  - Cloud services
  - VPN access
  - Administrative access
  - Financial systems

**Account Management:**
- Unique accounts for each user
- No shared accounts
- Disable accounts immediately upon termination
- Review inactive accounts monthly

### 4.3 Authorization

**Role-Based Access:**
- Access tied to job roles
- Documented authorization process
- Manager approval required
- Quarterly access reviews

**Privileged Access:**
- Limited to essential personnel
- Additional logging and monitoring
- Regular audits
- Separate administrative accounts

---

## 5. PHYSICAL SECURITY

### 5.1 Office Security

**Access Control:**
- Locked doors when unattended
- Visitor log maintained
- Escort requirement for visitors
- Key/access card management

**Equipment:**
- Lock screens when away (< 5 minutes)
- Secure storage for devices
- Cable locks for laptops in public
- Equipment inventory maintained

### 5.2 Clean Desk Policy

**Requirements:**
- Clear desk at end of day
- Lock away confidential documents
- No passwords written down
- Secure disposal of sensitive documents

### 5.3 Device Security

**Laptops and Mobile Devices:**
- Full disk encryption required
- Screen lock after 5 minutes
- Lost/stolen devices reported immediately
- Remote wipe capability enabled

---

## 6. NETWORK SECURITY

### 6.1 Network Architecture

**Segmentation:**
- Separate networks for different security levels
- DMZ for public-facing services
- Internal network protection
- Guest network isolated

**Firewalls:**
- Firewall at network perimeter
- Default deny policy
- Regular rule reviews
- Change management process

### 6.2 Remote Access

**VPN Requirements:**
- VPN required for remote work
- Strong encryption (AES-256)
- MFA for VPN access
- Split tunneling prohibited for work data

**Wireless Security:**
- WPA3 encryption minimum
- Strong wireless passwords
- Hidden SSID for production
- Guest network for visitors

### 6.3 Network Monitoring

- Intrusion detection system (IDS)
- Log collection and analysis
- Real-time alerts for suspicious activity
- Monthly security reviews

---

## 7. SYSTEM SECURITY

### 7.1 Operating Systems

**Configuration:**
- Hardened OS configurations
- Unnecessary services disabled
- Security baselines applied
- Regular compliance checks

**Patching:**
- Critical patches within 7 days
- High priority within 30 days
- Regular patch schedule
- Test patches before production

### 7.2 Antivirus and Anti-Malware

**Requirements:**
- Antivirus on all endpoints
- Real-time scanning enabled
- Daily definition updates
- Weekly full system scans
- Quarantine suspicious files

### 7.3 Backup and Recovery

**Backup Strategy:**
- Daily incremental backups
- Weekly full backups
- Monthly archival backups
- 3-2-1 backup rule (3 copies, 2 media types, 1 offsite)

**Backup Security:**
- Encrypted backups
- Secure offsite storage
- Access controls on backups
- Regular restore testing (quarterly)

**Recovery:**
- Documented recovery procedures
- Recovery Time Objective (RTO): 24 hours
- Recovery Point Objective (RPO): 24 hours
- Annual disaster recovery test

---

## 8. APPLICATION SECURITY

### 8.1 Secure Development

**Development Practices:**
- Security requirements in design
- Secure coding standards
- Input validation
- Output encoding
- Error handling without information leakage

**Testing:**
- Security testing in development
- Vulnerability scanning
- Penetration testing annually
- Code reviews for security

### 8.2 Third-Party Applications

**Assessment:**
- Security review before adoption
- Vendor security questionnaires
- Regular security updates
- License compliance

**Configuration:**
- Follow security best practices
- Disable unnecessary features
- Strong authentication
- Regular updates

---

## 9. DATA SECURITY

### 9.1 Encryption

**Data at Rest:**
- Full disk encryption (FDE)
- Database encryption
- Encrypted file storage
- AES-256 minimum

**Data in Transit:**
- TLS 1.2+ for all transmissions
- VPN for remote access
- Encrypted email for sensitive data
- Secure file transfer (SFTP/HTTPS)

### 9.2 Data Handling

**Storage:**
- Store data in approved locations only
- No personal device storage (without encryption)
- Cloud storage: approved services only
- Regular data inventory

**Transmission:**
- Encrypt confidential data
- Use secure channels
- Verify recipient before sending
- No sensitive data via unsecured email

**Disposal:**
- Secure deletion (multi-pass)
- Physical destruction of media
- Certificate of destruction
- Data sanitization verified

---

## 10. EMAIL AND COMMUNICATION

### 10.1 Email Security

**Requirements:**
- SPF, DKIM, DMARC configured
- Spam filtering enabled
- Phishing protection
- Email encryption for sensitive data

**User Guidelines:**
- Verify sender before clicking links
- Don't open suspicious attachments
- Report phishing attempts
- No confidential data in subject lines

### 10.2 Instant Messaging

**Approved Platforms:**
- [List approved platforms]
- End-to-end encryption preferred
- No file sharing of confidential data (without encryption)
- Professional communication standards

---

## 11. INCIDENT RESPONSE

### 11.1 Incident Types

- Unauthorized access
- Malware infection
- Data breach
- System compromise
- Denial of service
- Physical security breach

### 11.2 Response Procedure

**Detection and Reporting:**
1. Identify incident
2. Report immediately to Partners
3. Do not alter evidence
4. Document observations

**Containment:**
5. Isolate affected systems
6. Prevent spread
7. Preserve evidence
8. Notify stakeholders

**Eradication:**
9. Remove threat
10. Patch vulnerabilities
11. Restore from clean backups
12. Verify system integrity

**Recovery:**
13. Return to normal operations
14. Monitor for recurrence
15. Document actions taken

**Post-Incident:**
16. Conduct review
17. Update procedures
18. Implement lessons learned
19. Report to authorities if required

### 11.3 Incident Contacts

**Internal:**
- Partners: [phone numbers]
- IT Support: [contact]

**External:**
- Incident Response Service: [if applicable]
- Legal Counsel: [contact]
- Law Enforcement: [if needed]

---

## 12. THIRD-PARTY SECURITY

### 12.1 Vendor Management

**Due Diligence:**
- Security assessment before engagement
- Review security certifications
- Audit rights in contracts
- Regular security reviews

**Requirements:**
- Sign confidentiality agreements
- Comply with security policies
- Report incidents immediately
- Secure data handling

### 12.2 Cloud Services

**Approved Services:**
- [List approved cloud providers]
- Security assessment completed
- Data Processing Agreements signed
- Regular security reviews

**Requirements:**
- MFA enabled
- Data encrypted
- Access logs reviewed
- Compliance verified

---

## 13. SECURITY AWARENESS

### 13.1 Training

**Required Training:**
- Security awareness (all staff, annually)
- Phishing awareness (quarterly)
- Role-specific training
- Incident response training

**Content:**
- Password security
- Phishing recognition
- Social engineering
- Data handling
- Incident reporting

### 13.2 Communication

**Regular Updates:**
- Monthly security tips
- Threat intelligence sharing
- Policy updates
- Incident lessons learned

---

## 14. COMPLIANCE AND AUDIT

### 14.1 Compliance

**Applicable Standards:**
- ISO 27001 (framework reference)
- GDPR (for EU clients)
- Paraguay data protection laws
- Industry best practices

**Monitoring:**
- Regular compliance checks
- Automated compliance scanning
- Policy adherence reviews
- Corrective action tracking

### 14.2 Audit

**Internal Audits:**
- Quarterly security assessments
- Access reviews
- Log analysis
- Policy compliance checks

**External Audits:**
- Annual security audit (recommended)
- Penetration testing
- Vulnerability assessments
- Compliance audits as needed

---

## 15. ACCEPTABLE USE

### 15.1 Permitted Use

Company systems may be used for:
- Business purposes
- Reasonable personal use (limited)
- Professional development

### 15.2 Prohibited Activities

**Strictly Forbidden:**
- Unauthorized access attempts
- Malware distribution
- Copyright infringement
- Harassment or illegal content
- Unauthorized data disclosure
- Bypassing security controls
- Cryptocurrency mining
- Torrent or P2P file sharing

### 15.3 Monitoring

- Company reserves right to monitor systems
- No expectation of privacy on company systems
- Monitoring for security and compliance
- Appropriate use of monitoring data

---

## 16. MOBILE DEVICE SECURITY

### 16.1 Company-Owned Devices

**Requirements:**
- Device encryption enabled
- Screen lock (PIN/biometric)
- Antivirus installed
- Remote wipe enabled
- Regular updates
- Lost/stolen reported immediately

### 16.2 BYOD (Bring Your Own Device)

**If Permitted:**
- Separate work profile/container
- Encryption required
- MFA for access
- No confidential data storage (without approval)
- Remote wipe of work data
- Compliance with security policy

---

## 17. SOCIAL ENGINEERING

### 17.1 Awareness

**Common Tactics:**
- Phishing emails
- Vishing (voice phishing)
- Pretexting
- Baiting
- Tailgating

### 17.2 Prevention

**Best Practices:**
- Verify identity before sharing information
- Be suspicious of urgent requests
- Verify URLs before clicking
- Don't share passwords
- Report suspicious contacts

---

## 18. BUSINESS CONTINUITY

### 18.1 Critical Systems

**Identification:**
- Client service platforms
- Email and communication
- Financial systems
- Development environments
- Data storage

### 18.2 Continuity Plans

**Requirements:**
- Documented procedures
- Alternative work arrangements
- Backup communication methods
- Regular testing
- Annual review and update

---

## 19. ROLES AND RESPONSIBILITIES

### 19.1 Partners

- Overall security responsibility
- Policy approval
- Resource allocation
- Strategic direction

### 19.2 All Employees

- Follow security policies
- Report incidents
- Complete training
- Protect information assets

### 19.3 IT/Security Function

- Implement security controls
- Monitor systems
- Respond to incidents
- Maintain security documentation

---

## 20. POLICY MANAGEMENT

### 20.1 Review and Updates

**Review Schedule:**
- Annual review
- After significant incidents
- When regulations change
- As business needs evolve

### 20.2 Exception Handling

**Process:**
1. Written request with justification
2. Risk assessment
3. Partners approval required
4. Compensating controls implemented
5. Regular exception reviews

### 20.3 Enforcement

**Non-Compliance:**
- Verbal warning
- Written warning
- Disciplinary action
- Contract termination
- Legal action if warranted

---

## 21. CONTACT INFORMATION

**Security Inquiries:**
Email: security@aiwhisperers.com
Partners: Kyrian & Ivan Weiss Van Der Pol

**Incident Reporting:**
Email: incidents@aiwhisperers.com
Phone: [24/7 contact number]

---

## ACKNOWLEDGMENT

I acknowledge that I have read, understood, and agree to comply with this Information Security Policy.

Name: _______________________
Signature: _______________________
Date: _______________________

---

**Approved by:**

Kyrian Weiss Van Der Pol, Partner
Date: _______________________

Ivan Weiss Van Der Pol, Partner
Date: _______________________

---

**Version History:**
| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | Nov 2024 | Initial version | Partners |

---

*This policy should be reviewed by security professionals and legal counsel, and customized for specific operations.*
